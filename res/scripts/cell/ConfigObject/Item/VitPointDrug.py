# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemSpell as ItemSpell
import csstatus

class VitPointDrug(ItemSpell.ItemSpell):
	"""
	增加玩家饱食度药品
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)

	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		if owner.vitPoint == owner.vitPoint_Max:
			return csstatus.LHMJ_PLAYER_VIT_POINT_IS_FULL

		return ItemSpell.ItemSpell.checkUse( self, owner )