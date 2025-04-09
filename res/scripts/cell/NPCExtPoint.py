# -*- coding: utf-8 -*-
#
import KBEngine
import NPC
import Const
import csdefine
import Functions
import KST

class NPCExtPoint(NPC.NPC):
	"""
	据点
	"""
	def __init__(self):
		self.index = self.group
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP:
			spaceEntity.addNPCPointData(self.index,self.occupyPlayerDBID,self.occupyPlayerName,self.occupyTongDBID, self.occupyTongName,self.pointType,self.declareWarState,self.fightEndTime, self.restEndTime, self.readyEndTime,self.joinAttackPlayerDBIDs,self.joinProtectPlayerDBIDs)

		NPC.NPC.__init__( self )
		self.maxJoinPlayerNum = self.getScript().getMaxJoinPlayerNum()

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_NPC_POINT)

	def getIndex( self ):
		return self.index

	def getRemainReadyTime( self ):
		"""
		获得准备剩余时间
		"""
		remainTime = self.declareWarTime + self.getScript().getReadTime() - Functions.getTime()
		if remainTime > 0:
			return remainTime
		return 0

	def openNPCExtPointDetails( self, player ):
		"""
		打开据点详情面板
		"""
		pass
		# if self.declareWarState == csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE:
		# 	if player.getClient():
		# 		player.client.OpenNPCExtPointDetails( self.getUname(),self.pointType, self.declareWarState, [],[],self.maxJoinPlayerNum,0,self.id )
		# else:
		# 	occupyTongName = ""
		# 	occupyJoinMemberNum = 0
		# 	if self.occupyPlayerDBID > 0:
		# 		occupyTongName = self.occupyTongName
		# 		occupyJoinMemberNum = len( self.joinProtectPlayerDBIDs )

		# 	declareTongName = ""
		# 	declareJoinMemberNum = 0
		# 	if self.declareTongDBID > 0:
		# 		declareTongName = self.declareTongName
		# 		declareTongName = len( self.joinAttackPlayerDBIDs )

		# 	remainReadyTime = self.getRemainReadyTime()
		# 	if player.getClient():
		# 		player.client.OpenNPCExtPointDetails( self.getUname(), self.pointType, self.declareWarState, [declareTongName,occupyTongName],[declareJoinMemberNum,occupyJoinMemberNum],self.maxJoinPlayerNum,remainReadyTime,self.id)

	def setDeclareWarData( self, declarePlayerDBID, declareTongDBID, declareTongName, declarePlayerName ):
		"""
		设置宣战的数据
		"""
		self.declarePlayerDBID = declarePlayerDBID
		self.declareTongDBID = declareTongDBID
		self.declareTongName = declareTongName
		self.declarePlayerName = declarePlayerName
		self.declareWarTime = Functions.getTime()
		remainTime = self.getRemainReadyTime()
		readyEndTime = str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime())
		self.setNPCPointReadyEndTime(readyEndTime)
		self.addJoinAttackMembers( declarePlayerDBID )
		self.setNPCExtPointState( csdefine.NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE )

	def setNPCExtPointState( self, declareWarState ):
		"""
		设置据点状态
		"""
		self.declareWarState = declareWarState
		if self.declareWarState == csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE:
			self.fightEndTime = ""
			self.setNPCPointRestEndTime("")
			self.joinAttackPlayerDBIDs = []
			self.joinProtectPlayerDBIDs = []
		if self.declareWarState == csdefine.NPCEXTPOINT_STATE_REST:
			self.fightEndTime = ""
			restEndTime = str(self.getScript().getRestTime() * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime())
			self.setNPCPointRestEndTime(restEndTime)
			self.addTimerCallBack( self.getScript().getRestTime(),"setNPCExtPointState",(csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE,) )

	def addJoinAttackMembers( self, playerDBID ):
		"""
		增加参与攻击据点的人员
		"""
		if playerDBID not in self.joinAttackPlayerDBIDs:
			self.joinAttackPlayerDBIDs.append( playerDBID )

	def addJoinProtectMembers( self, playerDBID ):
		"""
		增加参与保护据点的人员
		"""
		if playerDBID not in self.joinProtectPlayerDBIDs:
			self.joinProtectPlayerDBIDs.append( playerDBID )

	def clearDeclareWarData( self ):
		"""
		清除宣战的数据
		"""
		self.declarePlayerDBID = 0
		self.declareTongDBID = 0
		self.declareTongName = ""
		self.declareWarTime = 0
		self.declarePlayerName = ""
		self.setNPCExtPointState( csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE )

	def setOccupyData( self, occupyPlayerDBID, occupyPlayerName, occupyTongDBID, occupyTongName ):
		"""
		设置被占领的数据
		"""
		self.occupyPlayerDBID = occupyPlayerDBID
		self.occupyPlayerName = occupyPlayerName
		self.setNPCPointOccupyTongDBID( occupyTongDBID )
		self.occupyTongName = occupyTongName
		self.setNPCExtPointState( csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE )

	def declareNPCExtPoint( self, playerID ):
		"""
		跟据点宣战
		"""
		if self.declareWarState != csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE:
			return

		player = KBEngine.entities.get( playerID, None )
		if not player:
			return

		if player.tongDBID == self.occupyTongDBID:
			return

		if player.getIsDeclarePointBHZB():
			return

		if self.occupyPlayerDBID == player.playerDBID:
			return

		self.setDeclareWarData( player.playerDBID, player.tongDBID, player.tongName, player.getName() )
		player.setIsDeclarePointBHZB( True )
		self.openNPCExtPointDetails( player )
		remainTime = self.getRemainReadyTime()
		if remainTime > 0:
			self.notifyID = self.addTimerCallBack( remainTime, "onEnterNPCExtPointWar", () )

	def onEnterNPCExtPointWar( self ):
		"""
		进入据点争夺战
		"""
		self.setNPCPointReadyEndTime("")
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP:
			if self.occupyPlayerDBID > 0:
				spaceScriptID = self.getScript().getEnterPVPSpace()
			else:
				spaceScriptID = self.getScript().getEnterPVESpace()

			for playerDBID in self.joinAttackPlayerDBIDs:
				roleMB = spaceEntity.getRoleMBByPlayerDBID( playerDBID )
				if roleMB == None:
					KBEngine.globalData["BHZBManager"].requestGotoNPCExtPointWar( playerDBID, self.index, spaceScriptID, self.occupyPlayerDBID, self.declareTongDBID, self.occupyTongDBID, self.pointType, self.getUname(),self,self.declareTongName,self.declarePlayerDBID,self.declarePlayerName )
					return
				roleMB.requestGotoNPCExtPointWar( self.index, spaceScriptID, self.occupyPlayerDBID, self.declareTongDBID, self.occupyTongDBID,self.pointType, self.getUname(), self,self.declareTongName,self.declarePlayerDBID,self.declarePlayerName )

			if self.occupyTongDBID > 0:
				for playerDBID in self.joinProtectPlayerDBIDs:
					roleMB = spaceEntity.getRoleMBByPlayerDBID(playerDBID)
					if roleMB == None:
						KBEngine.globalData["BHZBManager"].requestGotoNPCExtPointWar( playerDBID,self.index, spaceScriptID, self.occupyPlayerDBID, self.declareTongDBID, self.occupyTongDBID, self.pointType, self.getUname(), self,self.declareTongName,self.declarePlayerDBID,self.declarePlayerName )
						return
					roleMB.requestGotoNPCExtPointWar(  self.index, spaceScriptID, self.occupyPlayerDBID, self.declareTongDBID, self.occupyTongDBID,self.pointType, self.getUname(), self,self.declareTongName,self.declarePlayerDBID,self.declarePlayerName )

	def calculatFightEndTime( self, spaceScriptID ):
		"""
		计算战斗结束时间
		"""
		spaceObj = KST.g_objFactory.getSpaceObject( spaceScriptID )
		if not spaceObj:
			return
		self.fightEndTime = str(spaceObj.getSpaceLife() * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime())

	def cancelDeclareNPCExtPoint( self, playerID ):
		"""
		取消据点宣战
		"""
		if self.declareWarState != csdefine.NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE:
			return

		player = KBEngine.entities.get( playerID, None )
		if not player:
			return

		if self.declarePlayerDBID != player.playerDBID:
			return

		self.clearDeclareWarData()
		player.setIsDeclarePointBHZB( False )

	def joinNPCExtPointFight( self, playerID ):
		"""
		参与据点争夺
		"""
		if self.declareWarState != csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE:
			return

		player = KBEngine.entities.get( playerID, None )
		if not player:
			return

		if player.tongDBID == self.declareTongDBID:
			if len( self.joinAttackPlayerDBIDs ) > self.maxJoinPlayerNum:
				return
			self.addJoinAttackMembers( player.playerDBID )
			if self.declareWarState == csdefine.NPCEXTPOINT_STATE_FIGHT:
				player.requestGotoNPCExtPointWar( self.index, spaceScriptID, self.occupyPlayerDBID, self.declareTongDBID, self.occupyTongDBID,self.pointType, self.getUname(), self,self.declareTongName,self.declarePlayerDBID,self.declarePlayerName )

		elif player.tongDBID == self.occupyPlayerDBID:
			if len( self.joinProtectPlayerDBIDs ) > self.maxJoinPlayerNum:
				return
			self.addJoinProtectMembers( player.playerDBID )
			if self.declareWarState == csdefine.NPCEXTPOINT_STATE_FIGHT:
				player.requestGotoNPCExtPointWar( self.index, spaceScriptID, self.occupyPlayerDBID, self.declareTongDBID, self.occupyTongDBID,self.pointType, self.getUname(), self,self.declareTongName,self.declarePlayerDBID,self.declarePlayerName )

	def setNPCPointRestEndTime( self, restEndTime ):
		"""
		设置据点重置时间
		"""
		self.restEndTime = restEndTime
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP:
			spaceEntity.updataNPCPointRestEndTime( self.index, self.restEndTime )

	def setNPCPointReadyEndTime( self, readyEndTime ):
		"""
		设置据点准备时间
		"""
		self.readyEndTime = readyEndTime
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP:
			spaceEntity.updataNPCPointReadyEndTime( self.index, self.readyEndTime )

	def setNPCPointOccupyTongDBID( self, occupyTongDBID ):
		"""
		设置据点占领帮会
		"""
		self.occupyTongDBID = occupyTongDBID
		spaceEntity = self.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_BHZB_STAND_MAP:
			spaceEntity.updataNPCPointOccupyTongDBID( self.index,self.occupyTongDBID )

