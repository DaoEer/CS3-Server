# -*- coding: utf-8 -*-

import ObjectScript.Monster.Monster as Monster
import KBEDebug
class MonsterExtJingShiDongKu( Monster.Monster ):
	"""
	晶石洞窟副本 特殊怪物支持
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.pickUpDis = 0.0
		self.scopeDis = 0.0

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		if configData[ "Param1" ]:
			self.pickUpDis = float(configData[ "Param1" ])
		if configData[ "Param2" ]:
			self.scopeDis = float(configData[ "Param2" ])

	def getPickUpDis( self ):
		"""
		获取拾取范围
		"""
		return self.pickUpDis

	def getScopeDis( self ):
		"""
		获取打落距离
		"""
		return self.scopeDis
