# -*- coding:utf-8 -*-
import Math
import KBEMath
import Functions
from LoadModule import *


class TongSpaceCopyRewardLoader:
	"""
	帮会副本奖励配置
	"""
	def __init__(self):
		self.data = {}
	
	def loadConfig( self, path ):
		config = openJsonCfg(path)
		for data in config:
			self.data.setdefault(data["scriptID"], {})
			buffs = [int(buff) for buff in data["buff"].split("|") if data["buff"]]
			data["buffList"] = buffs
			self.data[data["scriptID"]][data["grade"]] = data
	
	def reloadConfig(self, path):
		self.data.clear()
		self.loadConfig(path)
		
	def getCfgByScriptIDAndValue(self, scriptID, value):
		"""
		"""
		if scriptID in self.data:
			for _, cfg in self.data[scriptID].items():
				if cfg["lower"] <= value and value <= cfg["upper"]:
					return cfg
		return None

g_TongSpaceCopyRewardLoader = TongSpaceCopyRewardLoader()