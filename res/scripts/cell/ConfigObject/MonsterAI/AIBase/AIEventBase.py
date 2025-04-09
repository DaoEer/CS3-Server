# -*- coding: utf-8 -*-
import KBEDebug
from ConfigObject.MonsterAI.AIBase import AIInstance

class AIEventBase:
	#事件AI
	_EVENT_CLASS = {}
	def __init__( self, eventType ):
		self._eventType = eventType	#状态
		self._AIInstances = []
		self._newAIInstances = []
	
	@classmethod
	def setEventClass( SELF, eventType, eventClass ):
		SELF._EVENT_CLASS[ eventType ] = eventClass
	
	@classmethod
	def getEventClass( SELF, eventType ):
		return SELF._EVENT_CLASS[ eventType ]( eventType )
		
	@classmethod
	def isHasEvent(SELF,eventType):
		if eventType in SELF._EVENT_CLASS:
			return True
		else:
			return False

	def initData( self, eventSection ):
		for instSection in eventSection:
			ids = instSection["id"]
			eid = instSection["EID"]
			AIInstObj = AIInstance.AIInstance(ids,eid )
			AIInstObj.initData( instSection )
			self._AIInstances.append(AIInstObj)

	def initNewAIEventsData(self, eventSection):
		"""
		"""
		for instSection in eventSection:
			ids = instSection["id"]
			eid = instSection["EID"]
			AIInstObj = AIInstance.AIInstance(ids,eid )
			AIInstObj.initData( instSection )
			self._newAIInstances.append(AIInstObj)
	
	def trigger( self, entity, eventArgs, triggerEntity ):
		"""
		触发一个AI事件
		"""
		self._onTrigger(entity, eventArgs, triggerEntity)

	def _onTrigger( self, entity, eventArgs, triggerEntity ):
		"""
		"""
		for AIInst in self._AIInstances:
			if AIInst.check( entity, eventArgs, triggerEntity ):
				KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 开始执行事件AI( aiID:%d )!"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, AIInst.getID() ))
				AIInst.do( entity, triggerEntity )
				KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 事件AI执行结束( aiID:%d )!"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, AIInst.getID() ))

	def triggerNewAIEvents( self, entity, eventArgs, triggerEntity ):
		"""
		触发一个AI事件
		"""
		self._onTriggerNewAIEvents(entity, eventArgs, triggerEntity)
	

	def _onTriggerNewAIEvents( self, entity, eventArgs, triggerEntity ):
		"""
		"""
		for AIInst in self._newAIInstances:
			if AIInst.check( entity, eventArgs, triggerEntity ):
				KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 开始执行事件AI( aiID:%d )!"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, AIInst.getID() ))
				AIInst.do( entity, triggerEntity )
				KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 事件AI执行结束( aiID:%d )!"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, AIInst.getID() ))