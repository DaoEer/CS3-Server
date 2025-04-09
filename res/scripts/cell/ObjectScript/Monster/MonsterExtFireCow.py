# -*- coding: utf-8 -*-
#############
# 火焰牛魔
#############

import ObjectScript.Monster.Monster as Monster


class MonsterExtFireCow( Monster.Monster ):
	"""
	火焰牛魔
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.recoverValue = 0
		self.aiCmd = ""
		
	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		self.aiCmd = configData["Param1"]
		if configData["Param2"]:
			self.recoverValue = int(configData["Param2"])

	def getAICmd(self):
		return self.aiCmd

	def getRecoverValue(self):
		return self.recoverValue