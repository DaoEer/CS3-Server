# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemQuest as ItemQuest
import ItemTypeEnum

class ItemUseTorture(ItemQuest.ItemQuest):
	"""
	任务物品
	"""
	def __init__(self, srcData):
		ItemQuest.ItemQuest.__init__(self, srcData)

	def isQuestItem(self):
		"""
		是否为任务物品, 放在任务背包中的物品
		"""
		return True

