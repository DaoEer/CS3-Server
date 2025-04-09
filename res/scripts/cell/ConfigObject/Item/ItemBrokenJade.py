# -*- coding: utf-8 -*-
import random
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
import Functions
import csstatus
import Const
import KBEDebug
import BaseDataStructure

class ItemBrokenJade( ItemUse.ItemUse ):
	"""
	破碎的玉玦
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._completeJadeID = int(srcData["Param1"])
		
	def checkUse(self, owner):
		"""
		使用物品检测
		"""		
		hasAmount = 0
		itemList = owner.getItemInstsByID(self.id)
		for item in itemList:
			hasAmount += item.getAmount()
		if hasAmount < 10:
			return csstatus.USE_ITEM_FORBID_BY_STATE

		return ItemUse.ItemUse.checkUse( self, owner )

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		if not target:
			target = owner

		owner.addItemByID(self._completeJadeID)
		owner.removeItemsByItemID( self.id, 10, csdefine.ITEM_REMOVE_BY_USE )

		dct = {}
		List = []
		itemList = owner.itemsBag.getItemByID(self._completeJadeID)
		if len(itemList):
			r = {}
			r.update({"key":str(itemList[0].uid)})
			r.update({"value":1})
			List.append(r)
		if List:
			dct.update({"dictData":List})
			obj = BaseDataStructure.g_dictStrInt.createObjFromDict(dct)
			owner.client.CLIENT_ShowItemListIcon(obj)
