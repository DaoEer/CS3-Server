# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug

import Const
import csdefine

from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase import SpellBoxAdvancedEventBase
from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase import SpellBoxAdvancedBehaviorInstance


class SpellBoxAdvancedSubState:
	"""
	"""
	#状态
	def __init__( self, id ):
		"""
		"""
		self._id = id	#状态ID
		self._enterInstances = []
		self._leaveInstances = []
		self._tickInstances = []
		self._eventInfos = {}
		self._holdEffectIDs = []
		self._tickTime = 0
		
	def getStateID(self):
		"""
		"""
		return self._id

	def initData( self, stateSection ):
		"""
		"""
		#持有效果
		self._holdEffectIDs  = stateSection["HoldEffectIDs"]
		#状态的心跳
		self._tickTime = stateSection["tickTime"]
		
		#进入
		for section in stateSection["enter"]:
			obj = SpellBoxAdvancedBehaviorInstance.SpellBoxAdvancedBehaviorInstance( )
			obj.initData( section["behavior"] )
			self._enterInstances.append(obj)
			
		#离开
		for section in stateSection["leave"]:
			obj = SpellBoxAdvancedBehaviorInstance.SpellBoxAdvancedBehaviorInstance( )
			obj.initData( section["behavior"] )
			self._leaveInstances.append(obj)
			
		#心跳
		for section in stateSection["tick"]:
			obj = SpellBoxAdvancedBehaviorInstance.SpellBoxAdvancedBehaviorInstance( )
			obj.initData( section["behavior"] )
			self._tickInstances.append(obj)
			
		#事件
		for section in stateSection[ "event" ]:
			eventType = section["eventType"]
			obj = SpellBoxAdvancedEventBase.SpellBoxAdvancedEventBase(eventType)
			obj.initData( section["eventBehavior"] )
			self._eventInfos[eventType] = obj
	
	def onEnter( self, entity ):
		"""
		进入状态
		"""
		#效果
		for effectID in self._holdEffectIDs:
			index = entity.addFixIDHoldEffect( effectID, entity )
			if index != -1:
				entity.interactiveStateHoldEffectList.append(index)
		
		#加定时器
		if self._tickTime > 0:
			entity.interactiveStateTimerID = entity.addTimerRepeatForScript(self._tickTime, "stateTick", ())
			
		for behaviorInst in self._enterInstances:
			if behaviorInst.check( entity, "" ):
				behaviorInst.do(entity)
		
	def onLeave( self, entity ):
		"""
		离开状态
		"""
		#移除效果
		for index in entity.interactiveStateHoldEffectList:
			entity.removeFixIDHoldEffect(index)
			
		#移除定时器
		if entity.interactiveStateTimerID > 0:
			entity.popTimer(entity.interactiveStateTimerID)
			entity.interactiveStateTimerID = 0
		
		for behaviorInst in self._leaveInstances:
			if behaviorInst.check( entity, "" ):
				behaviorInst.do(entity)
		
	def trigger( self, entity, eventType, eventArgs, triggerEntity ):
		"""
		触发事件
		"""
		if eventType in self._eventInfos:
			self._eventInfos[ eventType ].trigger( entity, eventArgs, triggerEntity )
			
	def stateTick( self, entity ):
		"""
		心跳
		"""
		for behaviorInst in self._tickInstances:
			if behaviorInst.check( entity, "" ):
				behaviorInst.do(entity)
	