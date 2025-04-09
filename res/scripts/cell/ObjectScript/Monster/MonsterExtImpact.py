# -*- coding: utf-8 -*-

import KBEngine
import ObjectScript.Monster.Monster as Monster


class MonsterExtImpact( Monster.Monster ):
	"""
	撞击怪物脚本
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.playAction = ""
		self.delayTime = 0.0
		self.buffIDs = []

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		self.playAction = configData["Param1"]
		if configData["Param2"]:
			self.delayTime = float(configData["Param2"])
		if configData["Param3"]:
			self.buffIDs = [ int(i) for i in configData["Param3"].split("|") ]

