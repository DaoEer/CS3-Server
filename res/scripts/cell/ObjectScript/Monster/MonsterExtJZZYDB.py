# -*- coding: utf-8 -*-
#############
# 真言地板(九字真言)
#############
import KBEngine
import ObjectScript.Monster.Monster as Monster


class MonsterExtJZZYDB( Monster.Monster ):
	"""
	地板
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.zhenYanType = 0
		
	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		self.zhenYanType = int(configData["Param1"])
