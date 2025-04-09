# -*- coding: utf-8 -*-
import KBEDebug

from ConfigObject.MonsterAI import AIConditions
from ConfigObject.MonsterAI.AIBase import AISubState

# 一个状态组
class AIGroupState( object ):
	def __init__( self, groupID ):
		self._groupID = groupID
		self._subStates = {}
		self._isDefault = False
		self._tiggerEventType = 0
		self._tiggerConditions = []
		self._groupHoldEffectIDs = []   #AI组状态持有效果列表
	
	def getGroupStateID( self ):
		return self._groupID

	def getSubStatesID( self ):
		return list(self._subStates.keys())
	
	def initData( self, groupDatas, stateDatas ):
		"""
		初始化数据
		"""
		self._isDefault = groupDatas[ "isDefault" ]
		self._tiggerEventType = groupDatas[ "tiggerEventType" ]
		#加载进入条件
		conditionsSec = groupDatas[ "triggerConditions" ]
		for condSec in conditionsSec:
			condScriptClass = condSec["script"]
			condScriptObject = AIConditions.AIConditionBase.AIConditionBase.getConditionClassObj( condScriptClass, 0 )
			condScriptObject.initData( condSec )
			self._tiggerConditions.append( condScriptObject )
			
		#加载组状态持有效果ID
		self._groupHoldEffectIDs = stateDatas["groupHoldEffectIDs"]

		#加截AI状态数据
		subStateDatas = stateDatas["subStateDatas"]
		if subStateDatas:
			for stateID, stateSec in subStateDatas.items():
				statusClassObject = AISubState.AISubState( stateID )
				statusClassObject.initData( stateSec )
				self._subStates[ stateID ] = statusClassObject
	
	def isCanEnter( self, entity, eventType, eventArgs, triggerEntity ):
		"""
		是否切换到些状态组
		"""
		result = True
		#if self._tiggerEventType == eventType:
		#	result = False
		
		if result:
			for cond in self._tiggerConditions:
				if not cond.check( None, entity, eventArgs, triggerEntity ):
					result = False
					break
		
		return result
	
	def onEnter( self, entity ):
		"""
		进入组状态
		"""
		for effectID in self._groupHoldEffectIDs:
			index = entity.addFixIDHoldEffect( effectID, entity )
			if index != -1:
				entity.monsterAIGroupHoldEffectIndexs.append( index )
	
		
		entity.monsterAISetCurGroupState( self._groupID )
		if len( self._subStates ):
			startSubState = min( self._subStates.keys() )
			self._subStates[ startSubState ].onEnter( entity )
		else:			
			entity.monsterAISetCurSubState( 0 )
			entity.monsterAIStopTick()
					
	def onLeave( self, entity ):
		"""
		离开组状态
		"""
		for index in entity.monsterAIGroupHoldEffectIndexs:
			entity.removeFixIDHoldEffect( index )
		entity.monsterAIGroupHoldEffectIndexs = []

		if entity.monsterAIGetCurSubState() in self._subStates:
			self._subStates[ entity.monsterAIGetCurSubState() ].onLeave( entity )
	
	def changeSubState( self, entity, oldSubState, newSubState ):
		"""
		切换状态
		"""
		if newSubState in self._subStates:
			self._subStates[ oldSubState ].onLeave( entity )
			self._subStates[ newSubState ].onEnter( entity )
		else:
			KBEDebug.ERROR_MSG( "Monster( scriptID:%s, id:%d ) groupState:%s not has subState:%s !!"%( entity.scriptID, entity.id, self._groupID, newSubState ) )
	
	def getCurrentSubState( self, entity ):
		return self._subStates.get( entity.monsterAIGetCurSubState() )
	
	def trigger( self, entity, eventType, eventArgs, triggerEntity ):
		"""
		触发事件AI
		"""
		subState = self.getCurrentSubState( entity )
		if subState:
			subState.trigger( entity, eventType, eventArgs, triggerEntity )
	
	def tick( self, entity ):
		"""
		状态循环
		"""
		subState = self.getCurrentSubState( entity )
		if subState:
			subState.tick( entity )