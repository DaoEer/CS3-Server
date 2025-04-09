#coding:utf-8

import sys
import KBEDebug
from ObjectScript.ObjectScriptBase import EntityPropertyLoader

class SpellBoxPropertyLoader( EntityPropertyLoader.EntityPropertyLoader ):
	def __init__( self ):
		EntityPropertyLoader.EntityPropertyLoader.__init__( self )
		self.areaData = {}

	def initData( self, configData ):
		if configData is not None:
			EntityPropertyLoader.EntityPropertyLoader.initData( self, configData )