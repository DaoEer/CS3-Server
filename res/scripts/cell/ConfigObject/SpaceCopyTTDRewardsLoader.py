# -*- coding:utf-8 -*-
from LoadModule import *


class SpaceCopyTTDRewardsLoader:
	"""
	通天塔 奖励配置
	"""
	def __init__(self):
		self.config = {}
		self.tongTianCfg = {}

	def loadConfig( self ):
		config = openJsonCfg("SpaceCopyTTDRewards.json")
		self.config = config
		ttconfig = openJsonCfg("LunHuiMiJin/TongTianDaCfg.json")
		for key, value in ttconfig.items():
			self.tongTianCfg[int(key)] = value

	def reloadConfig( self ):
		self.config.clear()
		self.loadConfig()
		
	def getLayerNumberByScriptID( self, scriptID ):
		""""""
		for layer, spaceScriptID in self.tongTianCfg.items():
			if spaceScriptID == scriptID:
				return layer
		return 0
		
	def getMaxLayerNumber( self ):
		""""""
		return max( self.tongTianCfg )

	def getRewardData( self, layerNumber, index ):
		"""
		获取不同阶段的奖励数据
		"""
		money = self.config[layerNumber][index]["money"]
		exp = self.config[layerNumber][index]["exp"]
		rewardID = str( self.config[layerNumber][index]["rewardID"])
		return money, exp, rewardID

g_SpaceCopyTTDRewards = SpaceCopyTTDRewardsLoader()