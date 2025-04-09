# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------
# 数据库kbe_Relation的保存格式：
# 1、主动发起关系者对应sm_playerDBID1，被动者为sm_playerDBID2
# 2、relationStatus（玩家之间的关系标记 UINT32）
#	高16位表示sm_playerDBID1玩家的关系状态，低16位表示sm_playerDBID2玩家的关系状态
# 3、数据的保存约定：目前改为双方都进行保存，后面保存的会覆盖之前保存的，所以要保证数据不出错，需要实时保持两边的数据进行同步
#-----------------------------------------------------------------------------------
import time
import KST
import Const
import csconst
import csdefine
import csstatus
import KBEDebug
import KBEngine
import Functions

from EntitySimulator.EntityModel import EntityModel
from EntitySimulator import Fields


RELATION_STATUS_OFFSET = 16				# sm_playerDBID1偏移量




QUERY_RELATION_DB_LAM = lambda databaseID:"""select cr.sm_playerDBID1, cr.sm_playerDBID2, cr.sm_relationStatus, cr.sm_uid, 
cr.sm_playerRemark1,cr.sm_playerRemark2, r.sm_playerName, r.sm_profession, r.sm_level, r.sm_camp, r.sm_tongName, r.sm_spaceScriptID
 from kbe_Relation as cr, tbl_Role as r where cr.sm_playerDBID1 = %s and cr.sm_playerDBID2 = r.id union select cr.sm_playerDBID1,
cr.sm_playerDBID2, cr.sm_relationStatus,cr.sm_uid, cr.sm_playerRemark1,cr.sm_playerRemark2, r.sm_playerName, r.sm_profession, 
r.sm_level, r.sm_camp, r.sm_tongName, r.sm_spaceScriptID from kbe_Relation as cr, tbl_Role as r where cr.sm_playerDBID2 = %s and
cr.sm_playerDBID1 = r.id;"""%( databaseID, databaseID )
		
class RelationItem:
	"""
	@param playerName : 对方名称
	@param profession : 对方职业
	@param level	: 对方等级
	@param camp 	: 对方阵营
	@param tongName : 对方玩家帮会名称
	@param localSpace : 对方玩家的所在位置
	
	@param playerBase : 对方玩家base mailbox
	
	@param relationStatus : 玩家之间的关系标记，INT32
	@param playerDBID : 对方玩家DBID
	@param remarkName : 对方玩家的备注
	
	
	relationStatus的详解：
	前16位表示sm_playerDBID1的关系状态，后16位表示sm_playerDBID2的关系状态
	relationOffset偏移量的详解：
	如果DB的sm_playerDBID1不是玩家自己，则需要偏移量设置为16，否则偏移量设置为0
	"""
	def __init__( self ):
		pass
	
	@property
	def playerID(self):
		if self.playerBase:
			return self.playerBase.id
		return 0
	
	def convertRelationStatus( self ):
		"""
		item与DBID的格式不同，需要转化relationStatus
		"""
		if self.relationOffset:
			relationStatus = self.relationStatus >> self.relationOffset
		else:
			relationStatus = self.relationStatus & 0xFFFF
		return relationStatus
			
	def addRelationEachOther( self, relation, isWriteDB = False ):
		"""
		给双方添加关系(双向关系，如：朋友<->朋友)
		"""
		self.relationStatus |= ( relation << RELATION_STATUS_OFFSET | relation )
		KBEDebug.DEBUG_MSG("%s[%d]: %d" %(self.__class__.__name__, self.databaseID, self.relationStatus))
		if True:
#			self.writeToDB( self.saveRelationItemCB )
			self.objects.filter(relationUID=self.relationUID).update(self.saveRelationItemCB, relationStatus=self.relationStatus)
		
	def addMyRelation( self, relation, isWriteDB = False ):
		"""
		给玩家自己添加关系（单向关系，如：师父<->徒弟）
		@param relation: INT16
		"""
		self.relationStatus |= ( relation << self.relationOffset )
		KBEDebug.DEBUG_MSG("%s[%d]: %d" %(self.__class__.__name__, self.databaseID, self.relationStatus))
		if True:
			self.objects.filter(relationUID=self.relationUID).update(self.saveRelationItemCB, relationStatus=self.relationStatus)
		
	def addTargetRelation( self, relation, isWriteDB = False ):
		"""
		给对方玩家添加关系（单向关系，如：师父<->徒弟）
		@param relation: INT16
		"""
		if self.relationOffset:
			self.relationStatus |= relation
		else:
			self.relationStatus |= ( relation << RELATION_STATUS_OFFSET )
		KBEDebug.DEBUG_MSG("%s[%d]: %d" %(self.__class__.__name__, self.databaseID, self.relationStatus))
		if True:
#			self.writeToDB( self.saveRelationItemCB )
			self.objects.filter(relationUID=self.relationUID).update(self.saveRelationItemCB, relationStatus=self.relationStatus)
		
	def removeRelationEachOther( self, relation, isWriteDB = False ):
		"""
		移除双方的关系
		"""
		templeRelation =  ~( relation << RELATION_STATUS_OFFSET | relation )
		self.relationStatus &= templeRelation
		KBEDebug.DEBUG_MSG("%s[%d]: %d" %(self.__class__.__name__, self.databaseID, self.relationStatus))
		if True:
			if self.relationStatus == 0:
				self.objects.delete( self.saveRelationItemCB, relationUID=self.relationUID )
			else:
#				self.writeToDB( self.saveRelationItemCB )
				self.objects.filter(relationUID=self.relationUID).update(self.saveRelationItemCB, relationStatus=self.relationStatus)
		
	def removeMyRelation( self, relation, isWriteDB = False ):
		"""
		移除玩家自己的关系
		@param relation: INT16
		"""
		self.relationStatus &= ~( relation << self.relationOffset )
		KBEDebug.DEBUG_MSG("%s[%d]: %d" %(self.__class__.__name__, self.databaseID, self.relationStatus))
		if True:
			if self.relationStatus == 0:
				self.objects.delete( self.saveRelationItemCB, relationUID=self.relationUID )
			else:
#				self.writeToDB( self.saveRelationItemCB )
				self.objects.filter(relationUID=self.relationUID).update(self.saveRelationItemCB, relationStatus=self.relationStatus)
		
	def removeTargetRelation( self, relation, isWriteDB = False ):
		"""
		移除对方玩家的关系
		@param relation: INT16
		"""
		old = self.relationStatus
		if self.relationOffset:
			self.relationStatus &= ~relation
		else:
			self.relationStatus &= ~( relation << RELATION_STATUS_OFFSET )
		KBEDebug.DEBUG_MSG("%s[%d:%d]: %d:%d, %d:%d:%d" %(self.__class__.__name__, self.playerID, self.databaseID, old, self.relationStatus, self.relationOffset, relation, ~relation))
		if True:
			if self.relationStatus == 0:
				self.objects.delete( self.saveRelationItemCB, relationUID=self.relationUID )
			else:
#				self.writeToDB( self.saveRelationItemCB )
				self.objects.filter(relationUID=self.relationUID).update(self.saveRelationItemCB, relationStatus=self.relationStatus)
		
	def hasRelationWithTarget( self, relation ):
		"""
		玩家是否与对方有 某种关系
		"""
		return self.relationStatus & ( relation << self.relationOffset )
		
	def targetHasRelationWithMe( self, relation ):
		"""
		目标与我还有关系
		"""
		if self.relationOffset:
			return self.relationStatus & relation
		else:
			return self.relationStatus & ( relation << RELATION_STATUS_OFFSET )
		
	def hasNoRelationWithTarget( self ):
		"""
		与对方没有关系
		"""
		return not self.relationStatus
	
	def setRelationRemarkName( self, name ):
		"""
		设置 好友备注
		目前只有好友、不友好支持 好友备注
		"""
		if self.hasRelationWithTarget( csdefine.ROLE_RELATION_FRIEND ) or self.hasRelationWithTarget( csdefine.ROLE_RELATION_FOE ):
			if self.remarkName == name:return
			self.remarkName = name
#			self.writeToDB( self.saveRelationItemCB )
			self.objects.filter(relationUID=self.relationUID).update( self.saveRelationItemCB, remarkName=name)
			
	def saveRelationItemCB( self, result, models ):
		pass

class ActiveRelationItem( EntityModel, RelationItem ):
	"""主动添加关系一方"""
	class Meta:
		db_table = "kbe_Relation"
	relationUID = Fields.INT32( db_column = "sm_uid" )
	databaseID = Fields.INT32( db_column = "id", primary_key = True )
	DBID = Fields.INT32( db_column = "sm_playerDBID1" )
	RName = Fields.UNICODE( db_column = "sm_playerRemark1" )
	relationStatus = Fields.INT32( db_column = "sm_relationStatus")
	playerDBID = Fields.INT32( db_column = "sm_playerDBID2" )
	remarkName = Fields.UNICODE( db_column = "sm_playerRemark2" )
	
	def __init__( self, *args, **kwargs ):
		EntityModel.__init__( self, *args, **kwargs )
		RelationItem.__init__( self )
		self.relationOffset = RELATION_STATUS_OFFSET
		
	def addRelationEachOther( self, relation ):
		"""
		给双方添加关系(双向关系，如：朋友<->朋友)
		"""
		RelationItem.addRelationEachOther( self, relation, True )
		
	def addMyRelation( self, relation ):
		"""
		给玩家自己添加关系（单向关系，如：师父<->徒弟）
		@param relation: INT16
		"""
		RelationItem.addMyRelation( self, relation, True )
		
	def addTargetRelation( self, relation ):
		"""
		给对方玩家添加关系（单向关系，如：师父<->徒弟）
		@param relation: INT16
		"""
		RelationItem.addTargetRelation( self, relation, True )
		
	def removeRelationEachOther( self, relation ):
		"""
		移除双方的关系
		"""
		RelationItem.removeRelationEachOther( self, relation, True )
		
	def removeMyRelation( self, relation, isWriteDB = False ):
		"""
		移除玩家自己的关系
		@param relation: INT16
		"""
		RelationItem.removeMyRelation( self, relation, True )
		
	def removeTargetRelation( self, relation ):
		"""
		移除对方玩家的关系
		@param relation: INT16
		"""
		RelationItem.removeTargetRelation( self, relation, True )

	
class PassiveRelationItem( EntityModel, RelationItem ):
	"""被动添加关系一方"""
	class Meta:
		db_table = "kbe_Relation"
		
	relationUID = Fields.INT32( db_column = "sm_uid" )
	databaseID = Fields.INT32( db_column = "id", primary_key = True )
	DBID = Fields.INT32( db_column = "sm_playerDBID2" )
	RName = Fields.UNICODE( db_column = "sm_playerRemark2" )
	
	relationStatus = Fields.INT32( db_column = "sm_relationStatus")
	
	playerDBID = Fields.INT32( db_column = "sm_playerDBID1" )
	remarkName = Fields.UNICODE( db_column = "sm_playerRemark1" )
	
	def __init__( self, *args, **kwargs ):
		EntityModel.__init__( self, *args, **kwargs )
		RelationItem.__init__( self )
		self.relationOffset = 0

	def addRelationEachOther( self, relation ):
		"""
		给双方添加关系(双向关系，如：朋友<->朋友)
		"""
		if self.playerBase is None:
			RelationItem.addRelationEachOther( self, relation, True )
		else:
			RelationItem.addRelationEachOther( self, relation, False )
		
	def addMyRelation( self, relation ):
		"""
		给玩家自己添加关系（单向关系，如：师父<->徒弟）
		@param relation: INT16
		"""
		if self.playerBase is None:
			RelationItem.addMyRelation( self, relation, True )
		else:
			RelationItem.addMyRelation( self, relation, False )
		
	def addTargetRelation( self, relation ):
		"""
		给对方玩家添加关系（单向关系，如：师父<->徒弟）
		@param relation: INT16
		"""
		if self.playerBase is None:
			RelationItem.addTargetRelation( self, relation, True )
		else:
			RelationItem.addTargetRelation( self, relation, False )
		
	def removeRelationEachOther( self, relation ):
		"""
		移除双方的关系
		"""
		if self.playerBase is None:
			RelationItem.removeRelationEachOther( self, relation, True )
		else:
			RelationItem.removeRelationEachOther( self, relation, False )
		
	def removeMyRelation( self, relation, isWriteDB = False ):
		"""
		移除玩家自己的关系
		@param relation: INT16
		"""
		if self.playerBase is None:
			RelationItem.removeMyRelation( self, relation, True )
		else:
			RelationItem.removeMyRelation( self, relation, isWriteDB )
		
	def removeTargetRelation( self, relation ):
		"""
		移除对方玩家的关系
		@param relation: INT16
		"""
		if self.playerBase is None:
			RelationItem.removeTargetRelation( self, relation, True )
		else:
			RelationItem.removeTargetRelation( self, relation, False )
		
class RoleRelationInterface:
	"""
	玩家关系
	"""
	def __init__( self ):
		self.relationDatas = {}			# { relationUID : relationItem ...}
		
		self.friends = {}				# { playerDBID : relationItem ...}， 玩家好友
		self.blacklist = {}				# { playerDBID : relationItem ...}， 玩家黑名单
		self.foeDict = {}				# { playerDBID : relationItem ...}， 仇人
		self.lastChat = {}				# { playerDBID : relationItem ...}， 最近联系人
		self.inviteFriendDict = {}		# 发起邀请好友的玩家base
		
		self.inviteGroupBase = None		# 发起邀请讨论组的玩家base
		self.inviteGroupIndex = -1	# 讨论组的index
		self.initNum = 0
		
		self.resetRelationCatalog()
		
	def getRelationItemByName( self, playerName ):
		"""
		"""
		for relationItem in self.relationDatas.values():
			if relationItem.playerName == playerName:
				return relationItem
		return None
	
	def onGetCell( self ):
		"""
		玩家cell创建完毕
		"""
		KBEngine.executeRawDatabaseCommand( QUERY_RELATION_DB_LAM( self.databaseID ), self._getRelationRecordCB )
		KBEngine.globalData["RelationManager"].onRoleGetCell( self, self.getName(), self.getLevel() )
		
	def onLoseCell( self ):
		"""
		玩家下线通知
		"""
		self.inviteFriendDict.clear()
		for uid, relationItem in self.relationDatas.items():
			if relationItem.playerBase:
				relationItem.playerBase.onPlayerLogout( uid, self.cellData["level"], self.cellData["spaceScriptID"] )
		KBEngine.globalData["RelationManager"].onRoleLoseCell( self.getName() )
	
	def _getRelationRecordCB( self, result, rows, insertid, errstr ):
		"""
		读取关系数据表回调

		record[0] : sm_playerDBID1
		record[1] : sm_playerDBID2
		record[2] : sm_relationStatus
		record[3] : sm_uid
		record[4] : sm_playerRemark1
		record[5] : sm_playerRemark2
		record[6] : sm_playerName
		record[7] : sm_profession
		record[8] : sm_level
		record[9] : sm_camp
		record[10] : sm_tongName
		record[11] : sm_spaceScriptID
		"""
		if self.isDestroyed:
			return
			
		if errstr:
			KBEDebug.ERROR_MSG( "player( %s ),errstr:%s" % ( self.getName(), errstr )  )
			return
		if rows == 0:
			DEBUG_MSG( "( %s )不存在关系数据。" % self.getName() )
			return
		for record in result:
			_uid = int( record[3] )
			_relationStatus = int( record[2] )
			_targetName = bytes.decode( record[6] )					# 字节 转化为 字符串
			_profession = int( record[7] )
			_level = int( record[8] )
			_camp = int( record[9] )
			_remarkName = ""
			_tongName = bytes.decode( record[10] )
			_localSpace = bytes.decode( record[11] )
			if self.databaseID == int(record[0]):
				_targetDBID = int( record[1] )
				_targetStatus = _relationStatus & 0xFFFF
				myStatus = _relationStatus >> RELATION_STATUS_OFFSET
				if record[5]:
					_remarkName = bytes.decode( record[5] )
					
				relationItem = ActiveRelationItem( relationUID=_uid, playerName=_targetName, profession=_profession, level=_level,\
				camp=_camp, relationStatus=_relationStatus, playerBase=None, playerDBID=_targetDBID,\
				remarkName=_remarkName, DBID=self.databaseID, tongName=_tongName, localSpace=_localSpace )
			else:
				_targetDBID = int( record[0] )
				_DBID = int(record[1])
				_targetStatus = _relationStatus >> RELATION_STATUS_OFFSET
				myStatus = _relationStatus & 0xFFFF
				if record[4]:
					_remarkName = bytes.decode( record[4] )
				
				relationItem = PassiveRelationItem( relationUID=_uid, playerName=_targetName, profession=_profession, level=_level,\
				camp=_camp, relationStatus=_relationStatus, playerBase=None, playerDBID=_targetDBID,\
				remarkName=_remarkName, DBID=_DBID, tongName=_tongName, localSpace=_localSpace )
			
			if _relationStatus == 0:
				relationItem.objects.delete( self.saveRoleRelationCB, relationUID=_uid )
				continue
				
			self.relationDatas[_uid] = relationItem
			# 处理不在线时的关系变化
			for relation in csconst.MULTI_RELATION_LIST:	# 双边关系处理
				if myStatus & relation == 0:
					continue
				if relation == csdefine.ROLE_RELATION_FRIEND:
					if _targetStatus & relation == 0:			# 即使别人当我是仇人，我也加他好友
						if _targetStatus & csdefine.ROLE_RELATION_BLACKLIST or _targetStatus & csdefine.ROLE_RELATION_FOE:
							self.friends[_targetDBID] = relationItem
						else:
							relationItem.removeMyRelation( relation, True )
							if relationItem.relationStatus == 0:
								del self.relationDatas[_uid]
							self.statusMessage( csstatus.RELATION_MSG_FRIEND_TARGET_REMOVE, relationItem.playerName )
					else:
						self.friends[_targetDBID] = relationItem
				else:
					if _targetStatus & relation == 0:			# 出现这个情况是因为，对方解除了关系。而玩家不在线
						relationItem.removeMyRelation( relation, True )
						self.statusMessage( csstatus.RELATION_MSG_FRIEND_TARGET_REMOVE, relationItem.playerName )
		
			for relation in csconst.SINGLE_RELATION_LIST:	# 单边关系处理
				if myStatus & relation == 0 and _targetStatus & relation == 0:continue
				if relation == csdefine.ROLE_RELATION_BLACKLIST and myStatus & relation:
					self.blacklist[_targetDBID] = relationItem
					self.updateCellBlacklist()
					
				if relation == csdefine.ROLE_RELATION_FOE and myStatus & relation:
					self.foeDict[_targetDBID] = relationItem
					
				if relation == csdefine.ROLE_RELATION_LAST_CHAT and myStatus & relation:
					self.lastChat[_targetDBID] = relationItem
		self.addTimerCallBack( 0.5, "onRoleGetCell", () )
					
	def onPlayerLogout( self, relationUID, level, localSpace ):
		"""
		<define method>
		存在关系的玩家下线
		"""
		relationItem = self.relationDatas.get(relationUID)
		if relationItem is None:
			KBEDebug.ERROR_MSG( "player(%s) has no relationUID(%i)!!"%( self.getName(), relationUID ) )
			return
		relationItem.playerBase = None
		if self.client:
			self.client.relation_onNoticePlayerLogout( str(relationUID), level, localSpace )
		
	def onRoleGetCell( self, *param ):
		"""
		"""
		stream = {"RelationCatalogDatas" : []}
		self.resetCatalogUID()
		for index in self.relationCatalog.keys():
			CatalogData = {}
			CatalogData["relationIndex"] = index
			CatalogData["catalogName"] = self.relationCatalogName[index]
			CatalogData["catalogList"] = self.relationCatalog[index]
			stream["RelationCatalogDatas"].append( CatalogData )
		if hasattr(self, "client") and self.client:
			self.client.relation_initRelationCatalog(  stream  )
			#self.client.OnSetRelationNotice( self.isNoticeRelation )
		if len( self.relationDatas ) > 0:
			for relationItem in self.relationDatas.values():
				KST.g_baseAppEntity.lookupRoleBaseByName( relationItem.playerName, Functions.Functor( self.__onNotifyCB, relationItem ) )
		else:
			if hasattr(self, "client") and self.client:
				self.client.OnInitRelationDataCompleted()
		
	def resetCatalogUID( self ):
		"""用于验证下线删除，uid没有删除"""
		uids = self.relationDatas.keys()
		for index, _uids in self.relationCatalog.items():
			for uid in list(_uids):
				if uid in self.relationDatas:
					playerDBID = self.relationDatas[uid].playerDBID
					if index == csdefine.RELATION_CATALOG_TYPE_FOE_LIST and playerDBID in self.foeDict:
						continue
					elif index == csdefine.RELATION_CATALOG_TYPE_BLEACK_LIST and playerDBID in self.blacklist:
						continue
					elif index == csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST and playerDBID in self.lastChat:
						continue
					elif playerDBID in self.friends:
						continue
						
				_uids.remove(uid)
		
	def __onNotifyCB( self, relationItem, callResult ):
		"""
		"""
		relationUID = relationItem.relationUID
		relationItem.playerBase = callResult
		id = 0
		if callResult:											# 无论对方玩家是否在线都要将 数据发给己方客户端
			callResult.onNotifyRoleLogin( self, relationUID )
			id = callResult.id

		self.client.relation_sendRelationData( str( relationUID ), relationItem.playerName, relationItem.remarkName, str( relationItem.playerDBID ),\
		id, relationItem.convertRelationStatus(), relationItem.profession, relationItem.level, relationItem.camp, relationItem.tongName, relationItem.localSpace )
		
		self.initNum += 1
		if self.initNum == len( self.relationDatas ):
			self.initNum = 0
			self.client.OnInitRelationDataCompleted()
		
	def onNotifyRoleLogin( self, baseMailBox, relationUID ):
		"""
		<define method>
		玩家上线，通知有关系的玩家
		"""
		relationItem = self.relationDatas.get( relationUID, None )
		if relationItem is None:
			KBEDebug.ERROR_MSG( "player(%s):relationItem(%i) is not exit!!" %( self.getName(), relationUID ) )
			return
		
		relationItem.playerBase = baseMailBox
#		baseMailBox.onNotifyRoleLoginCB( self, relationUID )
		self.client.relation_onNoticePlayerLogin( str( relationUID ), baseMailBox.id )
		
#	def onNotifyRoleLoginCB( self, baseMailBox, relationUID ):
#		"""
#		<define method>
#		返回 对方玩家的信息
#		"""
#		relationItem = self.relationDatas.get( relationUID, None )
#		if relationItem is None:
#			KBEDebug.ERROR_MSG( "player(%s):relationItem(%i) is not exit!!" %( self.getName(), relationUID ) )
#			return
#		relationItem.playerBase = baseMailBox
		
	#----------------------------------------------------------------------------------------------
	# Relation config
	#----------------------------------------------------------------------------------------------
	def setRelationNotice( self, isNotice ):
		"""
		<Exposed method>
		设置 对方好友上线是否 通知客户端
		"""
		if not self.validateClientCall():
			return
		
		if self.isNoticeRelation == isNotice: 
			return
		
		self.isNoticeRelation = isNotice
		self.client.OnSetRelationNotice(self.isNoticeRelation)
	
	def resetRelationCatalog( self ):
		"""
		初始化 玩家关系 好友分组
		"""
		if not self.relationCatalogName:
			self.relationCatalogName = { csdefine.RELATION_CATALOG_TYPE_FOE_LIST : "不友好",
										csdefine.RELATION_CATALOG_TYPE_BLEACK_LIST : "黑名单", 
										csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST : "最近联系人", 
										csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST : "好友" }
			self.relationCatalog = { csdefine.RELATION_CATALOG_TYPE_FOE_LIST : [],
									csdefine.RELATION_CATALOG_TYPE_BLEACK_LIST: [], 
									csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST : [], 
									csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST : []}
		
	def addRelationCatalog( self, catalogName ):
		"""
		<Exposed method>
		添加 新的好友分组
		"""
		if not self.validateClientCall():
			return
		if len( self.relationCatalog ) >= Const.RELATION_CATALOG_MAX:
			self.statusMessage( csstatus.RELATION_MSG_CATALOG_IS_LIMIT )
			return
		index = max( self.relationCatalog ) + 1
		self.relationCatalog[index] = []
		self.relationCatalogName[index] = catalogName
		self.client.relation_addRelationCatalog( index, catalogName )
		self.writeToDB()
		
	def delRelationCatalog( self, index ):
		"""
		<Exposed method>
		删除 一条好友分组
		"""
		if not self.validateClientCall():
			return
		if index in Const.RELATION_FIX_CATALOGS:		# 不能删除固定分组
			KBEDebug.ERROR_MSG("Cannot delete relation catalog!")
			return
		if index in self.relationCatalogName and index in self.relationCatalog:
			del self.relationCatalogName[index]
			
			# 将好友添加到默认分组下
			for relationUID in self.relationCatalog[index]:
				self.client.relation_moveToOtherCatalog(index, 1, str(relationUID))
			self.relationCatalog[1].extend( self.relationCatalog[index] )		
			del self.relationCatalog[index]
			
			self.client.relation_delRelationCatalog( index )
			self.writeToDB()
	
	def renameRelationCatalog( self, index, catalogName ):
		"""
		<Exposed method>
		更改 一条好友分组的名字
		"""
		if not self.validateClientCall():
			return
			
		if not catalogName:
			return
		
		if self.relationCatalogName.get( index, None ) is not None:
			self.relationCatalogName[index] = catalogName
			self.writeToDB()
			
	def addPlayerToCatalog( self, index, relationUID ):
		"""
		将好友添加到某个分组下
		"""
		if index in self.relationCatalog:
			if not relationUID in self.relationCatalog[index]:
				self.relationCatalog[index].append( relationUID )
		else:
			KBEDebug.ERROR_MSG( "RoleRelationInterface::addPlayerToCatalog add uid(%d) fail!!Can't find index(%d) in relationCatalog"%( relationUID, index))
			
	def delPlayerToCatalog( self, index, relationUID ):
		"""
		将好友移除出某分组
		"""
		if index in self.relationCatalog:
			if index == csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST:			# 如果是删除好友
				for catalogIndex, numbers in self.relationCatalog.items():
					if catalogIndex > 0:
						if relationUID in numbers:
							numbers.remove(relationUID)
			else:
				self.relationCatalog[index].remove( relationUID )
		else:
			KBEDebug.ERROR_MSG( "RoleRelationInterface::delPlayerToCatalog del uid(%d) fail!!Can't find index(%d) in relationCatalog"%( relationUID, index))
			
	def moveRelationItemToCatalog( self, oldIndex, newIndex, relationUID ):
		"""
		<Exposed method>
		将好友移动到一个 新分组下
		"""
		if not self.validateClientCall():
			return
		relationUID = int( relationUID )
		self.delPlayerToCatalog( oldIndex, relationUID )
		self.addPlayerToCatalog( newIndex, relationUID )
		self.client.relation_moveToOtherCatalog(oldIndex, newIndex, str(relationUID))
		self.writeToDB()
		
	def setRelationRemarkName( self, relationUID, name ):
		"""
		<Exposed method>
		设置 好友的备注
		"""
		if not self.validateClientCall():
			return
		relationUID = int( relationUID )
		relationItem = self.relationDatas.get( relationUID )
		if relationItem:
			relationItem.setRelationRemarkName( name )
			
	def saveRoleRelationCB( self, result, models ):
		pass
	#----------------------------------------------------------------------------------------------
	# friend method
	#----------------------------------------------------------------------------------------------
	def requestPlayerInfo( self, name ):
		"""
		<Exposed method>
		请求玩家数据
		"""
		if not self.validateClientCall():
			return
		KST.g_baseAppEntity.lookupRoleBaseByName( name, self._lookupRoleInfoCB )
		
	def _lookupRoleInfoCB( self, resultMB ):
		"""
		@param resultMB: 玩家baseMailbox
		"""
		if resultMB is None:
			self.statusMessage( csstatus.RELATION_MSG_PLAYER_IS_OFFLINE )
			return
		resultMB.remoteRequestRoleInfo( self )
		
	def remoteRequestRoleInfo( self, playerBase ):
		"""
		define method
		远程查询玩家数据
		"""
		playerBase.client.relation_requestPlayerInfo(self.getName(),self.getLevel(),self.getCamp(),self.getProfession())
	
	def addFriend( self, name ):
		"""
		<Exposed method>
		添加好友
		"""
		if not self.validateClientCall(): return
		if not self.canMakeFriend( name ): return
		
		relationItem = self.getRelationItemByName( name )
		if relationItem:
			# 此处，可能主动先添加对方黑名单！然后，接受了对方好友的邀请
			self.removeFoeAndBlacklist( relationItem )
			
			if relationItem.playerBase:
				relationItem.playerBase.beInvitedToFriend( self, self.getName() )
				return
				
		KST.g_baseAppEntity.lookupRoleBaseByName( name, self._lookupRoleBaseCB )
			
	def _lookupRoleBaseCB( self, resultMB ):
		"""
		@param resultMB: 玩家baseMailbox
		"""
		if resultMB is None:
			self.statusMessage( csstatus.RELATION_MSG_PLAYER_IS_OFFLINE )
			return
		
		resultMB.beInvitedToFriend( self, self.getName() )
	
	def beInvitedToFriend( self, playerMailBox, name ):
		"""
		<define method>
		被邀请为好友
		"""
		if self.hadBlacklist( name ):
			if hasattr(playerMailBox, 'client') and playerMailBox.client:
				playerMailBox.client.statusMessage( csstatus.RELATION_MSG_ADD_FRIEND_IN_BLACK_LIST, self.getName() )
			return
			
		self.inviteFriendDict[name] = playerMailBox
		self.client.ReceiveInviteToFriend( playerMailBox.id, name )
		# if self.hadBlacklist( name ):
		# 	self.inquireMessage( csstatus.RELATION_MSG_ADD_FRIEND_AS_BLACK_LIST, [name], "replyForFriendInvite", name )
		# elif self.hasFoe( name ):
		# 	self.inquireMessage( csstatus.RELATION_MSG_ADD_FRIEND_AS_FOE, [name], "replyForFriendInvite", name )
		# else:
		# 	self.inquireMessage( csstatus.RELATION_MSG_REQUEST_ADD_FRIEND, [name], "replyForFriendInvite", name )


	def replyInvitedToFriend(self, reply, name ):
		"""
		<Exposed method>
		从社交界面回应是否添加好友
		"""
		if not self.validateClientCall():
			return
		self.replyForFriendInvite( reply, name )

	def replyForFriendInvite( self, reply, name ):
		"""
		被邀请方 回应是否同意添加好友
		"""
		inviteFriendBase = self.inviteFriendDict.pop(name, None)
		if inviteFriendBase is None:return
		
		if not reply:
			inviteFriendBase.client.statusMessage( csstatus.RELATION_MSG_REFUSE_INVITATION, "" )
			self.statusMessage(csstatus.RELATION_MSG_I_REFUSE_OHTERS_INVITE, name)
		else:
			if self.canMakeFriend( name ):
				relationItem = self.getRelationItemByName( name )
				if relationItem: self.removeFoeAndBlacklist( relationItem )
				inviteFriendBase.addFriendReplyTrue( self, self.getName(), self.databaseID, self.getProfession(), self.getLevel(), self.getCamp(), self.tongName, self.birthSpace )

	def addFriendReplyTrue( self, playerMailBox, _playerName, _playerDBID, _profession, _level, _camp, _tongName, _localSpace ):
		"""
		<define method>
		对方玩家同意成为好友
		"""
		_relationUID = KST.g_baseAppEntity.getRelationUID()
		relationItem = self.getRelationItemByName( _playerName )
		if relationItem:
			# 此处，可能主动先添加对方黑名单！然后，接受了对方好友的邀请
			self.removeFoeAndBlacklist( relationItem )
			if relationItem.relationStatus: 
				_relationUID = relationItem.relationUID
		
		if _relationUID == -1: return
		_relationStatus = csdefine.ROLE_RELATION_FRIEND | ( csdefine.ROLE_RELATION_FRIEND << RELATION_STATUS_OFFSET )
		# 约定：发起加好友者作为sm_写入db
		relationItem = ActiveRelationItem( relationUID=_relationUID, playerName=_playerName, profession=_profession, level=_level,\
			camp=_camp, relationStatus=_relationStatus, playerBase=playerMailBox, playerDBID=_playerDBID, \
			DBID=self.databaseID, tongName=_tongName, localSpace=_localSpace )
		self.relationDatas[_relationUID] = relationItem
		relationItem.writeToDB( self.saveRoleRelationCB, True )
		
		self.friends[_playerDBID] = relationItem
		self.addPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST, _relationUID )
		self.client.relation_addFriendRelation( str(_relationUID), playerMailBox.id, _playerName, str(_playerDBID), relationItem.convertRelationStatus(), _profession, _level, _camp,_tongName,_localSpace )
		playerMailBox.addFriendSuccess( self, _relationUID, self.getName(), self.databaseID, self.getProfession(), self.getLevel(), self.getCamp(), self.tongName, self.birthSpace )
		self.writeToDB()
		
	def addFriendSuccess( self, playerMailBox, _relationUID, _playerName, _playerDBID, _profession, _level, _camp, _tongName, _localSpace ):
		"""
		<define method>
		成功添加朋友
		"""
		relationItem = self.getRelationItemByName( _playerName )
		_relationStatus = 0
		if relationItem:
			self.removeFoeAndBlacklist( relationItem )
			_relationStatus = relationItem.relationStatus
			
		_relationStatus |= csdefine.ROLE_RELATION_FRIEND | ( csdefine.ROLE_RELATION_FRIEND << RELATION_STATUS_OFFSET )
		relationItem = PassiveRelationItem( relationUID=_relationUID, playerName=_playerName, profession=_profession, level=_level, \
			camp=_camp, relationStatus=_relationStatus, playerBase=playerMailBox, \
			playerDBID=_playerDBID, DBID=self.databaseID, tongName=_tongName,localSpace=_localSpace )

		self.relationDatas[_relationUID] = relationItem
		self.friends[_playerDBID] = relationItem
		self.addPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST, _relationUID )
		self.client.relation_addFriendRelation( str(_relationUID), playerMailBox.id, _playerName, str(_playerDBID), relationItem.convertRelationStatus(), _profession, _level, _camp,_tongName,_localSpace )
		self.writeToDB()

	def removeFoeAndBlacklist( self, relationItem ):
		"""
		如果对方被加入 黑名单（仇人），先去除
		"""
		#因为这里是单边关系，所以需要本地存储
		if relationItem.hasRelationWithTarget( csdefine.ROLE_RELATION_BLACKLIST ):					# 如果对方被加入 黑名单，先去除
			relationItem.removeMyRelation( csdefine.ROLE_RELATION_BLACKLIST, True )
			del self.blacklist[relationItem.playerDBID]
			self.updateCellBlacklist()
			self.delPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_BLEACK_LIST, relationItem.relationUID )
			if relationItem.playerBase:
				relationItem.playerBase.removeTargetRelation( relationItem.relationUID, csdefine.ROLE_RELATION_BLACKLIST)
			self.client.relation_removeBlackList( str( relationItem.relationUID ) )
			
		if relationItem.hasRelationWithTarget( csdefine.ROLE_RELATION_FOE ):
			relationItem.removeMyRelation( csdefine.ROLE_RELATION_FOE, True )
			del self.foeDict[relationItem.playerDBID]
			self.delPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_FOE_LIST, relationItem.relationUID )
			if relationItem.playerBase:
				relationItem.playerBase.removeTargetRelation( relationItem.relationUID, csdefine.ROLE_RELATION_FOE)
			self.client.relation_removeFoe( str( relationItem.relationUID ) )
			
		if relationItem.relationStatus == 0:
			del self.relationDatas[relationItem.relationUID]
	
	def removeFriend( self,relationUID ):
		"""
		<Exposed method>
		删除好友
		"""
		if not self.validateClientCall():
			return
		relationUID = int( relationUID )
		relationItem = self.relationDatas.get( relationUID, None )
		if not relationItem:return
		if not self.canRemoveFriend( relationItem ):return
		
		if relationItem.playerBase:													# 如果对方在线,则让对方保存数据库
			relationItem.playerBase.dstRemoveFriend( relationUID )
			relationItem.removeRelationEachOther( csdefine.ROLE_RELATION_FRIEND )
		else:																		# 如果对方不在线，则只是移除自己的关系，并保存
			relationItem.removeMyRelation( csdefine.ROLE_RELATION_FRIEND )
		del self.friends[relationItem.playerDBID]
		if relationItem.relationStatus == 0:
			del self.relationDatas[relationItem.relationUID]
		self.delPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST, relationItem.relationUID )
		self.client.relation_removeFriend( str(relationUID ))
		self.writeToDB()
		self.statusMessage( csstatus.RELATION_MSG_REMOVE_FRIEND_SUCESS )
		
	def dstRemoveFriend( self, relationUID ):
		"""
		<define method>
		对方移除了好友关系，设置己方数据
		"""
		relationItem = self.relationDatas.get( relationUID, None )
		if relationItem:
			relationItem.removeRelationEachOther( csdefine.ROLE_RELATION_FRIEND )
			if relationItem.playerDBID in self.friends:
				del self.friends[relationItem.playerDBID]
				self.delPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST, relationItem.relationUID )
				self.statusMessage( csstatus.RELATION_MSG_FRIEND_TARGET_REMOVE, relationItem.playerName )
				self.client.relation_removeFriend( str( relationUID ))
			if relationItem.relationStatus == 0:
				del self.relationDatas[relationItem.relationUID]
			
			self.writeToDB()
		
	def canMakeFriend( self, playerName ):
		"""
		是否能添加该好友
		"""
		if self.getName() == playerName:
			self.statusMessage( csstatus.RELATION_MSG_CANOT_MAKE_FRIEND_YOURSELF )
			return False
		if self.getFriendCount() >= Const.FRIEND_FRIEND_MAX_COUNT:
			self.statusMessage( csstatus.RELATION_MSG_FRIEND_LIST_FULL )
			return False
		if self.hasFriend( playerName ):
			self.statusMessage( csstatus.RELATION_MSG_REPEAT_MAKE_FRIEND, playerName )
			return False
#		if self.hadBlacklist( playerName ):
#			self.statusMessage( csstatus.RELATION_MSG_IN_BLACK_CANOT_MAKE_FRI, playerName )
#			return False
		return True
		
	def canRemoveFriend( self, relationItem ):
		"""
		是否能删除该好友
		"""
		return True
		
	def getFriendCount( self ):
		return len( self.friends )
		
	def hasFriend( self, playerName ):
		for item in self.friends.values():
			if item.playerName == playerName:
				return True
		return False

	def hasFriendBuyPlayerDBID( self, playerDBID ):
		for key in self.friends:
			if key == playerDBID:
				return True
		return False

	def getFriendNameBuyPlayerDBID( self, playerDBID ):
		"""
		<Define method>
		通过好友的DBID获得好友的名字
		"""
		for key,item in self.friends.items():
			if key == playerDBID:
				return item.playerName
		return None

	def IsFriendOnLogin( self, playerDBID ):
		"""
		好友是否在线
		"""
		for key,item in self.friends.items():
			if key == playerDBID:
				return item.playerBase
		return None
		
	def addTargetRelation( self, _relationUID, _playerName, _profession, _level, _camp, _playerBase, _playerDBID, _tongName, _localSpace, relation ):
		"""
		define method
		添加单边关系，通知对方更新数据
		"""
		if _relationUID in self.relationDatas:
			self.relationDatas[_relationUID].addTargetRelation( relation )
			return
		
		_relationStatus = relation << RELATION_STATUS_OFFSET	#这里需要移动16位
		relationItem = PassiveRelationItem( relationUID=_relationUID, playerName=_playerName, profession=_profession, level=_level, \
			camp=_camp, relationStatus=_relationStatus, playerBase=_playerBase, \
			playerDBID=_playerDBID, DBID=self.databaseID, tongName=_tongName,localSpace=_localSpace )
		self.relationDatas[_relationUID] = relationItem
		
	def removeTargetRelation( self, relationUID, relation ):
		"""
		define method
		移除单边关系，通知对方更新数据
		"""
		if relationUID in self.relationDatas:
			self.relationDatas[relationUID].removeTargetRelation( relation )
	
	#----------------------------------------------------------------------------------------------
	# foe method
	#----------------------------------------------------------------------------------------------
	def addFoe( self, name ):
		"""
		<Exposed method>
		添加仇人
		"""
		if not self.validateClientCall():
			return
		if not self.canAddFoe( name ):return
		relationItem = self.getRelationItemByName( name )
		if relationItem is None:
			KST.g_baseAppEntity.lookupRoleBaseByName( name, Functions.Functor( self._addFoeLookUpBaseCB, name ) )
		else:
			if relationItem.hasRelationWithTarget( csdefine.ROLE_RELATION_FRIEND ):			# 如果之前是好友关系，则先解除好友关系
				if relationItem.playerBase:													# 如果对方在线,则让对方保存数据库
					relationItem.playerBase.dstRemoveFriend( relationItem.relationUID )
					relationItem.removeRelationEachOther( csdefine.ROLE_RELATION_FRIEND )
				else:																		# 如果对方不在线，则只是移除自己的关系，并保存
					relationItem.removeMyRelation( csdefine.ROLE_RELATION_FRIEND )
			
				#relationItem.removeMyRelation( csdefine.ROLE_RELATION_FRIEND )
				del self.friends[relationItem.playerDBID]
				self.delPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST, relationItem.relationUID )
				self.client.relation_removeFriend( str(relationItem.relationUID ))
				#if relationItem.playerBase:
				#	relationItem.playerBase.removeTargetRelation( relationItem.relationUID, csdefine.ROLE_RELATION_FRIEND )
			
			if relationItem.relationStatus != 0:
				relationItem.addMyRelation( csdefine.ROLE_RELATION_FOE )
				self.foeDict[relationItem.playerDBID] = relationItem
				self.addPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_FOE_LIST, relationItem.relationUID )
				self.client.relation_addFoeRelation( str(relationItem.relationUID), name, str(relationItem.playerDBID), \
				relationItem.playerID, relationItem.convertRelationStatus(), relationItem.profession, relationItem.level, relationItem.camp,\
				relationItem.tongName, relationItem.localSpace )
				if relationItem.playerBase:
					relationItem.playerBase.addTargetRelation( relationItem.relationUID, self.playerName, self.profession, self.level, self.camp, self, self.databaseID, self.tongName, self.birthSpace, csdefine.ROLE_RELATION_FOE )
				self.writeToDB()
				return
			
			del self.relationDatas[relationItem.relationUID]
			if relationItem.playerBase:
				relationItem.playerBase.cell.addFoeRequest( self )
				return
			
			KST.g_baseAppEntity.lookupRoleBaseByName( name, Functions.Functor( self._addFoeLookUpBaseCB, name ) )	
		
	def _addFoeLookUpBaseCB( self, playerName, resultMB ):
		"""
		查询欲加入仇人的玩家是否在线
		"""
		if resultMB is None:
			self.statusMessage( csstatus.RELATION_MSG_PLAYER_IS_OFFLINE )
			return
		resultMB.cell.addFoeRequest( self )
		
	def addFoeReply( self, _playerBase, _playerDBID, _playerName, _profession, _level, _camp, _tongName, _localSpace ):
		"""
		<Define method>
		加对方为仇人数据请求的回复
		"""
		relationItem = self.getRelationItemByName( _playerName )
		if relationItem is not None:
			KBEDebug.ERROR_MSG("Find relationItem is err!!item must be None !!")
			return
		
		_relationUID = KST.g_baseAppEntity.getRelationUID()
		if _relationUID == -1:return
		_relationStatus = csdefine.ROLE_RELATION_FOE << RELATION_STATUS_OFFSET
		relationItem = ActiveRelationItem( relationUID=_relationUID, playerName=_playerName, profession=_profession, level=_level, camp=_camp,\
					relationStatus=_relationStatus, playerBase=_playerBase, playerDBID=_playerDBID, DBID=self.databaseID,\
					tongName=_tongName, localSpace=_localSpace )
		
		self.relationDatas[_relationUID] = relationItem
		self.foeDict[_playerDBID] = relationItem
		self.addPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_FOE_LIST, _relationUID )
		relationItem.writeToDB( self.saveRoleRelationCB, True )
		self.client.relation_addFoeRelation( str( _relationUID ), _playerName, str(_playerDBID), _playerBase.id, relationItem.convertRelationStatus(), _profession, _level, _camp, _tongName, _localSpace )
		_playerBase.addTargetRelation(_relationUID, self.playerName, self.profession, self.level, self.camp, self, self.databaseID, self.tongName, self.birthSpace, csdefine.ROLE_RELATION_FOE)
		
	def removeFoe( self, relationUID ):
		"""
		<Exposed method>
		移除仇人
		"""
		if not self.validateClientCall():
			return
		relationUID = int(relationUID)
		relationItem = self.relationDatas.get( relationUID )
		if not relationItem:return
		relationItem.removeMyRelation( csdefine.ROLE_RELATION_FOE )
		del self.foeDict[relationItem.playerDBID]
		self.delPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_FOE_LIST, relationItem.relationUID )
		if relationItem.playerBase:
			relationItem.playerBase.removeTargetRelation( relationItem.relationUID, csdefine.ROLE_RELATION_FOE )
		self.client.relation_removeFoe( str( relationUID ) )
		self.writeToDB()
		
	def hasFoe( self, playerName ):
		"""
		是否存在该仇人
		"""
		for item in self.foeDict.values():
			if item.playerName == playerName:
				return True
		return False
		
	def canAddFoe( self, playerName ):
		if self.getName() == playerName:
			self.statusMessage( csstatus.RELATION_MSG_CANOT_MAKE_NFRIEND_YOURSELF )
			return False
		if self.hasFoe( playerName ):
			self.statusMessage( csstatus.RELATION_MSG_REPEAT_MAKE_FRIEND, playerName )
			return False
		if len( self.foeDict ) > Const.RELATION_FOE_NUM_LIMIT:
			self.statusMessage( csstatus.RELATION_MSG_NOT_FRIEND_LIST_FULL )
			return False
		return True
	
	#----------------------------------------------------------------------------------------------
	# black list method
	#----------------------------------------------------------------------------------------------
	def addBlacklist( self, name ):
		"""
		<Exposed method>
		添加黑名单  关系：主动添加黑名单<-->被添加黑名单
		如果 跟对方是好友，解除关系
		"""
		if not self.validateClientCall():
			return
		if not self.canAddBlackName( name ):return
		
		relationItem = self.getRelationItemByName( name )
		if relationItem is None:
			KST.g_baseAppEntity.lookupRoleBaseByName( name, self._addBlacklistLookUpBaseCB )
		else:												# 如果玩家在线,则在己方加入黑名单，并对方加入 被加入黑名单
			if relationItem.hasRelationWithTarget( csdefine.ROLE_RELATION_FRIEND ):
				if relationItem.playerBase:													# 如果对方在线,则让对方保存数据库
					relationItem.playerBase.dstRemoveFriend( relationItem.relationUID )
					relationItem.removeRelationEachOther( csdefine.ROLE_RELATION_FRIEND )
				else:																		# 如果对方不在线，则只是移除自己的关系，并保存
					relationItem.removeMyRelation( csdefine.ROLE_RELATION_FRIEND )
			
				#relationItem.removeMyRelation( csdefine.ROLE_RELATION_FRIEND )
				del self.friends[relationItem.playerDBID]
				self.delPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST, relationItem.relationUID )
				self.client.relation_removeFriend( str(relationItem.relationUID ))
				#if relationItem.playerBase:
				#	relationItem.playerBase.removeTargetRelation( relationItem.relationUID, csdefine.ROLE_RELATION_FRIEND )
				
			if relationItem.relationStatus != 0:
				relationItem.addMyRelation( csdefine.ROLE_RELATION_BLACKLIST )
				self.blacklist[relationItem.playerDBID] = relationItem
				self.updateCellBlacklist()
				self.addPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_BLEACK_LIST, relationItem.relationUID )
				self.client.relation_addBlacklistRelation( str( relationItem.relationUID ), relationItem.playerName, str(relationItem.playerDBID), relationItem.playerID,\
				relationItem.convertRelationStatus(), relationItem.profession, relationItem.level, relationItem.camp, relationItem.tongName, relationItem.localSpace )
				if relationItem.playerBase:
					relationItem.playerBase.addTargetRelation( relationItem.relationUID, self.playerName, self.profession, self.level, self.camp, self, self.databaseID, self.tongName, self.birthSpace, csdefine.ROLE_RELATION_BLACKLIST )
				self.writeToDB()
				return
			
			del self.relationDatas[relationItem.relationUID]
			if relationItem.playerBase:
				relationItem.playerBase.cell.addBlacklistRequest( self )
				return
			
			KST.g_baseAppEntity.lookupRoleBaseByName( name, Functions.Functor( self._addFoeLookUpBaseCB, name ) )	
	
	
	def _addBlacklistLookUpBaseCB( self, resultMB ):
		"""
		"""
		if resultMB is None:
			self.statusMessage( csstatus.RELATION_MSG_PLAYER_IS_OFFLINE )
			return
		resultMB.cell.addBlacklistRequest( self )

	def addBlacklistReply( self, _playerBase, _playerDBID, _playerName, _profession, _level, _camp, _tongName, _localSpace ):
		"""
		<Define method>
		加对方为黑名单数据请求的回复
		"""
		relationItem = self.getRelationItemByName( _playerName )
		if relationItem is not None:
			KBEDebug.ERROR_MSG("Find relationItem is err!!item must be None !!")
			return
			
		_relationUID = KST.g_baseAppEntity.getRelationUID()
		if _relationUID == -1:return
		
		_relationStatus = csdefine.ROLE_RELATION_BLACKLIST << RELATION_STATUS_OFFSET
		relationItem = ActiveRelationItem( relationUID=_relationUID, playerName=_playerName, profession=_profession, level=_level, camp=_camp,\
				relationStatus=_relationStatus, playerBase=_playerBase, playerDBID=_playerDBID, DBID=self.databaseID,\
				tongName=_tongName, localSpace=_localSpace )
		
		self.relationDatas[_relationUID] = relationItem
		self.blacklist[_playerDBID] = relationItem
		self.updateCellBlacklist(  )
		relationItem.writeToDB( self.saveRoleRelationCB, True )
		
		self.addPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_BLEACK_LIST, _relationUID )
		self.client.relation_addBlacklistRelation( str( _relationUID ), _playerName, str(_playerDBID), _playerBase.id, relationItem.convertRelationStatus(), _profession, _level, _camp, _tongName, _localSpace )
		_playerBase.addTargetRelation(_relationUID, self.playerName, self.profession, self.level, self.camp, self, self.databaseID, self.tongName, self.birthSpace, csdefine.ROLE_RELATION_BLACKLIST)
		self.writeToDB()
	
	def removeBlacklist( self, relationUID ):
		"""
		<Exposed method>
		移出黑名单
		"""
		if not self.validateClientCall():
			return
		relationUID = int( relationUID )
		relationItem = self.relationDatas.get( relationUID, None )
		if relationItem is None:
			KBEDebug.ERROR_MSG( "player(%s):relationItem(%i) is not exit!!" %( self.getName(), relationUID ) )
			return
		
		relationItem.removeMyRelation( csdefine.ROLE_RELATION_BLACKLIST )
		del self.blacklist[relationItem.playerDBID]
		self.updateCellBlacklist(  )
		self.delPlayerToCatalog( csdefine.RELATION_CATALOG_TYPE_BLEACK_LIST, relationItem.relationUID )
		self.client.relation_removeBlackList( str( relationItem.relationUID ) )
		if relationItem.playerBase:
			relationItem.playerBase.removeTargetRelation( relationItem.relationUID, csdefine.ROLE_RELATION_BLACKLIST )
		self.writeToDB()
		
	def canAddBlackName( self, playerName ):
		"""
		是否能添加黑名单
		"""
		if self.getName() == playerName:
			self.statusMessage( csstatus.RELATION_MSG_CANOT_MAKE_BLACK_YOURSELF )
			return False
		if self.hadBlacklist( playerName ):
			self.statusMessage( csstatus.RELATION_MSG_IN_BLACKLIST, playerName )
			return False
		if self.getBlacklistCount() > Const.FRIEND_BLACKLIST_MAX_COUNT:
			self.statusMessage( csstatus.RELATION_MSG_BLACK_LIST_FULL )
			return False
		return True
	
	def hadBlacklist( self, playerName ):
		"""
		是否已经存在黑名单
		"""

		for item in self.blacklist.values():
			if item.playerName == playerName:
				return True
		return False

	def getBlacklistCount( self ):
		return len( self.blacklist )

	def updateCellBlacklist( self ):
		CellBlacklist = []
		for item in self.blacklist.keys():
			CellBlacklist.append(item )
		self.cell.updateBlacklist( CellBlacklist )

	def onFriendChat( self, chatData ):
		"""
		define method
		好友聊天
		"""
		name = chatData.name
		
		relationItem = self.getRelationItemByName( name )
		if relationItem is None:return
		if relationItem.hasRelationWithTarget( csdefine.ROLE_RELATION_BLACKLIST ):
			self.statusMessage( csstatus.RELATION_MSG_IN_MY_BLACK_LIST, "" )
			return
		if relationItem and relationItem.playerBase:
			relationItem.playerBase.onFriendChatCB( self, chatData, self.playerName )
		else:
			self.statusMessage( csstatus.RELATION_MSG_SEND_MSG_AS_PALYER_OFFLINE, "" )
	
	def onFriendChatCB( self, srcEntityBase, chatData, srcPlayerName ):
		"""
		define method
		聊天回调
		"""
		if chatData.playerDBID in self.blacklist:
			srcEntityBase.statusMessage( csstatus.RELATION_MSG_IN_OTHER_BLACK_LIST, "" )
			return
		if chatData.type == csdefine.CHAT_TYPE_WHISPER:
			srcEntityBase.addRecentContacts(chatData.name.split("|")[1])
		else: 
			srcEntityBase.addRecentContacts(chatData.name)
		self.addRecentContacts(srcPlayerName)
		srcEntityBase.client.onReceiveChatMessageCB( chatData )
		self.client.onReceiveChatMessageCB( chatData )
		
	def onWhisperChat( self, chatData ):
		"""
		define method
		密语聊天
		"""
		name = chatData.name.split("|")[1]
		
		relationItem = self.getRelationItemByName( name )
		if relationItem:			# 如果有关系
			if relationItem.hasRelationWithTarget( csdefine.ROLE_RELATION_BLACKLIST ):
				self.statusMessage( csstatus.RELATION_MSG_IN_MY_BLACK_LIST, "" )
				return
			if relationItem.playerBase:
				relationItem.playerBase.onFriendChatCB( self, chatData, self.playerName )
			else:
				self.statusMessage( csstatus.RELATION_MSG_SEND_MSG_AS_PALYER_OFFLINE, "" )
		else:
			chatManager = KBEngine.globalData.get( "ChatManager", None )
			if chatManager != None:
				chatManager.onDesignatedChat( self, name, chatData, self.playerName )
	#----------------------------------------------------------------------------------------------
	# 最近联系人
	#----------------------------------------------------------------------------------------------
	def addRecentContacts( self, name ):
		"""
		<Exposed method>
		添加最近联系人
		"""
		if not self.validateClientCall():
			return
		relationItem = self.getRelationItemByName( name )
		if relationItem:
			self._addRecentContacts(relationItem)
		else:
			KST.g_baseAppEntity.lookupRoleBaseByName( name, self.addRecentContactsCB )
			
	def _addRecentContacts(self, relationItem):
		"""
		"""
		if relationItem is None:
			return
		
		UID = relationItem.relationUID
		if UID not in self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST]:
			self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST].insert( 0, UID )
			relationItem.addMyRelation( csdefine.ROLE_RELATION_LAST_CHAT )
			self.lastChat[relationItem.playerDBID] = relationItem
			if relationItem.playerBase:
				relationItem.playerBase.addTargetRelation( relationItem.relationUID, self.playerName, self.profession, self.level, self.camp, self, self.databaseID, self.tongName, self.birthSpace, csdefine.ROLE_RELATION_LAST_CHAT )
				if (UID not in self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_FRIEND_LIST]) and (UID not in self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_FOE_LIST]):
					self.client.relation_addRecentContactsDatas( str( UID ), relationItem.playerName, str(relationItem.playerDBID), relationItem.playerBase.id, relationItem.convertRelationStatus(), relationItem.profession,\
			 relationItem.level, relationItem.camp, relationItem.tongName, relationItem.localSpace )
					relationItem.writeToDB( self.saveRoleRelationCB, True )
				else:
					self.client.relation_addRecentContacts( str(UID ))
		else:
			if self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST][0] == UID:return
			self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST].remove( UID )
			self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST].insert( 0, UID )
			self.client.relation_addRecentContacts( str(UID ))
			
	def addRecentContactsCB( self, resultMB ):
		if resultMB is None:
			self.statusMessage( csstatus.RELATION_MSG_PLAYER_IS_OFFLINE )
			return
		resultMB.cell.addRecentContactsRequest( self )
	
	def addRecentContactsReply( self, _playerBase, _playerDBID, _playerName, _profession, _level, _camp, _tongName, _localSpace ):
		"""
		<define method>
		最近联系人 数据请求回应
		"""
		#这里是异步过来的，所以也需要先查一下有没关系
		relationItem = self.getRelationItemByName( _playerName )
		if relationItem:
			self._addRecentContacts(relationItem)
			return
		
		_relationUID = KST.g_baseAppEntity.getRelationUID()
		if _relationUID == -1:return
		_relationStatus = csdefine.ROLE_RELATION_LAST_CHAT << RELATION_STATUS_OFFSET
		relationItem = ActiveRelationItem( relationUID=_relationUID, playerName=_playerName, profession=_profession, level=_level, camp=_camp,\
					 relationStatus=_relationStatus, playerBase=_playerBase, playerDBID=_playerDBID, DBID=self.databaseID,\
					 tongName=_tongName, localSpace=_localSpace )
		
		self.relationDatas[_relationUID] = relationItem
		self.lastChat[_playerDBID] = relationItem
		if len( self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST] ) >= Const.RELATION_LAST_CHAT_LIMIT:
			lastUID = self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST][-1]
			self.removeRecentContacts( lastUID )
		self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST].insert( 0, _relationUID )
		relationItem.writeToDB( self.saveRoleRelationCB, True )
		self.client.relation_addRecentContactsDatas( str( _relationUID ), _playerName, str(_playerDBID), _playerBase.id, relationItem.convertRelationStatus(), _profession,\
		 _level, _camp, _tongName, _localSpace )
			
	def removeRecentContacts( self, relationUID ):
		"""
		<Exposed method>
		删除最近联系人
		"""
		if not self.validateClientCall():
			return
		relationUID = int( relationUID )
		if relationUID in self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST]:
			self.relationCatalog[csdefine.RELATION_CATALOG_TYPE_LASTTIME_LIST].remove( relationUID )
		relationItem = self.relationDatas.get( relationUID )
		if relationItem and relationItem.playerDBID in self.lastChat:
			self.lastChat.pop( relationItem.playerDBID )
			relationItem.removeMyRelation( csdefine.ROLE_RELATION_LAST_CHAT )
			if relationItem.playerBase:
				relationItem.playerBase.removeTargetRelation( relationItem.relationUID, csdefine.ROLE_RELATION_LAST_CHAT )
			self.client.relation_removeRecentContacts( str( relationItem.relationUID ) )
			
	def removeAllRecentContacts( self ):
		"""
		<Exposed method>
		清除最近联系人
		"""
		if not self.validateClientCall():
			return
		for relationItem in list(self.lastChat.values()):
			self.removeRecentContacts( relationItem.relationUID )
	#----------------------------------------------------------------------------------------------
	# 讨论组
	#----------------------------------------------------------------------------------------------
	def createGroup( self, groupName, isAllowJoin, passWord ):
		"""
		<Exposed method>
		创建一个讨论组
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["RelationManager"].createGroup( self, groupName, isAllowJoin, passWord, \
		self.getName(), self.databaseID, self.getProfession(), self.getLevel(), self.getCamp() )
		
	def deleteGroup( self, groupIndex ):
		"""
		<Exposed method>
		解散一个讨论组
		"""
		if not self.validateClientCall():
			return
		groupIndex = int( groupIndex )
		KBEngine.globalData["RelationManager"].deleteGroup( groupIndex )
		
	def invitedToGroup( self, groupIndex, targetName ):
		"""
		<Exposed method>
		邀请玩家加入讨论组
		"""
		if not self.validateClientCall():
			return
		groupIndex = int( groupIndex )
		KBEngine.globalData["RelationManager"].invitedToGroup( self, groupIndex, self.getName(), targetName )
		
	def beInvitedToGroup( self, playerMB, sourcePlayerName, groupName, index ):
		"""
		<define method>
		被邀请加入 讨论组
		"""
		self.inviteGroupBase = playerMB
		self.inviteGroupIndex = index
		
		self.inquireMessage( csstatus.RELATION_MSG_REQUEST_ADD_GROUP, [ sourcePlayerName, groupName ], "replyInvitedToGroup" )
		
	def replyInvitedToGroup( self, reply ):
		"""
		回应 邀请加入 讨论组
		"""
		if self.inviteGroupBase is None:return
		if reply:
			KBEngine.globalData["RelationManager"].replyForInvitedToGroup( self, self.inviteGroupIndex, self.getName(), self.databaseID, self.getProfession(), self.getLevel(), self.getCamp() )
		else:
			self.inviteGroupBase.client.statusMessage( csstatus.RELATION_MSG_REFUSE_INVITATION, "" )
			
		self.inviteGroupBase = None
		self.inviteGroupIndex = -1
		
	def requestEnterGroup( self, groupIndex ):
		"""
		<Exposed method>
		玩家主动申请加入讨论组
		"""
		if not self.validateClientCall():
			return
		groupIndex = int( groupIndex )
		KBEngine.globalData["RelationManager"].requestEnterGroup( self, groupIndex, self.getName(), self.databaseID, self.getProfession(), self.getLevel(), self.getCamp() )
		
	def requestEnterGroupByPassword( self, groupIndex, passWord ):
		"""
		<Exposed method>
		玩家主动申请加入讨论组
		"""
		if not self.validateClientCall():
			return
		groupIndex = int( groupIndex )
		KBEngine.globalData["RelationManager"].requestEnterGroupByPassword( self, groupIndex, passWord, self.getName(), self.databaseID, self.getProfession(), self.getLevel(), self.getCamp() )
		
	def activeLeaveGroup( self, groupIndex ):
		"""
		<Exposed method>
		申请 退出一个讨论组
		"""
		if not self.validateClientCall():
			return
		groupIndex = int( groupIndex )
		KBEngine.globalData["RelationManager"].activeLeaveGroup( groupIndex, self.getName() )
		
	def passiveLeaveGroup( self, groupIndex, playerName ):
		"""
		<Exposed method>
		管理员 请离一个组员
		"""
		if not self.validateClientCall():
			return
		groupIndex = int( groupIndex )
		KBEngine.globalData["RelationManager"].passiveLeaveGroup( self.getName(), groupIndex, playerName )
		
	def updateGroupInfo( self, uid, groupName, canJoin, passWord ):
		"""
		<Exposed method>
		更新讨论组信息
		"""
		if not self.validateClientCall():
			return
		groupIndex = int( uid )
		KBEngine.globalData["RelationManager"].updateGroupInfo( groupIndex, self.getName(), groupName, bool(canJoin), passWord )
	
	def changeGroupLeater( self, groupIndex, playerName ):
		"""
		<Exposed method>
		讨论组 修改管理员
		"""
		if not self.validateClientCall():
			return
		groupIndex = int( groupIndex )
		KBEngine.globalData["RelationManager"].changeGroupLeater( groupIndex, self.getName(), playerName )
		
	def addGroupBlackList( self, groupUID, playerName ):
		"""
		<Exposed method>
		讨论组 增加黑名单
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["RelationManager"].addGroupBlackList( self, int(groupUID), self.getName(), playerName )
		
	def delGroupBlackList( self, groupUID, playerName ):
		"""
		<Exposed method>
		讨论组 删除黑名单
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["RelationManager"].delGroupBlackList( self, int(groupUID), self.getName(), playerName )
		
	def addEndTime( self, groupIndex, endType ):
		"""
		<Exposed method>
		增加 讨论组使用时间
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["RelationManager"].addEndTime( self, int( groupIndex ), self.getName(), int(endType) )
		
	def addEndTimeSuccess( self, groupIndex, endType ):
		"""
		<define method>
		增加 讨论组使用时间
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["RelationManager"].addEndTimeSuccess( self, groupIndex, endType )
		
	def requestRandomGroup( self ):
		"""
		Exposed method
		请求获取随机讨论组
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["RelationManager"].requestRandomGroup( self )
