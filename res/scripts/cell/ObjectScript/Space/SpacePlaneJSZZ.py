# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from ObjectScript.Space.SpacePlane import SpacePlane
import Const
import Math

class SpacePlaneJSZZ( SpacePlane ):
	"""
	CST-7419 金树种子
	"""
	def __init__( self ):
		SpacePlane.__init__( self )
		self.treeScriptID = ""
		self.roleReviveTime = 5.0
		self.delyCloseSpaceTime = 0.0

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpacePlane.initData( self, configData )
		self.treeScriptID = configData["SpaceData"].get("treeScriptID","")
		self.delyCloseSpaceTime = configData["SpaceData"].get("delyCloseSpaceTime",0.0)

	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass
		
	def onEnter( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家进入位面
		"""
		selfEntity.calculateWallPosList( packArgs["centerPos"], packArgs["radius"] )
		if playerRole.getClient():
			playerRole.client.CLIENT_ShowJSZZPlaneWall( self.scriptID ,selfEntity.wallPosList )
		SpacePlane.onEnter( self, selfEntity, playerRole, packArgs )
		selfEntity.createEntityByScriptID( self.treeScriptID,packArgs["centerPos"],Math.Vector3(0,0,0),{} )

	def onLogin( self, selfEntity, playerRole ):
		"""
		此接口无效
		"""
		self.showSpaceLifeTime( selfEntity, playerRole )
		if selfEntity.leaveCloseTimer:
			selfEntity.popTimer( selfEntity.leaveCloseTimer )
			selfEntity.leaveCloseTimer = 0
		self.spaceStage_onPlayerEnter( selfEntity, playerRole )
		self.spaceStatistics_onPlayerEnter( selfEntity, playerRole )
		playerRole.addTimerCallBack( 0.2, 'callMonsterFollw',() )
		if playerRole.getClient():
			playerRole.client.CLIENT_ShowJSZZPlaneWall( self.scriptID ,selfEntity.wallPosList )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开位面
		"""
		from ObjectScript.Space.SpaceBase import SpaceBase
		SpaceBase.onLeave( self, selfEntity, playerRole, packArgs )
		if playerRole.getClient():
			playerRole.client.HideSpaceLife()
		self.spaceStage_onPlayerLeave( selfEntity, playerRole )
		self.spaceStatistics_onPlayerLeave( selfEntity, playerRole )
		playerRole.addTimerCallBack( 0.2, 'callMonsterFollw',() )


	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		packDict = SpacePlane.getPackDomainData( self, playerEntity, args )
		if playerEntity.hasQuest( Const.JSZZ_QUEST_ID ):
			packDict["centerPos"] = playerEntity.position
			packDict["radius"] = playerEntity.questTable[Const.JSZZ_QUEST_ID].getThirdTaskPlaneRadius()
		return packDict

	def onPlayerDie( self, selfEntity, playerID, playerMB ):
		"""
		"""
		selfEntity.addTimerCallBackForScript( self.roleReviveTime, "onRoleRevive",(playerID,) )

	def onRoleRevive( self, selfEntity, playerID ):
		player = KBEngine.entities.get(playerID,None)
		if not player:
			return
		treeEntities = selfEntity.getEntityMailBoxRecord( self.treeScriptID )
		if not len(treeEntities):
			return
		player.position = treeEntities[0].position
		player.reviveOnOrigin()

	def getReviveToExitInfo( self, playerRole ):
		return ( self.bigMapScriptID, playerRole.position, playerRole.direction )

	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		if packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_TELEPORT:
			selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( 0.5, "destroySelf", () )

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( spaceLifeSecond + self.delyCloseSpaceTime, "closeSpace", () )
		if self.isClientShowSpaceLife:
			selfEntity.lifeTime = self.spaceLife		# 副本时长
			selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
			for e in selfEntity._spaceRoles:
				e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown, str( Functions.getTime() ) )

		selfEntity.addTimerCallBackForScript(spaceLifeSecond,"onSpaceLifeEnd",())

	def onSpaceLifeEnd( self, selfEntity ):
		"""
		"""
		self.showJSZZSettlement( selfEntity,1 )

	def onSpaceSuccess( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本通关
		"""
		SpacePlane.onSpaceSuccess( self, selfEntity, isShowTimeCountDown )
		self.showJSZZSettlement( selfEntity,0 )

	def onSpaceSuccess( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本通关
		"""
		SpacePlane.onSpaceSuccess( self, selfEntity, isShowTimeCountDown )
		self.showJSZZSettlement( selfEntity,0 )

	def showJSZZSettlement( self, selfEntity, isSpaceLifeEnd ):
		"""
		显示结算界面
		"""
		rewardMoney = 0
		treeEntities = selfEntity.getEntityMailBoxRecord( self.treeScriptID )
		if len(treeEntities):
			rewardMoney = int(treeEntities[0].HP * selfEntity.curStageRewardMoney)
		for role in selfEntity._spaceRoles:
			role.abandonQuest( Const.JSZZ_QUEST_ID )
			if role.getClient():
				role.client.ShowJSZZSettlement(rewardMoney)

		if not isSpaceLifeEnd:
			selfEntity.addTimerCallBack(self.delyCloseSpaceTime,"closeSpace",())

 
