# -*- coding:utf-8 -*-
import random
import Functions
import KBEMath
from LoadModule import *


class JiYuanCfgLoader:
	"""
	机缘玩法配置加载（CST-12205）
	"""
	def __init__(self):
		self.data = {}
	
	def loadConfig( self, path ):
		config = openJsonCfg(path)
		for id, data in config.items():
			data["position"] = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert(data["position"]))
			data["direction"] = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert(data["direction"]))
			self.data[id] = data

	def reloadConfig(self, path):
		self.loadConfig(path)
	
	def getAllData(self):
		return self.data
		
	def getCfgByID(self, id):
		return self.data.get(id, None)

g_jiYuanCfgLoader = JiYuanCfgLoader()