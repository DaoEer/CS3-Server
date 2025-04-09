# -*- coding:utf-8 -*-
from LoadModule import *

class LingQuanProduceLoader:
	"""
	灵全泉产出配置
	"""
	def __init__(self):
		self.config = {}

	def loadConfig( self ):
		config = openJsonCfg("LunHuiMiJin/LingQuanProduceCfg.json")
		for data in config:
			self.config[int(data["Name"])] = data

	def reloadConfig( self ):
		self.config.clear()
		self.loadConfig()

	def getLingQuanTimeKey( self, lingQuanLevel ):
		"""
		获取产出的间隔时间(单位：分钟)
		"""
		return self.config[lingQuanLevel]["timeKey"] * 60

	def getOutLingQuanAmount( self, lingQuanLevel ):
		"""
		获取在每隔多少时间产出的灵能数
		"""
		return self.config[lingQuanLevel]["outLingNengAmount"]

	def getLingNengMaxAmount( self, lingQuanLevel ):
		"""
		获取产出最大的灵能数
		"""
		return self.config[lingQuanLevel]["lingNengMaxAmount"]

	def getLingQuanMaxHP( self, lingQuanLevel ):
		"""
		获取灵泉最大血量值
		"""
		return self.config[lingQuanLevel]["lingQuanMaxHP"]

g_LingQuanProduceLoader = LingQuanProduceLoader()