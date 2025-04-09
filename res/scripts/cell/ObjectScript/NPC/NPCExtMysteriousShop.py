# -*- coding: utf-8 -*-
from ObjectScript.NPC import NPC

class NPCExtMysteriousShop( NPC.NPC ):
	def __init__( self ):
		NPC.NPC.__init__( self )
		self.lifeTime = 0		#神秘商人出现时长
		
	def initData(self, configData):
		"""
		初始化数据
		@param data: dict
		"""
		NPC.NPC.initData(self, configData)
		if configData["Param1"]:
			self.lifeTime = float(configData["Param1"])
		
	