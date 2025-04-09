# -*- coding:utf-8 -*-
from LoadModule import *
import KBEDebug
import random

class ChuanChengSkillLoader:
	"""传承技能"""
	def __init__(self):
		self.skillLearnConfig = {}

	def loadConfig( self ):
		config = openJsonCfg("ChuanCheng/ChuanChengSkillLearnConfig.json")
		for data in config:
			self.skillLearnConfig[int(data["ID"])] = data

	def reloadConfig(self):
		self.skillLearnConfig.clear()
		self.loadConfig()

	def getSkillLearnData( self, skillID ):
		"""获取技能学习相关条件"""
		return self.skillLearnConfig.get( skillID, None )

	def getReqLevel(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["ReqLevel"]
		return 0
		
	def getNextSkill(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["NextLevelID"]
		return 0

	def getNextReqSkill(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["ReqSkill"]
		return 0

	def getNeedMoney(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["Money"]
		return 0

	def getNeedPotential(self, skillID):
		if skillID in self.skillLearnConfig:
			return self.skillLearnConfig[skillID]["ReqPotential"]
		return 0


g_ChuanChengSkillLoader = ChuanChengSkillLoader()