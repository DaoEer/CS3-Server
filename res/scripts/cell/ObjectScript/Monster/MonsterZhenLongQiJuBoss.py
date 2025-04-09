# -*- coding: utf-8 -*-

import KBEngine
import ObjectScript.Monster.Monster as Monster


class MonsterZhenLongQiJuBoss( Monster.Monster ):
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
		selfEntity.setHP(int(selfEntity.HP_Max * 0.5))
		selfEntity.setMP( selfEntity.MP_Max )
		selfEntity.setBootyOwner( None )


