# -*- coding: utf-8 -*-

class ConditionBase( object ):
	_CONDITION_CLASS = {}
	def __init__( self, config ):
		self.initData( config )
		
	@classmethod
	def setClass( SELF, className, classObj ):
		SELF._CONDITION_CLASS[ className ] = actionClass
	
	@classmethod
	def getClassObj( SELF, className, config ):
		return SELF._CONDITION_CLASS[ className ]( config )
	
	def initData( self, config ):
		pass
	
	def check( self, roleEntity ):
		return True