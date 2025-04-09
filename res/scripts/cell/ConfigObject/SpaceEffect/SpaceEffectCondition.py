# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import Math
import Functions
import KBEMath

class SpaceEffectConditionBase:
	"""
	效果条件基类
	"""
	_TYPE_DICT = {}
	@classmethod
	def getEffectCndObj( SELF, cndConfigSecion ):
		scriptName = cndConfigSecion[ "scriptName" ]
		if scriptName:
			cndObj = SELF._TYPE_DICT.get( scriptName )( cndConfigSecion )
			return cndObj

	@classmethod
	def addEffectCndType( SELF, typeName, typeClass ):
		SELF._TYPE_DICT[ typeName ] = typeClass

	def __init__( self, configDict ):
		if configDict:
			self.init( configDict )

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def check( self, spaceEntity, playerEntity ):
		"""
		virtual method
		"""
		return True

class SpaceEffectConditionQuest( SpaceEffectConditionBase ):
	"""
	根据玩家任务状态改变效果
	"""
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.questInfo = configDict["param1"]
		self.questState = [ int(i) for i in configDict["param2"].split("|") ]
		
	def check( self, spaceEntity, playerEntity ):
		"""
		virtual method
		"""
		if playerEntity.queryQuestStatus( int(self.questInfo) ) in self.questState:
			return True
		return False


SpaceEffectConditionBase.addEffectCndType( "SpaceEffectConditionQuest", SpaceEffectConditionQuest )

