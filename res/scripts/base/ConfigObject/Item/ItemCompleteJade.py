# -*- coding: utf-8 -*-

import ConfigObject.Item.ItemSpell as ItemSpell

class ItemCompleteJade(ItemSpell.ItemSpell):
	"""
	完整的玉玦
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)
