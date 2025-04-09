# -*- coding: utf-8 -*-

import KBEDebug
import Const
import csstatus
import random
import ItemTypeEnum
import ConfigObject.Item.ItemBase as ItemBase
from Reward.RewardBasicValueData import datas

class ItemIntensifyCrystal(ItemBase.ItemBase):
	"""
	强化材料
	玄晶\五彩玄晶\超级玄晶
	"""
	def __init__(self, srcData):
		ItemBase.ItemBase.__init__(self, srcData)
#		self.intensifyType = ItemTypeEnum.ITEM_XUANJING
		self.intensifyType = int( srcData["Param1"] )
		