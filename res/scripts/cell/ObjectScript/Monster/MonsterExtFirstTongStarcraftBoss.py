# -*- coding: utf-8 -*-

import ObjectScript.Monster.Monster as Monster
import KBEDebug

class MonsterExtFirstTongStarcraftBoss( Monster.Monster ):
	"""
	CST-7904 帮会争霸第一场 Boss怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		
	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		selfEntity.setBootyOwner( None )
		selfEntity.changeDefaultMove()

