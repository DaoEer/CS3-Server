# -*- coding:utf-8 -*-
from LoadModule import *
import KBEDebug
import random

class ShenTongSkillLoader:
	"""神通技能"""
	def __init__(self):
		self.comminutionConfig = {}

	def loadConfig( self ):
		config = openJsonCfg("ShenTong/ShenTongSkillComminution.json")
		for data in config:
			self.comminutionConfig[data["SkillID"]] = data

	def reloadConfig(self):
		self.comminutionConfig.clear()
		self.loadConfig()

	def getNextShenTongSkill(self, skillID):
		if skillID in self.comminutionConfig:
			return self.comminutionConfig[skillID]["NextSKillID"]
		return 0

	def getShenTongNeedMoney(self, skillID):
		if skillID in self.comminutionConfig:
			return self.comminutionConfig[skillID]["NeedMoney"]
		return 0

	def getShenTongNeedPotential(self, skillID):
		if skillID in self.comminutionConfig:
			return self.comminutionConfig[skillID]["NeedPotential"]
		return 0
	def getShenTongNeedExp(self, skillID):
		if skillID in self.comminutionConfig:
			return self.comminutionConfig[skillID]["NeedExp"]
		return 0

g_ShenTongSkillLoader = ShenTongSkillLoader()