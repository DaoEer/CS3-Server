# -*- coding: utf-8 -*-

import ObjectScript.Monster.MonsterExtMain as MonsterExtMain
import KBEDebug
import csdefine

class MonsterExtYXLMTower( MonsterExtMain.MonsterExtMain ):
	"""
	英雄联盟 防御塔
	"""
	def __init__( self ):
		MonsterExtMain.MonsterExtMain.__init__( self )
		
	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		pass
