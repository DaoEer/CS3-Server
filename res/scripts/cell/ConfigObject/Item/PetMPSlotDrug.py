# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemSpell as ItemSpell
import csstatus

class PetMPSlotDrug(ItemSpell.ItemSpell):
	"""
	幻兽蓝槽药品
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)

	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		if owner.petExtraMP == owner.petExtraMP_Max:
			return csstatus.PET_MPSLOT_IS_FULL
			
		return ItemSpell.ItemSpell.checkUse( self, owner )