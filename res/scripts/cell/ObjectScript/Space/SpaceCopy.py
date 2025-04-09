# -*- coding: utf-8 -*-

import Math
import time
import Const
import Define
import csdefine
import csstatus
import KBEngine
import Functions
import KBEMath
import csconst
import LogDefine
from KBEDebug import *
from MsgLogger import g_logger
from ObjectScript.Space.SpaceBase import SpaceBase
from ImpInterface.SpaceEventInterface import SpaceEventInterface
from ImpInterface.SpaceStageInterface import SpaceStageInterface
from ImpInterface.SpaceStatisticsInterface import SpaceStatisticsInterface
from ImpInterface.SpaceBunchInterface import SpaceBunchInterface
from ImpInterface.SpaceSettlementInterface import SpaceSettlementInterface
from ImpInterface.SpaceStrategyInterface import SpaceStrategyInterface


class SpaceCopy( SpaceBase, SpaceEventInterface, SpaceStageInterface, SpaceStatisticsInterface, SpaceBunchInterface, SpaceSettlementInterface, SpaceStrategyInterface ):
	def __init__( self ):
		SpaceBase.__init__( self )
		SpaceEventInterface.__init__( self )
		SpaceStageInterface.__init__( self )
		SpaceStatisticsInterface.__init__( self )
		SpaceBunchInterface.__init__( self )
		SpaceSettlementInterface.__init__( self )
		SpaceStrategyInterface.__init__( self )
		self.startLifeOnInit = True		# 是否初始化时就开始副本倒计时
		self.spaceLife = 0
		self._enterPos = Math.Vector3(0.0, 0.0, 0.0)
		self._enterDir = Math.Vector3(0.0, 0.0, 0.0)
		self.monsterUseSpaceLevel = 0
		self.spaceStrategyFile = ""
		self.forbidJumpSkillIDs = ""

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceBase.initData( self, configData )
		SpaceBunchInterface.initData( self, configData )
		SpaceSettlementInterface.initData( self, configData )
		self.spaceLife = configData["SpaceData"].get( "spaceLife", 0 ) * 60
		if self.spaceLife == 0:
			self.spaceLife = configData["SpaceData"].get( "spaceLifeSec", 0 )

		posStr = configData["SpaceData"].get( "enterPosition", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._enterPos = KBEMath.Unreal2KBEnginePosition( pos )

		dirStr = configData["SpaceData"].get( "enterDirection", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._enterDir = KBEMath.Unreal2KBEngineDirection( dir )

		spaceEventFile = configData["SpaceData"].get( "eventFile", "" )
		if spaceEventFile:
			self.initSpaceEvents( spaceEventFile )

		spaceStageFile = configData["SpaceData"].get( "stageFile", "" )
		if spaceStageFile:
			self.initSpaceStages( spaceStageFile )
			
		spaceStatisticsFile = configData["SpaceData"].get( "statisticsFile", "" )
		if spaceStatisticsFile:
			self.initSpaceStatistics( spaceStatisticsFile )

		self.spaceStrategyFile = configData["SpaceData"].get( "strategyFile", "" )
		if self.spaceStrategyFile:
			self.initSpaceStrategy( self.spaceStrategyFile )

		self.clientUseCharacterMovment = configData["SpaceData"].get( "clientUseCharacterMovment", 0 )
		
		
		self.startLifeOnInit = configData["SpaceData"].get("startLifeOnInit", 1)
		self.monsterUseSpaceLevel = configData["SpaceData"].get("monsterUseSpaceLevel", 0)
		self.isSpaceLifeMoveDown = configData["SpaceData"].get("isSpaceLifeMoveDown",0)  # 应策划要求需要他们控制副本时间的显示位置 详情见JIRA CST-4372
		self.logoutCloseTime = configData["SpaceData"].get( "logoutCloseTime", 300 )
		
		self.forbidJumpSkillIDs = configData["SpaceData"].get("forbidJumpSkillIDs", "")
		#下面的代码仅仅是为了测试技能有没有配置错误，避免客户端崩溃
		if self.forbidJumpSkillIDs:
			for skillID in self.forbidJumpSkillIDs.split("|"):
				id = int(skillID)
	
	def getEnterPosInfo( self ):
		return ( self._enterPos, self._enterDir )

	def getSpaceLife( self ):
		"""
		获得副本生命时间
		"""
		return self.spaceLife

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceBase.initEntity( self, selfEntity )
		if self.spaceLife and self.startLifeOnInit:
			self.startSpaceLife( selfEntity )
		selfEntity.monsterUseSpaceLevel = self.monsterUseSpaceLevel
		
		self.spaceStage_onSpaceInit( selfEntity )
		self.spaceEvent_onSpaceInit( selfEntity )
		self.spaceBunch_onSpaceInit( selfEntity )
		self.spaceStatistics_onSpaceInit( selfEntity )
		
	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( spaceLifeSecond, "closeSpace", () )
		if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		else:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))

	def stopSpaceLife( self, selfEntity ):
		"""
		停止计时
		"""
		if selfEntity.lifeTime <= 0:
			return
		
		selfEntity.lifeStopTime = time.time()		# 副本计时停止时间
		selfEntity.popTimer( selfEntity.lifeTimer )
		selfEntity.lifeTimer = 0
		selfEntity.popTimer( selfEntity.lifeNotifyTimer )
		selfEntity.lifeNotifyTimer = 0
		
		remainTime = selfEntity.lifeTime - int( selfEntity.lifeStopTime - selfEntity.lifeStartTime ) - selfEntity.lifeTotalStopTime + selfEntity.dynamicTime
		for e in selfEntity._spaceRoles:
			e.client.ShowStopSpaceLife( remainTime )

	def gotoSpaceLife( self, selfEntity ):
		"""
		继续倒计时
		"""
		if selfEntity.lifeStopTime > 0:
			selfEntity.lifeTotalStopTime += int(time.time() - selfEntity.lifeStopTime)
		remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) - selfEntity.lifeTotalStopTime + selfEntity.dynamicTime
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))

			
	def changeSpaceLife( self, selfEntity, dynamicTime ):
		"""
		改变计时
		"""
		selfEntity.popTimer( selfEntity.lifeTimer )
		selfEntity.lifeTimer = 0
		selfEntity.popTimer( selfEntity.lifeNotifyTimer )
		selfEntity.lifeNotifyTimer = 0
		
		selfEntity.dynamicTime += dynamicTime
		remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) - selfEntity.lifeTotalStopTime + selfEntity.dynamicTime
		if remainTime >= 0:
			selfEntity.lifeTimer = selfEntity.addTimerCallBack( remainTime, "closeSpace", () )
			if remainTime - Const.SPACE_LIFE_NOTIFY_TIME >= 0:
				if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
					selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( remainTime - Const.SPACE_LIFE_NOTIFY_TIME, \
																				"showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
				else:
					selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( remainTime - Const.SPACE_LIFE_NOTIFY_TIME, \
																				"showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
			for e in selfEntity._spaceRoles:
				e.client.ShowSpaceLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ) )
		else:
			selfEntity.closeSpace()

	def showSpaceLifeTime( self, selfEntity, playerRole ):
		"""
		玩家显示副本剩余时间
		"""
		if selfEntity.lifeTime <= 0:
			return
		
		if selfEntity.lifeStopTime > 0:
			remainTime = selfEntity.lifeTime - int( selfEntity.lifeStopTime - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
			playerRole.client.ShowStopSpaceLife( remainTime )
		else:
			remainTime = selfEntity.lifeTime - int( time.time() - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
			if playerRole.getClient():
				playerRole.client.ShowSpaceLife( str(remainTime * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()),  self.isSpaceLifeMoveDown,str( Functions.getTime() ) )

	def beforeDestroy( self, selfEntity ):
		"""
		销毁前做一些事
		"""
		SpaceBase.beforeDestroy( self, selfEntity )
		self.spaceBunch_onSpaceDestroy( selfEntity )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceBase.onEnter( self, selfEntity, playerRole, packArgs )
		self.showSpaceLifeTime( selfEntity, playerRole )
		if selfEntity.leaveCloseTimer:
			selfEntity.popTimer( selfEntity.leaveCloseTimer )
			selfEntity.leaveCloseTimer = 0
		self.spaceStage_onPlayerEnter( selfEntity, playerRole )
		self.spaceSettlement_onPlayerEnter( selfEntity, playerRole.base )
		self.spaceBunch_onPlayerEnter( selfEntity, playerRole.base, packArgs["playerDBID"] )
		self.spaceStatistics_onPlayerEnter( selfEntity, playerRole )
		if self.spaceStrategyFile:
			self.spaceStrategy_onPlayerEnter( selfEntity, playerRole, self.spaceStrategyFile )
		if self.clientUseCharacterMovment:
			if playerRole.getClient():
				playerRole.client.ChangeMovementMode(self.clientUseCharacterMovment)
			
		if self.forbidJumpSkillIDs and playerRole and playerRole.client: #禁用三段跳
			playerRole.client.CLIENT_SetForbidJumpSkillIDs(self.forbidJumpSkillIDs)
		
		#添加活动、副本参与日志
		g_logger.actCopyJoin(self.getSpaceType(), self.getSpaceName(), playerRole.playerDBID, playerRole.getName())

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceBase.onLogin( self, selfEntity, playerRole )
		self.showSpaceLifeTime( selfEntity, playerRole )
		if selfEntity.leaveCloseTimer:
			selfEntity.popTimer( selfEntity.leaveCloseTimer )
			selfEntity.leaveCloseTimer = 0
		self.spaceStage_onPlayerEnter( selfEntity, playerRole )
		self.spaceSettlement_onPlayerEnter( selfEntity, playerRole.base )
		if self.spaceStrategyFile:
			self.spaceStrategy_onPlayerEnter( selfEntity, playerRole, self.spaceStrategyFile )
		if self.clientUseCharacterMovment:
			if playerRole.getClient():
				playerRole.client.ChangeMovementMode(self.clientUseCharacterMovment)
				
		if self.forbidJumpSkillIDs and playerRole and playerRole.client: #禁用三段跳
			playerRole.client.CLIENT_SetForbidJumpSkillIDs(self.forbidJumpSkillIDs)

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		DEBUG_MSG( "Player(%s) leave space(%s)! reason:%s." % ( playerRole.id, selfEntity.id, packArgs[ "leaveReason" ] ) )
		SpaceBase.onLeave( self, selfEntity, playerRole, packArgs )
		if playerRole.getClient():
			playerRole.client.HideSpaceLife()
		if not selfEntity.getSpaceRoleNum():
			self.onLastPlayerLeave( selfEntity, playerRole, packArgs )
		self.spaceStage_onPlayerLeave( selfEntity, playerRole )
		self.spaceStatistics_onPlayerLeave( selfEntity, playerRole )
		self.spaceSettlement_onPlayerLeave( selfEntity, playerRole.base )
		if self.clientUseCharacterMovment:
			if playerRole.getClient():
				playerRole.client.ChangeMovementMode(0)
		
		#解除禁用三段跳
		if playerRole and playerRole.client:
			playerRole.client.CLIENT_SetForbidJumpSkillIDs("")

	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		if selfEntity.belongType == csdefine.SPACE_BELONG_PERSON and packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_LOGOUT:		# 单人下线
			selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( self.logoutCloseTime, "closeSpace", () )
		elif selfEntity.belongType == csdefine.SPACE_BELONG_PERSON and packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_TELEPORT:	# 单人传送
			selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( 10, "closeSpace", () )
		elif selfEntity.belongType == csdefine.SPACE_BELONG_TEAM and packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_LOGOUT:		# 队伍下线
			selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( 10, "closeSpace", () )
		elif selfEntity.belongType == csdefine.SPACE_BELONG_TEAM and packArgs[ "leaveReason" ] == Define.LEAVE_SPACE_REASON_TELEPORT:	# 队伍传送
			selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( 10, "closeSpace", () )

	def showTimeCountDown( self, selfEntity, statusID, remainTime ):
		"""
		所有玩家显示读秒倒计时
		"""
		for roleCell in selfEntity._spaceRoles:
			roleCell.statusMessage( statusID, remainTime )

	def onPlayerDie( self, selfEntity, playerID, playerMB ):
		"""
		玩家死亡
		"""
		self.spaceSettlement_onPlayerDie( selfEntity )
		self.spaceSettlement_onPlayerDie6369( selfEntity )

	def onMonsterDie( self, selfEntity, monsterID, monsterScriptID ):
		"""
		怪物死亡
		"""
		self.spaceStage_onMonsterDie( selfEntity, monsterScriptID )
		self.spaceStatistics_onMonsterDie( selfEntity, monsterScriptID )
		self.spaceStrategy_onMonsterDie( selfEntity,monsterScriptID )

	def onMonsterHPChanged( self, selfEntity, monsterEntity ):
		"""
		怪物血量改变
		"""
		self.spaceStrategy_onMonsterHPChanged( selfEntity, monsterEntity )

	def onTriggerBox( self, selfEntity, boxID, boxScriptID ):
		"""
		箱子被触发
		"""
		self.spaceStage_onTriggerBox( selfEntity, boxScriptID )
		self.spaceSettlement_onTriggerBox( selfEntity, boxScriptID )

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
		self.spaceStatistics_onConditionChange( selfEntity, senderType, senderID, conditionKey, extraValue )
		self.spaceEvent_onConditionChange( selfEntity, senderType, senderID, conditionKey, extraValue )
	
	def onSpaceSuccess( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本通关
		isShowTimeCountDown 是否显示倒计时提示 见JIRA-3404
		"""
		DEBUG_MSG("Space success! %s" % selfEntity.id)
		self.stopSpaceLife( selfEntity )
		self.spaceEvent_onSpaceSuccess( selfEntity )
		self.spaceBunch_onSpaceSuccess( selfEntity )
		self.spaceSettlement_onSpaceSuccess( selfEntity )	#必须在stopSpaceLife后调用
		selfEntity.addTimerCallBackForScript(1.0,"spaceSettlement_onSpaceSuccess6369",())
		if isShowTimeCountDown:
			selfEntity.addTimerCallBack( 60, "closeSpace", () )
			if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
				selfEntity.addTimerCallBackForScript( 50, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, 10 ) )
			else:
				selfEntity.addTimerCallBackForScript( 50, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, 10 ) )
			for roleCell in selfEntity._spaceRoles:
				roleCell.statusMessage( csstatus.SPACE_SUCCESS_TELEPORT,60 )
	
	def onSpaceFailure( self, selfEntity, isShowTimeCountDown = True ):
		"""
		副本失败
		isShowTimeCountDown 是否显示倒计时提示 见JIRA-3404
		"""
		self.stopSpaceLife( selfEntity )
		self.spaceEvent_onSpaceFailure( selfEntity )
		self.spaceSettlement_onSpaceFailure( selfEntity )
		if isShowTimeCountDown:
			selfEntity.addTimerCallBack( 60, "closeSpace", () )
			if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
				selfEntity.addTimerCallBackForScript( 50, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, 10 ) )
			else:
				selfEntity.addTimerCallBackForScript( 50, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, 10 ) )
			for roleCell in selfEntity._spaceRoles:
				roleCell.statusMessage( csstatus.SPACE_FAILUER_TELEPORT,60 )
		#添加副本失败日志
		for e in selfEntity._spaceRoles:
			startTime = int(selfEntity.lifeStartTime)
			costTime = int(time.time() - selfEntity.lifeStartTime)
			g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, e.accountDBID, e.playerDBID, e.getLevel(), "", "", startTime, costTime, LogDefine.ACTIVE_STATE_TYPE_FAIL, self.scriptID)
			
	def onSpaceSpawnPointLoadOver( self, selfEntity ):
		"""刷新点加载完成回调"""
		SpaceBase.onSpaceSpawnPointLoadOver(self, selfEntity)
		self.spaceEvent_onSpaceSpawnPointLoadOver( selfEntity )

	def onAddPotential( self, selfEntity, playerRole, potential, reason):
		"""
		增加潜能
		"""
		self.spaceSettlement_onAddPotential( selfEntity, playerRole, potential )
		
	def onAddExp( self, selfEntity, playerRole, exp, reason):
		"""
		增加经验
		"""
		self.spaceSettlement_onAddExp( selfEntity, playerRole, exp )
		
	def onClickedBtnGotoExitSpace( self, selfEntity, playerRole ):
		"""
		玩家点击退出副本按钮
		"""
		pass

#----------------------------队伍相关-------------------------------
	def onTeamDisband( self, selfEntity, teamID, memDBIDs ):
		"""
		队伍解散
		必须先将副本与队伍进行绑定(buildSpaceTeamRelation)，否则不会调用副本此接口
		"""
		if selfEntity.belongType == csdefine.SPACE_BELONG_TEAM:
			for roleCell in selfEntity._spaceRoles:
				if roleCell.playerDBID in memDBIDs:
					roleCell.remoteCall( "addTimerCallBack", ( 5, "gotoExitSpacePos", () ) )		# 5秒后传送出副本
					roleCell.statusMessage( csstatus.SPACE_TELEPORT_ON_LEAVE_TEAM, 5)

	def onTeamMemberLeave( self, selfEntity, teamID, playerDBID ):
		"""
		玩家离队
		必须先将副本与队伍进行绑定(buildSpaceTeamRelation)，否则不会调用副本此接口
		"""
		if selfEntity.belongType == csdefine.SPACE_BELONG_TEAM:
			for roleCell in selfEntity._spaceRoles:
				if roleCell.playerDBID == playerDBID:
					roleCell.remoteCall( "addTimerCallBack", ( 5, "gotoExitSpacePos", () ) )		# 5秒后传送出副本
					roleCell.statusMessage( csstatus.SPACE_TELEPORT_ON_LEAVE_TEAM, 5)
					
#-----------------------------------环任务副本相关-----------------------------------
	def onLoopQuestSpaceFailure( self, selfEntity, countDown ):
		"""
		环任务副本失败
		"""
		self.spaceEvent_onSpaceFailure( selfEntity )
		endTime = str( countDown * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime() )
		for e in selfEntity._spaceRoles:
			e.client.ShowLoopQuestSpaceFailure( endTime )
			KBEngine.globalData["RingTaskSpaceMgr"].onChildSceneFailure( str(e.playerDBID) )
			
			#添加环任务失败日志
			startTime = int(selfEntity.lifeStartTime)
			costTime = int(time.time() - selfEntity.lifeStartTime)
			g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, e.accountDBID, e.playerDBID, e.getLevel(), "", "", startTime, costTime, LogDefine.ACTIVE_STATE_TYPE_FAIL, self.scriptID)
			
		selfEntity.addTimerCallBack( countDown, "closeSpace", () )

	def onLoopQuestSpaceSuccess( self, selfEntity, countDown ):
		"""
		副本通关
		isShowTimeCountDown 是否显示倒计时提示 见JIRA-3404
		"""
		self.spaceEvent_onSpaceSuccess( selfEntity )
		for e in selfEntity._spaceRoles:
			KBEngine.globalData["RingTaskSpaceMgr"].onChildSceneSuccess( str(e.playerDBID) )
		#selfEntity.addTimerCallBack( countDown, "closeSpace", () )
		
		
	def isSpaceCopy(self):
		"""
		是否是副本地图（GM使用）
		"""
		return True