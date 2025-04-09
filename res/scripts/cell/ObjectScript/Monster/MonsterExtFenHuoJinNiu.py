# -*- coding: utf-8 -*-

import KBEngine
import ObjectScript.Monster.Monster as Monster


class MonsterExtFenHuoJinNiu( Monster.Monster ):
	"""
	环任务副本 焚火金牛怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def onRemoveEnemy( self, selfEntity, entityID ):
		"""
		重载掉此方法，敌人列表为空时不会进入重置状态
		"""
		pass	




	


	


