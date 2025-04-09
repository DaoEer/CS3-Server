# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemSpell as ItemSpell

class PetMPSlotDrug(ItemSpell.ItemSpell):
	"""
	幻兽蓝槽药品
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)