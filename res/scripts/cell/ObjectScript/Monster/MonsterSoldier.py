# -*- coding: utf-8 -*-

import ObjectScript.Monster.MonsterOptimize as MonsterOptimize
import csdefine

class MonsterSoldier( MonsterOptimize.MonsterOptimize ):
	"""
	士兵类型怪物script
	"""
	def __init__( self ):
		MonsterOptimize.MonsterOptimize.__init__( self )


	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态 不回血
		"""
		selfEntity.setBootyOwner( None )
		selfEntity.changeDefaultMove()

		
	def onEnterReset( self, selfEntity ):
		"""
		进入回走状态
		"""
		for bufIdx in list( selfEntity.getAttrBuffs().keys() ):#回走部分buff不移除 CST-1998
			buffData = selfEntity.getBuffData( bufIdx )
			if buffData and buffData.buffID not in selfEntity.resetKeepBuffs:
				selfEntity.removeBuffByIndex( bufIdx  )
		selfEntity.resetEnemyList()
		selfEntity.changeState(csdefine.ENTITY_STATE_FREE)
