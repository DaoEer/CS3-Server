# -*- coding: utf-8 -*-
#############
# 灵脉战场 Boss
#############

import ObjectScript.Monster.Monster as Monster


class MonsterExtLingMai( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		
	def onEnterDead( self, selfEntity ):
		"""
		死亡
		"""
		selfEntity.resetEnemyList()


