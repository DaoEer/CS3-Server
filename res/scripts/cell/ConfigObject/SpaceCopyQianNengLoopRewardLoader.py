# -*- coding:utf-8 -*-
from LoadModule import *


class SpaceCopyQianNengLoopRewardLoader:
	"""
	潜能副本环数和玩法 奖励配置（CST-11294）
	"""
	def __init__(self):
		self.config = {}

	def loadConfig( self ):
		config = openJsonCfg("QianNengSpaceLoopReward.json")
		for c in config:
			if c["Loop"] not in self.config:
				self.config[c["Loop"]] = {}
			self.config[c["Loop"]][c["Index"]] = c["Multiple"]

	def reloadConfig( self ):
		self.config.clear()
		self.loadConfig()

	def getRewardRate( self, loop, index ):
		"""
		获取不同阶段的奖励数据
		"""
		return self.config.get(loop, {}).get(index, 1.0)

g_SpaceCopyQianNengRewardsLoader = SpaceCopyQianNengLoopRewardLoader()