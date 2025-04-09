# -*- coding: utf-8 -*-

import KBEDebug
import csstatus
import csdefine
import ItemTypeEnum
import ConfigObject.Item.ItemUse as ItemUse
import copy
import ItemFactory

class ItemGift( ItemUse.ItemUse ):
	"""
	礼包
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self.giftID = srcData.get("Param1")	#奖励ID
		self._values = []	#根据奖励ID生成的经验等数值奖励
		self._items = []	#根据奖励ID生成的物品奖励奖励
	