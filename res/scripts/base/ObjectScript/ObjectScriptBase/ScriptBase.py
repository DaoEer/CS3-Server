# -*- coding: utf-8 -*-
import KBEngine

class ScriptBase( object ):
	def __init__( self ):
		self.scriptID = ""
		
	def initData( self, configData ):
		self.scriptID = configData[ "scriptID" ]