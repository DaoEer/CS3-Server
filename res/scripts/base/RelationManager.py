# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import Const
import csdefine
import csconst
import csstatus
import Functions
import random
import KST
from CoreObject import MgrPersistentObject
from EntitySimulator.EntityModel import EntityModel
from EntitySimulator import Fields



class PlayerItem( EntityModel ):
	"""讨论组成员(黑名单)实例"""
	class Meta:
		db_table = "kbe_RelationGroupInfo"
	
	id = Fields.INT32( db_column = "id", primary_key = True )
	uid = Fields.INT32( db_column = "sm_uid" )
	playerDBID = Fields.INT32( db_column = "sm_playerDBID" )
	blackName = Fields.UNICODE( db_column = "sm_blackName" )
	
	def __init__( self, *args, **kwargs ):
		EntityModel.__init__( self, *args, **kwargs )
		
		
	def onPlayerOnLine( self, playerMB, level ):
		"""玩家上线"""
		self.playerMB = playerMB
		if not self.level == level:
			self.level = level
		
	def onPlayerOffLine( self ):
		"""玩家下线"""
		self.playerMB = None
		
	def onOtherPlayerOnLine( self, uid, name, level ):
		"""同一讨论组的玩家上线"""
		if self.playerMB:
			self.playerMB.client.relation_onNoticePlayerOnLine( str( uid ), name, level )
		
	def onOtherPlayerOffLine( self, uid, name ):
		"""同一讨论组的玩家下线"""
		if self.playerMB:
			self.playerMB.client.relation_onPlayerOffLine( str( uid ), name )
			
	def changeGroupLeater( self, uid, leaterName ):
		"""更改组长"""
		if self.playerMB:
			self.playerMB.client.relation_changeGroupLeater( str(uid), leaterName )
			
	def updateGroupInfo( self, groupUID, groupName, canJoin, passWord ):
		"""更新讨论组信息"""
		if self.playerMB:
			self.playerMB.client.relation_updateGroupInfo( str( groupUID ), groupName, canJoin, passWord )
			
	def addEndTimeSuccess( self, uid, endTime ):
		"""添加免费时间"""
		if self.playerMB:
			self.playerMB.client.relation_addEndTime( str(uid), str(endTime) )
			
	def addGroupNum( self, groupUID, groupName, playerName, profession, level, camp ):
		"""添加讨论组员"""
		if self.playerMB:
			self.playerMB.client.statusMessage( csstatus.RELATION_MSG_ENTER_GROUP, "%s|%s"%(playerName, groupName) )
			self.playerMB.client.relation_receiverGroupInfo( groupUID, playerName, profession, level, camp, 1 )
			
	def removeGroupSelf( self, name, groupUID, groupName, leaveType ):
		"""自己离开该讨论组"""
		self.objects.delete( self.savePlayerItemCB, id = self.id )
		if self.playerMB:
			self.playerMB.client.relation_onDelectGroup( str( groupUID ) )
			if leaveType == csdefine.LEAVE_GROUP_TYPE_NORMAL:
				self.playerMB.client.statusMessage( csstatus.RELATION_MSG_LEAVE_GROUP, groupName )
			else:
				self.playerMB.client.statusMessage( csstatus.RELATION_MSG_LEAVE_GROUP_PASSIVE, groupName )
		
	def removeGroupOther( self, name, groupUID, groupName ):
		"""其他人离开该讨论组"""
		if self.playerMB:
			self.playerMB.client.relation_onPlayerRemoveGroup( str( groupUID ), name )
#			self.playerMB.client.statusMessage( csstatus.RELATION_MSG_TARGET_LEAVE_GROUP, "%s|%s"%(name, groupName) )
		
	def deleteGroup( self, groupUID ):
		"""解散该讨论组"""
		if self.playerMB:
			self.playerMB.client.relation_onDelectGroup( str( groupUID ) )
			
	def onGroupChat( self, chatData ):
		"""讨论组发言"""
		if self.playerMB:
			self.playerMB.cell.onReceiveGroupMessage( chatData )
			
	def addGroupBlackList( self, uid, name ):
		"""讨论组添加黑名单"""
		if self.playerMB:
			self.playerMB.client.relation_addGroupBlackList( str( uid), name )
			
	def delGroupBlackList( self, uid, name ):
		"""讨论组删除黑名单"""
		if self.playerMB:
			self.playerMB.client.relation_delGroupBlackList( str( uid), name )
			
	def savePlayerItemCB( self, result, models ):
		pass
	
class GroupItem( EntityModel ):
	class Meta:
		db_table = "kbe_RelationGroup"
	
	groupUID = Fields.INT32( db_column = "id", primary_key = True )
	groupName = Fields.UNICODE( db_column = "sm_groupName", default = "" )
	leaterName = Fields.UNICODE( db_column = "sm_playerName", default = "" )
	endTime = Fields.INT32( db_column = "sm_endTime" )
	isAllowJoin = Fields.INT32( db_column = "sm_isAllowJoin" )
	passWord = Fields.UNICODE( db_column = "sm_passWord" )
	
	"""
	讨论组
	"""
	def __init__( self, *args, **kwargs  ):
		EntityModel.__init__( self, *args, **kwargs  )
		self.staffList = []								# 组员
		self.blackList = []								# 黑名单
		
	def isGroupLeater( self, name ):
		"""是否是管理员"""
		return self.leaterName == name
	
	def changeGroupLeater( self, oldLeaterName, newLeaterName ):
		"""
		<Define method>
		管理员权限移交
		"""
		if self.leaterName != newLeaterName:
			self.leaterName = newLeaterName
			self.objects.filter( id=self.groupUID ).update( self.changeGroupLeaterCB, leaterName=newLeaterName )
			
	def changeGroupLeaterCB( self, result, models ):
		if result:
			for item in self.staffList:
				item.changeGroupLeater( self.groupUID, newLeaterName )
		
	def changeGroupName( self, name ):
		"""修改讨论组 名称"""
		if self.groupName != name:
			self.groupName = name
			self.objects.filter( id=self.groupUID ).update( self.saveGroupInfoCB, groupName=name )
			return True
		return False
	
	def isGroupNum( self, name ):
		"""是否是该组的成员"""
		for item in self.staffList:
			if item.playerName == name:
				return True
		return False
	
	def onPlayerOnLine( self, playerMB, name, level ):
		"""玩家上线"""
		blackList = []
		for item in self.blackList:
			blackList.append( item.blackName )
		playerMB.client.relation_receiverGroup( self.groupUID, self.groupName, str(self.endTime), self.leaterName, self.passWord, self.isAllowJoin, blackList )					# 同步讨论组信息
		for item in self.staffList:
			playerMB.client.relation_receiverGroupInfo( self.groupUID, item.playerName, item.profession, item.level, item.camp, bool( item.playerMB ) )								# 同步讨论组成员信息
			if item.playerName == name:
				item.onPlayerOnLine( playerMB, level )
			else:
				item.onOtherPlayerOnLine( self.groupUID, name, level )
		
	def onPlayerOffLine( self, name ):
		"""玩家下线"""
		for item in self.staffList:
			if item.playerName == name:
				item.onPlayerOffLine()
			else:
				item.onOtherPlayerOffLine( self.groupUID, name )
		
	def addGroupNum( self, _uid, _DBID, _playerName, _profession, _level, _camp, _playerMB = None, isWriteToDB = False ):
		"""添加讨论组员"""
		item = PlayerItem( uid = _uid, playerDBID = _DBID, playerName = _playerName, profession = _profession, level = _level, camp = _camp, playerMB = _playerMB )
		self.staffList.append( item )
		
		if isWriteToDB:
			item.writeToDB( self.addGroupNumCB )
			
	def addGroupNumCB( self, result, models ):
		if result:
			for playerItem in self.staffList:
				playerItem.addGroupNum( str( self.groupUID ), self.groupName, models.playerName, models.profession, models.level, models.camp )
		
	def removeGroup( self, playerName, leaveType ):
		"""退出讨论组"""
		for item in self.staffList:
			if item.playerName == playerName:
				self.staffList.remove( removeItem )
				item.removeGroupSelf( playerName, self.groupUID, self.groupName, leaveType )
			else:
				item.removeGroupOther( playerName, self.groupUID, self.groupName )
	
	def updateGroupInfo( self, groupName, canJoin, passWord ):
		"""更新讨论组信息"""
		if self.changeGroupName( groupName ) or self.setAllowJoin( canJoin ) or self.changePassWord( passWord ):
			for playerItem in self.staffList:
				playerItem.updateGroupInfo( self.groupUID, groupName, canJoin, passWord )
		
	def addGroupBlackList( self, name, playerMB = None, isWriteToDB = False ):
		"""
		<Define method>
		添加讨论组黑名单
		"""
		if len(self.blackList) >= Const.GROUP_BLACKLIST_MAX_COUNT:
			if playerMB:
				playerMB.client.statusMessage( csstatus.RELATION_MSG_GROUP_BLACK_IS_FULL, "" )
			return
		if playerMB:
			for item in self.blackList:
				if name == item.blackName:
					playerMB.client.statusMessage( csstatus.RELATION_MSG_GROUP_BLACK_REPEAT, "" )
					return
		
		item = PlayerItem( uid = self.groupUID, blackName = name )
		self.blackList.append( item )
		if isWriteToDB:
			item.writeToDB( self.saveGroupInfoCB )
			if playerMB:
				playerMB.client.statusMessage( csstatus.RELATION_MSG_MAKE_BLACK_SUCESS, "" )
			for item in self.staffList:
				item.addGroupBlackList( self.groupUID, name )
			
			
	def delGroupBlackList( self, name ):
		"""
		<Define method>
		删除讨论组黑名单
		"""
		for item in self.blackList:
			if item.blackName == name:
				item.objects.delete( Functions.Functor( self.delGroupBlackListCB, name ), id = item.id )
				self.blackList.remove( item )
				
	def delGroupBlackListCB( self, name, result, models ):
		if result:
			for item in self.staffList:
				item.delGroupBlackList( self.groupUID, name )
				
	def addEndTimeSuccess( self, endType ):
		"""讨论组 延期"""
		endTimeMapping = csconst.GROUP_ENDTIME_MAPPING.get( endType, None )
		if endTimeMapping is None:return
		if endTimeMapping[0] == 0:
			self.endTime = 0
		else:
			if self.endTime >= Functions.getTime():								# 免费的使用时间，还没有过
				self.endTime += endTimeMapping[0]
			else:
				self.endTime = int9( endTime[0] + Functions.getTime() )
		self.objects.filter(id=self.groupUID).update( self.addEndTimeCB, endTime = self.endTime )
		
	def deleteGroup( self ):
		"""删除讨论群"""
		self.staffList[0].objects.delete( self.saveGroupInfoCB, groupUID=self.groupUID )			# 数据库删除所有好友，以及黑名单数据
		for item in self.staffList:
			item.deleteGroup( self.groupUID )
		self.staffList.clear()
		self.blackList.clear()
		
	def addEndTimeCB( self, result, models ):
		if result:
			for item in self.staffList:
				item.addEndTimeSuccess( self.groupUID, self.endTime )
		
	def setAllowJoin( self, canJoin ):
		"""设置讨论组能否自由加入"""
		if self.isAllowJoin == canJoin:return False
		self.isAllowJoin = canJoin
		self.objects.filter(id=self.groupUID).update( self.saveGroupInfoCB, isAllowJoin=self.isAllowJoin )
		return True
		
	def changePassWord( self, passWord ):
		"""设置讨论组密码"""
		if self.passWord == passWord:return False
		self.passWord = passWord
		self.objects.filter(id=self.groupUID).update( self.saveGroupInfoCB, passWord=self.passWord)
		return True
		
	def onGroupChat( self, playerMB, chatData ):
		"""讨论组发言"""
		chatTime = Functions.getTime()
		if self.endTime and chatTime >= self.endTime:
			playerMB.client.statusMessage( csstatus.RELATION_MSG_GROUP_TIME_NOT_ENOUGH, "" )
			return
		for item in self.staffList:
			item.onGroupChat( chatData )
			
	def saveGroupInfoCB( self, result, models ):
		"""数据库操作回调"""
		pass
		
class RelationManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	此manager用来分配每个baseAPP的好友UID
	"""
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.maxUID = 0
		self.deceteTimer = None
#		self.groupDict = {}
#		self.delTable()
		self.createTable()								# 朋友关系数据库表
#		self.createGroupTable()							# 
		
	def delTable( self ):
		"""
		修改表的数据，需要先删除再重新创建（后续需要删除）
		"""
		sql = "Drop Table kbe_Relation, kbe_RelationGroup, kbe_RelationGroupInfo"
		KBEngine.executeRawDatabaseCommand( sql, self._delTableCallback )
		
	def _delTableCallback( self, result, rows, insertid, errstr ):
		self.createTable()								# 朋友关系数据库表
		self.createGroupTable()							# 
		
	def createTable( self ):
		"""
		创建kbe_Relation表
		
		`sm_playerDBID1` 玩家1的databaseID
		`sm_playerDBID2` 玩家2的databaseID
		`sm_playerRemark1` 玩家1对玩家2的备注
		`sm_playerRemark2` 玩家2对玩家1的备注
		`sm_relationStatus` 玩家1和玩家2的关系状态
		`sm_uid` 每条关系的唯一id
		
		sm_relationStatus是一个UINT32数据。左到右，前16位的位模式表示playerDBID1的关系状态
		后16位的位模式表示playerDBID2的关系状态
		"""
		sqlTable = """CREATE TABLE IF NOT EXISTS `kbe_Relation` (
						`id` bigint(20) NOT NULL AUTO_INCREMENT,
						`sm_uid` bigint(20) NOT NULL,
						`sm_playerDBID1` BIGINT(20) UNSIGNED NOT NULL,
						`sm_playerDBID2` BIGINT(20) UNSIGNED NOT NULL,
						`sm_playerRemark1` VARCHAR(24),
						`sm_playerRemark2` VARCHAR(24),
						`sm_relationStatus` int(32) unsigned NOT NULL,
						PRIMARY KEY (`id`),
						key `sm_playerDBID1Index` (sm_playerDBID1),
						key `sm_playerDBID2Index` (sm_playerDBID2)
						)ENGINE=InnoDB;
						"""
		KBEngine.executeRawDatabaseCommand( sqlTable, self._createTableCB )
		
	def _createTableCB( self, result, rows, insertid, errstr ):
		"""
		"""
		if errstr:
			KBEDebug.ERROR_MSG( "RelationManager create table error:%s." %errstr )
			return
		KBEngine.executeRawDatabaseCommand( "select max(sm_uid) from kbe_Relation;", self.queryUIDCB )
		
	def queryUIDCB( self, result, rows, insertid, errstr ):
		if errstr:
			KBEDebug.ERROR_MSG( "RelationManager query UID error:%s." %errstr )
			return
		
		if result[0][0] != b"NULL" and result[0][0] is not None:				# 一开始是空表
			self.maxUID = int( result[0][0] )
			
		KST.g_baseAppEntity.requestAllBaseRelationUID()
		self.onCompleteInit()
		
	def assignedRelationUID( self, baseEntityMB ):
		"""
		<Define method>
		
		分配baseEntity relationUID
		"""
		min = self.maxUID + 1
		self.maxUID += Const.RELATION_UID_SAND_MAX_COUNT
		baseEntityMB.receiveRelationUID( min )
		
	#-------------------------------------------------------------------------------------------------------
	# 讨论组
	#--------------------------------------------------------------------------------------------------------
	def createGroupTable( self ):
		"""
		创建 kbe_RelationGroup 表
		
		`id`						# 讨论组id
		`sm_groupName`				# 讨论组名
		`sm_playerName`				# 群主名
		`sm_endTime`				# 讨论组免费使用时间
		`sm_isAllowJoin`			# 是否允许自由加入
		`sm_passWord`				# 进讨论组密码
		"""
		sqlTable = """CREATE TABLE IF NOT EXISTS `kbe_RelationGroup` (
						`id` bigint(20) NOT NULL AUTO_INCREMENT,
						`sm_groupName` TEXT,
						`sm_playerName` TEXT,
						`sm_endTime` bigint(8) NOT NULL default 0,
						`sm_isAllowJoin` tinyint(1),
						`sm_passWord` TEXT,
						PRIMARY KEY (`id`)
						)ENGINE=InnoDB;
						"""
		KBEngine.executeRawDatabaseCommand( sqlTable, self._createGroupTableCB )
		
	def _createGroupTableCB( self, result, rows, insertid, errstr ):
		
		if errstr:
			KBEDebug.ERROR_MSG( "RelationManager createGroupTable error:%s." %errstr )
			return
		queryTable = "select rg.id, rg.sm_groupName, rg.sm_playerName, rg.sm_endTime, rg.sm_isAllowJoin, rg.sm_passWord from kbe_RelationGroup as rg"
		KBEngine.executeRawDatabaseCommand( queryTable, self._queryGroup )
		
	def _queryGroup( self, result, rows, insertid, errstr ):
		"""
		record[0] = id						# 讨论组id
		record[1] = sm_groupName			# 讨论组名
		record[2] = sm_playerName			# 创建讨论组的玩家名
		record[3] = sm_endTime				# 讨论组免费使用时间
		record[4] = sm_isAllowJoin			# 讨论组是否可以自由加入
		record[5] = sm_passWord				# 讨论组是否需要密码加入
		"""
		if errstr:
			KBEDebug.ERROR_MSG( "query Group fail!! error:%s" %errstr )
			return
		for record in result:
			uid = int( record[0])
			group = GroupItem( groupUID = uid, groupName = bytes.decode(record[1]), playerName = bytes.decode(record[2]), endTime = int(record[3]),\
				 isAllowJoin = int(record[4]), passWord = bytes.decode(record[5]) )
			self.groupDict[uid] = group
			
		self.createGroupInfoTable()
	
	def createGroupInfoTable( self ):
		"""
		创建 kbe_RelationGroupInfo 表
		在讨论组中，玩家的信息
		
		`sm_uid`					# 隐射到kbe_RelationGroup表
		`sm_playerDBID`				# 玩家的DBID
		`sm_blackName`				# 讨论组黑名单
		"""
		sqlTable = """CREATE TABLE IF NOT EXISTS `kbe_RelationGroupInfo` (
						`id` bigint(20) NOT NULL AUTO_INCREMENT,
						`sm_uid` int(32) unsigned NOT NULL,
						`sm_playerDBID` BIGINT NOT NULL,
						`sm_blackName` TEXT,
						PRIMARY KEY (`id`)
						)ENGINE=InnoDB;
						"""
		KBEngine.executeRawDatabaseCommand( sqlTable, self._createGroupInfoTableCB )
		
	def _createGroupInfoTableCB( self, result, rows, insertid, errstr ):
		if errstr:
#			KBEDebug.ERROR_MSG( "RelationManager createGroupTableInfo error:%s." %errstr )
			return
		queryTable = "select rgi.sm_uid, rgi.sm_playerDBID, r.sm_playerName, r.sm_profession, r.sm_level, r.sm_camp, rgi.sm_blackName from kbe_RelationGroupInfo as rgi, tbl_Role as r where r.id = rgi.sm_playerDBID"
		KBEngine.executeRawDatabaseCommand( queryTable, self._queryGroupInfo )
		
	def _queryGroupInfo( self, result, rows, insertid, errstr ):
		"""
		record[0] = sm_uid					# 讨论组uid
		record[1] = sm_playerDBID			# 讨论组成员DBID
		record[2] = sm_playerName			# 玩家名字
		record[3] = sm_profession			# 职业
		record[4] = sm_level				# 等级
		record[5] = sm_camp					# 阵营
		record[6] = sm_blackName			# 讨论组黑名单
		"""
		if errstr:
			KBEDebug.ERROR_MSG( "query Group info fail!! error:%s" %errstr )
			return
		for record in result:
			uid = int(record[0])
			DBID = int(record[1])
			playerName = bytes.decode(record[2])
			profession = int(record[3])
			level = int(record[4])
			camp = int(record[5])
			blackList = bytes.decode( record[6])
				
			group = self.groupDict.get(uid)
			if group is None:
				KBEDebug.ERROR_MSG( "kbe_RelationGroupInfo uid(%i) can not find in kbe_RelationGroup"%uid )
				continue
			if DBID:								# 如果有DBID，默认是组员;否则加入黑名单
				group.addGroupNum( uid, DBID, playerName, profession, level, camp, None, False )
				if not playerName in self.playerNameDict:
					self.playerNameDict[playerName] = 0
				self.playerNameDict[playerName] += 1
			else:
				group.addGroupBlackList( blackList )
		
	def createGroup( self, playerMB, _groupName, _isAllowJoin, _passWord, _playerName, DBID, _profession, _level, _camp ):
		"""
		<Define method>
		创建一个讨论组
		"""
		if self.playerNameDict.get( _playerName ) and self.playerNameDict[_playerName] >= Const.PLAYER_CAN_JOIN_GROUP_NUM:
			playerBase.client.statusMessage( csstatus.RELATION_MSG_PLAYER_GROUP_IS_LIMIT, "" )
			return False

		_endTime = Functions.getTime() + Const.GROUP_CAN_USE_TIME
		group = GroupItem( groupName = _groupName, playerDBID = DBID, playerName = _playerName, endTime = _endTime, isAllowJoin = _isAllowJoin, passWord = _passWord )
		group.writeToDB( Functions.Functor( self.createGroupCB, playerMB, _playerName, DBID, _profession, _level, _camp ) )
		
	def createGroupCB( self, playerMB, _playerName, DBID, _profession, _level, _camp, result, group ):
		if result:
			playerMB.client.statusMessage( csstatus.RELATION_MSG_CREATE_GROUP, group.groupName )
			
			uid = group.groupUID
			group.addGroupNum( uid, DBID, _playerName, _profession, _level, _camp, playerMB, True )
			self.groupDict[uid] = group
			if not _playerName in self.playerNameDict:
				self.playerNameDict[_playerName] = 0
			self.playerNameDict[_playerName] += 1
			
#			group.updateGroupInfo( group.groupName, endTime, _playerName )
			
	def invitedToGroup( self, playerMB, uid, sourcePlayerName, targetPlayerName ):
		"""
		<Define method>
		邀请玩家加入讨论组
		@param playerMB : 主动邀请的玩家
		@param uid 	: 进入讨论组的uid
		@param sourcePlayerName : 主动邀请方玩家的名字
		@param targetPlayerName : 被邀请方玩家的名字
		"""
		if not self._canAddToGroup( playerMB, uid, targetPlayerName ):return
		group = self.groupDict.get( uid )
		if group is None:return	
		KST.g_baseAppEntity.lookupRoleBaseByName( targetPlayerName, Functions.Functor( self._lookupRoleBaseCB, playerMB, sourcePlayerName, group.groupName, uid ) )
	
	def _lookupRoleBaseCB( self, playerMB, sourcePlayerName, groupName, uid, resultMB ):
		if resultMB is None:
			self.statusMessage( csstatus.RELATION_MSG_PLAYER_IS_OFFLINE )
			return
		resultMB.beInvitedToGroup( playerMB, sourcePlayerName, groupName, uid )
		
	def _canAddToGroup( self, playerBase, uid, playerName ):
		group = self.groupDict.get( uid )
		if group is None:return False
		
		if len( group.staffList ) >= Const.GROUP_MAX_COUNT:
			playerBase.client.statusMessage( csstatus.RELATION_MSG_GROUP_NEM_IS_LIMIT, "" )
			return False
		if playerName in group.blackList:
			playerBase.client.statusMessage( csstatus.RELATION_MSG_IN_BLACK_CANOT_JOIN_GROUP, playerName )
			return False
		if self.playerNameDict.get( playerName ) and self.playerNameDict[playerName] >= Const.PLAYER_CAN_JOIN_GROUP_NUM:
			playerBase.client.statusMessage( csstatus.RELATION_MSG_PLAYER_GROUP_IS_LIMIT, "" )
			return False
		if group.isGroupNum( playerName ):
			playerBase.client.statusMessage( csstatus.RELATION_MSG_PLAYER_IN_GROUP_AREADY, playerName )
			return False
		return True
		
	def replyForInvitedToGroup( self, playerMB, uid, playerName, playerDBID, profession, level, camp ):
		"""
		<Define method>
		对方回应 加入讨论组
		"""
		group = self.groupDict.get( uid )
		if group is None:return
		group.addGroupNum( uid, playerDBID, playerName, profession, level, camp, playerMB, True )
		if not playerName in self.playerNameDict:
			self.playerNameDict[playerName] = 0
		self.playerNameDict[playerName] += 1
	
	def requestEnterGroup( self, playerMB, uid, passWord, playerName, playerDBID, profession, level, camp ):
		"""
		<Define method>
		申请加入一个讨论组
		"""
		if playerName in group.blackList:
			playerMB.client.statusMessage( csstatus.RELATION_MSG_CANOT_JOIN_GROUP, "" )
		if not self._canAddToGroup( playerMB, uid, playerName ):return
		group = self.groupDict.get( uid )
		if group is None:return
		if not group.isAllowJoin:
			playerMB.client.statusMessage( csstatus.RELATION_MSG_GROUP_JOIN_FREEDOM, "" )
			return
		if group.passWord:
			playerMB.client.OpenGroupPassWordWidget( uid, group.groupName )
			return
		group.addGroupNum( uid, playerDBID, playerName, profession, level, camp, playerMB, True )
		if not playerName in self.playerNameDict:
			self.playerNameDict[playerName] = 0
		self.playerNameDict[playerName] += 1
		
	def requestEnterGroupByPassword( self, playerMB, uid, passWord, playerName, playerDBID, profession, level, camp ):
		"""
		<Define method>
		申请加入一个讨论组
		"""
		if not self._canAddToGroup( playerMB, uid, playerName ):return
		group = self.groupDict.get( uid )
		if group is None:return
		if not group.isAllowJoin:
			playerMB.client.statusMessage( csstatus.RELATION_MSG_GROUP_JOIN_FREEDOM, "" )
			return
		if group.passWord and group.passWord != passWord:
			playerMB.client.statusMessage( csstatus.RELATION_MSG_GROUP_PASSWORD_ERR, "" )
			return
		group.addGroupNum( uid, playerDBID, playerName, profession, level, camp, playerMB, True )
		if not playerName in self.playerNameDict:
			self.playerNameDict[playerName] = 0
		self.playerNameDict[playerName] += 1
		
	def activeLeaveGroup( self, uid, playerName ):
		"""
		<Define method>
		申请 退出一个讨论组
		"""
		group = self.groupDict.get( uid )
		if not group:
			KBEDebug.ERROR_MSG( "can not find uid(%i)"%uid )
			return
		self.removeGroup( uid, playerName, csdefine.LEAVE_GROUP_TYPE_NORMAL )	
		
	def passiveLeaveGroup( self, grouperName, uid, playerName ):
		"""
		<Define method>
		管理员 请离 一个组员
		"""
		group = self.groupDict.get( uid )
		if not group:
			KBEDebug.ERROR_MSG( "can not find uid(%i)"%uid )
			return
		if group.isGroupLeater( grouperName ):
			self.removeGroup( uid, playerName, csdefine.LEAVE_GROUP_TYPE_PASSIVE )

		
	def removeGroup( self, uid, playerName, leaveType ):
		"""
		退出一个讨论组
		"""
		group = self.groupDict.get( uid )
		if group.isGroupNum( playerName ):
			group.removeGroup( playerName, leaveType )
			self.playerNameDict[playerName] -= 1
		
	def deleteGroup( self, groupUID ):
		"""
		<Define method>
		解散一个讨论组
		"""
		group = self.groupDict.get( groupUID )
		if not group:
			KBEDebug.ERROR_MSG( "can not find groupUID(%i)"%groupUID )
			return
		for playerItem in group.staffList:
			self.playerNameDict[playerItem.playerName] -= 1
			
		group.deleteGroup()
		del self.groupDict[groupUID]
		
	def getGroupItemByName( self, name ):
		"""通过名字获取 玩家加入的讨论群"""
		list = []
		for group in self.groupDict.values():
			for item in group.staffList:
				if item.playerName == name:
					list.append( group )
					continue
		return list
		
	def onRoleGetCell( self, playerMB, name, level ):
		"""
		<Define method>
		玩家cell创建完成
		"""
		groups = self.getGroupItemByName( name )
		for group in groups:
			group.onPlayerOnLine( playerMB, name, level )
			
	def onRoleLoseCell( self, name ):
		"""
		<Define method>
		玩家下线通知
		"""
		groups = self.getGroupItemByName( name )
		for group in groups:
			if group.isGroupNum( name ):
				group.onPlayerOffLine( name )
			
	def onGroupChat( self, playerMB, chatData ):
		"""
		<Define method>
		讨论组 聊天
		"""
		uid = chatData["groupUID"]
		group = self.groupDict.get( uid )
		if group is None:return
		group.onGroupChat( playerMB, chatData )
		
	def changeGroupLeater( self, uid, LeaterName, targetName ):
		"""
		<Define method>
		讨论组 修改管理员
		"""
		group = self.groupDict.get( uid )
		if group is None:
			KBEDebug.ERROR_MSG( "can not find the group(%i)!!"%uid )
			return
		if group.isGroupLeater( LeaterName ):
			group.changeGroupLeater( LeaterName, targetName )
			
	def updateGroupInfo( self, uid, LeaterName, groupName, canJoin, passWord ):
		"""
		<Define method>
		更新讨论组信息
		"""
		if not group.isGroupLeater( LeaterName ):return
		group = self.groupDict.get( uid )
		if group is None:
			KBEDebug.ERROR_MSG( "can not find the group(%i)!!"%uid )
			return
		group.updateGroupInfo( groupName, canJoin, passWord )
			
	def addEndTime( self, playerMB, uid, LeaterName, endType ):
		"""
		<Define method>
		讨论组 延期
		"""
		group = self.groupDict.get( uid )
		if group is None:
			KBEDebug.ERROR_MSG( "can not find the group(%i)!!"%uid )
			return
		if group.isGroupLeater( LeaterName ):
			endTimeMapping = csconst.GROUP_ENDTIME_MAPPING.get( endType, None )
			if endTimeMapping is None:return
			money = endTimeMapping[1]
			if money > 0:
				playerMB.addEndTimePayMoney( money, uid, endType )
			else:
				self.addEndTimeSuccess( uid, endType )
			
	def addEndTimeSuccess( self, uid, endType ):
		"""
		Define method
		讨论组 支付成功添加延期
		"""
		group = self.groupDict.get( uid )
		if group is None:
			KBEDebug.ERROR_MSG( "can not find the group(%i)!!"%uid )
			return
		group.addEndTimeSuccess( uid, endType )
	
	def addGroupBlackList( self, playerMB, uid, LeaterName, playerName ):
		"""
		<Define method>
		讨论组 增加黑名单
		"""
		group = self.groupDict.get( uid )
		if group is None:
			KBEDebug.ERROR_MSG( "can not find the group(%i)!!"%uid )
			return
		if group.isGroupLeater( LeaterName ):
			group.addGroupBlackList( playerName, playerMB, True )
			
	def delGroupBlackList( self, uid, LeaterName, playerName ):
		"""
		<Define method>
		讨论组 删除黑名单
		"""
		group = self.groupDict.get( uid )
		if group is None:
			KBEDebug.ERROR_MSG( "can not find the group(%i)!!"%uid )
			return
		if group.isGroupLeater( LeaterName ):
			group.delGroupBlackList( playerName )
			
	def requestRandomGroup( self, playerMB ):
		"""
		Define method
		请求获取随机讨论组
		"""
		if self.groupDict:
			keys = self.groupDict.keys()
			size = len(keys)
			num = min( size, 10 )
			choiceList = random.sample( keys, num )
			dictData = {}
			for index, uid in choiceList:
				temp = {}
				item = self.groupDict[uid]
				temp["uid"] = uid
				temp["groupName"] = item.groupName
				temp["nums"] = len( item.staffList )
				dictData.update( temp )
			
			playerMB.client.relation_recommendGroup( Functions.toJsonString( dictData ) )
