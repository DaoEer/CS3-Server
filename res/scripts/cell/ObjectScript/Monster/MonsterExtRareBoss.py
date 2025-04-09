# -*- coding: utf-8 -*-
import ObjectScript.Monster.Monster as Monster
import csdefine
import KBEngine
import KBEDebug

class MonsterExtRareBoss( Monster.Monster ):
	"""
	稀有Boss怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def onEnterDead( self, selfEntity ):
		"""
		死亡
		"""
		Monster.Monster.onEnterDead( self, selfEntity )
		spaceEntity = selfEntity.getCurrentSpace()
		if spaceEntity:
			KBEngine.globalData[ "RareMonsterMgr" ].onBossOnEnterDead( spaceEntity.base, spaceEntity.scriptID )
