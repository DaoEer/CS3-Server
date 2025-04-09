# -*- coding: utf-8 -*-

import time, operator

import KBEngine
import KBEDebug
import csdefine
from CoreObject.GameObject import GameObject
from ImpInterface.TeamSpaceRelationInterface import TeamSpaceRelationInterface
import csstatus
import csconst
import json

OFFLINE_LEAVE_TIMER = 1 	# 玩家下线，离线处理检测TIMER

class TeamMember(object): 
	"""
	"""
	def hasMemberMB(self):
		"""
		"""
		return hasattr(self, "baseMailbox") and self.baseMailbox
		
	def hasMemberClient(self):
		"""
		"""
		if not self.hasMemberMB():
			return False
		
		memberMB = self.baseMailbox
		return hasattr(memberMB, "client") and memberMB.client

class TeamEntity( KBEngine.Entity, GameObject, TeamSpaceRelationInterface ):
	def __init__( self ):
		KBEngine.Entity.__init__( self )
		GameObject.__init__( self )
		TeamSpaceRelationInterface.__init__( self )
		
		# 取队伍管理器
		self.teamManager = KBEngine.globalData.get("TeamManager", None)
		if self.teamManager == None:
			KBEDebug.ERROR_MSG( "get teammanager entity fault!" )
			return
		# 注册管理器
		self.teamManager.register( self )
		
		self.captainID = self.teamArg["captainID"]		# 记录队长entityID
		self.captainName = self.teamArg["captainName"]	# 记录队长名字
		self.signerID = self.captainID					# 拥有标记权的队员
		self.member = []								# [(entityID, instance of TeamMember), ...]; see also self.join()
		self.allocation = self.teamArg["allocation"]	#分配模式
		self.quality = self.teamArg["quality"]			#分配品质
		self.offlineTime = 0.0							# 离线记时ID
		self.offlineDBIDs = {}							# { playerDBID : ( id, logout time ) } # 加入id，主要是为了处理离队
		self.teamSignData = {}							# 队伍标记数据{entityID: signNumber}
		self.followList = []							# 组队跟随中的队员ID
		self.followLeaderID = 0							# 记录队伍跟随领导者ID（目前是队长领导，但是不排除以后可以由其他人领导）
		del self.teamArg	# 删除初始化数据
		self.isReqCopyCampYXLM = False  #是否在申请英雄联盟排队
		self.isReqCopyCampSGMZ = False  #是否在申请上古密阵排队
		self.isReqCampRandomFit = False  #是否在申请阵营战场随机匹配
		self.isReqBattle = False #是否在申请团队竞技战场匹配
		self.offlineTimeKey = 0
		self.fastTeamMaxMemberNum = csconst.TEAM_MEMBER_MAX #快速组队默认队伍最大人数

		self.isReqFastTeam = False		#是否在申请快速组队
		self.fastTeamSpaceScriptID = "" #正在申请快速组队的副本
		self.disbandNotifyMember = [] #解散队伍是已通知的成员ID

	def _getMemberInfoByDBID( self, playerDBID ):
		"""
		获取entity的mailbox
		@return: 队伍成员的entityID及信息字典
		"""
		for entityID, info in self.member:
			if info.dbid == playerDBID:
				return entityID, info
		return None, None

	def _getMemberInfoByEntityID( self, entityID ):
		"""
		通过玩家的id获得玩家的信息

		@param entityID : OBJECT_ID
		"""
		for playerID, info in self.member:
			if playerID == entityID:
				return info
		return None

	def _removeOfflineDBID( self, playerDBID ):
		"""
		从离线表中清出一个玩家
		"""
		self.offlineDBIDs.pop( playerDBID, None )

	def _notifyInfoToJoinPlayer( self, playerBase ):
		"""
		向新队员发送队伍信息

		@param playerBase: 玩家的BaseEntityMailbox
		"""
		memberInfo = []
		for entityID, info in self.member:
			info = { "DBID":info.dbid,"entityID":entityID, "name":info.name, "baseMB":info.baseMailbox, "profession":info.profession, "level":info.level }
			memberInfo.append( info )
		
		signKeys = []
		signValues = []
		for k,v in self.teamSignData.items():
			signKeys.append(k)
			signValues.append(v)
		
		playerBase.teamInfoNotifyOnJoin( self.captainID, self, self.allocation, self.quality, memberInfo, self.signerID, signKeys, signValues )

	def _autoSelectCaptain( self ):
		"""
		自动选择一个队长，此函数一般用于当队长直接（断）下线时或队长离开队伍
		"""
		if len(self.member) - len(self.offlineDBIDs) <= 0:		# 当全部队员不在线的时候，不更换队长。第一个上线的就是新队长
			return

		maxTime = float( 0x7FFFFFFF )
		captain = 0
		for entityID, info in self.member:
			if info.baseMailbox != None and info.time < maxTime:	# 在线时间最长且没有掉线（有base mailbox）
				captain = info.baseMailbox.id
				maxTime = info.time
		self.changeCaptain( captain )

	def _autoSelectSigner( self ):
		"""
		拥有标记权的玩家离线，系统自动将权限转移给队中入队时间最长的队员
		"""
		if len(self.member) - len(self.offlineDBIDs) <= 0:		# 当全部队员不在线的时候，不更换标记权。第一个上线拥有标记权
			return

		maxTime = float( 0x7FFFFFFF )
		newSignerID = 0
		for entityID, info in self.member:
			if info.baseMailbox != None and info.time < maxTime:	# 在线时间最长且没有掉线（有base mailbox）
				newSignerID = info.baseMailbox.id
				maxTime = info.time
		self.changeTeamSigner( newSignerID )
		
	def isTeamFull(self, isFastTeam = False):
		"""
		"""
		#此处不能用self.isReqFastTeam判断是否是款式组队，因为快速组队队伍满员后self.isReqFastTeam值为False
		if (isFastTeam and len( self.member ) >= self.fastTeamMaxMemberNum) or len( self.member ) >= csconst.TEAM_MEMBER_MAX:
			return True
		return False
		
	def setFastTeamMaxMemberNum(self, maxNum):
		"""
		defined method
		设置快速组队队员最大人数
		"""
		self.fastTeamMaxMemberNum = maxNum

	def join( self, playerDBID, playerName, playerBase, profession, eMetaClass, level, isCreateTeam, camp ):
		"""
		<defined method>
		添加玩家到队伍中

		@param playerDBID: 玩家DBID
		@param playerBase: 玩家BaseEntityMailbox
		@param playerName: string; 玩家名称
		@param profession: INT8; 玩家职业
		@param eMetaClass: INT32;玩家实体id
		@param isCreateTeam: BOOL;是不是队伍创建时,加入创建者
		"""
		# 异步情况下什么都有可能发生，因此需要判断队伍人数是否已满
		if self.isTeamFull():
			# 快速组队至多允许三人,非快速组队至多允许五人，队伍已满，需要通知加入队伍失败
			playerBase.clearTeamInfo()
			playerBase.client.statusMessage(csstatus.TEAM_FULL_REFUSE_JOIN,"")
			return
			
		#加入别人的队伍，取消快速组队
		playerBase.fastTeamCancel()
		
		# 通知所有人有队伍成员，有新玩家加入队伍
		for entityID, info in self.member:
			if info.baseMailbox:
				info.baseMailbox.onMemberjoin( playerDBID, playerBase.id, playerName, playerBase, profession, level )
				#互相加为最近联系人
				info.baseMailbox.cell.addRecentContactsRequest(playerBase)
				playerBase.cell.addRecentContactsRequest(info.baseMailbox)
				if info.hasMemberClient():
					info.baseMailbox.client.statusMessage( csstatus.TEAM_MEMBER_JOIN, playerName )
		
		# 加入新成员到队伍中
		newMemberInfo = TeamMember()
		newMemberInfo.__dict__.update( {	"dbid"        : playerDBID,
								"name"        : playerName,
								"baseMailbox" : playerBase,
								"profession"  : profession,
								"eMetaClass"  : eMetaClass,
								"level"		  : level,
								"camp"		  : camp,
								"time"        : time.time(), } )
		self.member.append( ( playerBase.id, newMemberInfo ) )
			
		if newMemberInfo.hasMemberClient():
			if self.captainID == playerBase.id:
				if isCreateTeam :
					playerBase.client.statusMessage( csstatus.TEAM_CREATE_TEAM, "" )
			else:
				playerBase.client.statusMessage( csstatus.TEAM_JOIN_TEAM_SUCCESS, self.captainName )
		
		# 通知新成员队伍数据
		self._notifyInfoToJoinPlayer( playerBase )
		self.fastTeamOnMemberJoin( newMemberInfo )
		TeamSpaceRelationInterface.onAddMember( self, playerDBID )
		self.campRandomFitOnTeamChange()
		self.battleOnTeamChange()




	def leave( self, srcID, dstID ):
		"""
		<define method>
		开除指定玩家或者玩家自己离队
		1、如果srcID == dstID则表示自己是离队；
		2、如果srcID != dstID且srcID是队长则表示队长开除玩家出队伍

		@param srcID: OBJECT_ID; 使dstID离开队伍的ID
		@param dstID: OBJECT_ID; 离开队伍的玩家ID
		"""
		# dstID有可能是客户端过来的参数，需判断其合法性；
		# 或者远程调用leave时，dstID已经被踢出队伍，进行下面的操作前需检查dstID是否还合法。
		dstInfo = self._getMemberInfoByEntityID( dstID )
		if dstInfo is None:
			return
		
		if srcID != dstID and srcID != self.captainID:	# 既不是自己离队，也不是队长开除，直接忽略
			return
		
		for entityID, info in self.member:
			# 通知每一个在线的玩家，谁离开了队伍
			if info.baseMailbox:
				if info.hasMemberClient():
					if info.baseMailbox.id == dstID:
						info.baseMailbox.client.statusMessage( csstatus.TEAM_LEAVE, "" )
					else:
						info.baseMailbox.client.statusMessage( csstatus.TEAM_MEMBER_LEAVE_TEAM, dstInfo.name )
				info.baseMailbox.leaveTeamNotify( dstID, dstInfo.dbid )
		
		self._removeOfflineDBID( dstInfo.dbid )  # 如果玩家在离线列表中，则从离线列表中移除
		self.handleFollowOnLeave( dstInfo.baseMailbox, dstID, dstInfo.name )	# 必须在member移除和重选队长之前执行，以便离开者和队伍都能正常结束跟随
		self.member.remove( ( dstID, dstInfo ) ) # 删除离队的人员
		TeamSpaceRelationInterface.onRemoveMember( self, dstInfo.dbid )
		
		if len(self.member) <= 1:	#只剩一个人了就直接解散
			self.disband()
		else:						#没解散的话，如果离队的是队长则重选队长
			if dstID == self.captainID:
				self._autoSelectCaptain()
			if dstID == self.signerID:
				self._autoSelectSigner()
			self.fastTeamOnMemberLeave(dstInfo.baseMailbox)
		self.campYXLMOnTeamChange()
		self.campSGMZOnTeamChange()
		self.campRandomFitOnTeamChange()
		self.battleOnTeamChange()

	def changeCaptain( self, newCaptainID ):
		"""
		<define method>
		移交队长权限

		@param newCaptainID: OBJECT_ID; 新队长的entity id
		"""
		captainInfo = self._getMemberInfoByEntityID( newCaptainID )
		if captainInfo is None:
			return
		# 目标已经离线则忽略
		# 这个出现的概率会很小，但在异步的情况下确实有可能发生
		if captainInfo.baseMailbox is None:
			return
		
		oldCaptainID = self.captainID
		self.captainID = newCaptainID
		#队长换了，记录的队长名字也要换呀
		self.captainName = captainInfo.name
		
		# 通知所有成员
		for ( entityID, info ) in self.member:
			if info.baseMailbox:
				info.baseMailbox.changeCaptainNotify( newCaptainID )
				
				if info.hasMemberClient():
					info.baseMailbox.client.statusMessage( csstatus.TEAM_MEMBER_CHANGE_CANPTAIN, captainInfo.name )
		
		# 跟随新队长
		self.handleFollowOnChangeCaptain( oldCaptainID, newCaptainID )
		self.campSGMZOnTeamChange()

#------------------------------解散队伍-----------------------------
	def disband( self ):
		"""
		<define method>
		请求解散队伍，并且通知所有成员，队伍解散
		"""
		# 通知成员队伍销毁  队长最后通知
		captainInfo = None
		for entityID, info in self.member:
			if entityID == self.captainID:
				captainInfo = info
				continue
			if info.baseMailbox:
				info.baseMailbox.disbandTeamNotify()
				if info.hasMemberClient():
					info.baseMailbox.client.statusMessage( csstatus.TEAM_DISBAND, "" )

		if captainInfo != None and captainInfo.baseMailbox:
			captainInfo.baseMailbox.disbandTeamNotify()
			if captainInfo.hasMemberClient():
				captainInfo.baseMailbox.client.statusMessage( csstatus.TEAM_DISBAND, "" )
		
	def onDisbandTeamNotifyCallback(self, playerDBID):
		"""
		<define method>
		通知队员解散队伍的回调
		"""
		if id not in self.disbandNotifyMember:
			self.disbandNotifyMember.append(playerDBID)
		
		isFinished = True
		for entityID, info in self.member:
			if info.dbid not in self.disbandNotifyMember: 
				if info.dbid not in self.offlineDBIDs:
					#没有通知到并且没有在掉线类别中
					isFinished = False
					break
		
		#所有玩家通知完成
		if isFinished:
			for entityID, info in self.member:
				if info.baseMailbox:
					info.baseMailbox.onDisbandTeam()
			
			self.fastTeamOnTeamDisband()
			self.handleTeamFollowOnDisband()
			TeamSpaceRelationInterface.onDisband( self )
			self.teamManager.deregister( self.id )  # 注销自己
			self.destroySelf()                          # 销毁自己

#--------------------------------队伍玩家上下线-----------------------
	def teammateLogout( self, playerDBID ):
		"""
		<define method>
		玩家下线

		@param playerDBID: 玩家DBID
		"""
		entityID, info = self._getMemberInfoByDBID( playerDBID )
		if info is None:
			return

		logoutTime = time.time()
		self.offlineDBIDs[info.dbid] = {"id":info.eMetaClass , "logoutTime":logoutTime}
		if len(self.offlineDBIDs) == len( self.member ):
			self.offlineTime = logoutTime
		
		# 清除离队成员BASE
		info.baseMailbox = None
		if not self.offlineTimeKey:
			self.offlineTimeKey = self.addTimerRepeat( 60, "teamDisband", ())

		self.handleFollowOnLogout( entityID, info.name )	#必须在重选队长前执行，以便正常结束跟随
		if entityID == self.captainID:
			self._autoSelectCaptain()	# 重新选择队长并通知队伍所有成员

		if entityID == self.signerID:
			self._autoSelectSigner()	# 拥有分配标记权
			
		#通知在线的队友，有人下线了
		for ( _entityID, _info ) in self.member:
			if _info.baseMailbox:
				_info.baseMailbox.onTeamMateLogout( playerDBID, info.eMetaClass )
		
	def teamDisband( self ):
		"""
		队员离线超过时限剔出队伍，如果队伍只剩一人则解散队伍
		"""
		t = time.time() - csconst.TEAM_SURVIVAL_TIME
		for dbid in list(self.offlineDBIDs.keys()):
			info = self.offlineDBIDs[dbid]
			if info["logoutTime"] <= t:
				self._removeOfflineDBID(dbid)
				oldEntityID, _ = self._getMemberInfoByDBID( dbid )
				dstInfo = self._getMemberInfoByEntityID( oldEntityID )
				self.member.remove( (oldEntityID, dstInfo) )
				
				# 通知每一个在线的玩家，谁离开了队伍
				for id, member in self.member:
					if member.baseMailbox:
						member.baseMailbox.leaveTeamNotify( oldEntityID, dbid )
					if member.hasMemberClient():
						member.baseMailbox.client.statusMessage( csstatus.TEAM_MEMBER_LEAVE_TEAM, dstInfo.name )
				
		if len(self.offlineDBIDs) <= 0:		
			self.popTimer(self.offlineTimeKey)
			self.offlineTimeKey = 0
		
		if len(self.member) <= 1:
			self.disband()

	def teammateLogin( self, playerDBID, playerBase ):
		"""
		<define method>
		玩家上线，申请重新入队

		@param playerDBID: 玩家DBID
		@param playerBase: 玩家Base	
		"""
		if self.offlineTime>0 and self.offlineTime + csconst.TEAM_SURVIVAL_TIME <time.time():
			#队伍不应该存在了，解散掉（队伍无人在线超过时限）
			self.disband()
			playerBase.onRejoinTeamFailed()
			return

		oldEntityID, info = self._getMemberInfoByDBID( playerDBID )
		dic = dict( self.member )
		if info is None:
			# 找不到则表示该玩家已经被清除出队伍
			playerBase.onRejoinTeamFailed()
			return
		if self.offlineTime>0:
			#队伍全员离线，第一个上线的人将会成为队长
			self.captainID = playerBase.id
			self.signerID = playerBase.id
			self.offlineTime = 0.0
		
		self.member.remove( ( oldEntityID, dic[oldEntityID] ) )	# 先删除旧的玩家信息

		# 通知所有的在线成员，某人重新上线加入队伍了
		for entityID, tempinfo in self.member:
			if tempinfo.baseMailbox:
				tempinfo.baseMailbox.onRejoinTeam( oldEntityID, playerDBID, playerBase )

		info.baseMailbox = playerBase                 # 更新playerBase
		self.member.append( ( playerBase.id, info ) ) # 以新的entityID重新关联玩家信息
		info.eMetaClass = playerBase.id
		
		#擦，这个地方有可能已经改了队长，不管怎么样重新设置下队长的名字也是正确的
		captainInfo = self._getMemberInfoByEntityID( self.captainID )
		if captainInfo:
			self.captainName = captainInfo.name

		# 队伍向上线玩家发送成员列表
		self._notifyInfoToJoinPlayer( playerBase )		
		self._removeOfflineDBID( playerDBID )
		self.fastTeamOnMemberLogin( playerBase,playerDBID )

	def setAllocation( self, allocation ):
		"""
		<define method>
		修改队伍物品分配模式
		
		@param allocation: INT32;分配模式
		"""
		self.allocation = allocation
		for entityID, info in self.member:
			if info.baseMailbox:
				info.baseMailbox.modifyAllocation( allocation )
	
	def setQuality( self, quality ):
		"""
		<define method>
		修改队伍物品分配品质标准
		
		@param quality:  INT32;物品品质标准
		"""
		if self.allocation == csdefine.TEAM_PICKUP_TYPE_FREEDOM: #自由拾取 禁止设置品质
			return
		self.quality = quality
		for entityID, info in self.member:
			if info.baseMailbox:
				info.baseMailbox.modifyQuality( quality )

	def addTeamSign( self, playerBase, entityID, signNumber ):
		"""
		define method
		给entity打标记
		"""
		#根据最新文档，标记权和队长保持一致
		if playerBase.id != self.captainID:
			return
		
		#if playerBase.id != self.signerID:
		#	return
		
		self.teamSignData[ entityID ] = signNumber
		for memberID, info in self.member:
			if info.hasMemberClient():
				info.baseMailbox.client.AddTeamSignCB( entityID, signNumber )

	def changeTeamSigner( self, playerID ):
		"""
		define method
		移交标记权限
		"""
		if playerID != 0 and playerID == self.signerID:
			return
		
		self.signerID = playerID
		#memInfo = self._getMemberInfoByEntityID( playerID )
		
		# 目标已经离线则忽略
		# 这个出现的概率会很小，但在异步的情况下确实有可能发生
		#if memInfo.baseMailbox is None:
		#	return
		if self.teamSignData.get(playerID,None ) != None:
			self.teamSignData.pop(playerID)
			for memberID, info in self.member:
				if info.hasMemberClient():
					info.baseMailbox.client.RemoveTeamSigner(playerID)

	def sendMessageToMember( self, ids, messageType, message = "" ):
		"""
		<define method>
		给指定的队员发送消息
		
		@param ids: INT32 List;指定的ID列表
		@param messageType: INT32;消息类型
		@param message: string;消息额外参数
		"""
		for id in ids:
			info = self._getMemberInfoByEntityID( id )
			if info and info.hasMemberClient():
				info.baseMailbox.client.statusMessage( messageType, message )

	def popOfflineTimeKey( self ):
		"""
		"""
		if self.offlineTimeKey > 0:		
			self.popTimer(self.offlineTimeKey)
			self.offlineTimeKey = 0
	
	#-------------------组队跟随-----------------------
	def isInTeamFollow( self ):
		"""
		在组队跟随中？
		"""
		return len(self.followList) != 0
	
	def requestLeadTeamFollow( self, operatorMB, operatorName ):
		"""
		define method
		队长发起组队跟随
		"""
		hasFollowList = []
		for ( entityID, info ) in self.member:
			if not info.baseMailbox:
				continue
			if info.baseMailbox.id == operatorMB.id:
				continue
			if info.baseMailbox.id in self.followList:
				hasFollowList.append( info.name )
				continue
			info.baseMailbox.cell.receiveTeamFollowRequest( operatorMB, operatorName )
		
		# “XXX,YYY,ZZZ已经跟随您”
		if len(hasFollowList) != 0:
			nameStr = ""
			for index, name in enumerate( hasFollowList ):
				nameStr += name
				if index != len( hasFollowList ) - 1:	# 不是最后一个
					nameStr += ","
			operatorMB.client.statusMessage( csstatus.TEAMATE_FOLLOW_SUCCESS, nameStr )
		
		# “您向队员发出了组队跟随邀请”
		operatorMB.client.statusMessage( csstatus.TEAM_CAPTAIN_LEAD_TEAM, "" )
	
	def cancelLeadTeamFollow( self, operatorMB, operatorName ):
		"""
		define method
		队长取消组队跟随
		"""
		if operatorMB.id != self.followLeaderID:
			return
		self.cancelTeamFollow()
	
	def memberAcceptTeamFollow( self, memberMB, memberName, requesterMB ):
		"""
		define method
		队员同意跟随队长
		"""
		if memberMB.id not in self.followList:
			self.followList.append( memberMB.id )
			memberMB.cell.startTeamFollow( requesterMB.id )
			requesterMB.client.statusMessage( csstatus.TEAMATE_FOLLOW_SUCCESS, memberName )
			
			if len(self.followList) == 1:	#第一个同意的人，队长进入领导跟随状态
				requesterMB.cell.startLeadTeamFollow()
				self.followLeaderID = requesterMB.id
	
	def memberCancelTeamFollow( self, memberMB, memberName, reason ):
		"""
		define method
		队员取消跟随队长
		"""
		if memberMB.id in self.followList:
			self.followList.remove( memberMB.id )
			memberMB.cell.stopTeamFollow()
			if reason == csdefine.TF_CANCEL_REASON_TO_FAR:
				memberMB.client.statusMessage( csstatus.TEAM_TO_FAR_TO_FOLLOW, "" )
			else:
				memberMB.client.statusMessage( csstatus.TEAM_CANCEL_TEAM_FOLLOW, "" )
			
			leaderInfo = self._getMemberInfoByEntityID( self.followLeaderID )
			if leaderInfo and leaderInfo.hasMemberClient():
				if reason == csdefine.TF_CANCEL_REASON_TO_FAR:
					leaderInfo.baseMailbox.client.statusMessage( csstatus.TEAM_MEM_TO_FAR_TO_FOLLOW, memberName )
				else:
					leaderInfo.baseMailbox.client.statusMessage( csstatus.TEAM_MEM_CANCEL_TEAM_FOLLOW, memberName )
			
			if len(self.followList) == 0:
				if leaderInfo and leaderInfo.baseMailbox:
					leaderInfo.baseMailbox.cell.stopLeadTeamFollow()
				self.followLeaderID = 0
	
	def handleFollowOnLeave( self, leaverMB, leaverID, leaverName ):
		"""
		队员离开，处理组队跟随
		"""
		if leaverID in self.followList:
			self.followList.remove( leaverID )
			leaverMB.cell.stopTeamFollow()
			leaverMB.client.statusMessage( csstatus.TEAM_CANCEL_TEAM_FOLLOW, "" )
			
			leaderInfo = self._getMemberInfoByEntityID( self.followLeaderID )
			if leaderInfo and leaderInfo.hasMemberClient():
				leaderInfo.baseMailbox.client.statusMessage( csstatus.TEAM_MEM_CANCEL_TEAM_FOLLOW, leaverName )
			
			if len(self.followList) == 0:
				if leaderInfo and leaderInfo.baseMailbox:
					leaderInfo.baseMailbox.cell.stopLeadTeamFollow()
				self.followLeaderID = 0
		
		elif leaverID == self.followLeaderID:
			self.cancelTeamFollow()
	
	def handleFollowOnLogout( self, leaverID, leaverName ):
		"""
		玩家下线, 处理组队跟随
		"""
		if leaverID in self.followList:
			self.followList.remove( leaverID )
			
			leaderInfo = self._getMemberInfoByEntityID( self.followLeaderID )
			if leaderInfo and leaderInfo.hasMemberClient():
				leaderInfo.baseMailbox.client.statusMessage( csstatus.TEAM_MEM_CANCEL_TEAM_FOLLOW, leaverName )
			
			if len(self.followList) == 0:
				if leaderInfo and leaderInfo.baseMailbox:
					leaderInfo.baseMailbox.cell.stopLeadTeamFollow()
				self.followLeaderID = 0
		
		elif leaverID == self.followLeaderID:
			self.cancelTeamFollow()
	
	def handleFollowOnChangeCaptain( self, oldCaptainID, newCaptainID ):
		"""
		队长改变, 处理组队跟随
		"""
		if not self.isInTeamFollow():
			return
		
		if self.followLeaderID != oldCaptainID:
			return
		
		if ( newCaptainID not in self.followList ):		#新队长不在跟随列表，组队跟随结束
			self.cancelTeamFollow()
			return
		
		newCaptainInfo = self._getMemberInfoByEntityID( newCaptainID )
		oldCaptainInfo = self._getMemberInfoByEntityID( oldCaptainID )
		
		# 新队长开始领导跟随
		self.followList.remove( newCaptainID )
		newCaptainInfo.baseMailbox.cell.stopTeamFollow()
		newCaptainInfo.baseMailbox.cell.startLeadTeamFollow()
		self.followLeaderID = newCaptainID
		
		# 原队长变成跟随者（队伍未退出跟随说明原队长一定还在队伍中）
		oldCaptainInfo.baseMailbox.cell.stopLeadTeamFollow()
		self.followList.append( oldCaptainID )
		oldCaptainInfo.baseMailbox.cell.startTeamFollow( newCaptainID )
		
		# 其他人开始跟随新队长
		for id in self.followList:
			if id == oldCaptainID:
				continue
			memberInfo = self._getMemberInfoByEntityID( id )
			if memberInfo.baseMailbox:
				memberInfo.baseMailbox.cell.followNewCaptain( newCaptainID )
	
	def handleTeamFollowOnDisband( self ):
		"""
		队伍解散，处理组队跟随
		"""
		if not self.isInTeamFollow():
			return
		self.cancelTeamFollow()
	
	def cancelTeamFollow( self ):
		"""
		取消组队跟随
		"""
		leaderName = ""
		leaderInfo = self._getMemberInfoByEntityID( self.followLeaderID )
		if leaderInfo:
			leaderName = leaderInfo.name
			if leaderInfo.baseMailbox:
				leaderInfo.baseMailbox.cell.stopLeadTeamFollow()
				if leaderInfo.hasMemberClient():
					leaderInfo.baseMailbox.client.statusMessage( csstatus.TEAM_CANCEL_TEAM_FOLLOW, "" )
		
		for ( entityID, info ) in self.member:
			if not info.baseMailbox:
				continue
			if info.baseMailbox.id in self.followList:
				info.baseMailbox.cell.stopTeamFollow()
				if info.hasMemberClient():
					info.baseMailbox.client.statusMessage( csstatus.TEAM_LEADER_CANCEL_TEAM_FOLLOW, leaderName )
		
		self.followList = []
		self.followLeaderID = 0

	def memberShareBigMapCustomMarker( self, memberMB, levelName, position, markerType ):
		"""
		define method
		队员分享大地图标记
		"""
		memberInfo = self._getMemberInfoByEntityID( memberMB.id )
		memberName = memberInfo.name
		for entityID, info in self.member:
			if memberMB.id != entityID:
				info.baseMailbox.cell.otherMemberShareBigMapCustomMarker( memberName, levelName, position, markerType )


#-------------------------------英雄联盟副本相关-------------------------------------------------
	def setIsReqCopyCampYXLM( self, isReq ):
		"""
		设置队伍是否正在排队英雄联盟
		"""
		self.isReqCopyCampYXLM = isReq

	def campYXLMOnTeamChange( self ):
		"""
		队伍人数变动，取消申请
		"""
		if self.isReqCopyCampYXLM:
			KBEngine.globalData["CampYXLMCopyMgr"].yingXiong_onTeamChange( self )

#-------------------------------上古密阵副本相关-------------------------------------------------
	def setIsReqCopyCampSGMZ( self, isReq ):
		"""
		设置队伍是否正在排队上古密阵
		"""
		self.isReqCopyCampSGMZ = isReq

	def campSGMZOnTeamChange( self ):
		"""
		队伍人数变动，取消申请
		"""
		if self.isReqCopyCampSGMZ:
			KBEngine.globalData["CampSGMZCopyMgr"].miZhen_onTeamChange( self )

#-------------------------------快速组队相关----------------------------------------------
	def fastTeamReqTeam( self, player, spaceScriptID ):
		"""
		申请快速组队
		"""
		memberDataList = []
		for entityID, info in self.member:
			tempDict = {}
			tempDict["playerMB"] = info.baseMailbox
			tempDict["playerDBID"] = info.dbid
			tempDict["level"] = info.level
			tempDict["name"] = info.name
			memberDataList.append(tempDict)
		KBEngine.globalData["FastTeamMgr"].fastTeam_reqTeam( spaceScriptID,player,self,memberDataList )

	def fastTeamOnReq( self, spaceScriptID ):
		"""
		队伍申请快速组队
		"""
		self.isReqFastTeam = True
		self.fastTeamSpaceScriptID = spaceScriptID

	def fastTeamOnCancel( self ):
		"""
		队伍取消快速组队
		"""
		self.isReqFastTeam = False
		self.fastTeamSpaceScriptID = ""

	def onReceiveRemoteTeamApply(self, applyBaseMailBox, applyName, applyDBID, applyProfession, applyLevel, applyCamp):
		"""
		defined method
		"""
		if self.isTeamFull(True):
			applyBaseMailBox.client.statusMessage(csstatus.TEAM_FULL_REFUSE_JOIN, "")
		else:
			captainInfo = self._getMemberInfoByEntityID( self.captainID )
			captainInfo.baseMailbox.cell.receiveJoinTeamRequest(applyName, applyDBID, applyProfession, applyLevel, applyCamp, applyBaseMailBox)
		
	def fastTeamOnMemberLeave( self, memberMailBox ):
		"""
		成员离开队伍
		"""
		if self.isReqFastTeam:
			KBEngine.globalData["FastTeamMgr"].fastTeam_OnMemberLeave( self, self.fastTeamSpaceScriptID, memberMailBox )

	def fastTeamOnMemberLogin( self, memberMailBox,memberDBID ):
		"""
		成员上线
		"""
		if self.isReqFastTeam:
			KBEngine.globalData["FastTeamMgr"].fastTeam_OnMemberLogin( self, self.fastTeamSpaceScriptID,memberMailBox,memberDBID )

	def fastTeamOnTeamDisband( self ):
		"""
		队伍解散
		"""
		if self.isReqFastTeam:
			KBEngine.globalData["FastTeamMgr"].fastTeam_OnTeamDisband( self, self.fastTeamSpaceScriptID )

	def fastTeamOnMemberJoin( self, memberInfo ):
		"""
		有新成员加入
		"""
		if self.isReqFastTeam:
			KBEngine.globalData["FastTeamMgr"].fastTeam_OnMemberJoin( self, self.fastTeamSpaceScriptID,memberInfo.baseMailbox,memberInfo.name,memberInfo.dbid,memberInfo.level )

	def signUpSGMZ( self, playerMailbox, camp, level, profession ):
		"""
		define method
		报名参加上古密阵
		"""
		memberDataList = []
		for entityID, info in self.member:
			tempDict = {}
			tempDict["playerMB"] = info.baseMailbox
			tempDict["playerDBID"] = info.dbid
			tempDict["level"] = info.level
			tempDict["name"] = info.name
			tempDict["camp"] = info.camp
			tempDict["profession"] = info.profession
			memberDataList.append(tempDict)
		KBEngine.globalData["CampSGMZCopyMgr"].miZhen_reqTeam( playerMailbox, self, camp, memberDataList, level, profession )


#---------------------------------------阵营战场随机匹配相关-------------------------------------------------
	def setIsReqCampRandomFit( self, isReq ):
		"""
		设置队伍是否正在排队英雄联盟
		"""
		self.isReqCampRandomFit = isReq

	def campRandomFitOnTeamChange( self ):
		"""
		队伍人数变动，取消申请
		"""
		if self.isReqCampRandomFit:
			KBEngine.globalData["CampActivityRandomFitMgr"].randomFit_onTeamChange( self )


#---------------------------------------团队竞技战场匹配相关-------------------------------------------------
	def setIsReqBattle( self, isReq ):
		"""
		设置队伍是否正在排队
		"""
		self.isReqBattle= isReq

	def battleOnTeamChange( self ):
		"""
		队伍人数变动，取消申请
		"""
		if self.isReqBattle:
			KBEngine.globalData["BattleActivityMgr"].onTeamChange( self )


#-----------------------------------帮会争霸特殊离队-------------------------------------
	def onBHZBLeaveTeam( self,srcID, dstID ):
		"""
		帮会争霸离开队伍
		"""
		KBEDebug.ERROR_MSG("+++++++++++++++onBHZBLeaveTeam+++++++++++++++",dstID)
		dstInfo = self._getMemberInfoByEntityID( dstID )
		if dstInfo is None:
			return
		
		if srcID != dstID and srcID != self.captainID:	# 既不是自己离队，也不是队长开除，直接忽略
			return
		
		for entityID, info in self.member:
			# 通知每一个在线的玩家，谁离开了队伍
			if info.baseMailbox:
				info.baseMailbox.leaveTeamNotify( dstID, dstInfo.dbid )
				if info.hasMemberClient():
					if info.baseMailbox.id == dstID:
						info.baseMailbox.client.statusMessage( csstatus.TEAM_LEAVE, "" )
					else:
						info.baseMailbox.client.statusMessage( csstatus.TEAM_MEMBER_LEAVE_TEAM, dstInfo.name )
		
		self._removeOfflineDBID( dstInfo.dbid )  # 如果玩家在离线列表中，则从离线列表中移除
		self.handleFollowOnLeave( dstInfo.baseMailbox, dstID, dstInfo.name )	# 必须在member移除和重选队长之前执行，以便离开者和队伍都能正常结束跟随
		self.member.remove( ( dstID, dstInfo ) ) # 删除离队的人员
		TeamSpaceRelationInterface.onRemoveMember( self, dstInfo.dbid )
		
		if len(self.member) <= 1:	#只剩一个人了就直接解散
			pass
		else:						#没解散的话，如果离队的是队长则重选队长
			if dstID == self.captainID:
				self._autoSelectCaptain()
			if dstID == self.signerID:
				self._autoSelectSigner()
	
