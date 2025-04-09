# -*- coding: utf-8 -*-
import  KBEDebug
import Math
import csdefine

class SpellBoxAdvancedActionBase:
	_ACTIONS_CLASS = {}
	def __init__( self ):
		pass
		
	@classmethod
	def setActionClass( SELF, className, actionClass ):
		SELF._ACTIONS_CLASS[ className ] = actionClass
	
	@classmethod
	def getActionClassObj( SELF, className ):
		return SELF._ACTIONS_CLASS[ className ]()

	def initData( self, section ):
		"""
		初始化数据函数
		"""
		pass

	def do(self, ai, entity, triggerEntity):
		"""
		vitural method
		@param	ai		: 	拥有此的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		pass


