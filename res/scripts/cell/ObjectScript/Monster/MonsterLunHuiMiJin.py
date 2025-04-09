# -*- coding: utf-8 -*-
import ObjectScript.Monster.Monster as Monster
import csdefine

class MonsterLunHuiMiJin( Monster.Monster ):
	"""
	轮回秘境 -- 有远程攻击属性怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.quality = 0
		self.itemPetEgg = 0

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		if configData[ "Param1" ]:
			self.quality = int(configData[ "Param1" ])
		if configData[ "Param2" ]:
			self.itemPetEgg = int(configData[ "Param2" ])