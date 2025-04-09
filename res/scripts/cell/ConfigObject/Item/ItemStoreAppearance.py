# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
import Functions
import ItemTypeEnum
import csstatus
import KBEDebug

class ItemStoreAppearance( ItemUse.ItemUse ):
	"""
	商城外观
	"""
	def __init__(self, srcData): 
		ItemUse.ItemUse.__init__(self, srcData)
		self._type = int(srcData["Param1"])
		self._appearanceID = srcData["Param2"]

	def checkUse(self, owner):
		"""
		使用物品检测
		"""	
		gender = self.getItemDir("ReqGender")
		if gender!= 0 and owner.getGender() != gender:
			return csstatus.STORE_STORE_APPEARANCE_GENDER
		for i in owner.getItemListByKBType(ItemTypeEnum.BAG_APPEARANCE):
			if i.id == self.id:
				return csstatus.ITEM_USE_AMOUNT_LIMIT

		dstorder = owner.getFreeOrderByItemInst( ItemTypeEnum.BAG_APPEARANCE )
		if dstorder == None:
			return csstatus.BAG_NOT_ENOUGHSPACE
		return ItemUse.ItemUse.checkUse( self, owner )

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		dstorder = owner.getFreeOrderByItemInst( ItemTypeEnum.BAG_APPEARANCE )
		owner.CELL_swapItem(owner.id, self.order, dstorder)
		owner.setStoreAppearanceByType( self._type, self._appearanceID )
		owner.onUseStoreAppearance(self.id)
		if self.isLimitTimeItem():
			self.setLimitTimeData()
			owner.onAddLimitTimeItem(self)