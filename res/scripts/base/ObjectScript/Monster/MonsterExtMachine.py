# -*- coding: utf-8 -*-

import KBEngine
import Math
import csdefine
import ObjectScript.Monster.Monster as Monster


class MonsterExtMachine( Monster.Monster ):
	"""
	机关怪脚本  机关怪的状态：未决，自由，警戒，死亡，表演 
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )


	def onRemoveEnemy( self, selfEntity, entityID ):
		"""
		重载掉此方法，敌人列表为空时不会进入重置状态
		"""
		pass	




	


	


