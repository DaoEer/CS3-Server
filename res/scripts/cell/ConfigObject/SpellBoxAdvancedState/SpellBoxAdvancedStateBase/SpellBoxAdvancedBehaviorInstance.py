# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug

from ConfigObject.SpellBoxAdvancedState import SpellBoxAdvancedActions
from ConfigObject.SpellBoxAdvancedState import SpellBoxAdvancedConditions


class SpellBoxAdvancedBehaviorInstance:
	"""
	行为(包括条件和执行的操作)
	"""
	def __init__( self ):
		"""
		"""
		self._actions = []
		self._conditions = []
	
	def initData( self, section ):
		"""
		"""
		#初始化条件数据
		conditionsSec = section[ "condition" ]
		for condSec in conditionsSec:
			condScriptClass = condSec["script"]
			condScriptObject = SpellBoxAdvancedConditions.SpellBoxAdvancedConditionBase.getConditionClassObj( condScriptClass )
			condScriptObject.initData( condSec )
			self._conditions.append( condScriptObject )
	
		#初始化行为数据
		actionsSec = section[ "action" ]
		for actSec in actionsSec:
			actScriptClass = actSec["script"]
			actScriptObject = SpellBoxAdvancedActions.SpellBoxAdvancedActionBase.getActionClassObj( actScriptClass )
			actScriptObject.initData( actSec )
			self._actions.append( actScriptObject )

	def check( self, entity, args, triggerEntity = None ):
		"""
		检查条件
		"""
		for condition in self._conditions:
			if not condition.check( self, entity, args, triggerEntity):
				#KBEDebug.INFO_MSG("SpellBoxAdvancedBehavior check: False")
				return False
		return True
	
	def do( self, entity, triggerEntity = None ):
		"""
		执行行为
		"""
		for action in self._actions:
			action.do( self, entity, triggerEntity )


