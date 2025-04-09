# -*- coding: utf-8 -*-
import random

import csdefine
from ConfigObject.MonsterAI import AIActions
from ConfigObject.MonsterAI import AIConditions
import KBEDebug

class NewAIInstance:
	def __init__( self,ids, eaiid ):
		self._actions = []
		self._conditions = []
		self._odds = 0
		self._id = ids
		self._eai_list = eaiid
		self._delayTime = 0.0 					#初次执行延迟时间
		self._repeatTime = 0.0 					#循环间隔时间
		self._maxLoops = 0 						#最多可执行次数


	def initData( self, section ):
		#初始化动作数据
		self._odds = int( section[ "odds" ] * 100 )
		self._delayTime = max(0.0,float(section["delayTime"]))
		self._repeatTime = max(0.0,float(section["repeatTime"]))
		self._maxLoops = int(section["maxLoops"])

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
	
	def getID(self):
		"""
		返回当前AIID
		"""
		return self._id

	def check( self, entity,  args, triggerEntity=None ):
		"""
		检查
		"""
		if entity.monsterAIHasEAI(self._id):
			KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) AI检测未通过 (AIid=%d) 原因:存在Eid！( Eid=%d )!"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, self.getID(), self._id ))
			return False
		
		
		if self._odds == 100 or  random.randint( 0, 99 ) >= self._odds:
			KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) AI检测未通过 (AIid=%d) 原因:未触发！ ( odds:%d )!"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, self.getID(), self._odds ))
			return False

		for cond in self._conditions:
			if not cond.check( self, entity, args, triggerEntity):
				KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) AI检测未通过 (AIid=%d) 原因:%s未通过！"\
					%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, self.getID(), cond.__class__.__name__ ))
				return False
		KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) 开始执行AI！( aiID:%d )!"\
				%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, self.getID() ))
		return True

	def doActions(self, entity, triggerEntity = None):
		"""
		"""
		if len(self._eai_list) > 0 :
			entity.monsterAIExtEAI( self._eai_list )

		for action in self._actions:
			action.do(self, entity, triggerEntity)

		KBEDebug.DEBUG_MSG_FOR_AI(entity, "entity( id:%d scriptID:%s AI组状态:%s, AI子状态:%s ) AI执行结束！( aiID:%d )!"\
			%(entity.id, entity.scriptID, entity.monsterAICurGroupState, entity.monsterAICurSubState, self.getID() ))

		if entity.monsterAIGetFSM().getAIDataType() == "AIDatas2":
			if self._maxLoops<0:
				return
			loops = entity.getAIIDLoops(self.getID())
			loops += 1
			entity.setAIIDLoops(self.getID(), loops)
			if loops >= self._maxLoops:
				entity.monsterAIAddEAI(self._id)
				if self.getID() in entity.monsterAIDoInstTimerID:
					entity.stopMonsterAIInst(self._id)

	def do(self, entity, triggerEntity = None):
		"""
		"""
		if self._repeatTime > 0.0 or self._delayTime > 0.0:
			entity.monsterAIDoInst(self, triggerEntity)
		else:
			self.doAI(entity, triggerEntity)


	def doAI(self, entity, triggerEntity = None):
		"""
		"""
		if self.check(entity, ""):
			self.doActions(entity, triggerEntity)





