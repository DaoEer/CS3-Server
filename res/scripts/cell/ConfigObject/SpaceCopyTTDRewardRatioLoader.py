# -*- coding:utf-8 -*-
from LoadModule import *


class SpaceCopyTTDRewardRatioLoader:
	"""
	通天塔 奖励系数配置
	"""
	def __init__(self):
		self.config = {}

	def loadConfig( self ):
		config = openJsonCfg("SpaceCopyTTDRewardRatio.json")
		self.config = config


	def reloadConfig( self ):
		self.config.clear()
		self.loadConfig()

	def getRewardRatioData( self, septum ):
		"""
		获取不同阶段的奖励数据
		"""
		moneyRatio = self.config[ septum ][ "moneyRatio" ]
		expRatio = self.config[ septum ][ "expRatio" ]
		rewardRatio = self.config[ septum ][ "rewardRatio" ]
		extraRewardID = str(self.config[ septum ][ "extraRewardID" ])
		return moneyRatio, expRatio, rewardRatio, extraRewardID

g_SpaceCopyTTDRewardRatioLoader = SpaceCopyTTDRewardRatioLoader()