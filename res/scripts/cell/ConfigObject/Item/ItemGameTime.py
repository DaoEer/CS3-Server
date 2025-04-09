# -*- coding: utf-8 -*-

import csdefine
import ConfigObject.Item.ItemUse as ItemUse


class ItemGameTime(ItemUse.ItemUse):
	"""
	充值游戏时长
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		
		self.gameTime = int(srcData.get("Param1")) #使用道具所获得的时长，单位：分
		
	def use(self, owner, target):
		"""
		使用
		"""
		ItemUse.ItemUse.use(self, owner, target)
		
		owner.base.addGameTime(self.gameTime * 60)
		
		owner.removeItemByAmount(self, 1, csdefine.ITEM_REMOVE_BY_USE)