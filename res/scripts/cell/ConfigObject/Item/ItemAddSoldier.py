# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemUse as ItemUse
import csstatus
import csdefine

class ItemAddSoldier(ItemUse.ItemUse):
	"""
	添加士兵道具
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)

		self.sildierType = int(srcData["Param1"])
		self.scriptID = srcData["Param2"]
		self.level = int(srcData["Param3"])
		self.count = int(srcData["Param4"])
		
	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		if not owner.checkBarracksCount(self.sildierType, self.scriptID, self.count):
			return csstatus.USE_ITEM_FORBID_BY_STATE

		return ItemUse.ItemUse.checkUse( self, owner )
		
	def use(self, owner, target):
		"""
		使用
		"""
		ItemUse.ItemUse.use(self, owner, target)
		
		owner.addSoldier(self.sildierType, self.scriptID, self.level, self.count)
		
		owner.removeItemByAmount( self, 1, csdefine.ITEM_REMOVE_BY_USE )