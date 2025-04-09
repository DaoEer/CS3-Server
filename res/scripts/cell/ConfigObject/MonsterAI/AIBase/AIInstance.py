# -*- coding: utf-8 -*-
import random

import csdefine
from ConfigObject.MonsterAI import AIActions
from ConfigObject.MonsterAI import AIConditions
import KBEDebug

class AIInstance:
	def __init__( self,ids, eaiid ):
		self._actions = []
		self._conditions = []
		self._odds = 0
		self._id = ids
		self._eai_list = eaiid
		
		self.__cache_check_list = []
		self.__cache_do_list = []

	def initData( self, section ):
		#初始化动作数据
		self._odds = int( section[ "odds" ] * 100 )
		actionsSec = section[ "Actions" ]
		for actSec in actionsSec:
			actScriptClass = actSec["script"]
			actScriptObject = AIActions.AIActionBase.AIActionBase.getActionClassObj( actScriptClass, self._id )
			actScriptObject.initData( actSec )
			self._actions.append( actScriptObject )
		
		#初始化条件数据
		conditionsSec = section[ "Conditions" ]
		for condSec in conditionsSec:
			condScriptClass = condSec["script"]
			condScriptObject = AIConditions.AIConditionBase.AIConditionBase.getConditionClassObj( condScriptClass, self._id )
			condScriptObject.initData( condSec )
			self._conditions.append( condScriptObject )
		
		self.initCache()
	
	def initCache( self ):
		for a in self._actions:
			self.__cache_do_list.append( a.do )
		
		for c in self._conditions:
			self.__cache_check_list.append( c.check )
	
	def getID(self):
		"""
		返回当前AIID
		"""
		return self._id

	def check( self, entity,  args, triggerEntity=None ):
		"""
		检查
		"""
		if entity.monsterAIHasEAI(self._id ):
			KBEDebug.DEBUG_MSG_FOR_AI(entity, "AIid = %d, EAI :%d is exist!"%(self._id,self._id))
			return False

		if self._odds != 100 and random.randint( 0, 99 ) >= self._odds:
			KBEDebug.DEBUG_MSG_FOR_AI(entity,"AIid = %d ,_odds :%d "%(self._id, self._odds))
			return False
		
		for c in self.__cache_check_list:
			if not c( self, entity, args, triggerEntity):
				KBEDebug.DEBUG_MSG_FOR_AI(entity, "AIid = %d, %s is not True! "%(self._id, c.__self__.__class__))
				return False

		return True
	
	def do( self, entity, triggerEntity = None ):
		"""
		执行
		"""
		if self._eai_list:
			entity.monsterAIExtEAI( self._eai_list )

		for a in self.__cache_do_list:
			a( self, entity, triggerEntity )


