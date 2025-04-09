# -*- coding: utf-8 -*-

# 副本策略点完成条件
import SpaceStrategyConditionDataType
import Define
import KBEngine
import csdefine
class SpaceStrategyPointConditionBase( SpaceStrategyConditionDataType.SpaceStrategyConditionDataType ):
	type = Define.SPACE_STRATEGYPOINT_CONDITION_NONE

	def __init__( self ):
		SpaceStrategyConditionDataType.SpaceStrategyConditionDataType.__init__( self )
		self.id = 0
		self.conditionBelongType = Define.SPACE_STRATEGYPOINT_CONDITION_NONE
		self.value = 0
		self.reqValue = 0
		self.param1 = ""
		self.param2 = ""
		self.param3 = ""

	def init( self, id, datas ):
		"""
		"""
		self.id = id
		self.value = datas["value"]
		self.reqValue = datas["reqValue"]
		self.param1 = datas["param1"]
		self.param2 = datas["param2"]
		self.param3 = datas["param3"]
		self.conditionBelongType = datas["conditionBelongType"]

	def getType( self ):
		return Define.SPACE_STRATEGYPOINT_CONDITION_NONE

	def increaseVal( self, value ):
		if value == 0:
			return False
		
		self.value += value
		return True

	def decreaseVal( self, value ):
		if value == 0:
			return False
		
		if self.value == 0:
			return False
		
		self.value = max( 0, self.value - value )
		return True

	def isCompleted( self ):
		return self.value >= self.reqValue

class SStrategyCondition_onRoleAddBuff( SpaceStrategyPointConditionBase ):
	"""
	玩家增加buff
	"""
	def getType( self ):
		return Define.SPACE_STRATEGYPOINT_CONDITION_ROLE_ADDBUFF

	def checkBuffID( self, buffID ):
		buffIDList = [int(i) for i in self.param1.split("|")]
		return buffID in buffIDList

class SStrategyCondition_onKillMonster( SpaceStrategyPointConditionBase ):
	"""
	杀怪
	"""
	def getType( self ):
		return Define.SPACE_STRATEGYPOINT_CONDITION_KILLMONSTER

	def checkScriptID( self, scriptID ):
		scriptIDList = self.param1.split("|")
		return scriptID in scriptIDList


SpaceStrategyConditionDataType.MAP_CONDITION_TYPE_TO_CONDITION_CLASS( Define.SPACE_STRATEGYPOINT_CONDITION_ROLE_ADDBUFF, SStrategyCondition_onRoleAddBuff )
SpaceStrategyConditionDataType.MAP_CONDITION_TYPE_TO_CONDITION_CLASS( Define.SPACE_STRATEGYPOINT_CONDITION_KILLMONSTER, SStrategyCondition_onKillMonster )
