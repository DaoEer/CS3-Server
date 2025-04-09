# -*- coding: utf-8 -*-
import ObjectScript.Monster.MonsterExtAttackCityLadder as MonsterExtAttackCityLadder
import KBEDebug

class MonsterExtCollisionCar( MonsterExtAttackCityLadder.MonsterExtAttackCityLadder ):
	def __init__( self ):
		MonsterExtAttackCityLadder.MonsterExtAttackCityLadder.__init__( self )
		self.skillID = 0

	def initData( self, configData ):
		MonsterExtAttackCityLadder.MonsterExtAttackCityLadder.initData( self, configData )
		if configData["Param2"]:
			self.skillID = int(configData["Param2"])

