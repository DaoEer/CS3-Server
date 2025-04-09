# -*- coding: utf-8 -*-

from ConfigObject.MonsterAI.AIBase import AIInstance
from ConfigObject.MonsterAI.AIBase import NewAIInstance
from ConfigObject.MonsterAI import AIEvents
import KBEDebug
import Const
import csdefine
import ECBProximityDefine

class AISubState:
	#状态AI
	def __init__( self, subID ):
		self._subID = subID	#子状态ID
		self._tick = 2.0
		self._initiativeAreaXZ = "0.0"				# 主动反应区域陷阱
		self.isServerInitiativeTrap = False			# 默认使用客户端陷阱
		self.initiativeTrapType = 0					# 陷阱类型
		self.initiativeTrapShape = csdefine.TRAP_SHAPE_SQUARE		# 主动反应陷阱形状：默认为方形（配为服务器端陷阱时可以减少消耗）
		self._AIInstances = []
		self._AIEventInfos = {}
		self._subHoldEffectIDs = []
		self._newAIInstances = [] 				#新版AI实例
		self._newAIEventInfos = {}

	def initData( self, stateSection ):
		#加载子状态持有效果ID
		self._subHoldEffectIDs = stateSection["subHoldEffectIDs"]

		#状态AI循环
		self._tick = stateSection[ "tickTimer" ]
		
		self._initiativeAreaXZ = stateSection[ "initiativeAreaXZ" ]
		self.initiativeTrapType = stateSection[ "initiativeTrapType" ]

		if self.initiativeTrapType:
			self.isServerInitiativeTrap = True
		
		if "initiativeTrapShape" in stateSection:
			if stateSection["initiativeTrapShape"] not in csdefine.TRAP_SHAPE_LIST:
				KBEDebug.ERROR_MSG("Initiative trap shape error! %i, %i" % (self._subID, stateSection["initiativeTrapShape"]))
			else:
				self.initiativeTrapShape = stateSection["initiativeTrapShape"]


		if "newStatesAI" in stateSection:
			for instSection in stateSection[ "newStatesAI" ]:
				AIID = instSection["id"]
				eID = instSection["EID"]
				AIInstObj = NewAIInstance.NewAIInstance( AIID,eID )
				AIInstObj.initData( instSection )
				self._newAIInstances.append(AIInstObj)

		for instSection in stateSection[ "statesAI" ]:
			AIID = instSection["id"]
			eID = instSection["EID"]
			AIInstObj = AIInstance.AIInstance( AIID,eID )
			AIInstObj.initData( instSection )
			self._AIInstances.append(AIInstObj)
		
		#加载事件AI
		for eventType,eventSection in stateSection[ "eventsAI" ].items():
			eventClassObject = AIEvents.AIEventBase.AIEventBase.getEventClass(eventType)
			eventClassObject.initData( eventSection )
			self._AIEventInfos[ eventType ] = eventClassObject
		if "newEventsAI" in stateSection:
			for eventType,eventSection in stateSection[ "newEventsAI" ].items():
				eventClassObject = AIEvents.AIEventBase.AIEventBase.getEventClass(eventType)
				eventClassObject.initNewAIEventsData( eventSection )
				self._newAIEventInfos[ eventType ] = eventClassObject
	
	def getInitiativeTrapParams( self ):
		return ( self.isServerInitiativeTrap, self.initiativeTrapShape, self._initiativeAreaXZ)
	
	def onEnter( self, entity ):
		"""
		进入状态
		"""
		for effectID in self._subHoldEffectIDs:
			index = entity.addFixIDHoldEffect( effectID, entity )
			if index != -1:
				entity.monsterAISubHoldEffectIndexs.append( index )

		KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 进入AI子状态( AICurrentState:%d )!"\
			%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, self._subID ))
		entity.monsterAISetCurSubState( self._subID )
		if entity.monsterAIGetFSM().getAIDataType() == "AIDatas2":
			self.doAIInst(entity)
		entity.monsterAISetTickSpeed( self._tick )
		if  self._initiativeAreaXZ!="0.0" and  not entity.findProximityByUserArg( ECBProximityDefine.PROXIMITY_AI_INITIATIVE_1 ):
			entity.mosnterAIAddInitiativeTrap()
			
		
	def onLeave( self, entity ):
		"""
		离开状态
		"""
		for index in entity.monsterAISubHoldEffectIndexs:
			entity.removeFixIDHoldEffect( index )
		entity.monsterAISubHoldEffectIndexs = []

		KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 离开AI子状态( AICurrentState:%d )!"\
			%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, self._subID ))
		entity.monsterAICancelInitiativeTrap()
		if entity.monsterAIGetFSM().getAIDataType() == "AIDatas2":
			self.stopAIInst(entity)
	
	def trigger( self, entity, eventType, eventArgs, triggerEntity ):
		"""
		触发事件AI
		"""
		self._onTrigger( entity, eventType, eventArgs, triggerEntity )
		

	def _onTrigger(self, entity, eventType, eventArgs, triggerEntity):
		"""
		"""
		if entity.monsterAIGetFSM().getAIDataType() == "AIDatas1" and eventType in self._AIEventInfos:
			KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 触发事件AI  %s"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState,eventType))
			self._AIEventInfos[ eventType ].trigger( entity, eventArgs, triggerEntity )

		elif entity.monsterAIGetFSM().getAIDataType() == "AIDatas2" and eventType in self._newAIEventInfos:
			KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 触发事件AI  %s"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState,eventType))
			self._newAIEventInfos[ eventType ].triggerNewAIEvents( entity, eventArgs, triggerEntity )
			
	def tick( self, entity ):
		"""
		AI的一个心跳
		"""
		groupState = entity.monsterAIGetCurGroupState()
		for AIInst in self._AIInstances:
			if AIInst.check( entity,"" ):
				KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 开始执行AI！( aiID:%d )!"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, AIInst.getID() ))
				if groupState != entity.monsterAIGetCurGroupState() or self._subID != entity.monsterAIGetCurSubState():
					break
				AIInst.do( entity )
				KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) AI执行结束！( aiID:%d )!"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, AIInst.getID() ))

	def doAIInst(self, entity):
		"""
		执行AI实例
		"""
		groupState = entity.monsterAIGetCurGroupState()
		for AIInst in self._newAIInstances:
			if groupState != entity.monsterAIGetCurGroupState() or self._subID != entity.monsterAIGetCurSubState():
					break
			AIInst.do(entity)
				

	def stopAIInst(self, entity):
		"""
		停止执行AI实例
		"""
		for AIInst in self._newAIInstances:
			if AIInst.getID() in entity.monsterAIDoInstTimerID:
				timerID = entity.monsterAIDoInstTimerID[AIInst.getID()]
				if timerID!= 0:
					entity.popTimer(timerID)
					entity.monsterAIDoInstTimerID[AIInst._id] = 0

