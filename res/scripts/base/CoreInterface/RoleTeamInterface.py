# -*- coding: utf-8 -*-

import KBEngine
import KST
import time
import Functions
import KBEDebug
import csdefine
import csconst
import csstatus
import Define

#清理队伍过期数据时间间隔
#如邀请信息 申请信息等等
CLEAR_TEAM_DATA_OUT_TIME = 3 * 60

class RoleTeamInterface:
	def __init__(self):
		self.captainID = 0              # 队长ID
		self.teamMailBox = None         # 队伍mailbox
		self._teamMembers = {}          # 队伍成员列表：{ playerDBID : {"entityID" : 12345, "playerMailBox" : MAILBOX}, ... }
		self._inviterDict ={}			# 记录邀请者们的信息。格式：{ entityID:{"name":xxx,"baseMailbox":yyy} }
		self._joinTeamRequestDict = {}  # 临时表，用于存放申请加入队伍的申请者信息。格式：{ entityID : { "name" : xxx, "baseMailbox" : yyy }, ...}
		self.allocation = self.cellData["allocation"]
		self.quality = self.cellData["quality"]
		self.forbidTeamInvite = self.cellData["forbidTeamInvite"]
		self._initTeamData()

		#-------------------------快速组队------------------------------
		self.isMatchFastTeam = False 		# 是否在匹配队伍 （主要用于刚开始单个玩家报名）队伍在teamEntiy上
		self._applyDict = {}				# 记录申请者们的信息 格式{ entityID:{"name":xxx,"baseMailbox":yyy} }

		#已匹配成功后的标识
		self.isFastTeamCreateTeam = False 	# 是否需要创建一只队伍
		self.fastTeamSpaceScriptID = ""		# 匹配的副本
		self.isFastTeamToLeaveTeam = False 	# 是否需要离开队伍
		self.fastTeamInfo =	None 			# 保存快速组队信息 (队长ID，teamMailBox)
		
		self._clearTeamDataTimerID = 0
		
	def getTeamMemberDBID( self, entityID ):
		"""
		根据队员的entityID获取相对应的dbid

		@return: databaseID
		"""
		for dbid, mb in self._teamMembers.items():
			if mb["entityID"] == entityID:
				return dbid
		return 0

	def getTeamCaptainMailBox( self ):
		"""
		获取队长baseMailbox
		"""
		for e in self._teamMembers.values():
			if self.captainID == e["entityID"]:
				return e["playerMailBox"]
		return None

	def getTeamMemberMailbox( self, entityID ):
		"""
		通过玩家的entity ID获取相应的mailbox
		"""
		for e in self._teamMembers.values():
			if entityID == e["entityID"]:
				return e["playerMailBox"]
		return None

	def isInTeam( self ):
		"""
		判断自己是否在队伍里

		@return: BOOL
		@rtype:  BOOL
		"""
		return self.teamMailBox != None

	def isTeamCaptain( self ):
		"""
		判断我是不是队长，
		非声明方法。

		@return: 是队长则返回True，否则返回False
		@rtype:  BOOL
		"""
		return self.captainID == self.id

	def isTeamFull( self ):
		"""
		是否队伍满员
		"""
		return len(self._teamMembers) >= csconst.TEAM_MEMBER_MAX

	def getTeamMemberPlayerDBIDs( self ):
		"""
		获得队员的playerDBIDs
		"""
		return list( self._teamMembers.keys() )

	def getTeamMemberByPlayerDBID( self, playerDBID ):
		"""
		通过playerDBID 获得teamMember
		"""
		if playerDBID in self._teamMembers:
			return self._teamMembers[playerDBID]
		return None
		
	def clearTempTeamData( self ):
		"""
		"""
		t = time.time() - CLEAR_TEAM_DATA_OUT_TIME
		for id in list(self._applyDict.keys()):
			if t >= self._applyDict[id]["time"]:
				self._applyDict.pop(id)
	
		for id in list(self._inviterDict.keys()):
			if t >= self._inviterDict[id]["time"]:
				self._inviterDict.pop(id)
				
		for id in list(self._joinTeamRequestDict.keys()):
			if t >= self._joinTeamRequestDict[id]["time"]:
				self._joinTeamRequestDict.pop(id)
				
		if len(self._applyDict) or len(self._inviterDict) or len(self._joinTeamRequestDict):
			return
			
		if self._clearTeamDataTimerID > 0:
			self.popTimer(self._clearTeamDataTimerID)
			self._clearTeamDataTimerID = 0

	def destroySelf( self ):
		"""
		玩家销毁时调用
		"""
		if self.teamID !=0 and self.teamMailBox != None:
			self.teamMailBox.teammateLogout( self.databaseID )
			
			#在这里对自身记录的队伍信息进行一次清理
			#主要是清理队伍成员列表和队伍Entity
			#防止出现内存泄漏
			self._clearTeamInfo(False)

			self.bhzbTeamMemberLoginOut()
			
		#这里清空一下，防止同进程的玩家对象交叉引用，导致可能存在的内存泄漏
		self._inviterDict ={}
		self._applyDict = {}
		
		if self._clearTeamDataTimerID > 0:
			self.popTimer(self._clearTeamDataTimerID)
			self._clearTeamDataTimerID = 0

	def addTeamMember( self, playerDBID, entityID, playerName, playerBase, playerProfession, level ):
		"""
		添加成员
		@param         entityID:   OBJECT_ID; 玩家的ID
		@param       playerDBID: DATABASE_ID; 玩家DBID
		@param         entityID: OBJECT_ID; 队员的entityID，有此值的原因是新加入的队员也需要知道已下线的队员的entityID(已下线的队员的mailbox为None)
		@param       playerBase: 玩家BaseEntityMailbox
		@param       playerName: string; 玩家名称
		@param playerProfession: INT32; 玩家职业
		"""
		self._teamMembers[playerDBID] = {"entityID" : entityID, "playerMailBox" : playerBase,"level":level}

	def removeTeamMember( self, playerID ):
		"""
		移除队员
		"""
		playerDBID = self.getTeamMemberDBID( playerID )
		if playerDBID != 0:
			self._teamMembers.pop( playerDBID )

	def teamInfoNotifyOnJoin( self, captainID, teamEntity, allocation, quality, teamMemberInfo, teamSignerID, teamSignKeys, teamSignValues ):
		"""
		<define method>
		入队时通知队伍信息
		
		@param captainID: OBJECT_ID; 队长的entity id
		@param teamEntity: 队伍Entity的BaseEntityMailbox，如果值为None，则表示队伍不再存在
		"""
		self.teamMailBox = teamEntity
		self.captainID = captainID
		self.teamID = teamEntity.id
		self.allocation = allocation
		self.quality = quality
		
		for info in teamMemberInfo:
			self.addTeamMember( info["DBID"], info["entityID"], info["name"], info["baseMB"], info["profession"], info["level"] )
		
		#通知cell
		self.cell.teamInfoNotifyOnJoin( captainID, teamEntity, allocation, quality, teamMemberInfo )
		
		#通知客户端
		if hasattr( self, "client" ) and self.client:
			self.client.teamInfoNotifyOnJoin( captainID, teamEntity.id, allocation, quality, teamSignerID, teamSignKeys, teamSignValues )
			#新队员入队是需要通知客户端更新分配模式和品质
			self.client.modifyAllocation(allocation)
			self.client.modifyQuality(quality)
		for info in teamMemberInfo:
			if hasattr( self, "client" ) and self.client:
				self.client.addTeamMember( str(info["DBID"]), info["entityID"], info["name"], info["profession"], int( info["baseMB"] is not None ), info["level"] )
				
		if allocation in Define.TEAM_PICK_UP_ALLOCATION_MSG:
			self.statusMessage(Define.TEAM_PICK_UP_ALLOCATION_MSG[allocation])
		if quality in Define.TEAM_PICK_UP_QUALITY_MSG:
			self.statusMessage(Define.TEAM_PICK_UP_QUALITY_MSG[quality])
		
		self.onCampYXLMMemberJoin()
		self.onBHZBMemberJoin()
		self.onGCZMemberJoin()
		#完成队伍系统的初始化
		if not self._hasTeamInit:
			self.onTeamInit()

	def clearTeamInfo( self ):
		"""
		清除队伍信息，此方法一般会用于队伍解散或加入队伍失败时。
		如：调用teamMailBox.join()尝试加入队伍失败时就会调用此方法。
		"""
		self._clearTeamInfo(True)
		
	def _clearTeamInfo( self, cleanTeamID ):
		"""
		清除队伍信息
		
		@cleanTeamID:是否清理队伍ID 
		"""
		#玩家退出队伍的情况是需要清理的，但是玩家如果是掉线，则不需要清理其队伍ID
		if cleanTeamID:
			self.teamID = 0			
			
		self.captainID = 0
		self.teamMailBox = None
		#self.allocation = 0	#分配品质和分配模式不清零，下次组队还要用，这里注释掉，备忘
		#self.quality = 0

		# 这些不清除，会引发内存泄漏，
		# 一个是自己作为队员也会在里面记录，
		# 另一个就是别的队员有可能与自己在同一服务器，会互相引用
		self._teamMembers.clear()
		self._joinTeamRequestDict.clear()

	def onMemberjoin( self, playerDBID, entityID, playerName, playerBase, playerProfession, level ):
		"""
		define method
		有新队员加入
		"""
		self.addTeamMember( playerDBID, entityID, playerName, playerBase, playerProfession, level )
		
		if hasattr( self, "cell" ) and self.cell != None:
			self.cell.onMemberjoin( playerDBID, playerBase )
		
		if hasattr( self, "client" ) and self.client:		#通知客户端
			self.client.addTeamMember(str(playerDBID), entityID, playerName, playerProfession, int( playerBase is not None ), level)

		self.matchFastTeamOnJoinTeam( playerDBID,playerName, playerBase, level )

	#-----------------------申请入队-----------------------
	def captainReceiveJoinTeamRequest( self, memberName, playerName, playerDBID, profession, level, camp, playerBase ):
		"""
		define method
		队长收到入队申请
		"""
		# 如果在我的拒绝列表中，直接通知对方，我不想和你玩耍
		if playerDBID in self.blacklist:
			if hasattr(playerBase, "client") and playerBase.client:
				playerBase.client.statusMessage( csstatus.TEAM_REQUEST_FORBID, "" )
			return
		
		if playerBase.id in self._joinTeamRequestDict:
			if hasattr(playerBase, "client") and playerBase.client:
				playerBase.client.statusMessage( csstatus.TEAM_INVITED_IS_SEAD, "" )
			return
		
		self._joinTeamRequestDict[playerBase.id] = { "name" : playerName, "baseMailbox" : playerBase, "time" : time.time() }
		#通知客户端显示
		if hasattr(self, "client") and self.client:
			self.client.OnReceiveJoinTeamRequest(playerBase.id, playerName, camp, profession, level )
		if hasattr(playerBase, "client") and playerBase.client:
			playerBase.client.statusMessage( csstatus.TEAM_SEND_JOIN_REQUEST, memberName )	#您申请加入[{0}]的队伍。
		
		if self._clearTeamDataTimerID <= 0:
			self._clearTeamDataTimerID = self.addTimerRepeat(CLEAR_TEAM_DATA_OUT_TIME, "clearTempTeamData", ())

	def replyPlayerJoinTeam( self, agree, playerID ):
		"""
		<Define method>
		回复玩家的远程加队申请：同意还是不同意

		@param     agree: INT32; 是否同意加入
		@param playerID : OBJECT_ID; 被通知的玩家的entity id
		"""
		if playerID not in self._joinTeamRequestDict:
			return
		
		playerBase = self._joinTeamRequestDict.pop(playerID)["baseMailbox"]
		if not agree:
			if hasattr( playerBase, "client" ) and playerBase.client:
				playerBase.client.statusMessage( csstatus.TEAM_REQUEST_FORBID, "" )
			return
		
		if not self.isTeamCaptain():
			self.statusMessage( csstatus.TEAM_NOT_CAPTAIN )
			return
		
		if self.isTeamFull():
			self.statusMessage( csstatus.TEAM_FULL )
			return
			
		if hasattr( playerBase, "isDestroyed" ) and playerBase.isDestroyed:
			self.statusMessage(csstatus.TEAM_NOT_FIND_PLAYER)
			return
		
		if not hasattr( playerBase, "client" ) or not playerBase.client:
			self.statusMessage( csstatus.TEAM_NOT_FIND_PLAYER )
			return
		
		playerBase.captainAcceptJoinRequest( self, self.teamMailBox, self.captainID, self.allocation, self.quality )

	def captainAcceptJoinRequest( self, captainBase, teamMailBox, captainID, allocation, quality ):
		"""
		define method
		队长同意了我的入队申请
		"""
		if self.isInTeam():
			captainBase.client.statusMessage( csstatus.TEAM_PLAYER_IN_TEAM, "" )
			return
		if not self.isOnCrossService:	#可能已经跨服
			self.joinTeamNotify( teamMailBox, False, captainID, allocation, quality )
		else:
			captainBase.client.statusMessage( csstatus.TEAM_NOT_FIND_INVITER, "" )

	#-----------------------邀请组队-----------------------
	def remoteTeamInviteFB(self, playerName):
		"""
		<define method>
		有cell发送请求，远程邀请某玩家入队

		@param playerName: string;被邀请者的名称		
		"""
		KST.g_baseAppEntity.lookupRoleBaseByName( playerName, Functions.Functor( self._remoteTeamInviteFC, playerName ) )

	def _remoteTeamInviteFC(self, targetName, resultMB):
		"""
		通过名字查询指定玩家，结果通知邀请者的Base

		@param resultMB: 所查询玩家的MailBox
		"""
		if resultMB is None:
			KST.g_baseAppEntity.checkRoleByNameFromDB(targetName, Functions.Functor( self.inviteRoleQueryResult, targetName))
			return
		
		if hasattr(resultMB, "cell") and resultMB.cell:
			resultMB.cell.checkIsCanJoinTeam( self, self.databaseID, targetName )
			
	def inviteRoleQueryResult(self, playerName, result):
		"""
		邀请玩家组队，通过名字查询不到指定玩家Base时，通过查询数据库检查玩家是否存在
		"""
		if result: #能查到数据，说明被邀请者已经离线
			self.client.statusMessage(csstatus.ITEM_INVITE_TARGET_OFF_LINE, "")
		else:
			KBEDebug.ERROR_MSG("CANT FOUND ROLE IN BASE WHO YOU REMOTEINVITED !")
		
	def teamInviteCB( self, resultMB, targetName ):
		if self.isInTeam():
			if self.isTeamCaptain():
				resultMB.teamInviteBy( self, self.getName(), 1, self.level, self.getCamp(), csdefine.TEAM_INVITE_TYPE_JOIN_TEAM, self.teamMailBox.id, )
			else:
				self.cell.teamInviteByTeammate( targetName, resultMB.getCamp(), resultMB.getProfession(), resultMB.getLevel(), resultMB )
		else:
			resultMB.receiveRemoteTeamInvite( self, self.getName(), self.databaseID, 1, self.level, self.getCamp() )
	
	def receiveRemoteTeamInvite( self, inviterMailbox, inviterName, inviterDBID, inviterProfession, inviterLevel, inviteCamp ):
		"""
		Define method.
		收到远程组队请求
		
		@param inviterMailbox : 发起者的mailbox
		@type inviterMailbox : MAILBOX
		@param inviterName : 发起者的名字
		@type inviterName : STRING
		"""
		if self.isInTeam():
			self.cell.receiveJoinTeamRequest( inviterName, inviterDBID, inviterProfession, inviterLevel, inviteCamp, inviterMailbox )
		else:
			self.teamInviteBy( inviterMailbox, inviterName, inviterProfession, inviterLevel, inviteCamp,  csdefine.TEAM_INVITE_TYPE_CREATE_TEAM, 0 )

	def teamInviteBy( self, inviterBase, inviterName, inviterProfession, inviterLevel, inviteCamp, inviteType, inviteTeamID ):
		"""
		<define method>
		被某玩家邀请组队，这里是邀请组队的最终入口，无论是近程邀请还是远程邀请。

		@param inviterBase: 邀请者的BaseEntityMailbox
		@param inviterName: string; 邀请者名称
		"""
		if not inviterBase:
			KBEDebug.ERROR_MSG("invite player base is none.")
			return

		# 如果已经组队，则通知邀请者：对方已经加入了一支队伍。
		if self.isInTeam():
			if hasattr(inviterBase, "client") and inviterBase.client:
				inviterBase.client.statusMessage( csstatus.TEAM_PLAYER_IN_TEAM, "")
			return

		# 已经被该玩家邀请，尚未处理
		for v in self._inviterDict.values():
			if v["name"] == inviterName:
				if hasattr(inviterBase, "client") and inviterBase.client:
					inviterBase.client.statusMessage( csstatus.TEAM_PLAYER_IN_TEAM_INVITE, "")
				return

		# 设置为“拒绝邀请”
		if self.forbidTeamInvite:
			if hasattr(inviterBase, "client") and inviterBase.client:
				inviterBase.client.statusMessage( csstatus.TEAM_PLAYER_FORBID_INVITE, "")
			return

		# 记录邀请者
		inviterData = { 
						"name"			: inviterName,
						"baseMailbox"	: inviterBase,
						"inviteType"	: inviteType,
						"inviteTeamID"	: inviteTeamID,
						"time" 			: time.time(),
					}
		self._inviterDict[inviterBase.id] = inviterData
		if hasattr(inviterBase, "client") and inviterBase.client:
			inviterBase.client.statusMessage( csstatus.TEAM_INVITE_PLAYER, self.getName() )
		
		if hasattr(self, "client") and self.client:
			self.client.OnTeamInviteBy(inviterBase.id, inviterName, inviteCamp, inviterProfession, inviterLevel)		#通知被邀请者的客户端，确定邀请信息并回复是否加入队伍

		if self._clearTeamDataTimerID <= 0:
			self._clearTeamDataTimerID = self.addTimerRepeat(CLEAR_TEAM_DATA_OUT_TIME, "clearTempTeamData", ())
			
	def replyTeamInviteByFB( self, agree, inviterID):
		"""
		<define method>
		由cell调用，答复组队邀请，因此此方法会在被邀请者的base上执行。

		@param agree: INT32; 同意加入
		@param inviterID: 邀请者的EntitiyID
		"""
		if inviterID not in self._inviterDict:
			KBEDebug.ERROR_MSG( "Can't find invite data! inviterID:%s."%inviterID )
			return
		
		inviterBase = self._inviterDict[inviterID]["baseMailbox"]
		inviterName = self._inviterDict[inviterID]["name"]
		inviteType = self._inviterDict[inviterID]["inviteType"]
		inviteTeamID = self._inviterDict[inviterID]["inviteTeamID"]
		del self._inviterDict[inviterID]
		
		#CST-5287
		#邀请者已下线，这里之所以这样写，是因为邀请者和被邀请者在同一base中的话
		#这里记录的则是role对象，如果邀请者下线，此处记录的对象并没被清空，导致后面代码出错
		if hasattr( inviterBase, "isDestroyed" ) and inviterBase.isDestroyed:	
			self.statusMessage( csstatus.TEAM_NOT_FIND_PLAYER, inviterName )
			return
		
		if not agree:
			self.statusMessage( csstatus.TEAM_REFUSE_JOIN, inviterName )
			if hasattr( inviterBase, "client" ) and inviterBase.client:
				inviterBase.client.statusMessage( csstatus.TEAM_PLAYER_REFUSE_INVITE, self.getName() )
			return
		
		# 防止在异步的情况下出现问题
		if self.isInTeam():	# 已加入队伍
			self.statusMessage( csstatus.TEAM_SELF_IN_TEAM )
			if hasattr( inviterBase, "client" ) and inviterBase.client:
				inviterBase.client.statusMessage( csstatus.TEAM_PLAYER_IN_TEAM, "" )
			return
		
		if not hasattr( inviterBase, "client" ) or not inviterBase.client:	#邀请者已下线
			self.statusMessage( csstatus.TEAM_NOT_FIND_PLAYER, inviterName )
			return
		
		inviterBase.playerAgreeTeamInvite( self, inviteType, inviteTeamID )

	def playerAgreeTeamInvite( self, replierBase, inviteType, inviteTeamID ):
		"""
		<define method>
		由被邀请者的base通知邀请者的base：我同意加入你的队伍；因此此方法会在邀请者的base上执行。

		@param replierBase: 回复者的BaseEntityMailbox
		@param inviteType: csdefine枚举值; 是新建队伍还是邀请入队
		@param inviteTeamID: 邀请入队时邀请者所在队伍ID
		"""
		# 创建队伍
		if inviteType == csdefine.TEAM_INVITE_TYPE_CREATE_TEAM:
			if not self.isInTeam():
				if self.isOnCrossService:
					return
				teamArg = { "captainID": self.id,
							"captainName": self.getName(),
							"allocation": self.allocation,		#队伍创建后，通过队长去同步所有成员的分配模式和分配品质
							"quality": self.quality
							}
				teamMailBox = KBEngine.createEntityLocally( "TeamEntity", { "teamArg" : teamArg } )
				if teamMailBox:
					self.joinTeamNotify( teamMailBox, True, self.id, self.allocation, self.quality )
					replierBase.joinTeamNotify( teamMailBox, True, self.id, self.allocation, self.quality )
			else:
				#replierBase.client.statusMessage( csstatus.TEAM_PLAYER_IN_TEAM, "")
				#return
				
				# 通知玩家加入
				replierBase.joinTeamNotify( self.teamMailBox, False, self.captainID, self.allocation, self.quality )
		
		#邀请入队
		elif inviteType == csdefine.TEAM_INVITE_TYPE_JOIN_TEAM:
			# 不在队伍中
			if not self.isInTeam():
				replierBase.client.statusMessage( csstatus.TEAM_NOT_IN_TEAM, "" )
			# 换了队伍
			elif inviteTeamID != self.teamMailBox.id:
				replierBase.client.statusMessage( csstatus.TEAM_JOIN_FAILURE, "" )
			# 不是队长
			elif not self.isTeamCaptain():
				replierBase.client.statusMessage( csstatus.TEAM_JOIN_FAILURE,"" )
			# 队伍已满
			elif self.isTeamFull():
				replierBase.client.statusMessage( csstatus.TEAM_FULL_REFUSE_JOIN,"" )
			
			else:
				# 通知玩家加入
				replierBase.joinTeamNotify( self.teamMailBox, False, self.captainID, self.allocation, self.quality )

	def joinTeamNotify( self, teamMailBox, isCreateTeam, captainID, allocation, quality ):
		"""
		<define method>
		由邀请者通知被邀请者加入队伍，因此此方法会在被邀请者的base上执行

		@param teamMailBox: 队伍的BaseEntityMailbox
		@param isCreateTeam: 是不是创建队伍时，创建者加入
		"""
		# 如果我已经加入队伍，那就异常中断吧，虽然不影响任何流程，但总得知道是怎么回事
		if self.isInTeam():
			KBEDebug.ERROR_MSG("I have team!",self.id, teamMailBox.id)
			return
		
		#CST-4114 (QRN)
		#以下说明针对多baseapp的情况
		#必须在这里将相应的内容设置好，因后面的流程是一个异步处理的过程
		#如果teamEntity不在当前的baseapp上，这里不设置，在向teamMailBox发送join协议后，存在其他可能性（如短时间内同意多个队伍的要求等）代码还会执行到这里，导致加入多个队伍
		self.teamMailBox = teamMailBox
		self.captainID = captainID
		self.teamID = teamMailBox.id
		self.allocation = allocation
		self.quality = quality
		
		# 把自己添加到队伍
		teamMailBox.join( self.databaseID, self.getName(), self, self.profession, self.id, self.level, isCreateTeam, self.camp )
		self.campRandomFitOnJoinTeam()
		self.battleActivityOnJoinTeam()

	#-----------------------------离队、下线、重登、解散队伍----------------------
	def leaveTeamFB( self, playerID ):
		"""
		<define method>
		由客户端请求：玩家自己离队或开除玩家离队。
		1、如果playerID是自己则是离队；
		2、如果playerID不是自己且自己是队长则开除playerID出队伍
		
		@param playerID: 开除的玩家ID
		@type  playerID: OBJECT_ID
		"""
		if not self.isInTeam():
			# 未加入任何队伍
			return

		if self.id != playerID and self.id != self.captainID:
			# 既不是自己离队，也不是队长开除，直接忽略
			return
			
		self.teamMailBox.leave( self.id, playerID )

	def leaveTeamNotify( self, dstEntityID, leaverDBID ):
		"""
		<define method>
		由TeamEntity通知：玩家离开通知，此接口由TeamEntity调用
		
		@param dstEntityID: OBJECT_ID; 离开队伍的玩家ID
		"""
		# 在异步的情况下，不存在cell或client是有可能出现的
		if hasattr( self, "cell" ) and self.cell != None :
			self.cell.leaveTeamNotify( leaverDBID )
			
		if hasattr( self, "client" ) and self.client:
			self.client.leaveTeamNotify( dstEntityID, int( self.id == dstEntityID ) )		#通知客户端，是自己离队还是有队员离队

		if dstEntityID == self.id:
			# 自己离开
			self.clearTeamInfo()
		else:
			# 队友离开
			self.removeTeamMember( dstEntityID )

		self.campYXLMOnLevelTeam()
		self.fastTeamOnLeaveTeam()
		self.bhzbOnLeaveTeam()
		self.bhzbTeamMemberLoginOut()
		self.GCZOnLeaveTeam()

	def onTeamMateLogout(self, dbid, entityID):
		"""
		<define method>
		队员离线通知
		"""
		# 在异步的情况下，不存在cell或client是有可能出现的
		if hasattr( self, "cell" ) and self.cell:
			self.cell.logoutNotify( entityID )
		
		# 在异步的情况下，不存在cell或client是有可能出现的
		if hasattr( self, "client" ) and self.client:
			self.client.logoutNotify( entityID )
		
		#
		if dbid not in self._teamMembers:
			return
			
		self._teamMembers[dbid]["playerMailBox"] = None

	def rejoinTeam( self ):
		"""
		define method
		上线
		"""
		teamManager = KBEngine.globalData.get("TeamManager", None)
		if teamManager == None:
			return
		
		oldTeamID = self.teamID
		self.teamID = 0
		
		if oldTeamID != 0:
			self.registerSystemForInit("RoleTeam")	#申请重新加入队伍，这里才是正在的队伍初始化（以前存在队伍的情况下）
			teamManager.rejoinTeam( oldTeamID ,self.databaseID ,self )

	def onRejoinTeam( self, oldEntityID, playerDBID, playerBase ):
		"""
		<define method>
		由TeamEntity通知所有的在线成员：某人重新上线加入队伍了

		@param playerDBID: 玩家DBID
		@param playerBase: 上线重新加入队伍的玩家的BaseEntityMailbox
		"""
		self._teamMembers[playerDBID] = {"entityID" : playerBase.id, "playerMailBox" : playerBase}
		
		# 在异步的情况下，不存在cell或client是有可能出现的
		if hasattr( self, "cell" ) and self.cell != None:
			self.cell.onRejoinTeam( playerDBID, playerBase )
		
		if hasattr( self, "client" ) and self.client != None:
			self.client.onRejoinTeam( oldEntityID, playerBase.id )

	def disbandTeamFB( self ):
		"""
		<define method>
		请求解散队伍
		"""
		if not self.isTeamCaptain():
			# 实际上，正常情况下，如果调用者不是队长，那就不应该调用此方法
			# 但对于异步来说，什么事情都有可能发生
			self.statusMessage( csstatus.TEAM_NOT_CAPTAIN, "")
			return
			
		if not self.isInTeam():
			return
			
		self.teamMailBox.disband()

	def disbandTeamNotify( self ):
		"""
		<define method>
		队伍解散通知，此方法由TeamEntity调用
		"""
		if hasattr( self, "cell" ) and self.cell != None:
			self.cell.disbandTeamNotify()
		
		if hasattr( self, "client" ) and self.client != None:
			self.client.disbandTeamNotify()		#通知客户端,队伍解散
		
		tempTeamMailBox = self.teamMailBox
		self.clearTeamInfo()
		tempTeamMailBox.onDisbandTeamNotifyCallback(self.databaseID)
		
	def onDisbandTeam(self):
		"""
		Define method
		队伍解散，所有成员都已通知完成的回调
		"""
		self.campYXLMOnLevelTeam()
		self.fastTeamOnLeaveTeam()
		self.bhzbOnLeaveTeam()
		self.GCZOnLeaveTeam()

	#-----------------------------队长变更----------------------------
	def changeCaptainFB( self, playerID ):
		"""
		<define method>
		移交队长权限，此接口由cell调用

		@param playerID: 玩家的DBID
		"""
		# 没有加入任何队伍或不是队长，我们都认为它不是队长
		if not self.isInTeam() or not self.isTeamCaptain():
			self.statusMessage( csstatus.TEAM_NOT_CAPTAIN, "")
			return

		# 队伍中没有此玩家
		if self.getTeamMemberDBID( playerID ) == 0:
			self.statusMessage( csstatus.TEAM_IS_NOT_MEMBER, "")
			return

		# 该队员不在线
		if not self.getTeamMemberMailbox( playerID ):
			self.statusMessage( csstatus.TEAM_MEMBER_NOT_ON_LINE, "")
			return

		self.teamMailBox.changeCaptain( playerID )

	def changeCaptainNotify( self, captainID ):
		"""
		<define method>
		由TeamEntity通知：队伍的队长改变了

		过程：
		　改变队长标记，设置新队长
		　通知cell，队长改变

		@param captainID: 队长玩家DBID
		@type  captainID: DATABASE_ID
		"""
		self.captainID = captainID
		if hasattr( self, "cell" ) and self.cell != None:
			self.cell.changeCaptainNotify( captainID )		    #通知cell
		if hasattr( self, "client" ) and self.client:
			self.client.changeCaptainNotify( captainID )		#通知客户端

		self.onBHZBChangeCaptainCB()

	#-----------------------奖励分配----------------------
	def modifyAllocation( self, allocation ):
		"""
		<define method>
		修改队伍物品分配模式
		
		@param allocation: INT32; 分配模式
		"""
		self.allocation = allocation
		if hasattr( self, "cell" ) and self.cell != None:
			self.cell.modifyAllocation( allocation )
		if hasattr( self, "client" ) and self.client:		#通知客户端
			self.client.modifyAllocation( allocation )
		
		if allocation in Define.TEAM_PICK_UP_ALLOCATION_MSG:
			self.statusMessage(Define.TEAM_PICK_UP_ALLOCATION_MSG[allocation])
	
	def modifyQuality( self, quality ):
		"""
		<Define method>
		修改队伍物品分配品质标准
		
		@param quality: INT32; 物品品质标准
		"""
		self.quality = quality
		if hasattr( self, "cell" ) and self.cell != None:
			self.cell.modifyQuality( quality )
		if hasattr( self, "client" ) and self.client:		#通知客户端
			self.client.modifyQuality( quality )
		
		if quality in Define.TEAM_PICK_UP_QUALITY_MSG:
			self.statusMessage(Define.TEAM_PICK_UP_QUALITY_MSG[quality])

	#-----------------拒绝邀请组队功能---------------------
	def setForbidTeamInvite( self, value ):
		"""
		define method
		设置“拒绝邀请”
		"""
		self.forbidTeamInvite = value

	#-----------------队伍系统初始化相关-------------------
	def onRejoinTeamFailed( self ):
		"""
		上线重新加入队伍失败
		"""
		self.onTeamInit()
		
	def _initTeamData( self ):
		"""
		"""
		#最近一次下线没加入任何队伍
		if self.teamID <= 0:
			self._hasTeamInit = True
			return
		
		#最近有加入队伍，可能需要重新加入
		self._hasTeamInit = False
		
	def onTeamInit( self ):
		"""
		队伍系统初始化完毕
		"""
		self._hasTeamInit = True
		self.onSystemInit("RoleTeam")


	def createSelfTeamLocally( self ):
		"""
		在本地base上创建自己的队伍
		"""
		if self.isInTeam():
			return
			
		teamArg = { "captainID": self.id,
					"captainName": self.getName(),
					"allocation": self.allocation,		#队伍创建后，通过队长去同步所有成员的分配模式和分配品质
					"quality": self.quality
				}
		teamMailBox = KBEngine.createEntityLocally( "TeamEntity", { "teamArg" : teamArg } )
		if teamMailBox:
			self.joinTeamNotify( teamMailBox, True, self.id, self.allocation, self.quality )

	#----------------------------快速组队------------------------
	def onLoseCell( self ):
		"""
		"""
		if self.isMatchFastTeam:
			KBEngine.globalData["FastTeamMgr"].fastTeam_perSonCancelSignUp( self.fastTeamSpaceScriptID, self.id )

	def fastTeamReqTeam( self, spaceScriptID ):
		"""
		队长申请快速组队
		"""
		if self.isMatchFastTeam:
			spaceName = ""
			spaceobj = KST.g_objFactory.getBunchSpaceObject( self.fastTeamSpaceScriptID )
			if spaceobj:
				spaceName = spaceobj.getBunchSpaceName()
			self.inquireMessage( csstatus.FAST_TEAM_IS_ALREADY_REQ, [spaceName,spaceName], "replyfastTeamReqTeam", spaceScriptID )
		else:
			self.teamMailBox.fastTeamReqTeam(self, spaceScriptID)
		
	def replyfastTeamReqTeam( self, reply, spaceScriptID ):
		"""
		"""
		if reply:
			KBEngine.globalData["FastTeamMgr"].fastTeam_teamCancelSignUp( self.fastTeamSpaceScriptID, self.teamID )
			self.teamMailBox.fastTeamReqTeam(self, spaceScriptID)
		
	def fastTeamReqPerson( self, spaceScriptID ):
		"""
		个人申请快速组队
		"""
		if self.isMatchFastTeam:
			spaceName = ""
			spaceobj = KST.g_objFactory.getBunchSpaceObject( self.fastTeamSpaceScriptID )
			if spaceobj:
				spaceName = spaceobj.getBunchSpaceName()
			self.inquireMessage( csstatus.FAST_TEAM_IS_ALREADY_REQ, [spaceName,spaceName], "replyfastTeamReqPerson", spaceScriptID )
		else:
			KBEngine.globalData["FastTeamMgr"].fastTeam_reqPerson( spaceScriptID, self,self.databaseID,self.getLevel(),self.getName())
	
	def replyfastTeamReqPerson( self, reply, spaceScriptID ):
		"""
		"""
		if reply:
			KBEngine.globalData["FastTeamMgr"].fastTeam_perSonCancelSignUp( self.fastTeamSpaceScriptID, self.id )
			KBEngine.globalData["FastTeamMgr"].fastTeam_reqPerson( spaceScriptID, self,self.databaseID,self.getLevel(),self.getName())

	def notifyClientFastTeamSignUp( self, spaceScriptID, matchTime ):
		"""
		通知客户端已发起快速组队
		"""
		# camp = self.fastTeamSetData.camp
		# profession = self.fastTeamSetData.profession
		# minLevel = self.fastTeamSetData.minLevel
		# maxLevel = self.fastTeamSetData.maxLevel
		# chatType = self.fastTeamSetData.chatType
		bunchSpaceName = ""
		bunchSpaceObj = KST.g_objFactory.getBunchSpaceObject( self.fastTeamSpaceScriptID )
		if bunchSpaceObj:
			bunchSpaceName = bunchSpaceObj.getBunchSpaceName()
		if hasattr( self, "client" ) and self.client:
			self.client.CLIENT_OnStartTeamSearch(bunchSpaceName)

	def notifyClientFastTeamCancelSignUp( self ):
		"""
		通知客户端取消快速组队
		"""
		if hasattr( self, "client" ) and self.client:
			self.client.CLIENT_OnFastTeamCancelMatch()

	def fastTeamOnjoin(self, spaceScriptID):
		"""
		参加快速组队
		"""
		self.isMatchFastTeam = True
		self.fastTeamSpaceScriptID = spaceScriptID

	def fastTeamOnCancel( self ):
		"""
		取消快速组队
		"""
		self.isMatchFastTeam = False
		self.fastTeamSpaceScriptID = ""

	def BASE_setFastTeamData( self, camp, profession,minLevel,maxLevel,chatType ):
		"""
		exposed method
		设置快速组队的信息
		"""
		if self.isInTeam() and not self.isTeamCaptain():
			#自己已有队伍
			self.statusMessage(csstatus.FAST_TEAM_IS_IN_TEAM_LIMIT,"")
			return
		self.fastTeamSetData.camp = camp
		self.fastTeamSetData.profession = profession
		self.fastTeamSetData.minLevel = minLevel
		self.fastTeamSetData.maxLevel = maxLevel
		self.fastTeamSetData.chatType = chatType
		bunchSpaceName = ""
		bunchSpaceObj = KST.g_objFactory.getBunchSpaceObject( self.fastTeamSpaceScriptID )
		if bunchSpaceObj:
			bunchSpaceName = bunchSpaceObj.getBunchSpaceName()
		#发送频道消息
		self.cell.sendFastTeamChatMsg( chatType, bunchSpaceName )

	def applyJoinFastTeam( self, playerName ):
		"""
		<define method>
		cell 请求加入某玩家队列
		"""
		KST.g_baseAppEntity.lookupRoleBaseByName( playerName, Functions.Functor( self._applyJoinFastTeam) )

	def _applyJoinFastTeam( self, resultMB ):
		"""
		"""
		if resultMB:
			if self.isInTeam():
				self.statusMessage( csstatus.SELF_IS_IN_TEAM_NOT_JOIN,"" )
				return
			resultMB.receiveRemoteTeamApply( self, self.getName(), self.databaseID, self.getProfession(), self.level,self.getCamp() )
		else:
			self.statusMessage(csstatus.SENDER_IS_LOGIN_OFF,"")

	def receiveRemoteTeamApply( self, applyBaseMailBox, applyName, applyDBID, applyProfession, applyLevel, applyCamp ):
		"""
		收到远程申请组队请求
		"""
		if self.fastTeamSetData.camp >= csdefine.CMAP_NONE and self.fastTeamSetData.camp != applyCamp:
			return
		if self.fastTeamSetData.profession >= csdefine.CLASS_UNKNOWN and self.fastTeamSetData.profession != applyProfession:
			applyBaseMailBox.statusMessage( csstatus.FAST_TEAM_FORBID_PROFESSION,"" )
			return
		if applyLevel < self.fastTeamSetData.minLevel or applyLevel > self.fastTeamSetData.maxLevel:
			applyBaseMailBox.client.statusMessage(csstatus.FAST_TEAM_FORBID_LEVEL, str(self.fastTeamSetData.minLevel) + "|" + str(self.fastTeamSetData.maxLevel))
			return
		
		if self.isInTeam() and self.isTeamCaptain():
			self.teamMailBox.onReceiveRemoteTeamApply(applyBaseMailBox, applyName, applyDBID, applyProfession, applyLevel, applyCamp)
		else:
			self.teamApplyBy( applyBaseMailBox, applyName, applyDBID,applyProfession, applyLevel, applyCamp, csdefine.TEAM_INVITE_TYPE_CREATE_TEAM, 0 )

	def teamApplyBy( self, applyBaseMailBox, applyName, applyDBID,applyProfession, applyLevel, applyCamp, applyType, applyTeamID ):
		"""
		某玩家申请组队
		"""
		if not applyBaseMailBox:
			KBEDebug.ERROR_MSG(" apply player base is none ")
			return

		#如果已经组队
		if self.isInTeam() and self.isTeamCaptain():
			self.cell.receiveJoinTeamRequest( applyName, applyDBID, applyProfession, applyLevel, applyCamp, applyBaseMailBox )
			return

		# 已经被改玩家申请，尚未处理
		for v in self._applyDict.values():
			if v["name"] == applyName:
				applyBaseMailBox.client.statusMessage( csstatus.TEAM_PLAYER_IN_TEAM_APPLY,"" )
				return

		# 记录申请者
		applyData = { 
						"name"			: applyName, 
						"baseMailbox"	: applyBaseMailBox,
						"applyType"		: applyType,
						"applyTeamID"	: applyTeamID,
						"applyDBID"		: applyDBID,
						"applyProfession" : applyProfession,
						"applyLevel"	: applyLevel,
						"applyCamp"		: applyCamp,
						"time"			: time.time(),
					}
	
		self._applyDict[applyBaseMailBox.id] = applyData
		if hasattr( self, "client" ) and self.client:
			self.client.CLIENT_teamByApply( applyBaseMailBox.id, applyName, applyCamp, applyProfession,applyLevel )
			
		if self._clearTeamDataTimerID <= 0:
			self._clearTeamDataTimerID = self.addTimerRepeat(CLEAR_TEAM_DATA_OUT_TIME, "clearTempTeamData", ())

	def replyTeamApplyFastTeam( self, agree, applyID ):
		"""
		<define method>
		由cell调用 答复组队申请，
		
		@param agree: INT32; 同意加入
		@param applyID: 申请者的EntitiyID
		"""
		if applyID not in self._applyDict:
			KBEDebug.ERROR_MSG( "Can't find apply data! applyID:%i."%applyID )
			return
		
		applyBaseMailBox = self._applyDict[applyID]["baseMailbox"]
		applyName = self._applyDict[applyID]["name"]
		applyType = self._applyDict[applyID]["applyType"]
		applyTeamID = self._applyDict[applyID]["applyTeamID"]
		applyDBID = self._applyDict[applyID]["applyDBID"]
		applyProfession = self._applyDict[applyID]["applyProfession"]
		applyLevel = self._applyDict[applyID]["applyLevel"]
		applyCamp = self._applyDict[applyID]["applyCamp"]
		del self._applyDict[applyID]

		if hasattr(applyBaseMailBox,"isDestroyed") and applyBaseMailBox.isDestroyed:
			self.statusMessage( csstatus.TEAM_NOT_FIND_PLAYER, inviterName )
			return

		if not agree:
			self.statusMessage( csstatus.TEAM_REFUSE_JOIN, applyName )
			if hasattr( applyBaseMailBox,"client" ) and applyBaseMailBox.client:
				applyBaseMailBox.client.statusMessage( csstatus.TEAM_PLAYER_REFUSE_JOIN, self.getName() )
			return

		#防止在异步的情况下出现问题
		if self.isInTeam():
			if self.isTeamCaptain():
				self.cell.receiveJoinTeamRequest( applyName, applyDBID, applyProfession, applyLevel, applyCamp, applyBaseMailBox )
			else:
				self.statusMessage( csstatus.TEAM_SELF_IN_TEAM )
				if hasattr( applyBaseMailBox, "client" ) and applyBaseMailBox.client:
					applyBaseMailBox.client.statusMessage( csstatus.TEAM_DISBAND, "" )
			return
		
		self.playerAgreeTeamInvite( applyBaseMailBox, applyType, applyTeamID )

	def fastTeamCreateTeam( self, spaceScriptID ):
		"""
		创建一只队伍
		"""
		if self.isInTeam():
			if self.isTeamFull():
				KBEngine.globalData["FastTeamMgr"].fastTeam_onUseCurrTeam( spaceScriptID, self, self.teamMailBox )
				return
			self.isFastTeamCreateTeam = True
			self.fastTeamSpaceScriptID = spaceScriptID
			if self.isTeamCaptain():
				self.disbandTeamFB()
			else:
				self.leaveTeamFB( self.id )
		else:
			self.createSelfTeamLocally()
			KBEngine.globalData["FastTeamMgr"].fastTeam_onCreateTeam( spaceScriptID, self, self.teamMailBox )

	def fastTeamOnJoinTeam( self, captainID, teamMailBox ):
		"""
		加入队伍
		"""
		if self.isInTeam():
			self.isFastTeamToLeaveTeam = True
			self.fastTeamInfo = ( teamMailBox, captainID )
			if self.isTeamCaptain():
				self.disbandTeamFB()
			else:
				self.leaveTeamFB( self.id )
		else:
			self.joinTeamNotify( teamMailBox, False, captainID, self.allocation, self.quality )

	def fastTeamOnLeaveTeam( self ):
		"""
		队员离开队伍的回调
		"""
		if self.isFastTeamCreateTeam:
			self.createSelfTeamLocally()
			KBEngine.globalData["FastTeamMgr"].fastTeam_onCreateTeam( self.fastTeamSpaceScriptID, self, self.teamMailBox )
			self.isFastTeamCreateTeam = False
			#self.fastTeamSpaceScriptID = ""

		if self.isFastTeamToLeaveTeam:
			self.joinTeamNotify( self.fastTeamInfo[0], False, self.fastTeamInfo[1], self.allocation, self.quality )
			self.isFastTeamToLeaveTeam = False
			self.fastTeamInfo = None

	def matchFastTeamOnJoinTeam( self, playerDBID,playerName, playerBase, level ):
		"""
		匹配时加入了队伍
		"""
		if self.isMatchFastTeam:
			if self.isInTeam():
				if self.isTeamCaptain():
					if len(self._teamMembers) > 2:
						return
					memberDataList = []
					tempDict = {}
					selfTempDict = {}
					tempDict["playerMB"] = playerBase
					tempDict["playerDBID"] = playerDBID
					tempDict["level"] = level
					tempDict["name"] = playerName
					selfTempDict["playerMB"] = self
					selfTempDict["playerDBID"] = self.databaseID
					selfTempDict["level"] = self.getLevel()
					selfTempDict["name"] = self.getName()
					memberDataList.append(selfTempDict)
					memberDataList.append(tempDict)
					KBEngine.globalData["FastTeamMgr"].fastTeam_matchFastTeamOnJoinTeam(self.fastTeamSpaceScriptID, self, self.teamMailBox,memberDataList )
				# else:
				# 	KBEngine.globalData["FastTeamMgr"].fastTeam_perSonCancelSignUp( self.fastTeamSpaceScriptID, self.id )
				
	def fastTeamCancel(self):
		"""
		Define method
		取消快速组队
		"""
		if self.isMatchFastTeam and self.isInTeam() and self.isTeamCaptain():
			KBEngine.globalData["FastTeamMgr"].fastTeam_teamCancelSignUp( self.fastTeamSpaceScriptID, self.teamMailBox.id )
		elif self.isMatchFastTeam:
			KBEngine.globalData["FastTeamMgr"].fastTeam_perSonCancelSignUp( self.fastTeamSpaceScriptID, self.id )

	def requestFastTeam( self, camp, profession,minLevel,maxLevel,chatType, spaceScriptID ):
		"""
		Define method
		客户端请求快速组队
		"""
		if self.level < minLevel or self.level > maxLevel:
			self.client.statusMessage(csstatus.FAST_TEAM_FORBID_LEVEL, str(minLevel) + "|" + str(maxLevel))
			return
			
		if self.isInTeam():
			if not self.isTeamCaptain():
				self.client.statusMessage(csstatus.SPACE_ENTER_NOT_CAPTAIN, "")
				return
			self.fastTeamReqTeam(spaceScriptID)
		else:
			self.fastTeamReqPerson( spaceScriptID )
			
		self.fastTeamSetData.camp = camp
		self.fastTeamSetData.profession = profession
		self.fastTeamSetData.minLevel = minLevel
		self.fastTeamSetData.maxLevel = maxLevel
		self.fastTeamSetData.chatType = chatType

	def requestCancelFastTeamMatch( self ):
		"""
		exposed method
		请求取消快速组队
		"""
		self.fastTeamCancel()

#---------------------------------------阵营战场随机匹配相关-------------------------------------------------
	def campRandomFitOnJoinTeam( self ):
		"""
		加入队伍，原来的匹配取消
		"""
		if self.isMatchCampRandomFit:
			KBEngine.globalData["CampActivityRandomFitMgr"].randomFit_onJoinTeam( self )

	def battleActivityOnJoinTeam(self):
		"""
		加入队伍，原来的匹配取消
		"""
		if self.isMatchCampRandomFit:
			KBEngine.globalData["BattleActivityMgr"].onJoinTeam(self)