# -*- coding:utf-8 -*-
import Functions
from LoadModule import *


class AuctionCfgLoader:
	"""
	物品竞拍配置
	"""
	def __init__(self):
		self.data = {}
		self.maxIndex = 0
	
	def init( self, config ):
		for data in config:
			self.data[(data["index"])] = data
			if int(data["index"]) > self.maxIndex:
				self.maxIndex = int(data["index"])
	
	def getCfByIndex(self, index):
		"""
		"""
		#竞拍轮数大于配置最大值后，使用最大配置值
		if index in self.data:
			return self.data[index]
		return self.data.get(self.maxIndex, None)

g_AuctionCfgLoader = AuctionCfgLoader()