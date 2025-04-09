# -*- coding: utf-8 -*-

import KBEDebug
import Const
import csstatus
import random
import ItemTypeEnum
import ConfigObject.Item.ItemBase as ItemBase
from Reward.RewardBasicValueData import datas

class ItemIntensifySpar(ItemBase.ItemBase):
	"""
	强化附加材料
	晶石\五彩晶石\超级晶石
	"""
	def __init__(self, srcData):
		ItemBase.ItemBase.__init__(self, srcData)
#		self.intensifyType = ItemTypeEnum.ITEM_WHITESPAR
		self.intensifyType = int( srcData["Param1"] )
		self.goldProbability = float( srcData["Param2"] )			# 金星概率加成
		self.silberProbability = float( srcData["Param3"] )			# 银星概率加成