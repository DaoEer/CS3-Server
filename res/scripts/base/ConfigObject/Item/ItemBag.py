# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemUse as ItemUse

class ItemBag(ItemUse.ItemUse):
	"""
	扩展背包物品
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemUse.ItemUse.__init__(self, srcData)
		self.gridNum = int(srcData.get("Param1"))	#扩展背包格子数

	def checkUse(self, owner):
		"""
		"""
		return ItemUse.ItemUse.checkUse( self, owner )
		
	def use(self):
		"""
		"""
		passs