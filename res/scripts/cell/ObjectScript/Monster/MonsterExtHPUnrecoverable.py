# -*- coding: utf-8 -*-

import KBEngine
import ObjectScript.Monster.Monster as Monster


class MonsterExtHPUnrecoverable( Monster.Monster ):
	"""
	不可自动回复血量怪物脚本
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
		selfEntity.changeDefaultMove()


