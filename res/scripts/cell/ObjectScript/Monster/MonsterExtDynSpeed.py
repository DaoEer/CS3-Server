# -*- coding: utf-8 -*-

import ObjectScript.Monster.Monster as Monster

class MonsterExtDynSpeed( Monster.Monster ):
	"""
	动态速度
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def getRunSpeed( self, selfEntity ):
		""""""
		speed = selfEntity.queryTemp("runSpeed", 0.0)
		if not speed:
			speed = self.runSpeed
		return speed
		
	def getWalkSpeed( self, selfEntity ):
		""""""
		speed = selfEntity.queryTemp("walkSpeed", 0.0)
		if not speed:
			speed = self.walkSpeed
		return speed
