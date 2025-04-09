# -*- coding: utf-8 -*-

import Math
import Const
import Define
import csdefine
import csstatus
import KBEngine
import Functions
import csconst
from KBEDebug import *
from ObjectScript.Space.SpaceBase import SpaceBase
from ImpInterface.SpaceEventInterface import SpaceEventInterface
from ImpInterface.SpaceStageInterface import SpaceStageInterface
from ImpInterface.SpaceStatisticsInterface import SpaceStatisticsInterface

class SpacePlane( SpaceBase, SpaceEventInterface, SpaceStageInterface, SpaceStatisticsInterface ):
	def __init__( self ):
		SpaceBase.__init__( self )
		SpaceEventInterface.__init__( self )
		SpaceStageInterface.__init__( self )
		SpaceStatisticsInterface.__init__( self )
		self.spaceLife = 0
		self.isClientShowSpaceLife = 0
		self.startLifeOnInit = False		# 是否初始化时就开始位面倒计时
		self.monsterUseSpaceLevel = 0
		self.bigMapScriptID = "" 	# 位面所在的大地图

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceBase.initData( self, configData )
		self.spaceLife = configData["SpaceData"].get( "spaceLife", 0 ) * 60
		if self.spaceLife == 0:
			self.spaceLife = configData["SpaceData"].get( "spaceLifeSec", 0 )

		spaceEventFile = configData["SpaceData"].get( "eventFile", "" )
		if spaceEventFile:
			self.initSpaceEvents( spaceEventFile )

		spaceStageFile = configData["SpaceData"].get( "stageFile", "" )
		if spaceStageFile:
			self.initSpaceStages( spaceStageFile )
	
		spaceStatisticsFile = configData["SpaceData"].get( "statisticsFile", "" )
		if spaceStatisticsFile:
			self.initSpaceStatistics( spaceStatisticsFile )
		
		self.isClientShowSpaceLife = configData["SpaceData"].get("clientShowSpaceLife", 0)
		self.startLifeOnInit = configData["SpaceData"].get("startLifeOnInit", 0)
		self.monsterUseSpaceLevel = configData["SpaceData"].get("monsterUseSpaceLevel", 0)
		self.isSpaceLifeMoveDown = configData["SpaceData"].get("isSpaceLifeMoveDown",0)  # 应策划要求需要他们控制副本时间的显示位置 详情见JIRA CST-4372

		self.bigMapScriptID = self.scriptID.split("_Planes")[0] 	#位面所在的大地图

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		selfEntity.monsterUseSpaceLevel = self.monsterUseSpaceLevel
		SpaceBase.initEntity( self, selfEntity )
		if self.spaceLife and self.startLifeOnInit:
			self.startSpaceLife( selfEntity )
		
		self.spaceStage_onSpaceInit( selfEntity )
		self.spaceEvent_onSpaceInit( selfEntity )
		self.spaceStatistics_onSpaceInit( selfEntity )

	def isInSameBigMap( self, mapScriptID ):
		"""
		是否在同一大地图
		"""	
		if mapScriptID == self.bigMapScriptID:
			return True
		return False

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( spaceLifeSecond, "closeSpace", () )
		if self.isClientShowSpaceLife:
			selfEntity.lifeTime = self.spaceLife		# 副本时长
			selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
			for e in selfEntity._spaceRoles:
				e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ) )

	def stopSpaceLife( self, selfEntity ):
		"""
		停止计时
		"""
		if selfEntity.lifeTimer > 0:
			selfEntity.popTimer( selfEntity.lifeTimer )
			selfEntity.lifeTimer = 0
		if selfEntity.lifeNotifyTimer > 0:
			selfEntity.popTimer( selfEntity.lifeNotifyTimer )
			selfEntity.lifeNotifyTimer = 0
		
		if self.isClientShowSpaceLife:
			if selfEntity.lifeStopTime > 0:
				selfEntity.lifeTotalStopTime += int(time.time() - selfEntity.lifeStopTime)
			selfEntity.lifeStopTime = time.time()		# 副本计时停止时间
			remainTime = selfEntity.lifeTime - int( selfEntity.lifeStopTime - selfEntity.lifeStartTime ) - selfEntity.lifeTotalStopTime + selfEntity.dynamicTime
			for e in selfEntity._spaceRoles:
				e.client.ShowStopSpaceLife( remainTime )

	def gotoSpaceLife( self, selfEntity ):
		"""
		继续倒计时
		"""
		remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) - selfEntity.lifeTotalStopTime + selfEntity.dynamicTime
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))
				
	def changeSpaceLife( self, selfEntity, dynamicTime ):
		"""
		改变副本计时
		"""
		selfEntity.popTimer( selfEntity.lifeTimer )
		selfEntity.lifeTimer = 0
		
		selfEntity.dynamicTime += dynamicTime
		remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) - selfEntity.lifeTotalStopTime + selfEntity.dynamicTime
		if remainTime >= 0:
			selfEntity.lifeTimer = selfEntity.addTimerCallBack( remainTime, "closeSpace", () )
			if remainTime - Const.SPACE_LIFE_NOTIFY_TIME >= 0:
				selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( remainTime - Const.SPACE_LIFE_NOTIFY_TIME, \
																				"showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
			for e in selfEntity._spaceRoles:
				e.client.ShowSpaceLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() )  )
		else:
			selfEntity.closeSpace()
		
	def showSpaceLifeTime( self, selfEntity, playerRole ):
		"""
		玩家显示副本剩余时间
		"""
		if selfEntity.lifeTime <= 0 or not self.isClientShowSpaceLife:
			return
		
		if selfEntity.lifeStopTime > 0:
			remainTime = selfEntity.lifeTime - int( selfEntity.lifeStopTime - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
			playerRole.client.ShowStopSpaceLife( remainTime )
		else:
			remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
			playerRole.client.ShowSpaceLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() )  )
	
	def onEnter( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家进入位面
		"""
		SpaceBase.onEnter( self, selfEntity, playerRole, packArgs )
		self.showSpaceLifeTime( selfEntity, playerRole )
		if selfEntity.leaveCloseTimer:
			selfEntity.popTimer( selfEntity.leaveCloseTimer )
			selfEntity.leaveCloseTimer = 0
		self.spaceStage_onPlayerEnter( selfEntity, playerRole )
		self.spaceStatistics_onPlayerEnter( selfEntity, playerRole )
#		if playerRole.isInTeam():
#			playerRole.noticeTeamEnterPlane()
		playerRole.addTimerCallBack( 0.2, 'callMonsterFollw',() )

	def onLogin( self, selfEntity, playerRole ):
		"""
		此接口无效
		"""
		pass

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开位面
		"""
		DEBUG_MSG( "Player(%s) leave plane(%s)! reason:%s." % ( playerRole.id, selfEntity.id, packArgs[ "leaveReason" ] ) )
		SpaceBase.onLeave( self, selfEntity, playerRole, packArgs )
		self.spaceStage_onPlayerLeave( selfEntity, playerRole )
		self.spaceStatistics_onPlayerLeave( selfEntity, playerRole )
		playerRole.addTimerCallBack( 0.2, 'callMonsterFollw',() )
		selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( 0.5, "closeSpace", () )

	def onMonsterDie( self, selfEntity, monsterID, monsterScriptID ):
		"""
		怪物死亡
		"""
		self.spaceStage_onMonsterDie( selfEntity, monsterScriptID )
		self.spaceStatistics_onMonsterDie( selfEntity, monsterScriptID )

	def onTriggerBox( self, selfEntity, boxID, boxScriptID ):
		"""
		箱子被触发
		"""
		self.spaceStage_onTriggerBox( selfEntity, boxScriptID )

	def onNPCObjectDestroy( self, selfEntity, enityID, entityScriptID ):
		"""
		NPCObject销毁
		"""
		self.spaceStage_onNPCObjectDestroy( selfEntity, enityID, entityScriptID )

	def onPlayerGetItem( self, selfEntity, playerRole, itemInstID, amount ):
		"""
		玩家获得物品
		"""
		self.spaceStage_onPlayerGetItem( selfEntity, itemInstID, amount )
		self.spaceStatistics_onPlayerGetItem( selfEntity, itemInstID, amount )

	def onPlayerRemoveItem( self, selfEntity, playerRole, itemInstID, amount ):
		"""
		玩家移除物品
		"""
		self.spaceStage_onPlayerRemoveItem( selfEntity, itemInstID, amount )
		self.spaceStatistics_onPlayerRemoveItem( selfEntity, itemInstID, amount )

	def onPlayerUseItem( self, selfEntity, playerRole, itemInstID, amount ):
		"""
		玩家使用物品
		"""
		self.spaceStage_onPlayerUseItem( selfEntity, itemInstID, amount )

	def onPlayerUseTitle( self, selfEntity, playerRole, titleID ):
		"""
		玩家装备称号
		"""
		self.spaceStage_onPlayerUseTitle( selfEntity, titleID )

	def onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue ):
		"""
		副本某条件改变
		@param senderType: AI发的填"AI"，镜头事件发的填"STORY"
		@param senderID: AI发的填entity scriptID，镜头事件发的填镜头ID
		@param conditionKey: 通知ID，string类型
		"""
		self.spaceStage_onConditionChange( selfEntity, senderType, senderID, conditionKey, extraValue )
		self.spaceEvent_onConditionChange( selfEntity, senderType, senderID, conditionKey, extraValue )
		self.spaceStatistics_onConditionChange( selfEntity, senderType, senderID, conditionKey, extraValue )
	
	def onSpaceSuccess( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本通关
		"""
		DEBUG_MSG("Space success! %s" % selfEntity.id)
		self.stopSpaceLife( selfEntity )
		self.spaceEvent_onSpaceSuccess( selfEntity )
	
	def onSpaceFailure( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本失败
		"""
		self.stopSpaceLife( selfEntity )
		self.spaceEvent_onSpaceFailure( selfEntity )
		
	def onSpaceSpawnPointLoadOver( self, selfEntity ):
		"""刷新点加载完成回调"""
		SpaceBase.onSpaceSpawnPointLoadOver( self, selfEntity )
		self.spaceEvent_onSpaceSpawnPointLoadOver( selfEntity )

	def showTimeCountDown( self, selfEntity, statusID, remainTime ):
		"""
		所有玩家显示读秒倒计时
		"""
		for roleCell in selfEntity._spaceRoles:
			roleCell.statusMessage( statusID, remainTime )
			
	def onClickedBtnGotoExitSpace( self, selfEntity, playerRole ):
		"""
		玩家点击退出副本按钮
		"""
		pass

##----------------------------队伍相关-------------------------------
#	def onTeamDisband( self, selfEntity, teamID, memDBIDs ):
#		"""
#		队伍解散
#		必须先将副本与队伍进行绑定(buildSpaceTeamRelation)，否则不会调用副本此接口
#		"""
#		if selfEntity.belongType == csdefine.SPACE_BELONG_TEAM:
#			for roleCell in selfEntity._spaceRoles:
#				if roleCell.playerDBID in memDBIDs:
#					roleCell.remoteCall( "addTimerCallBack", ( 5, "gotoExitSpacePos", () ) )		# 5秒后传送出副本
#					roleCell.statusMessage( csstatus.SPACE_TELEPORT_ON_LEAVE_TEAM, 5)
#
#	def onTeamMemberLeave( self, selfEntity, teamID, playerDBID ):
#		"""
#		玩家离队
#		必须先将副本与队伍进行绑定(buildSpaceTeamRelation)，否则不会调用副本此接口
#		"""
#		if selfEntity.belongType == csdefine.SPACE_BELONG_TEAM:
#			for roleCell in selfEntity._spaceRoles:
#				if roleCell.playerDBID == playerDBID:
#					roleCell.remoteCall( "addTimerCallBack", ( 5, "gotoExitSpacePos", () ) )		# 5秒后传送出副本
#					roleCell.statusMessage( csstatus.SPACE_TELEPORT_ON_LEAVE_TEAM, 5)