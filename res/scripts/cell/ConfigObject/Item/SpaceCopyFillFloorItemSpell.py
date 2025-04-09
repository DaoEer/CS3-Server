# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemSpell as ItemSpell
import csstatus

class SpaceCopyFillFloorItemSpell(ItemSpell.ItemSpell):
	"""
	副本填充格子物品 CST-6096 仙岛归墟
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)
