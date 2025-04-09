# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemSpell as ItemSpell
import ItemTypeEnum

class ItemQuest(ItemSpell.ItemSpell):
	"""
	任务物品
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)

