# -*- coding:utf-8 -*-
from LoadModule import *


class SpaceCopyLLBZRewardsLoader:
	"""
	玲珑宝珠 奖励配置
	"""
	def __init__(self):
		self.config = {}

	def loadConfig( self ):
		config = openJsonCfg("SpaceCopyLLBZRewards.json")
		for data in config:
			self.config[data["level"]] = data


	def reloadConfig(self):
		self.config.clear()
		self.loadConfig()

	def getLLBZExpRewards(self, level):
		if level in self.config:
			return self.config[level]["exp"]
		return 0

	def getLLBZMoneyRewards(self, level):
		if level in self.config:
			return self.config[level]["money"]
		return 0

	def getLLBZPotentialRewards(self, level):
		if level in self.config:
			return self.config[level]["potential"]
		return 0


g_SpaceCopyLLBZRewards = SpaceCopyLLBZRewardsLoader()