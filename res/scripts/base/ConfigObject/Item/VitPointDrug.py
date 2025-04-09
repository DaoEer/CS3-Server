# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemSpell as ItemSpell

class VitPointDrug(ItemSpell.ItemSpell):
	"""
	增加玩家饱食度药品
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)