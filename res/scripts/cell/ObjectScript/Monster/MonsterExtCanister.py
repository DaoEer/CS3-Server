# -*- coding: utf-8 -*-
import ObjectScript.Monster.Monster as Monster
import KBEDebug

class MonsterExtCanister( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.skillID = 0

	def initData( self, configData ):
		Monster.Monster.initData( self, configData )
		if configData["Param1"]:
			self.skillID = int( configData["Param1"] )
		if configData["Param2"]:
			self.setEntityProperty("ammo",int( configData["Param2"] ))
		if configData["Param3"]:
			self.loadCD = float( configData["Param3"] )

			
