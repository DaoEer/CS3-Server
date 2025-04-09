# -*- coding: utf-8 -*-
#############
#替身脚本 目前用于玩家
#############

import ObjectScript.Monster.Monster as Monster
class MonsterExtTiShen( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		
	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		pass


