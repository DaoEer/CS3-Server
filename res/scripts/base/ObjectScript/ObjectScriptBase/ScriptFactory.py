# -*- coding: utf-8 -*-

import Singleton

class ScriptFactory( Singleton.Singleton ):
	def __init__( self ):
		Singleton.Singleton.__init__( self )
	
	def loadData( self, config ):
		pass
	
	def getObject( self, scriptID ):
		return None