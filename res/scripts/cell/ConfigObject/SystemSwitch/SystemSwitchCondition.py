# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import Math
import Functions
import KBEMath

class SystemSwitchConditionBase:
	"""
	系统开关条件基类
	"""
	_CONDITIONS_CLASS = {}
	@classmethod
	def getConditionClassObj( SELF, cndConfigSecion ):
		className = cndConfigSecion[ "scriptName" ]
		if className:
			cndObj = SELF._CONDITIONS_CLASS.get( className )( cndConfigSecion )
		return cndObj

	@classmethod
	def setConditionClass( SELF, className, conditionClass ):
		SELF._CONDITIONS_CLASS[ className ] = conditionClass

	def __init__( self, configDict ):
		if configDict:
			self.init( configDict )

	def init( self, configDict ):
		"""
		virtual method
		"""
		pass
	
	def check( self, playerEntity ):
		"""
		virtual method
		"""
		return True

class SystemConditionOpenLevel( SystemSwitchConditionBase ):
	"""
	根据玩家的等级开启某系统
	"""
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._openLevel = int(configDict["param1"])
		
	def check( self, playerEntity ):
		"""
		virtual method
		"""
		if playerEntity.level >= self._openLevel:
			return True
		return False

class SystemConditionCloseLevel( SystemSwitchConditionBase ):
	"""
	根据玩家的等级关闭某系统
	"""
	def init( self, configDict ):
		"""
		virtual method
		"""
		self._closeLevel = int(configDict["param1"])
		
	def check( self, playerEntity ):
		"""
		virtual method
		"""
		if playerEntity.level <= self._openLevel:
			return True
		return False

class SystemConditionQuestState( SystemSwitchConditionBase ):
	"""
	根据玩家任务状态开启某系统
	"""
	def init( self, configDict ):
		"""
		virtual method
		"""
		self.questInfo = configDict["param1"]
		self.questState = [ int(i) for i in configDict["param2"].split("|") ]
		
	def check( self, playerEntity ):
		"""
		virtual method
		"""
		if playerEntity.queryQuestStatus( int(self.questInfo) ) in self.questState:
			return True
		return False

SystemSwitchConditionBase.setConditionClass( "SystemConditionOpenLevel", SystemConditionOpenLevel )
SystemSwitchConditionBase.setConditionClass( "SystemConditionCloseLevel", SystemConditionCloseLevel )
SystemSwitchConditionBase.setConditionClass( "SystemConditionQuestState", SystemConditionQuestState )
