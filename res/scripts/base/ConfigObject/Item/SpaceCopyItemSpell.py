# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemSpell as ItemSpell
import csstatus

class SpaceCopyItemSpell(ItemSpell.ItemSpell):
	"""
	副本专用物品
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)
