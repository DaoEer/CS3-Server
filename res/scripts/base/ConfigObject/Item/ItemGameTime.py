# -*- coding: utf-8 -*-

import ConfigObject.Item.ItemUse as ItemUse


class ItemGameTime(ItemUse.ItemUse):
	"""
	充值游戏时长
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)