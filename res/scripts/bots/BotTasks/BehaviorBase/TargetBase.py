# -*- coding: utf-8 -*-

class TargetBase( object ):
	_TARGET_CLASS = {}
	def __init__( self, config ):
		pass
		
	@classmethod
	def setClass( SELF, className, classObj ):
		SELF._TARGET_CLASS[ className ] = classObj
	
	@classmethod
	def getClassObj( SELF, config ):
		scriptName = config[ "Script" ]
		return SELF._TARGET_CLASS[ scriptName ]( config )

	def checkIsCompleted( self, roleEntity ):
		return True

		