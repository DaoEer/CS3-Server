# -*- coding: utf-8 -*-


"""
usage:
	被动技能栏配置

attribute:
	pass

member function:
	pass

callback:
	pass

"""

import KBEngine
#common
import Singleton
import KBEDebug
import LoadModule
import SmartImport
import csconst
import json
import csdefine

class PassiveSkillBarLoader( Singleton.Singleton ):
	"""
	被动技能栏配置
	"""
	def __init__( self ):
		self._datas = {}
	
	def __getitem__( self, index ):
		return self._datas.get( index, None )
		
	def getItem( self, index ):
		return self._datas.get(index, None)
		
	def getDatas(self):
		return self._datas
	
	def reloadConfig( self ):
		"""
		被动技能栏配置热更新支持
		"""
		self._datas.clear()
		self.loadConfig()
		return True
		
	def loadConfig( self ):
		datas = LoadModule.openJsonCfg("Skill/SkillConfigs/PassiveSkillBarData.json")
		for data in datas:
			tmp = {}
			tmp["id"] = int(data["id"])
			tmp["money"] = int(data["money"])
			tmp["isLock"] = int(data["isLock"])
			tmp["level"] = int(data["level"])
			tmp["xianshi"] = int(data["xianshi"])
			
			tmp["material"] = {}
			if data["material_1"]: tmp["material"][data["material_1"]] = int(data["mNum_1"])
			if data["material_2"]: tmp["material"][data["material_2"]] = int(data["mNum_2"])
			if data["material_3"]: tmp["material"][data["material_3"]] = int(data["mNum_3"])
			self._datas[int(data["id"])] = tmp


g_passiveSkillBars = PassiveSkillBarLoader()
g_passiveSkillBars.loadConfig()


