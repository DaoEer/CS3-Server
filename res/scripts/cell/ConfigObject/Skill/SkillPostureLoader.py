import KBEngine

#common
import Singleton
import KBEDebug
import csconst
import json
from LoadModule import *
from EquipPropertyParse import g_EquipPropertyLoadInst


class SkillPostureLoader(Singleton.Singleton):
	"""
	技能心法配置加载
	"""
	def __init__(self ):
		self._datas = {}

	def getData( self, skillPosture, level ):
		if skillPosture not in self._datas:
			return None
		return self._datas[skillPosture].get( level, None )

	def loadAllPosture(self):
		"""
		加载数据
		"""
		Datas = []
		Datas = openJsonCfg("Skill/SkillConfigs/SkillPostureConfig.json")
		for Data in Datas:
			if Data["PostureType"] in self._datas:				
				self._datas[Data["PostureType"]].update({Data["PostureLevel"]:Data})
			else:
				self._datas.update({Data["PostureType"]:{Data["PostureLevel"]:Data}})


	def reloadConfig( self ):
		"""
		技能热更新
		"""
		try:
			openJsonCfg("Skill/SkillConfigs/SkillPostureConfig.json")
			self._datas.clear()
			self.loadAllPosture()
			return True
		except:
			return False

	def getAttackPropertiesStr(self, skillPosture, level ):
		"""
		获取战斗属性
		"""
		attackProperties = {}
		if skillPosture not in self._datas:
			return attackProperties
		Data = self._datas[skillPosture].get( level, None )
		if not Data:
			return attackProperties
		PropertyID = Data["PropertyID"]
		if PropertyID:
			attackProperties = g_EquipPropertyLoadInst.getDataByID(int(PropertyID))

		return attackProperties


g_skillPosture = SkillPostureLoader()
g_skillPosture.loadAllPosture()