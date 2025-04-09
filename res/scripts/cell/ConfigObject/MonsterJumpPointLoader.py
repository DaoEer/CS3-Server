# -*- coding:utf-8 -*-
from LoadModule import *
import MonsterJumpPointCfgNew
import KBEDebug
import Functions
import KBEMath
import copy

class MonsterJumpPointLoader:
	"""读取怪物跳跃点的配置"""
	def __init__(self):
		self.monsterJumpPointConfig = {}
		self.monsterJumpPointConfigNew = {}
		self.minRouteMap ={}

	def loadConfig( self ):
		config = openJsonCfg("MonsterJumpPointCfg.json")
		for data in config:
			if data["spaceID"] not in self.monsterJumpPointConfig:
				self.monsterJumpPointConfig[data["spaceID"]] = []
			tempDict = {"beginPoint":data["beginPoint"], "endPoint":data["endPoint"], "jumpHeight":data["jumpHeight"]}
			self.monsterJumpPointConfig[data["spaceID"]].append(tempDict)

		confignew = copy.deepcopy(MonsterJumpPointCfgNew.Datas)
		for spaceID, datas in confignew.items():
			if spaceID not in self.monsterJumpPointConfigNew:
				self.monsterJumpPointConfigNew[spaceID] = {}

			jumpArea = datas["jumpArea"]
			for key,value in jumpArea.items():
				positionList = []
				for position in value["positionList"]:
					_position = Functions.vector3TypeConvert(position)
					if _position:
						_position = KBEMath.Unreal2KBEnginePosition(_position)
						positionList.append(_position)
					else:
						KBEDebug.ERROR_MSG("error area = %s, error position = %s"%(key, position))
				jumpArea[key]["positionList"] = positionList
				
				centerPos = Functions.vector3TypeConvert(value["centerPos"])
				if centerPos:
					jumpArea[key]["centerPos"] = KBEMath.Unreal2KBEnginePosition(centerPos)
				else:
					KBEDebug.ERROR_MSG("error area = %s, error centerPos = %s"%(key, value["centerPos"]))
				

			self.monsterJumpPointConfigNew[spaceID] = datas

			if spaceID not in self.minRouteMap:
				self.minRouteMap[spaceID] = {}

	def getMonsterJumpPointdata( self, spaceID ):
		if spaceID in self.monsterJumpPointConfig.keys():
			return self.monsterJumpPointConfig[spaceID]
		return []

	def getMonsterJumpPointdataNew(self, spaceID):
		"""
		"""
		if not spaceID in self.monsterJumpPointConfigNew:
			KBEDebug.ERROR_MSG("spaceID = %s not in self.monsterJumpPointConfigNew"%spaceID)
			return None
		return self.monsterJumpPointConfigNew[spaceID]

	def getJumpRoute(self,spaceData, startPoint, endPoint):
		"""
		"""
		KBEDebug.ERROR_MSG("startPoint = %s, endPoint = %s"%(startPoint, endPoint))
		for route in spaceData["jumpRoute"].values():
			if startPoint in route and endPoint in route:
				idxs = route.index(startPoint)
				idxe = route.index(endPoint)
				if idxs < idxe:
					return route[idxs:idxe+1]
		return []

	def reloadConfig(self):
		self.monsterJumpPointConfig.clear()
		self.monsterJumpPointConfigNew.clear()
		self.loadConfig()



		
g_MonsterJumpPoint = MonsterJumpPointLoader()