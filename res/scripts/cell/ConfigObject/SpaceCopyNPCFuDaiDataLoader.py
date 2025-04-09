# -*- coding:utf-8 -*-
from LoadModule import *
import KBEDebug
import random

MONSTER_DROP = ["10000976", "10000977", "10000978", "10000979", "10000980", "10000981", "10000982", "10000983"]
class SpaceCopyNPCFuDaiDataLoader:
	"""副本--福袋NPC配置"""
	def __init__(self):
		self.config = {}

	def loadConfig( self ):
		config = openJsonCfg("SpaceCopyNPCFuDaiData.json")
		for data in config:
			self.config[data["scriptID"]] = data

	def reloadConfig(self):
		self.config.clear()
		self.loadConfig()

	def getRandomScriptIDOutList(self):
		"""
		"""
		scriptIDList = list(self.config)
		for i in MONSTER_DROP:
			if i in scriptIDList:
				scriptIDList.remove(i)
		random.shuffle(scriptIDList)
		return scriptIDList[0]

	def getEffect(self, scriptID, index):
		if scriptID in self.config:
			effectList = self.config[scriptID]["effectIDs"].split("|")
			if len(effectList) == 1:
				return effectList[0]
			if len(effectList) > index:
				return effectList[index]
		return ""

	def isOneEffect(self, scriptID):
		if scriptID in self.config:
			effectList = self.config[scriptID]["effectIDs"].split("|")
			return len(effectList) == 1
		return False

	def getDropSound(self, scriptID, index):
		if scriptID in self.config:
			SoundList = self.config[scriptID]["dropSound"].split("|")
			if len(SoundList) == 1:
				return SoundList[0]
			if len(SoundList) > index:
				return SoundList[index]
		return ""

	def isOneDropSound(self, scriptID):
		if scriptID in self.config:
			SoundList = self.config[scriptID]["dropSound"].split("|")
			return len(SoundList) == 1
		return False

	def getrewardEffect(self, scriptID):
		if scriptID in self.config:
			return self.config[scriptID]["rewardEffectID"]
		return ""

	def getmonsterEffect(self, scriptID):
		if scriptID in self.config:
			return self.config[scriptID]["monsterEffectID"]
		return ""

	def getDestroyTime(self, scriptID):
		if scriptID in self.config:
			return self.config[scriptID]["destroyTime"]
		return 0.0

	def getAllRewardsList(self, scriptID):
		if scriptID in self.config:
			reward = int(self.config[scriptID]["rewardIDs"])
			return reward
		return 0

	def getResistance(self, scriptID):
		if scriptID in self.config:
			return self.config[scriptID]["resistance"]
		return 0.0

	def getMonster(self, scriptID):
		if scriptID in self.config:
			string = self.config[scriptID]["monster"]
			if not string:
				return []
			strList = string.split("|")
			List = [strList[0], float(strList[1]), float(strList[2]), strList[3]]
			return List
		return []

	def getRewardSound(self, scriptID, rewardID):
		if scriptID in self.config:
			SoundList = self.config[scriptID]["rewardSound"].split("|")
			for string in SoundList:
				i = string.split(":")
				if rewardID == i[0]:
					return i[1]
		return ""

	def getRewardRate(self, scriptID, stage):
		if scriptID in self.config:
			List = self.config[scriptID]["rate"].split("|")
			if stage < int(List[0]):
				return 1.0
			rNum = random.randint(0, 10000)
			if rNum <= int(List[1]):
				return 1.0
			elif rNum > int(List[1]) and rNum <= (int(List[1])+int(List[2])):
				return 2.0
			elif rNum > (int(List[1])+int(List[2])) and rNum <= (int(List[2])+int(List[3])):
				return 0.5

		return 1.0


	def getRewardRateSoundID(self, scriptID, rate):
		if scriptID in self.config:
			if not self.config[scriptID]["rateSound"]:
				return ""
			List = self.config[scriptID]["rateSound"].split("|")
			if rate > 1.0:
				return List[0]
			elif rate < 1.0:
				return List[1]
		return ""

	def getCreateBuffID(self, scriptID):
		if scriptID in self.config:
			return self.config[scriptID]["createBuffID"]
		return 0

g_SpaceCopyNPCFuDaiData = SpaceCopyNPCFuDaiDataLoader()