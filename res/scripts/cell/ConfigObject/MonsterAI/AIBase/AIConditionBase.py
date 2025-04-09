# -*- coding: utf-8 -*-
import KBEDebug
import Math
import csdefine
class AIConditionBase:
	_CONDITIONS_CLASS = {}
	
	def __init__( self, aiID ):
		self._aiID = aiID
		conditionName = ""
		
	@classmethod
	def setConditionClass( SELF, className, conditionClass ):
		SELF._CONDITIONS_CLASS[ className ] = conditionClass
	
	@classmethod
	def getConditionClassObj( SELF, className, aiID ):
		SELF.conditionName = className
		return SELF._CONDITIONS_CLASS[ className ](aiID)

	def getAIID(self):
		return self._aiID

	def initData( self, section ):
		"""
		初始化数据函数
		"""
		pass

	def check( self, ai, entity, args, triggerEntity ):
		"""
		vitural method
		@param	ai		: 	拥有此条件的AI ( 做此支持是为了得到或写AI的动态数据 )
		@type	ai		:	AIInstanceBase
		@param	entity	: 	执行此AICondition的entity
		@type	entity	:	entity
		"""
		return True

