# -*- coding: utf-8 -*-
"""
"""
import KBEngine
import KBEDebug

from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase import SpellBoxAdvancedBehaviorInstance

class SpellBoxAdvancedEventBase:
	#事件
	_EVENT_CLASS = {}
	def __init__( self, eventType ):
		self._eventType = eventType	#状态
		self._behaviorInsts = []
	
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
		for section in eventSection:
			obj = SpellBoxAdvancedBehaviorInstance.SpellBoxAdvancedBehaviorInstance( )
			obj.initData( section["behavior"] )
			self._behaviorInsts.append(obj)
	
	def trigger( self, entity, eventArgs, triggerEntity ):
		"""
		触发一个事件
		"""
		for behaviorInst in self._behaviorInsts:
			if behaviorInst.check( entity, eventArgs, triggerEntity ):
				behaviorInst.do( entity, triggerEntity )
				