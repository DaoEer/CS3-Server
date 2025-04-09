# -*- coding: utf-8 -*-

import ConfigObject.Item.ItemUse as ItemUse

class ItemApparatus(ItemUse.ItemUse):
	"""
	任务物品
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)