# -*- coding: utf-8 -*-
import ObjectScript.Monster.Monster as Monster
import KBEDebug

class MonsterExtClickAndInteractive( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.range = 0.0

	def initData( self, configData ):
		Monster.Monster.initData( self, configData )
		if configData["Param1"]:
			self.range = float( configData["Param1"] )

			
