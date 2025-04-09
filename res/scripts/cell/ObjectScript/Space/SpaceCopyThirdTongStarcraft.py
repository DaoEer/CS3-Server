# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Functions
import time
import KBEngine
import Const
import KBEMath
import Math
import csstatus
import csconst
import csdefine
import Define

class SpaceCopyThirdTongStarcraft( SpaceCopy ):
	"""
	帮会争霸 第三场
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.limitEnterFieldNumber = 0
		self.enterFieldInfo = []
		self.winIntegral = 0
		self.reviveInfo = [] #[(),()] [红方,蓝方]
		self.successSound = ""
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.limitEnterFieldNumber = configData["SpaceData"].get("limitEnterFieldNumber",0)
		enterPosInfos = configData["SpaceData"].get("enterFieldPos","").split("|")
		enterDirInfos = configData["SpaceData"].get("enterFieldDir","").split("|")
		self.winIntegral = configData["SpaceData"].get( "winIntegral",0 )
		self.endCloseTime = configData["SpaceData"].get("endCloseTime",0)
		self.addIntegral = configData["SpaceData"].get("addIntegral",0)
		self.addIntegralTimer = configData["SpaceData"].get("addIntegralTimer",1.0)
		self.checkAddIntegralRange = configData["SpaceData"].get("checkAddIntegralRange",0.0)
		self.checkAddIntegralTimer = configData["SpaceData"].get("checkAddIntegralTimer",1.0)
		self.redSideAddBuffID = configData["SpaceData"].get("redSideAddBuffID",0)
		self.buleSideAddBuffID = configData["SpaceData"].get("buleSideAddBuffID",0)
		self.successSound = configData["SpaceData"].get("successSound","")
		revivePosInfos = configData["SpaceData"].get("revivePos","").split("|")
		reviveDirInfos = configData["SpaceData"].get("reviveDir","").split("|")
		enterPosList = []
		enterDirList = []
		for enterPosInfo in enterPosInfos:
			pos = Functions.vector3TypeConvert(enterPosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( tuple(pos) )
			enterPosList.append(pos)

		for enterDirInfo in enterDirInfos:
			dir = Functions.vector3TypeConvert(enterDirInfo)
			dir = KBEMath.Unreal2KBEngineDirection( tuple(dir) )
			enterDirList.append(dir)
		for i in range(0,len(enterPosList)):
			self.enterFieldInfo.append( (Math.Vector3(enterPosList[i]), Math.Vector3(enterDirList[i])) )

		revivePosList = []
		reviveDirList = []
		for revivePosInfo in revivePosInfos:
			pos = Functions.vector3TypeConvert(revivePosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( tuple(pos) )
			revivePosList.append(pos)

		for reviveDirInfo in reviveDirInfos:
			dir = Functions.vector3TypeConvert(reviveDirInfo)
			dir = KBEMath.Unreal2KBEngineDirection( tuple(dir) )
			reviveDirList.append(dir)
		for i in range(0,len(revivePosList)):
			self.reviveInfo.append( (Math.Vector3(revivePosList[i]), Math.Vector3(reviveDirList[i])) )
	
	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass
	
	def getLimitEnterFieldNumber( self ):
		"""
		获得进入内场人员限制数量
		"""
		return self.limitEnterFieldNumber

	def getEntrFieldInfoByIndex( self, index ):
		"""
		获得进入内场的坐标和朝向
		"""
		return self.enterFieldInfo[index]

	def getReviveInfoBySide( self, side ):
		"""
		获得某一方的复活点
		"""
		return self.reviveInfo[side]

	def getWinIntegral( self ):
		"""
		"""
		return self.winIntegral

	def onPlayerDie( self, selfEntity, playerID, playerMB ):
		"""
		玩家死亡
		"""
		SpaceCopy.onPlayerDie( self, selfEntity, playerID, playerMB )
		player = KBEngine.entities.get( playerID,None )
		for signUpPlayerDBIDs in selfEntity.tongSignUpPlayerDBIDs.values():
			if player.playerDBID in signUpPlayerDBIDs:
				signUpPlayerDBIDs.remove(player.playerDBID)
				player.reviveOnOrigin()
				player.addTimerCallBack(1.0,"gotoExitSpacePos",())
				break

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		side = packArgs["thirdSide"]
		otherSide = csdefine.TONG_BELONG_RED_SIDE
		if side == csdefine.TONG_BELONG_RED_SIDE:
			otherSide = csdefine.TONG_BELONG_BLUE_SIDE
		selfEntity.warInfos.addThirdTongStarcraftMember( packArgs["tongDBID"], packArgs["tongName"],packArgs["playerDBID"],side,playerRole,packArgs["otherTongDBID"],packArgs["otherTongName"], otherSide)
		selfEntity.notifyClientAllOccupySpellBox( playerRole )
		tongDBID = packArgs["tongDBID"]
		if tongDBID not in selfEntity.tongSide:
			selfEntity.tongSide[tongDBID] = packArgs["thirdSide"]

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		tongObject = selfEntity.warInfos.get(playerRole.tongDBID,None)
		if not tongObject:
			return
		selfEntity.warInfos.addThirdTongStarcraftMember( tongObject.tongDBID, tongObject.tongName,playerRole.playerDBID,tongObject.side,playerRole )
		selfEntity.notifyClientAllOccupySpellBox( playerRole )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )
		if packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_TELEPORT:
			tongObject = selfEntity.warInfos.get(playerRole.tongDBID,None)
			if not tongObject:
				return
			tongObject.removeMember( playerRole.playerDBID )

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		selfEntity.addTimerCallBackForScript(self.spaceLife,"onSpaceLifeEnd",())
		spaceLifeSecond = self.spaceLife
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		#selfEntity.lifeTimer = selfEntity.addTimerCallBack( spaceLifeSecond, "closeSpace", () )
		#selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.CLIENT_ShowThirdTongStarcraftLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()) )

	def showSpaceLifeTime( self, selfEntity, playerRole ):
		"""
		玩家显示副本剩余时间
		"""
		if selfEntity.lifeTime <= 0:
			return

		remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
		if playerRole.getClient():
			playerRole.client.CLIENT_ShowThirdTongStarcraftLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()) )

	def onSpaceLifeEnd( self, selfEntity ):
		"""
		副本时间到达
		"""
		if not selfEntity.winTongDBID:
			self.setWinTong( selfEntity,selfEntity.warInfos.getFirstTong().tongDBID )

	def addTongIntegral( self, selfEntity, tongDBID, value ):
		"""
		"""
		selfEntity.warInfos.addThirdTongStarcraftIntegral(tongDBID, value)
		integral = selfEntity.warInfos.getThirdTongStarcraftIntegral( tongDBID )
		if integral >= self.getWinIntegral() and not selfEntity.winTongDBID:
			self.setWinTong( selfEntity,tongDBID )

	def setWinTong( self, selfEntity,tongDBID ):
		"""
		设置胜利帮会
		"""
		destroyEntity = []
		for entities in selfEntity.getAllEntityMailBoxRecord().values():
			destroyEntity.extend(entities)
		for entity in entities:
			entity.destroySelf()
		selfEntity.winTongDBID = tongDBID
		side = selfEntity.tongSide.get(tongDBID,0)
		tongName = selfEntity.warInfos[selfEntity.winTongDBID].tongName
		for tongDBID in selfEntity.warInfos.getAllTongs():
			members = selfEntity.warInfos[tongDBID].getMembers()
			if tongDBID == selfEntity.winTongDBID:
				for member in members:
					if member.roleMB and member.roleMB.getClient():
						member.roleMB.showMessagePlaySound( self.successSound )
						member.roleMB.client.CLIENT_ShowWinTong( 1 ) #客户端显示“胜”
			else:
				for member in members:
					if member.roleMB and member.roleMB.getClient():
						member.roleMB.client.CLIENT_ShowWinTong( 0 ) #客户端显示“败”
		KBEngine.globalData["TongStarcraftManager"].onThirdTongStarcraftEnd( tongName, selfEntity.camp )
		selfEntity.addTimerCallBack(self.endCloseTime,"closeSpace",())
		self.showTimeCountDown( selfEntity, csstatus.SPACE_CLOSE_NOTIFY, self.endCloseTime )
