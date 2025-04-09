# -*- coding: utf-8 -*-

import LoadModule
import CampMoraleConfig

class CampMoraleConfigLoader(object):
	__instance=None
	def __new__(cls):
		if cls.__instance==None:
			cls.__instance = object.__new__(cls)
			return  cls.__instance
		else:
			return cls.__instance

	def __init__( self ):
		self._moraleDifTuple = ()
		self._moraleSkills = ()
		self._moraleTuple = ()
		self._moraleRewards = ()
		self._titleRewards = {}
		self.init()

	def init(self):
		keyList = sorted(CampMoraleConfig.Datas, key = lambda i: i, reverse=False )
		valuesList = []
		for i in keyList:
			valuesList.append(CampMoraleConfig.Datas[i])
		self._moraleDifTuple = tuple(keyList)
		self._moraleSkills = tuple(valuesList)


	def loadConfig(self ):
		"""
		读取CampMoraleReward配置
		"""
		Datas = LoadModule.openJsonCfg( "CampMoraleReward.json" )
		tempDict={}
		for data in Datas:
			if data["title"]:
				self._titleRewards[data["title"]] = data["rewardID"]
			else:
				tempDict[data["morale"]] = data["rewardID"]

		keyList2 = sorted(tempDict, key = lambda i: i, reverse=False )
		valuesList2 = []
		for i in keyList2:
			valuesList2.append(tempDict[i])
		self._moraleTuple = tuple(keyList2)
		self._moraleRewards = tuple(valuesList2)

	def reloadConfig(self):
		"""
		配置热更新
		"""
		self._moraleTuple = ()
		self._moraleRewards = ()
		self._titleRewards.clear()
		self.loadConfig()

	def getMoraleSkillID( self, moraleDif ):
		"""
		根据气运差，获取相对应的技能id
		@moraleDif : 气运差，可以为负，小于 self._moraleDifTuple[0] 时，技能id为 self._moraleSkills[0]
					 moraleDif落于区间 [ self._moraleDifTuple[i], self._moraleDifTuple[i+1] ) 时，
					 技能id为 self._moraleSkills[i]
		"""
		if not len(self._moraleDifTuple):
			return []
		if moraleDif < self._moraleDifTuple[0] :
			return self._moraleSkills[0]
		lenDif = len( self._moraleDifTuple )
		index = 0
		while index < lenDif - 1 :
			if self._moraleDifTuple[index] <= moraleDif < self._moraleDifTuple[index+1] :
				break
			else :
				index += 1
		return self._moraleSkills[index]


	def getAllMoraleSkillID( self, moraleDif ):
		"""
		根据士气差，获取所有小于该士气差对应的技能id
		@moraleDif : 士气差，可以为负
		"""
		if not len(self._moraleDifTuple):
			return []
		if moraleDif < self._moraleDifTuple[0] :
			return [ self._moraleSkills[0] ]
		
		lenDif = len( self._moraleDifTuple )
		index = 0
		while index < lenDif - 1 :
			if self._moraleDifTuple[index] <= moraleDif < self._moraleDifTuple[index+1] :
				break
			else :
				index += 1
		return list( self._moraleSkills[0:index] )

	def getRewardIDByMorale(self, morale):
		"""
		通过气运获得奖励
		"""
		if not len(self._moraleTuple):
			return []
		if morale < self._moraleTuple[0] :
			return self._moraleRewards[0]
		lenDif = len( self._moraleTuple )
		index = 0
		while index < lenDif - 1 :
			if self._moraleTuple[index] <= moraleDif < self._moraleTuple[index+1] :
				break
			else :
				index += 1
		return [self._moraleRewards[index]]


	def getRewardIDByTitle(self, title):
		"""
		通过称号获得奖励
		"""
		if title in self._titleRewards:
			Rewards = self._titleRewards[title]
			RewardList = [int(i) for i in Rewards.split("|")]
			return RewardList



g_campMoraleConfig = CampMoraleConfigLoader()