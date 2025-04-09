# -*- coding: utf-8 -*-

# 副本事件条件
import KBEDebug

class SEConditionBase:
	"""
	基类
	"""
	_CONDITIONS_CLASS = {}
	def __init__( self, dataDict = {} ):
		self.id = dataDict.get( "id", 0 )
		self.param1 = dataDict.get( "param1", "" )
		self.param2 = dataDict.get( "param2", "" )
		self.param3 = dataDict.get( "param3", "" )
		self.param4 = dataDict.get( "param4", "" )
		self.isClientCon = False

	@classmethod
	def setConditionClass( SELF, className, actionClass ):
		SELF._CONDITIONS_CLASS[ className ] = actionClass
	
	@classmethod
	def getConditionClassObj( SELF, className ):
		return SELF._CONDITIONS_CLASS.get(className,None)
	
	def init( self, section ):
		self.id = section["id"]
		self.param1 = section["param1"]
		self.param2 = section["param2"]
		self.param3 = section["param3"]
		self.param4 = section["param4"]
	
	def check( self, entity, eventParams ):
		return True
		
	def getParams( self ):
		return {"param1":self.param1, "param2":self.param2, "param3":self.param3, "param4":self.param4}

