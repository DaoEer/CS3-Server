# -*- coding: utf-8 -*-
# 副本事件接口
import imp
import time
import Define
import Functions
from KBEDebug import *
from SmartImport import smartImport
from ConfigObject.SpaceEvent.SpaceEventBase.SpaceEvent import SpaceEvent
from SpaceEvent.SpaceEvents import Datas as g_spaceEventDatas

class SpaceEventInterface:
	def __init__( self ):
		self.events = {}

	def initSpaceEvents( self, fileName ):
		"""
		加载阶段内容配置
		@type	stage_file_path:	string
		@param	stage_file_path:	file path
		"""
		try:
			mod = smartImport( "GameObject.SpaceObject.SpaceEventFile.%s"%fileName )
			mod = imp.reload(mod)
			configData = mod.Datas
		except:
			ERROR_MSG( "Space(%s) event file(%s) is not exist!"%( self.scriptID, fileName ) )
			return
		
		for eventType, eventDatas in configData.items() :
			for data in eventDatas:
				event = SpaceEvent()
				event.init( fileName,data["id"], eventType, data )
					
				self.__addEvent( event )

	def __addEvent( self, event ):
		"""
		添加事件
		"""
		if event.eventType not in self.events:
			self.events[ event.eventType ] = []
		self.events[ event.eventType ].append( event )

	def npcObjectBindSpaceEvent( self, monster ):
		"""
		怪物绑定副本事件
		"""
		monster.clearListenSpaceEvents()	#先清空一下
		for eventType, eventList in self.events.items():
			if g_spaceEventDatas[ eventType ][ "triggerType" ] == Define.SPACE_EVENT_TRIGGER_TYPE_MONSTER:
				for event in eventList:
					event.bindForTrigger( self.scriptID, monster )

	def roleBindSpaceEvent( self, player ):
		"""
		玩家绑定副本事件
		"""
		for eventType, eventList in self.events.items():
			if g_spaceEventDatas[ eventType ][ "triggerType" ] == Define.SPACE_EVENT_TRIGGER_TYPE_ROLE:
				for event in eventList:
					event.bindForTrigger( self.scriptID, player )

	def triggerEvent( self, selfEntity, eventType, eventIDs, triggerID, eventParams ):
		"""
		怪物或玩家触发副本事件
		"""
		DEBUG_MSG("Be trigger space event! space id:%s. "%selfEntity.id, eventType, eventIDs, triggerID, eventParams)
		for event in self.events[ eventType ]:
			if event.id not in eventIDs:
				continue
			if not event.canLoop and self.isSpaceEventHasDo( selfEntity, eventType, event.id ):
				continue
			if event.checkSpaceCon( selfEntity, eventParams ):
				if not event.canLoop:
					self.addSpaceEventRecord( selfEntity, eventType, event.id )
				event.do( selfEntity, triggerID, eventParams )
				DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, triggerID, "怪物/玩家结束触发副本事件：event(Type:%d, id:%d)" %(eventType, event.id))

	def triggerEventBySelf( self, selfEntity, eventType, eventParams ):
		"""
		副本自身触发副本事件
		"""
		DEBUG_MSG("Be trigger space event by self! space id:%s. "%selfEntity.id, eventType, eventParams)
		if eventType not in self.events:
			return
		for event in self.events[ eventType ]:
			if not event.canLoop and self.isSpaceEventHasDo( selfEntity, eventType, event.id ):
				continue
			if event.checkTriggerCon( selfEntity, eventParams ) and event.checkSpaceCon( selfEntity, eventParams ):
				event.do( selfEntity, selfEntity.id, eventParams )
				DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身结束触发副本事件：event(Type:%d, id:%d)" %(eventType, event.id))
				if not event.canLoop:
					self.addSpaceEventRecord( selfEntity, eventType, event.id )

	def addSpaceEventRecord( self, selfEntity, eventType, eventID ):
		"""
		记录不能重复执行的事件
		"""
		if eventType not in selfEntity.spaceEventRecord:
			selfEntity.spaceEventRecord[ eventType ] = [ eventID ]
		else:
			selfEntity.spaceEventRecord[ eventType ].append( eventID )

	def removeSpaceEventRecord( self, selfEntity, eventType ):
		"""
		移除记录不能重复执行的某事件
		"""
		if eventType in selfEntity.spaceEventRecord:
			selfEntity.spaceEventRecord.pop(eventType)

	def isSpaceEventHasDo( self, selfEntity, eventType, eventID ):
		"""
		某事件是否已执行
		"""
		return eventID in selfEntity.spaceEventRecord.get( eventType, [] )

	def doGivenSpaceEventAction( self, selfEntity, eventType, eventID, actionIndex, triggerID, eventParams ):
		"""
		执行某事件某行为
		"""
		for event in self.events[ eventType ]:
			if event.id != eventID:
				continue
			event.doGivenAction( selfEntity, actionIndex, triggerID, eventParams )

	#------------------------------timer处理---------------------------------
	def spaceEvent_addTimer( self, selfEntity, timerKey, time, isLoop ):
		"""
		添加timer
		"""
		if not isLoop:
			timerID = selfEntity.addTimerCallBackForScript( time, "spaceEvent_onTimer", ( timerKey, ) )
		else:
			timerID = selfEntity.addTimerRepeatForScript( time, "spaceEvent_onTimer", ( timerKey, ) )
		selfEntity.spaceEventTimers[ timerKey ] = ( timerID, isLoop, time, Functions.getTime())
		
	def spaceEvent_onTimer( self, selfEntity, timerKey ):
		"""
		timer到达
		"""
		if timerKey in selfEntity.spaceEventTimers:
			tupleData = selfEntity.spaceEventTimers[ timerKey ]
			isLoop = tupleData[1]
			DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(timer到达)：event(Type:%d, isLoop:%s)" %(Define.SPACE_EVENT_TYPE_SPACE_ON_TIMER, isLoop))
			self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPACE_ON_TIMER, { "timerKey": timerKey } )
			if not isLoop:
				selfEntity.spaceEventTimers.pop( timerKey )

	def spaceEvent_cancelTimer( self, selfEntity, timerKey ):
		"""
		取消timer
		"""
		if timerKey in selfEntity.spaceEventTimers:
			tupleData = selfEntity.spaceEventTimers[ timerKey ]
			timerID = tupleData[0]
			selfEntity.popTimer( timerID )
			selfEntity.spaceEventTimers.pop( timerKey )

	#--------------------------------计数功能---------------------------------
	def spaceEvent_addCount( self, selfEntity, countKey, addValue ):
		"""
		增加某计数
		"""
		if countKey not in selfEntity.spaceEventCountInt:
			selfEntity.spaceEventCountInt[ countKey ] = addValue
		else:
			selfEntity.spaceEventCountInt[ countKey ] += addValue
		DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(增加某计数)：event(Type:%d)" %(Define.SPACE_EVENT_TYPE_SPACE_COUNT_CHANGE))
		self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPACE_COUNT_CHANGE, { "countKey": countKey, "newValue": selfEntity.spaceEventCountInt[ countKey ], "addValue":addValue} )

	#------------------- 各种副本事件触发接口-----------------------
	def spaceEvent_onSpaceInit( self, selfEntity ):
		"""
		副本初始化
		"""
		DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(副本初始化)：event(Type:%d)" %(Define.SPACE_EVENT_TYPE_SPACE_ON_INIT))
		self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPACE_ON_INIT, {} )

	def spaceEvent_onStageStart( self, selfEntity, stageIndex ):
		"""
		副本阶段开始
		"""
		DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(某阶段开始)：event(Type:%d stageIndex:%s)" %(Define.SPACE_EVENT_TYPE_SPACE_STAGE_START, stageIndex))
		self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPACE_STAGE_START, { "stageIndex": stageIndex } )

	def spaceEvent_onStageComplete( self, selfEntity, stageIndex ):
		"""
		副本某阶段完成
		"""
		DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(某阶段完成)：event(Type:%d stageIndex:%s)" %(Define.SPACE_EVENT_TYPE_SPACE_STAGE_COMPLETE, stageIndex))
		self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPACE_STAGE_COMPLETE, { "stageIndex": stageIndex } )

	def spaceEvent_onStageTaskComplete( self, selfEntity, stageIndex, taskIndex ):
		"""
		副本某阶段目标完成
		"""
		DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(某阶段目标完成)：event(Type:%d stageIndex:%s taskIndex:%s)" %(Define.SPACE_EVENT_TYPE_SPACE_ON_INIT, stageIndex, taskIndex))
		self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPACE_STAGE_TASK_COMPLETE, {"stageIndex": stageIndex,"taskIndex":taskIndex} )

	def spaceEvent_onSpaceSuccess( self, selfEntity ):
		"""
		"""
		DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(副本通关)：event(Type:%d)" %(Define.SPACE_EVENT_TYPE_SPACE_ON_SUCCESS))
		self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPACE_ON_SUCCESS, {} )

	def spaceEvent_onSpaceFailure( self, selfEntity ):
		"""
		"""
		DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(副本通关失败)：event(Type:%d)" %(Define.SPACE_EVENT_TYPE_SPACE_ON_SUCCESS))
		self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPACE_ON_FAILURE, {} )

	def spaceEvent_onConditionChange( self, selfEntity, senderType, senderID, conditionKey, extraValue ):
		"""
		"""
		DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(副本条件改变)：event(Type:%d, conditionKey:%s)" %(Define.SPACE_EVENT_TYPE_SPACE_CON_CHANGE, conditionKey))
		self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPACE_CON_CHANGE, { "senderType": senderType, "senderID": senderID, "conditionKey": conditionKey, "extraValue": extraValue } )
	
	def spaceEvent_onSpaceStatisticsFinish( self, selfEntity, entryIndex ):
		"""
		副本某个统计完成
		"""
		DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(某个统计完成)：event(Type:%d, entryIndex:%s)" %(Define.SPACE_EVENT_TYPE_SPACE_STATISTICS_COMPLETE, entryIndex))
		self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPACE_STATISTICS_COMPLETE, { "entryIndex": entryIndex } )
		
	def spaceEvent_onSpaceSpawnPointLoadOver( self, selfEntity ):
		"""
		刷新点加载完成
		"""
		DEBUG_MSG_FOR_SPACECOPY_PLOT(selfEntity, selfEntity.id, "副本自身触发(刷新点加载完成)：event(Type:%d)" %(Define.SPACE_EVENT_TYPE_SPAWN_POINT_LOAD_OVER))
		self.triggerEventBySelf( selfEntity, Define.SPACE_EVENT_TYPE_SPAWN_POINT_LOAD_OVER, {} )
	
	#-------------------玩家登陆其他地图事件-----------------------
	def spaceEvent_onLoginDiffSpace( self, roleEntity ):
		"""
		玩家登陆其他地图
		"""
		#触发玩家登陆其他地图事件，此事件中配置一些大退、小退、服务器崩溃等非传送离开副本的情况都需要执行的行为，如重置玩家任务、移除buff等。
		eventType = Define.SPACE_EVENT_TYPE_ROLE_LOGIN_DIFF_SPACE
		if eventType not in self.events:
			return
		eventParams = {}
		for event in self.events[ eventType ]:
			if event.checkTriggerCon( roleEntity, eventParams ):		#还是要判断触发条件的
				event.doOnRoleLoginDiffSpace( roleEntity, eventParams )
