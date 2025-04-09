# -*- coding: utf-8 -*-

import KBEDebug
import Const
import csstatus
import random
import ItemTypeEnum
import ConfigObject.Item.ItemBase as ItemBase
from Reward.RewardBasicValueData import datas

class ItemIntensifySymbol(ItemBase.ItemBase):
	"""
	回火材料
	"""
	def __init__(self, srcData):
		ItemBase.ItemBase.__init__(self, srcData)
#		self.intensifyType = ItemTypeEnum.ITEM_HUIHUO
		self.intensifyType = int( srcData["Param1"] )