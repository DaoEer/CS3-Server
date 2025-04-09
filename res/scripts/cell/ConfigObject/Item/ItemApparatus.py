# -*- coding: utf-8 -*-

import csdefine
import ConfigObject.Item.ItemUse as ItemUse


class ItemApparatus(ItemUse.ItemUse):
	"""
	器械建造
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		
		self.scriptID = srcData.get("Param1")
		self.modelID = srcData.get("Param2")
		self.modelScale = float(srcData.get("Param3"))

	def use(self, owner, target):
		"""
		使用
		"""
		ItemUse.ItemUse.use(self, owner, target)
		if owner.getClient():
			owner.client.OnEnterEquipBuild(self.scriptID, self.modelID, self.modelScale, str(self.uid))
		
		#owner.removeItemByAmount( self, 1, csdefine.ITEM_REMOVE_BY_USE )