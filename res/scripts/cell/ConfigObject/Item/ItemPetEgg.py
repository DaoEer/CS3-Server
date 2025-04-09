# -*- coding: utf-8 -*-

import KBEDebug
import Const
import csstatus
import random
import ItemTypeEnum
import ConfigObject.Item.ItemSpell as ItemSpell
from Reward.RewardBasicValueData import datas

class ItemPetEgg(ItemSpell.ItemSpell):
	"""
	幻兽蛋
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)


	def onUseResult(self, owner, useResult ):
		"""
		使用物品结果
		"""
		if not useResult:
			return

		ItemSpell.ItemSpell.onUseResult(self, owner, useResult )