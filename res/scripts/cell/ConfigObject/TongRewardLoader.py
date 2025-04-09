# -*- coding:utf-8 -*-
import Math
import KBEMath
import Functions
from LoadModule import *


class TongRewardLoader:
	"""
	帮会相关奖励配置加载（帮会争霸/帮会掠夺）
	"""
	def __init__(self):
		self.data = {}
	
	def loadConfig( self, path ):
		config = openJsonCfg(path)
		for data in config:
			lst = []
			if data["reward"]:
				rewardList = data["reward"].split("|")
				for reward in rewardList:
					lst.append(reward)
					
			position = (0.0, 0.0, 0.0)
			if data["position"]:
				ue4pos = Functions.vector3TypeConvert(data["position"])
				position = KBEMath.Unreal2KBEnginePosition(ue4pos)
			
			direction = (0.0, 0.0, 0.0)
			if data["direction"]:
				ue4dir = Functions.vector3TypeConvert(data["direction"])
				direction = KBEMath.Unreal2KBEngineDirection(ue4dir)
				
			modelScale = 1.0
			if data["modelScale"] > 0:
				modelScale = data["modelScale"]
			
			self.data[data["key"]] = {"position" : position, "direction" : direction, "reward" : lst, "modelNumber" : data["modelNumber"], "modelScale" : modelScale}
	
	def reloadConfig(self, path):
		self.data.clear()
		self.loadConfig(path)
		
	def getConfigByKey(self, key):
		return self.data.get(key, None)

g_TongRewardLoader = TongRewardLoader()