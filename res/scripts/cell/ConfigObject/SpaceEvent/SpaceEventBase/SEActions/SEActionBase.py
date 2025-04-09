# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug

class SEActionBase:
	"""
	基类
	"""
	_ACTIONS_CLASS = {}
	def __init__( self ):
		self.id = 0
		self.delayTime = 0
		self.params = {}

	@classmethod
	def setActionClass( SELF, className, actionClass ):
		SELF._ACTIONS_CLASS[ className ] = actionClass
	
	@classmethod
	def getActionClassObj( SELF, className ):
		return SELF._ACTIONS_CLASS.get(className,None)

	def init( self, section ):
		self.id = section["id"]
		self.delayTime = section["delayTime"]
		self.params = {"param1":section["param1"], "param2":section["param2"], "param3":section["param3"], "param4":section["param4"]}
	
	def do( self, spaceEntity, triggerID, eventParams ):
		pass
		
	def getParams( self ):
		return self.params
