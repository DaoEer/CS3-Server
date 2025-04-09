# -*- coding:utf-8 -*-
from LoadModule import *
import KBEDebug
import random

class PetSkillLearnLoader:
	"""读取幻兽技能学习的配置"""
	def __init__(self):
		self.skillLearnConfig = {}

	def loadConfig( self ):
		config = openJsonCfg("Skill/SkillConfigs/petSkillLearnConfig.json")
		for data in config:
			self.skillLearnConfig[int(data["ID"])] = data

	def reloadConfig(self):
		self.skillLearnConfig.clear()
		self.loadConfig()

	def getskilldata( self, skillid ):
		if skillid in self.skillLearnConfig.keys():
			return self.skillLearnConfig[skillid]
		return None

	def getLevel(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["Level"]
		return 0

	def getReqLevel(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["ReqLevel"]
		return 0
		
	def getNextSkill(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["NextLevelID"]
		return 0

	def getReqSkill(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["ReqSkill"]
		return 0

	def getReqPotential(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["ReqPotential"]
		return 0

	def getMoney(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["Money"]
		return 0

	def getSkillBook(self, skillID):
		SkillBook = 0
		if skillID in self.skillLearnConfig:
			 if self.skillLearnConfig[skillID]["SkillBook"]:
			 	SkillBook = int(self.skillLearnConfig[skillID]["SkillBook"])
		return SkillBook
		
g_PetSkillLearn = PetSkillLearnLoader()