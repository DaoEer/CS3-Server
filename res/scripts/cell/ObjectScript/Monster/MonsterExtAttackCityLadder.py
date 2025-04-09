# -*- coding: utf-8 -*-
import ObjectScript.Monster.MonsterExtMain as MonsterExtMain
import KBEDebug

class MonsterExtAttackCityLadder( MonsterExtMain.MonsterExtMain ):
	def __init__( self ):
		MonsterExtMain.MonsterExtMain.__init__( self )
		self.actionID = ""
		self.delyTimeMove = 0.0
		self.beginAddBuffID = 0
		self.endAddBuffID = 0
		self.patrolRoute = 0

	def initData( self, configData ):
		MonsterExtMain.MonsterExtMain.initData( self, configData )
		self.actionID = configData["Param2"]
		if configData["Param3"]:
			self.delyTimeMove = float( configData["Param3"] )
		if configData["Param4"]:
			Param4 = configData["Param4"].split("|")
			self.beginAddBuffID = int( Param4[0] )
			if len(Param4)>1:
				self.endAddBuffID = int( Param4[1] )
		if configData["Param5"]:
			self.patrolRoute = int(configData["Param5"])

