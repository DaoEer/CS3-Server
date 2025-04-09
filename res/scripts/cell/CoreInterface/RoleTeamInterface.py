# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import csconst
import csstatus
import Math
import KBEMath
import KST
import Const
from ChatDataType import ChatData
import cschannel_msgs
from ConfigObject.Chat.ChatBase.ChatMgr import g_chatMgr
from ConfigObject.BunchChildStrategy.StrategyLoader import g_bunchChildStrategyLoader
from ConfigObject.Talk.TalkBase import NPCTalkLoader
from ConfigObject.BHZBPointDataLoader import g_BHZBPointDataLoader

g_npcTalk = NPCTalkLoader.NPCTalkLoader.instance()



class RoleTeamInterface:
	def __init__(self):
		pass
		#self.teamMembers = ()		# 队伍成员：[{"dbID" : 12345, "mailbox" : MAILBOX}, ... ]
		#self.captainID = 0			# 队长ID
		#self.teamMailbox = None		# 队伍的MAILBOX
		
	def beforeDestroy( self ):
		"""
		销毁前做一些事
		"""
		#在这里对队伍的相关数据进行清理
		#如果不清理的话，会将部分数据打包到base
		#其中teamMembers中所记录的mailbox在base侧可能会还原成玩家的引用，玩家自身记录自身（未释放的话）可能会导致内存泄漏
		self.clearTeamInfo()

	def onTeleportCompleted( self, isFirst ):
		"""
		传送结束，场景已加载完毕
		"""
		if isFirst:	#登陆
			self.base.rejoinTeam()

	def onEnterDead( self ):
		"""
		玩家死亡
		"""
		if self.isTeamFollowing():
			self.cancelTeamFollowFC( self.id, csdefine.TF_CANCEL_STATE_LIMIT )
		if self.isTeamFollowLeading():
			self.cancelLeadTeamFollowFC( self.id )
		if self.isNormalFollowing():
			self.cancelNormalFollowFC( self.id )
	
	def effectStateChanged( self, estate, disabled ):
		"""
		效果改变.
			@param estate		:	效果标识(非组合)
			@type estate		:	integer
			@param disabled		:	效果是否生效
			@param disabled		:	bool
		"""
		if disabled and estate in csconst.TEAM_FOLLOW_FORBID_EFFECT:
			if self.isTeamFollowing():
				self.cancelTeamFollowFC( self.id, csdefine.TF_CANCEL_STATE_LIMIT )
			if self.isNormalFollowing():
				self.cancelNormalFollowFC( self.id )

	def isInTeam( self ):
		"""
		判断自己是否在队伍里

		@return: BOOL
		@rtype:  BOOL
		"""
		return self.teamMailbox != None

	def isTeamCaptain( self ):
		"""
		判断我是不是队长，
		非声明方法。

		@return: 是队长则返回True，否则返回False；未加入队伍视为非队长
		@rtype:  BOOL
		"""
		return self.captainID == self.id

	def isTeamFull( self ):
		"""
		是否队伍满员
		"""
		return len(self.teamMembers) >= csconst.TEAM_MEMBER_MAX

	def isTeammate( self, targetID ):
		"""
		是自己队友？
		注：下线玩家判断不了
		"""
		for e in self.teamMembers:
			if e["mailbox"] and e["mailbox"].id == targetID:
				return True
		return False

	def getTeamCaptainMailBox( self ):
		"""
		获取队长baseMailbox
		"""
		for e in self.teamMembers:
			if e["mailbox"] and e["mailbox"].id == self.captainID:
				return e["mailbox"]
		return None
		
	def getTeamCaptainName( self ):
		"""
		获取队长名称
		"""
		captain = KBEngine.entities.get(self.captainID)
		if captain:
			return captain.playerName
		return ""

	def getTeamMemberMailbox( self, entityID ):
		"""
		通过玩家的entity ID获取相应的mailbox
		"""
		for e in self.teamMembers:
			if e["mailbox"] and e["mailbox"].id == entityID:
				return e["mailbox"]
		return None

	def getAllTeamMemberMB( self ):
		"""
		获取所有队友的mailbox（不包括下线的）
		"""
		mbList = []
		for _dict in self.teamMembers:
			if _dict["mailbox"]:
				mbList.append( _dict["mailbox"] )
		return mbList

	def getAllTeamMemberDBIDs( self ):
		"""
		获得所有队友的DBID
		"""
		mbDBIDList = []
		for _dict in self.teamMembers:
			mbDBIDList.append(_dict["dbID"])

		return mbDBIDList
	
	def getInRangeTeammate( self, range ):
		"""
		获取在范围内的队友entity，包括自己
		"""
		members = []
		for mb in self.getAllTeamMemberMB():
			entity = KBEngine.entities.get( mb.id, None )
			if not entity or entity.spaceID != self.spaceID:
				continue
			if entity.position.flatDistTo( self.position ) <= range:
				members.append( entity )
		return members
	
	def getNotInRangeTeammateDBID( self, range ):
		"""
		获取不在范围内的队友的DBID（不包括下线的）
		"""
		notInRangeDBID = []
		
		inRangeIDs = [ e.id for e in self.getInRangeTeammate( range ) ]
		for _dict in self.teamMembers:
			if ( _dict["mailbox"] ) and ( _dict["mailbox"].id not in inRangeIDs ):
				notInRangeDBID.append( _dict["dbID"] )
		
		return notInRangeDBID

	def getOwnerAllocation( self ):
		"""
		获取分配方式
		"""
		return self.allocation
		
	def getOwnerQuality( self ):
		"""
		获取分配品质标准
		"""
		return self.quality

	def addTeamMember( self, dbid, playerBase ):
		"""
		添加队员
		"""
		for mem in self.teamMembers:
			if mem["dbID"] == dbid:
				self.teamMembers.remove( mem )
				break
		self.teamMembers.append( { "dbID" : dbid, "mailbox" : playerBase } )

	def removeTeamMember( self, playerDBID ):
		"""
		移除队员
		"""
		for memberMB in self.teamMembers:
			if memberMB["dbID"] == playerDBID:
				self.teamMembers.remove( memberMB )
				break

	def teamInfoNotifyOnJoin( self, captainID, teamMailbox, allocation, quality, teamMemberInfo ):
		"""
		<define method>
		入队时通知队伍信息

		@param captainID: OBJECT_ID; 队长的entity id
		@param teamEntity: 队伍Entity的BaseEntityMailbox，如果值为None，则表示队伍不再存在
		"""
		self.teamMailbox = teamMailbox
		self.captainID = captainID
		self.allocation = allocation
		self.quality = quality
		
		for info in teamMemberInfo:
			self.addTeamMember( info["DBID"], info["baseMB"] )
		
		if not self.hasFlag( csdefine.ROLE_FLAG_TEAMMING ):
			self.addFlag( csdefine.ROLE_FLAG_TEAMMING )
		
		if self.id == captainID:
			if self.getClient():
				self.client.RefreshAroundBoxStatus( csdefine.SPELL_BOX_LISTEN_EVENT_IS_CAPTAIN )	#更新周围箱子可交互状态（有的箱子要求队长才能交互）
		
		self.updateRelation()	# 与队友的关系改变了（变为友好了），触发一下关系改变接口
		self.triggerEntityEvent(csdefine.ENTITY_EVENT_ROLE_TEAM_JOIN, [self.teamMailbox.id])

	def clearTeamInfo( self ):
		"""
		清除退伍数据
		"""
		self.teamMailbox = None
		oldCaptainID = self.captainID
		self.captainID = 0
		self.teamMembers = []
		#self.allocation = 0	#分配品质和分配模式不清零，下次组队还要用，这里注释掉，备忘
		#self.quality = 0
		
		if self.hasFlag( csdefine.ROLE_FLAG_TEAMMING ):
			self.removeFlag( csdefine.ROLE_FLAG_TEAMMING )
		
		if self.id == oldCaptainID:
			if hasattr( self, "client" ) and self.client:
				self.client.RefreshAroundBoxStatus( csdefine.SPELL_BOX_LISTEN_EVENT_IS_CAPTAIN )	#更新周围箱子可交互状态（有的箱子要求队长才能交互）
		
		self.updateRelation()	# 与队友的关系改变了（不再为友好），触发一下关系改变接口

	def onMemberjoin( self, dbid, playerBase ):
		"""
		<define method>
		新队员加入
		"""
		self.addTeamMember( dbid, playerBase )

	#-----------------------近程申请入队-----------------------
	def requestJoinTeamNear( self, srcEntityID, playerID ):
		"""
		<Exposed method>
		近程申请加入某人的队伍（我没队伍，对方有队伍）
		"""
		if not self.validateClientCall( srcEntityID ):
			# 申请加入自己的队伍是不对的
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() in [csdefine.SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS, csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP]:
			return
		
		if self.isInTeam():
			self.statusMessage( csstatus.TEAM_SELF_IN_TEAM )
			return

		spaceObj = self.getCurrentSpaceObject()
		if spaceObj and not spaceObj.canJoinTeam():
			self.statusMessage( csstatus.SPACE_NOT_ALLOW_JOIN_TEAM,"" )
			return
		
		objPlayer = KBEngine.entities.get( playerID )
		if objPlayer is None:
			return
		
		#如果自身在对方的黑名单列表中
		if objPlayer.cellHadBlacklist(self.playerDBID):
			return

		#当前地图禁止仙魔组队
		if spaceEntity.scriptID in csconst.FORBID_XIAN_MO_INVITE_EACE_OTHER and self.camp != objPlayer.camp:
			self.statusMessage(csstatus.TEAM_FORBID_DIFF_CAMP_INVITE_EACH_OHER, "")
			return

		# 当前地图禁止不同阵营的人组队
		if spaceEntity.scriptID in csconst.FORBID_DIFF_CAMP_INVITE_EACH_OTHER and self.tempCamp != objPlayer.tempCamp:
			self.statusMessage(csstatus.TEAM_FORBID_DIFF_CAMP_INVITE_EACH_OHER, "")
			return

		objPlayer.receiveJoinTeamRequest( self.getName(), self.playerDBID, self.profession, self.level, self.camp, self.base )

	def receiveJoinTeamRequest( self, playerName, playerDBID, profession, level, camp, playerBase ):
		"""
		define method
		收到入队申请
		"""
		if not self.isInTeam():
			if hasattr(playerBase, "client") and playerBase.client:
				playerBase.client.statusMessage( csstatus.TEAM_NOT_IN_TEAM, "" )
			return
		
		if self.isTeamFull():
			if hasattr(playerBase, "client") and playerBase.client:
				playerBase.client.statusMessage( csstatus.TEAM_FULL_REFUSE_JOIN, "" )
			return
		
		captainMB = self.getTeamCaptainMailBox()
		if captainMB:
			captainMB.captainReceiveJoinTeamRequest( self.getName(), playerName, playerDBID, profession, level, camp, playerBase )

	def replyPlayerJoinTeamFC( self, srcEntityID, agree, playerID ):
		"""
		<Exposed method>
		回复玩家的远程加队申请：同意还是不同意

		@param     agree: INT32; 是否同意加入
		@param playerID : OBJECT_ID; 被通知的玩家的entity id
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.base.replyPlayerJoinTeam( agree, playerID )
	
	#-----------------------近程邀请组队-----------------------
	def teamInviteFC( self, srcEntityID, playerID ):
		"""
		<exposed method>
		自己近程邀请某人组队
		
		@param playerID: 玩家的EntityID
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() in [csdefine.SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS, csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP]:
			return

		# 不允许邀请自己
		if self.id == playerID:
			self.statusMessage( csstatus.TEAM_NOT_INVITE_SELF, "")
			return

		spaceObj = self.getCurrentSpaceObject()
		if spaceObj and not spaceObj.canJoinTeam():
			self.statusMessage( csstatus.SPACE_NOT_ALLOW_JOIN_TEAM,"" )
			return

		objPlayer = KBEngine.entities.get( playerID )
		if objPlayer is None:
			return

		#如果自身在对方的黑名单列表中
		if objPlayer.cellHadBlacklist(self.playerDBID):
			self.statusMessage(csstatus.RELATION_MSG_FORBID_JOIN_TEAM_BLACK_LIST, objPlayer.getName())
			return

		#当前地图禁止仙魔组队
		if spaceEntity.scriptID in csconst.FORBID_XIAN_MO_INVITE_EACE_OTHER and self.camp != objPlayer.camp:
			self.statusMessage(csstatus.TEAM_FORBID_DIFF_CAMP_INVITE_EACH_OHER, "")
			return

		# 当前地图禁止不同阵营的人组队
		if spaceEntity.scriptID in csconst.FORBID_DIFF_CAMP_INVITE_EACH_OTHER and self.tempCamp != objPlayer.tempCamp:
			self.statusMessage(csstatus.TEAM_FORBID_DIFF_CAMP_INVITE_EACH_OHER, "")
			return

		# 队伍满了
		if self.isTeamFull():
			#告诉玩家队伍已满，无法邀请他人
			self.statusMessage( csstatus.TEAM_FULL, "")
			return

		# 目标已经有队伍了
		if objPlayer.isInTeam():
			self.statusMessage( csstatus.TEAM_PLAYER_IN_TEAM, "")
			return

		# 只有我没有组队或我是队长的时候才允许邀请别人组队/加入队伍
		if not self.isInTeam():
			objPlayer.base.teamInviteBy( self.base, self.getName(), self.profession, self.level, self.getCamp(), csdefine.TEAM_INVITE_TYPE_CREATE_TEAM, 0 )
		elif self.isTeamCaptain():
			objPlayer.base.teamInviteBy( self.base, self.getName(), self.profession, self.level, self.getCamp(), csdefine.TEAM_INVITE_TYPE_JOIN_TEAM, self.teamMailbox.id )
		else:
			self.teamInviteByTeammate( objPlayer.getName(), objPlayer.getCamp(), objPlayer.getProfession(), objPlayer.getLevel(), objPlayer.base )

	def teamInviteByTeammate( self, targetName, camp, profession, level, targetMB ):
		"""
		define method.
		自己向队长请求邀请某人组队
		"""
		captainMB = self.getTeamCaptainMailBox()
		if captainMB:
			if hasattr(captainMB, "client") and captainMB.client:
				captainMB.client.TeamInviteByTeammate( targetMB.id, targetName, camp, profession, level, self.getName(), self.id )
			self.statusMessage( csstatus.TEAMATE_INVITE_SEND_TO_CAPTAIN )

	def replyTeammateInvite( self, srcEntityID, targetID, targetName, teammateID, agree ):
		"""
		<exposed method>
		队长答复队员邀请其他玩家入队
		
		@param targetID: 目标玩家id
		@param targetName: 目标玩家名字
		@param teammateID: 队员id
		@param agree: 同意或拒绝
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if agree:
			if KBEngine.entities.get( targetID ):
				self.teamInviteFC( self.id, targetID )
			else:
				self.remoteTeamInviteFC( self.id, targetName )
		
		teammateMailBox = self.getTeamMemberMailbox( teammateID )
		if teammateMailBox and hasattr(teammateMailBox, "client") and teammateMailBox.client:
			if agree:
				teammateMailBox.client.statusMessage( csstatus.TEAM_CAPTAIN_AGREE_INVITE, targetName )
			else:
				teammateMailBox.client.statusMessage( csstatus.TEAM_CAPTAIN_REFUSE_INVITE, targetName )

	#-----------------------远程邀请组队-----------------------
	def remoteTeamInviteFC(self, srcEntityID, playerName):
		"""
		<exposed method>
		有客户端发送请求，远程邀请某玩家入队

		@param playerName: string;被邀请者的名称		
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() in [csdefine.SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS, csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP]:
			return

		if self.getCurrentSpaceScriptID() in csconst.BHZB_HOME_BARRACKS_SPACE or self.getCurrentSpaceScriptID() in g_BHZBPointDataLoader.getAllBHZBPVEAndPVPSpace():
			self.statusMessage( csstatus.BHZB_POINT_WAR_CALL_NOT_TEAM,"" )
			return

		# 队伍满了
		if self.isTeamFull():
			#告诉玩家队伍已满，无法邀请他人
			self.statusMessage( csstatus.TEAM_FULL )
			return

		spaceObj = self.getCurrentSpaceObject()
		if spaceObj and not spaceObj.canJoinTeam():
			self.statusMessage( csstatus.SPACE_NOT_ALLOW_JOIN_TEAM,"" )
			return
		
		# 不允许邀请自己
		if self.getName() == playerName:
			self.statusMessage( csstatus.TEAM_NOT_INVITE_SELF )
			return
		
		self.base.remoteTeamInviteFB(playerName)

	def checkIsCanJoinTeam( self, invitePlayer, inviterDBID, targetName):
		"""
		检查玩家是否在可以组队
		"""
		#如果对方在自身的黑名单列表中
		if self.cellHadBlacklist(inviterDBID):
			if hasattr(invitePlayer, "client") and invitePlayer.client:
				invitePlayer.client.statusMessage(csstatus.RELATION_MSG_FORBID_JOIN_TEAM_BLACK_LIST, self.getName())
			return
		
		spaceObj = self.getCurrentSpaceObject()
		if spaceObj and not spaceObj.canJoinTeam():
			invitePlayer.statusMessage( csstatus.ROLE_IN_NOT_ALLOW_JOIN_TEAM_SPACE,"" )
			return
		
		invitePlayer.teamInviteCB( self.base, targetName )

	def replyTeamInviteByFC( self, srcEntityID, agree, inviterID):
		"""
		<exposed method>
		由客户端调用，答复组队邀请，因此此方法会在被邀请者的base上执行。

		@param agree:INT32; 是否同意加入
		@param inviterID: 邀请者的EntitiyID
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		self.base.replyTeamInviteByFB( agree, inviterID )

	#---------------------离队、下线、解散队伍--------------------------
	def leaveTeamFC( self, srcEntityID, playerID ):
		"""
		<exposed method>
		由客户端请求：玩家自己离队或开除玩家离队。
		1、如果playerID是自己则是离队；
		2、如果playerID不是自己且自己是队长则开除playerID出队伍
		
		@param playerID: 开除的玩家ID
		@type  playerID: OBJECT_ID
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() in [csdefine.SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS, csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP]:
			return

		if self.getCurrentSpaceScriptID() in csconst.BHZB_HOME_BARRACKS_SPACE or self.getCurrentSpaceScriptID() in g_BHZBPointDataLoader.getAllBHZBPVEAndPVPSpace():
			self.statusMessage( csstatus.BHZB_POINT_WAR_CALL_NOT_TEAM,"" )
			return

		self.base.leaveTeamFB( playerID )
	
	def leaveTeamNotify( self, playreID ):
		"""
		define method
		成员离队通知
		"""
		self.triggerEntityEvent(csdefine.ENTITY_EVENT_ROLE_TEAM_LEAVE, [self.teamMailbox.id])
		if playreID == self.playerDBID:
			# 自己离开
			self.clearTeamInfo()
		else:
			# 队友离开
			self.removeTeamMember( playreID )


	def logoutNotify( self, playerID ):
		"""
		define method
		成员下线
		"""
		for e in self.teamMembers:
			if e["mailbox"] and e["mailbox"].id == playerID:
				e["mailbox"] = None

	def onRejoinTeam( self, playrDBID, playerMB ):
		"""
		define method
		成员上线
		"""
		for e in self.teamMembers:
			if e["dbID"] == playrDBID:
				e["mailbox"] = playerMB

	def disbandTeamFC( self, srcEntityID ):
		"""
		<exposed method>
		请求解散队伍，此方法用于客户端
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.getCurrentSpaceScriptID() in csconst.BHZB_HOME_BARRACKS_SPACE or self.getCurrentSpaceScriptID() in g_BHZBPointDataLoader.getAllBHZBPVEAndPVPSpace():
			self.statusMessage( csstatus.BHZB_POINT_WAR_CALL_NOT_TEAM,"" )
			return

		self.base.disbandTeamFB()

	def disbandTeamNotify( self ):
		"""
		<define method>
		队伍解散通知，此方法由self.base调用
		"""
		self.clearTeamInfo()
		#将来可能加入事件，用于副本规则(如：队伍解散时候自动退出副本)
		

	#-----------------------队长变更----------------------
	def changeCaptainFC( self, srcEntityID, playerID ):
		"""
		<exposed method>
		移交队长权限，此接口由client调用

		@param playerID: 玩家的ID
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() in [csdefine.SPACE_TYPE_CHILD_BHZB_HOME_BARRACKS, csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP]:
			return
		
		if self.getCurrentSpaceScriptID() in csconst.BHZB_HOME_BARRACKS_SPACE or self.getCurrentSpaceScriptID() in g_BHZBPointDataLoader.getAllBHZBPVEAndPVPSpace():
			self.statusMessage( csstatus.BHZB_POINT_WAR_CALL_NOT_TEAM,"" )
			return
		# 移交的目标不能是自己
		if self.id == playerID:
			return

		#移交队长权限时需要移交标记权
		self.teamMailbox.changeTeamSigner( playerID )
		self.base.changeCaptainFB(playerID)	

	def changeCaptainNotify( self, captainID ):
		"""
		<define method>
		由自己的base通知：队长改变了

		@param captainID: OBJECT_ID; 队长ID
		"""
		oldCaptainID = self.captainID
		self.captainID = captainID
		
		if self.id == captainID or self.id == oldCaptainID:
			if self.getClient():
				self.client.RefreshAroundBoxStatus( csdefine.SPELL_BOX_LISTEN_EVENT_IS_CAPTAIN )	#更新周围箱子可交互状态（有的箱子要求队长才能交互）
			belongType = csdefine.SPACE_BELONG_TEAM
			if (belongType, self.teamMailbox.id ) in KBEngine.globalData["MagicMazeParentSpaceGlobalRecord"]:
				spaceEntity = self.getCurrentSpace()
				if spaceEntity:
					spaceEntity.getScript().onTeamCaptainChange(spaceEntity)

	#------------------------------请求队员信息--------------------------
	def requestTeammateInfoFC( self, srcEntityID, playerID ):
		"""
		<exposed method>
		客户端申请获取队伍中某个队伍成员的数据

		@param playerID: OBJECT_ID；玩家的entity id
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		mailbox = self.getTeamMemberMailbox( playerID )
		if mailbox is None:
			KBEDebug.INFO_MSG("'%s' try get offline team member data!" % (self.getName()))
			return
		mailbox.cell.requestTeammateInfo( self.base )

	def requestTeammateInfo( self, requesterBase ):
		"""
		<Define method>
		由请求者的base请求：请把你的队伍信息发送给我

		@param requesterBase: 玩家BASE
		"""
		#发送自身队伍信息给请求者
		#预留接口，很多属性尚不存在
		if hasattr(requesterBase, "client") and requesterBase.client:
			requesterBase.client.teammateInfoNotify(self.id, self.level, self.HP, self.HP_Max, self.MP, self.MP_Max, self.getCurrentSpaceScriptID(), self.lineNumber)

	#-----------------------奖励分配----------------------
	def setAllocationFC( self, srcEntityID, allocation ):
		"""
		<exposed method>
		设置奖励分配方式
		
		@param allocation: INT32; 分配模式
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.captainID == self.id:
			self.teamMailbox.setAllocation( allocation )
		
	def setQualityFC( self, srcEntityID, quality ):
		"""
		<exposed method>
		设置奖励分配品质标准
		
		@param quality: INT32; 物品品质标准
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.captainID == self.id:
			self.teamMailbox.setQuality( quality )
	
	def modifyAllocation( self, allocation ):
		"""
		<define method>
		修改队伍物品分配模式
		
		@param allocation: INT32;分配模式
		"""
		self.allocation = allocation
		
	def modifyQuality( self, quality ):
		"""
		<define method>
		修改队伍物品分配品质标准
		
		@param quality: INT32; 物品品质标准
		"""
		self.quality = quality

	#-----------------拒绝邀请组队功能---------------------
	def setForbidTeamInviteFC( self, srcEntityID, value ):
		"""
		exposed method
		客户端设置“拒绝邀请”
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.forbidTeamInvite = value
		self.base.setForbidTeamInvite( value )
	
	#--------------队员buff图标显示----------------------------
	def notifyClientAddBuff( self, buffData, buffTotalTime, buffTime ):
		"""
		添加buff
		"""
		if not self.isInTeam():
			return
		for mb in self.getAllTeamMemberMB():
			if hasattr(mb, "client") and mb.client:
				mb.client.OnTeamMemberAddBuff( self.id, buffData.index, buffData.buffID, buffTotalTime, buffTime )
	
	def notifyClientRemoveBuff( self, buffData ):
		"""
		删除buff
		"""
		if not self.isInTeam():
			return
		for mb in self.getAllTeamMemberMB():
			if hasattr(mb, "client") and mb.client:
				mb.client.OnTeamMemberRemoveBuff( self.id, buffData.index )
	
	def onResetBuffEndTime( self, buffIndex, buffTime ):
		"""
		重置buff持续时间回调
		"""
		if not self.isInTeam():
			return
		for mb in self.getAllTeamMemberMB():
			if hasattr(mb, "client") and mb.client:
				mb.client.OnTeamMemberResetBuffTime( self.id, buffIndex, buffTime )
	
	#--------------给entity打标记---------------------------
	def requestAddTeamSignFC( self, srcEntityID, entityID, signNumber ):
		"""
		exposed method
		打标记
		
		@param entityID: 要标记的entity id
		@param signNumber: 标记编号
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not self.isInTeam():
			return
		playerEntity = KBEngine.entities.get( entityID,None )
		if not playerEntity:
			self.statusMessage( csstatus.TEAM_CAN_NOT_SIGN_NUMBER )
			return
		self.teamMailbox.addTeamSign( self.base, entityID, signNumber )
	
	#-----------------队伍跟随-------------------------------
	def isTeamFollowing( self ):
		"""
		在组队跟随？
		"""
		return self.teamFollowTarget != 0
	
	def isTeamFollowLeading( self ):
		"""
		在领导组队跟随？
		"""
		return self.leadTeamFollowFlag == 1
	
	def requestLeadTeamFollowFC( self, srcEntityID ):
		"""
		exoposed method
		队长发起组队跟随
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not self.isTeamCaptain():
			return
		self.teamMailbox.requestLeadTeamFollow( self.base, self.getName() )
	
	def cancelLeadTeamFollowFC( self, srcEntityID ):
		"""
		exposed method
		队长取消组队跟随
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.teamMailbox.cancelLeadTeamFollow( self.base, self.getName() )
	
	def receiveTeamFollowRequest( self, requesterMB, requesterName ):
		"""
		define method
		队员收到队长跟随邀请
		"""
		requester = KBEngine.entities.get( requesterMB.id, None )
		if not requester:
			return
		if self.spaceID != requester.spaceID:
			return
		if self.position.distTo( requester.position ) > csconst.TEAM_FOLLOW_REQUEST_DISTANCE:
			return
		self.inquireMessage( csstatus.TEAM_INVITE_FOLLOW_OTHER_PLAYER , (requesterName,), "replyTeamFollowRequestFC", requesterMB.id )
	
	def replyTeamFollowRequestFC( self, agree, requesterID ):
		"""
		队员答复队长组队跟随
		"""
		if not self.isInTeam():
			return
		
		if self.captainID != requesterID:	#队长已经换人了
			return
		
		requesterMB = self.getTeamMemberMailbox( requesterID )
		if not requesterMB:
			return
		
		if not agree:
			if hasattr(requesterMB, "client") and requesterMB.client:
				requesterMB.client.statusMessage( csstatus.TEAMATE_FOLLOW_REPLY_FALSE, self.getName() )
			return
		
		#有这些效果时，不能跟随
		for eState in csconst.TEAM_FOLLOW_FORBID_EFFECT:
			if self.hasEffectState( eState ):
				if eState == csdefine.EFFECT_STATE_DIZZY:
					self.statusMessage( csstatus.TEAM_FOLLOW_FORBID_DIZZY )
				if eState == csdefine.EFFECT_STATE_SLEEP:
					self.statusMessage( csstatus.TEAM_FOLLOW_FORBID_SLEEP )
				if eState == csdefine.EFFECT_STATE_FIX:
					self.statusMessage( csstatus.TEAM_FOLLOW_FORBID_FIX )
				if eState == csdefine.EFFECT_STATE_WIND:
					self.statusMessage( csstatus.TEAM_FOLLOW_FORBID_WIND )
				return
		
		self.teamMailbox.memberAcceptTeamFollow( self.base, self.getName(), requesterMB )
	
	def cancelTeamFollowFC( self, srcEntityID, reason ):
		"""
		exposed method
		队员取消组队跟随
		不管是服务器还是客户端，取消跟随都用此接口
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not self.isInTeam():
			return
		self.teamMailbox.memberCancelTeamFollow( self.base, self.getName(), reason )
	
	def startTeamFollow( self, leaderID ):
		"""
		define method
		开始组队跟随
		TeamEntity回调
		"""
		if self.isTeamFollowing():
			return
		
		if self.isNormalFollowing():	# 在普通跟随中的话，先打断普通跟随
			self.cancelNormalFollowFC( self.id )
		
		self.teamFollowTarget = leaderID
		if self.getClient():
			self.client.StartTeamFollow( leaderID )
	
	def stopTeamFollow( self ):
		"""
		define method
		结束组队跟随
		TeamEntity回调
		"""
		if not self.isTeamFollowing():
			return
		self.teamFollowTarget = 0
		if hasattr( self, "client" ) and self.client:
			self.client.StopTeamFollow()
	
	def followNewCaptain( self, newCaptainID ):
		"""
		define method
		队长改变，跟随新队长
		TeamEntity回调
		"""
		self.teamFollowTarget = newCaptianID
		if self.getClient():
			self.client.FollowNewCaptain( newCaptianID )
	
	def startLeadTeamFollow( self ):
		"""
		define method
		开始领导组队跟随
		"""
		self.leadTeamFollowFlag = 1
	
	def stopLeadTeamFollow( self ):
		"""
		define method
		停止领导组队跟随
		"""
		self.leadTeamFollowFlag = 0
	
	def npcTeamFollowTransport( self, talkEntity, dlgKey ):
		"""
		队长过地图了把队员带过去
		talkEntity是realEntity，自己有可能是ghost
		"""
		if not self.isTeamFollowLeading():
			return
		for e in talkEntity.entitiesInRangeExt( csconst.TEAM_FOLLOW_TRANSPORT_DISTANCE, "Role" ):
			if e.id == self.id:		# 验证一下，避免无限对话造成死循环
				return
			if e.teamFollowTarget == self.id:	# 是跟随自己的玩家
				talkEntity.talkWith( e.id, dlgKey, {} )
	
	def doorTeamFollowTransport( self, doorEntity, spaceScriptID, position, direction ):
		"""
		队长过传送门把队员带过去
		"""
		if not self.isTeamFollowLeading():
			return
		for e in talkEntity.entitiesInRangeExt( csconst.TEAM_FOLLOW_TRANSPORT_DISTANCE, "Role" ):
			if e.id == self.id:		# 验证一下，避免死循环
				return
			if e.teamFollowTarget == self.id:	# 是跟随自己的玩家
				e.gotoSpaceUE4( spaceScriptID, position, direction )
	
	#-------------------普通跟随：严格来说跟队伍没什么关系，但现在限制为只能跟随队友，所以还是放在队伍接口里----------------------
	def isNormalFollowing( self ):
		"""
		是否在普通跟随中
		"""
		return self.normalFollowTarget != 0

	def hasNormalFollowID( self ):
		return self.normalFollowID != 0

	def setNormalFollowID(self, targetID):
		self.normalFollowID = targetID
	
	def requestNormalFollowFC( self, srcEntityID, targetID ):
		"""
		exposed method
		请求普通跟随
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		entity = KBEngine.entities.get( targetID, None )
		if entity is None:
			return
			
		if entity.isState( csdefine.ENTITY_STATE_DEAD ):
			self.statusMessage( csstatus.COMMON_FOLLOW_PLAYER_DEAD )
			return
		if self.isState( csdefine.ENTITY_STATE_STALL ):
			self.statusMessage( csstatus.COMMON_FOLLOW_FAIL )
			return
		if self.position.distTo( entity.position ) > csconst.TEAM_FOLLOW_REQUEST_DISTANCE:
			self.statusMessage( csstatus.COMMON_FOLLOW_TO_FAW_AWAY )
			return

		#有这些效果时，不能跟随
		for eState in csconst.TEAM_FOLLOW_FORBID_EFFECT:
			if self.hasEffectState( eState ):
				if eState == csdefine.EFFECT_STATE_DIZZY:
					self.statusMessage( csstatus.TEAM_FOLLOW_FORBID_DIZZY )
				if eState == csdefine.EFFECT_STATE_SLEEP:
					self.statusMessage( csstatus.TEAM_FOLLOW_FORBID_SLEEP )
				if eState == csdefine.EFFECT_STATE_FIX:
					self.statusMessage( csstatus.TEAM_FOLLOW_FORBID_FIX )
				if eState == csdefine.EFFECT_STATE_WIND:
					self.statusMessage( csstatus.TEAM_FOLLOW_FORBID_WIND )
				return
		
		if self.isTeamFollowing():
			self.cancelTeamFollowFC( self.id, csdefine.TF_CANCEL_ACTIVE_CANCEL )
		
		self.normalFollowTarget = targetID
		entity.setNormalFollowID(self.id)
		self.statusMessage( csstatus.COMMON_FOLLOW_THE_SUCCESSFUL )
		entity.statusMessage( csstatus.COMMON_FoOLLOW_TO_BEING, self.getName() )
		self.client.StartNormalFollow( targetID )
	
	def cancelNormalFollowFC( self, srcEntityID ):
		"""
		exposed method
		取消普通跟随
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		entity = KBEngine.entities.get( self.normalFollowTarget, None )
		if hasattr( self, "client" ) and self.client:
			self.client.StopNormalFollow()
			if not entity:
				self.statusMessage( csstatus.COMMON_FOLLOW_TO_CANCEL )
			elif self.isState( csdefine.ENTITY_STATE_DEAD ) or entity.spaceID != self.spaceID\
			 or self.position.distTo( entity.position ) > csconst.TEAM_FOLLOW_REQUEST_DISTANCE:
				self.statusMessage( csstatus.COMMON_FOLLOW_TO_CANCEL )
				entity.statusMessage( csstatus.COMMON_FoOLLOW_TO_STOP, self.getName() )
			else:
				self.statusMessage( csstatus.COMMON_FOLLOW_TO_CANCEL )
				entity.statusMessage( csstatus.COMMON_FoOLLOW_TO_STOP, self.getName() )
		self.normalFollowTarget = 0
		self.normalFollowID = 0

	def _cancelNormalFollowFC( self, srcEntityID ):
		"""
		被跟随者死亡的处理
		"""
		if self.id != srcEntityID:
			return
		entity = KBEngine.entities.get( self.normalFollowID, None )
		if hasattr( entity, "client" ) and entity.client:
			entity.client.StopNormalFollow()
			entity.statusMessage( csstatus.COMMON_FOLLOW_TO_CANCEL )
			self.statusMessage( csstatus.COMMON_FoOLLOW_TO_STOP, self.getName() )
		self.normalFollowID = 0

	def requestRoleTeamSpellBoxFollow(self, srcEntityID, targetID):
		"""
		exposed method
		通过场景物件被队友传送到队友身边
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		entity = KBEngine.entities.get( targetID, None )
		if not entity or entity.spaceID != self.spaceID:
			self.statusMessage( csstatus.TEAM_TO_FOLLOW_FAILD  )
			return
		spaceScriptID = self.getCurrentSpaceScriptID()
		self.gotoSpace(spaceScriptID,Math.Vector3(entity.position),(0,0,0))
		

	def roleTeamSpellBoxFollow(self, casterID, timeValue):
		"""
		"""
		self.client.RoleTeamSpellBoxFollow(casterID, timeValue)

	def shareBigMapCustomMarker( self, srcEntityID, levelName, position, markerType):
		"""
		exposed method
		共享大地图共享标记给其他队友
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.teamMailbox.memberShareBigMapCustomMarker( self.base, levelName, position, markerType )
	
	def otherMemberShareBigMapCustomMarker( self, memberName, levelName, position, markerType ):
		"""
		define method
		TeamEntity回调
		"""
		if hasattr( self, "client" ) and self.client:
			self.client.onMemberShareBigMapCustomMarker( memberName, levelName, position, markerType )

	def CELL_updateMembersPos( self, srcEntityID, entityIDList ):
		"""
		exposed method
		更新同一大地图队友的位置
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not self.isInTeam():
			return
		for mb in self.getAllTeamMemberMB():
			if mb.id in entityIDList:
				mb.cell.onUpdatePosToTarget(self.spaceScriptID, self )

	def onUpdatePosToTarget( self, spaceScriptID, targetPlayer ):
		"""
		更新位置信息到targetPlayer
		"""
		position = Math.Vector3(KBEMath.KBEngine2UnrealPosition(tuple(self.position)))
		tempDict = {}
		tempDict["objectID"] = self.id
		tempDict["position"] = position
		tempDict["name"] = self.playerName
		targetPlayer.OnUpdateMemeberPos( tempDict )

	def OnUpdateMemeberPos( self, memberDataDict ):
		if self.getClient():
			self.client.CLIENT_OnUpdateMemeberPos( memberDataDict )

	def CELL_callAllTeamMemberToCaptainLineNumber( self, srcEntityID, entityIDList ):
		"""
		exposed method
		队长召唤全队同线
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not self.isTeamCaptain():
			return
		if int(self.getCurrentSpaceData( Const.SPACE_DATA_SPACE_TYPE )) != csdefine.SPACE_TYPE_MULTILINE:
			self.statusMessage( csstatus.TEAM_CAPTAIN_LIMIT_CALL )
			return
		if self.getState() in [csdefine.ENTITY_STATE_STALL,csdefine.ENTITY_STATE_DEAD]:
			self.statusMessage( csstatus.TEAM_CAPTAIN_STATE_NOT_ALLOW_CALL )
			return
		spaceObj = self.getCurrentSpaceObject()
		if not spaceObj or (spaceObj.checkFullOnTeleport( self.getCurrentSpace() ) == False):
			self.statusMessage( csstatus.TEAM_CAPTAIN_LINENUMBER_IS_FULL )
			return
		for mb in self.getAllTeamMemberMB():
			if mb.id in entityIDList:
				mb.cell.receiveCaptainInvite( self,self.lineNumber, self.spaceScriptID, self.position, self.direction )
	
	def receiveCaptainInvite( self, inviterPlayer,lineNumber, spaceScriptID, position, direction ):
		"""
		接收到队长召唤的请求
		"""
		if self.spaceScriptID == spaceScriptID and self.lineNumber == lineNumber:
			return
		if self.getState() in [csdefine.ENTITY_STATE_STALL,csdefine.ENTITY_STATE_DEAD]:
			self.statusMessage( csstatus.STATE_NOT_ALLOW_TEAM_CALL,"" )
			inviterPlayer.statusMessage( csstatus.ROLE_IN_NOT_ALLOW_CALL_STATE,self.getName() )
			return
		self.inquireMessage( csstatus.TEAM_CAPTAIN_CALL_YOU, [],"replyForCaptainInvite",lineNumber,spaceScriptID,position,direction )

	def replyForCaptainInvite( self, reply, lineNumber, spaceScriptID, position, direction ):
		"""
		队长召唤你去与他相同的线，是否同意
		"""
		if reply:
			spaceObj = KST.g_objFactory.getSpaceObject( spaceScriptID )
			if not spaceObj or spaceObj.checkFullOnTeleport( self.getCurrentSpace() ) == False:
				self.statusMessage( csstatus.TEAM_LINENUMBER_IS_FULL )
				return
			self.setTemp("lineNumber",lineNumber)
			self.gotoSpace( spaceScriptID, position, direction )
			self.removeTemp("lineNumber")

	#--------------------------------------快速组队--------------------------------------
	def fastTeamOnjoin(self):
		"""
		参加快速组队
		"""
		self.isMatchFastTeam = True
		self.setFastTeamTalkNpcID(self.tempFastTeamTalkNpcID)

	def fastTeamOnCancel( self ):
		"""
		取消快速组队
		"""
		self.isMatchFastTeam = False

	def getIsMatchFastTeam( self ):
		return self.isMatchFastTeam
		
	def getFastTeamTalkNpcID(self):
		return self.fastTeamTalkNpcID
		
	def setFastTeamTalkNpcID(self, talkNpcID):
		self.fastTeamTalkNpcID = talkNpcID
		
	def setTempFastTeamTalkNpcID(self, talkNpcID):
		self.tempFastTeamTalkNpcID = talkNpcID

	def sendFastTeamChatMsg( self, chatType, bunchSpaceName ):
		"""
		发送快速组队消息
		"""
		chatData = ChatData()
		chatData.init( self.playerDBID, self.getName(), chatType, int(self.getEntityFlag()), (cschannel_msgs.FAST_TEAM_MSG%(self.getName(),self.getName(),bunchSpaceName,self.getName(),self.getName())),"", {} )
		g_chatMgr.onSend( self, chatData )

	def CELL_applyJoinFastTeam( self, srcEntityID, playerName ):
		"""
		exposed method
		加入某个队伍
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		# 不允许邀请自己
		if self.getName() == playerName:
			self.statusMessage( csstatus.TEAM_NOT_JOIN_SELF,"" )
			return

		if self.isInTeam():
			self.statusMessage( csstatus.SELF_IS_IN_TEAM_NOT_JOIN,"" )
			return

		spaceObj = self.getCurrentSpaceObject()
		if spaceObj and not spaceObj.canJoinTeam():
			self.statusMessage( csstatus.SPACE_NOT_ALLOW_JOIN_TEAM,"" )
			return

		self.base.applyJoinFastTeam(playerName)

	def CELL_replyTeamApplyFastTeam( self, srcEntityID, agree, applyID ):
		"""
		exposed method
		答复快速组队的申请
		@param agree:INT32; 是否同意加入
		@param applyID: 申请者的EntitiyID
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.base.replyTeamApplyFastTeam( agree, applyID )

	def CELL_callMemberEnterSpaceCopy( self,srcEntityID,entityID):
		"""
		exposed method
		邀请进入副本
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not self.isInSpaceCopy():
			return
		memberMailbox = self.getTeamMemberMailbox( entityID )
		if not memberMailbox:
			return
		spaceObj = self.getCurrentSpaceObject()
		if not spaceObj:
			return
		bunchObj = spaceObj.getBunchSpaceObj()
		if not bunchObj:
			return
		spaceScriptID = self.getCurrentSpaceScriptID()
		memberMailbox.cell.receiveMemberInvitedToEnterSpaceCopy( self.getName(),bunchObj.scriptID,spaceScriptID,self.position, self.direction )

	def receiveMemberInvitedToEnterSpaceCopy( self, inviterName,bunchSpaceScriptID,spaceScriptID,position,direction ):
		"""
		接受队员进入副本的邀请
		"""
		if not self.isCanInvitedToEnterSpace: #不能被邀请进入副本
			return
		bunchSpaceName = ""
		bunchObj = KST.g_objFactory.getBunchSpaceObject( bunchSpaceScriptID )
		if bunchObj:
			bunchSpaceName = bunchObj.getBunchSpaceName()
		self.inquireMessage(csstatus.TEAM_CAPTAIN_CALL_YOU, [inviterName,bunchSpaceName],"replyForMemberInviteToEnterSpaceCopy",[bunchSpaceScriptID,spaceScriptID,position,direction] )

	def replyForMemberInviteToEnterSpaceCopy( self,reply,bunchSpaceScriptID,spaceScriptID,position,direction ):
		"""
		回答队员邀请
		"""
		if reply:
			belongType = csdefine.SPACE_BELONG_TEAM
			self.gotoBunchSpace( bunchSpaceScriptID, { "packBelongType": belongType, "destChildSpace": spaceScriptID } )
		else:
			self.isCanInvitedToEnterSpace = False
			self.addTimerCallBack( 60.0, "changeInvitedToEnterSpaceState",() )

	def changeInvitedToEnterSpaceState( self ):
		"""
		改变是否能被邀请
		"""
		self.isCanInvitedToEnterSpace = True
		
	def requestFastTeam( self, srcEntityID, camp, profession,minLevel,maxLevel,chatType, spaceScriptID, npcScriptID, npcID, talkKey ):
		"""
		请求快速组队
		"""
		"""
		npcEntity = KBEngine.entities.get(npcID, None)
		if not npcEntity:
			KBEDebug.ERROR_MSG("can not find npc: %s" % npcID)
			return
		talkObj = g_npcTalk.get(npcScriptID)
		talkDialog = talkObj.getDialog(talkKey)
		if talkDialog:
			if talkDialog.canDo(self, npcEntity, ""):
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		self.setTempFastTeamTalkNpcID(npcID)
		self.base.requestFastTeam(camp, profession,minLevel,maxLevel,chatType, spaceScriptID)
		
	def fastTeamRequestGotoBunchSpace( self,srcEntityID, spaceScriptID, npcScriptID, npcID, talkKey ):
		"""
		exposed method
		快速组队进入副本
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		"""
		if not self.isInTeam():
			return
		"""	
		"""
		spaceObj = KST.g_objFactory.getSpaceObject(spaceScriptID)
		#如果是副本串，获取到的spaceObj可能是None，其他副本不会
		if not spaceObj or (hasattr(spaceObj, "isBunchChildSpace") and spaceObj.isBunchChildSpace()):
			#副本串\试炼副本
			self.fastTeamGotoBunchSpace(spaceScriptID)
		"""
		npcEntity = KBEngine.entities.get(npcID, None)
		if not npcEntity:
			KBEDebug.ERROR_MSG("can not find npc: %s" % npcID)
			return
		
		talkObj = g_npcTalk.get(npcScriptID)
		talkDialog = talkObj.getDialog(talkKey)
		if talkDialog:
			talkDialog.doTalk(talkKey, self, npcEntity, "")
			
	def fastTeamGotoBunchSpace(self, bunchSpaceScriptID):
		"""
		快速组队进入副本串
		"""
		globalRecord = KBEngine.globalData["BunchSpaceGlobalRecord"]
		belongType = csdefine.SPACE_BELONG_TEAM
		spaceKey = str( self.teamMailbox.id )

		if ( bunchSpaceScriptID in globalRecord ) and \
			( belongType in globalRecord[ bunchSpaceScriptID ] ) and \
			( spaceKey in globalRecord[ bunchSpaceScriptID ][ belongType ] ):	# 存在副本
			self.gotoBunchSpace( bunchSpaceScriptID, { "packBelongType": belongType, "destChildSpace": destSpace,"bunchLevel":self.getLevel() } )
		else:
			if not self.isTeamCaptain():	# 副本不存在的情况下，这里一定是队长对话
				return
			teammates = []
			for memMB in self.getAllTeamMemberMB():
				if memMB.id != self.id:
					teammates.append( memMB )
			bunchObj = KST.g_objFactory.getBunchSpaceObject( bunchSpaceScriptID )
			destSpace = g_bunchChildStrategyLoader.getFirstSpace( bunchObj, self )	#CST-1938 按策略随机第一个子副本
			self.gotoBunchSpace(bunchSpaceScriptID, { "packBelongType": belongType,  "destChildSpace": destSpace,"bunchLevel":self.getLevel(), "teammates": teammates } )

	def CELL_teamAssembled(self, srcEntityID, spaceScriptID, position):
		"""
		<Exposed/>
		队伍集结
		"""
		mblist = self.getAllTeamMemberMB()
		for mb in mblist:
			if hasattr(mb, "client") and mb.client:
				mb.client.CLIENT_onTeamAssembled(spaceScriptID, position )

