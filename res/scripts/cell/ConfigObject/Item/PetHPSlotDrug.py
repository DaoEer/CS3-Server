# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemSpell as ItemSpell
import csstatus

class PetHPSlotDrug(ItemSpell.ItemSpell):
	"""
	幻兽血槽药品
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)

	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		if owner.petExtraHP == owner.petExtraHP_Max:
			return csstatus.PET_HPSLOT_IS_FULL

		return ItemSpell.ItemSpell.checkUse( self, owner )