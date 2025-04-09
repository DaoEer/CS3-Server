# -*- coding: utf-8 -*-

import ObjectScript.Monster.Monster as Monster
import KBEDebug

class MonsterExtXuanTianBaoLu( Monster.Monster ):
	"""
	玄天宝录副本 旋转怪物支持
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.rotatorSpeed = 0.0

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		if configData[ "Param1" ]:
			self.rotatorSpeed = float(configData[ "Param1" ])

	def getRotatorSpeed( self ):
		"""
		获取旋转速度
		"""
		return self.rotatorSpeed