# -*- coding: utf-8 -*-

import KBEngine
import ObjectScript.Monster.Monster as Monster


class MonsterSparHunTing( Monster.Monster ):
	"""
	晶石狩猎场 怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )

	def onEnterFree( self, selfEntity ):
		"""
		virtual method
		进入自由状态
		"""
		selfEntity.setBootyOwner( None )
		
	def onEnterDead( self, selfEntity ):
		"""
		死亡
		"""
		selfEntity.addTimerCallBack(5.0,"monsterAIReset",())
		selfEntity.addTimerCallBack(5.0,"resetEnemyList",())
		selfEntity.delayDestroy( 5 )
