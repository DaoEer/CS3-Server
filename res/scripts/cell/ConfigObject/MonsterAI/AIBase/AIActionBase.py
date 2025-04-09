# -*- coding: utf-8 -*-
import  KBEDebug
import Math
import csdefine

import ConfigObject.Skill.SkillLoader as SkillLoader

class AIActionBase:
	_ACTIONS_CLASS = {}
	def __init__( self, aiID ):
		self._aiID = aiID
		
	@classmethod
	def setActionClass( SELF, className, actionClass ):
		SELF._ACTIONS_CLASS[ className ] = actionClass
	
	@classmethod
	def getActionClassObj( SELF, className, aiID ):
		return SELF._ACTIONS_CLASS[ className ](aiID)

	def getAIID(self):
		return self._aiID
	
	def checkSkillIsExit( self, skillID ):
		"""
		检查配置的技能是否存在
		"""
		return True
		
		skillObj = SkillLoader.g_skills[ skillID ]
		if skillObj == None:
			KBEDebug.CRITICAL_MSG( "AI action( %s ) config skill %i not exist. AI ID:%d" % ( self.__class__.__name__, skillID, self._aiID ) )
			return False
		else:
			return True

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


