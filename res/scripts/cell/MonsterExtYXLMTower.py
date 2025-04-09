# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import MonsterExtMain
import KBEDebug
from ConfigObject.SpaceCopyYXLMMonsterDataLoader import g_spaceCopyYXLMMonsterDataLoader
import ItemSystemExp
import csconst

class MonsterExtYXLMTower( MonsterExtMain.MonsterExtMain ):
	"""
	英雄联盟 （防御塔）
	"""
	def __init__( self ):
		MonsterExtMain.MonsterExtMain.__init__( self )
		if self.getScript().param2:
			self.wayType = int(self.getScript().param2)

	def addExp( self, value ):
		"""
		增加经验
		"""
		pass
	
	def getBaseProperties(self):
		"""
		通过配置获取基础属性数值
		@return: dict {propertyID: value}
		"""
		if self.levelYXLM == 1:
			return ItemSystemExp.g_SpaceCopyYXLMMonsterPropertyValueCfg_1.getData( self.profession, self.attrLevel, self.level)
		elif self.levelYXLM == 2:
			return ItemSystemExp.g_SpaceCopyYXLMMonsterPropertyValueCfg_2.getData( self.profession, self.attrLevel, self.level)
		elif self.levelYXLM == 3:
			return ItemSystemExp.g_SpaceCopyYXLMMonsterPropertyValueCfg_3.getData( self.profession, self.attrLevel, self.level)
	
	
