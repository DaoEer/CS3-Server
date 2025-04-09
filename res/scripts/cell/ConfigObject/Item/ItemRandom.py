# -*- coding: utf-8 -*-

import random
import csdefine
import ItemFactory
import csstatus
import ConfigObject.Item.ItemUse as ItemUse

class ItemRandom( ItemUse.ItemUse ):

	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self.randomList = [int(i) for i in srcData["Param1"].split("|")]	 # 随机物品ID


	def onAddItem( self, owner ):
		"""
		往背包添加物品
		"""
		random.shuffle(self.randomList)
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(self.randomList[0] )
		owner.addItem( itemInst, csdefine.ITEM_ADD_BY_SYS )


	def use(self, owner, target):
		"""
		使用物品
		"""
		ItemUse.ItemUse.use(self, owner, target)
		owner.removeItemByAmount( self, 1, csdefine.ITEM_REMOVE_BY_USE )
		self.onAddItem(owner)
		return csstatus.ITEM_USE_GO_ON_MSG


