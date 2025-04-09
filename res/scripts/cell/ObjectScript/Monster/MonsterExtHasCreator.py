# -*- coding: utf-8 -*-

#------------------
#专属怪
#------------------

import ObjectScript.Monster.Monster as Monster

class MonsterExtHasCreator( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.destroyTime = 0

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		if configData["Param1"]:
			self.destroyTime = float(configData["Param1"])

	def getDestroyTime(self):
		return self.destroyTime