# -*- coding: utf-8 -*-

import KBEDebug
import Const
import csstatus
import random
import ItemTypeEnum
import ConfigObject.Item.ItemBase as ItemBase
from Reward.RewardBasicValueData import datas

class ItemShuffle(ItemBase.ItemBase):
	"""
	洗练/重铸材料
	洗练石\重铸宝珠
	"""
	def __init__(self, srcData):
		ItemBase.ItemBase.__init__(self, srcData)
#		self.intensifyType = ItemTypeEnum.ITEM_WASH
		self.intensifyType = int( srcData["Param1"] )
