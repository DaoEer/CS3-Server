# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemGift as ItemGift
import csstatus
import Functions

class ItemLevelGift(ItemGift.ItemGift):
	"""
	等级礼包
	"""
	def __init__(self, srcData):
		ItemGift.ItemGift.__init__(self, srcData)

	def setOwner(self, player):
		"""
		设置拥有者DBID
		"""
		self.setGiftItemsDescribe(player)  # 设置物品
		ItemGift.ItemGift.setOwner( self, player )

	def checkUse(self, owner ):
		"""
		使用物品检测
		"""
		result = ItemGift.ItemGift.checkUse( self, owner )
		if result == csstatus.ITEM_USE_LV_LESS_MSG:				# 等级不够
			reqLevel = self.getItemDir("ReqLevel", 1)
			ids, amounts = self.getIDAndAmount()
			owner.client.CLIENT_ShowNextLevelGift( reqLevel, ids, amounts )
			return None
		elif result == csstatus.ITEM_USE_GO_ON_MSG:	# 可以使用
			ids, amounts = self.getIDAndAmount()
			owner.client.CLIENT_ShowLevelGift( str(self.uid), ids, amounts )
			return None
		return result
		
	def getIDAndAmount( self ):
		"""
		"""
		id = []
		amount = []
		for item in self._items:
			id.append(item.id)
			amount.append(item.amount)
		return id, amount

	def setGiftItemsDescribe(self, owner):
		giftData = self.getGiftData(self.giftID, owner)
		self.doGift(giftData, owner)

	def getDynamicDataForClient(self, entity ):
		#礼包数据的特别处理
		if not self._items:
			self.setGiftItemsDescribe( entity )

		discribe = "|打开礼包获得："
		for item in self._items:
			discribe += "|" + item.getItemDir("ItemName") + "x" + str(item.amount)

		return  Functions.toJsonString( {"discribe":discribe} )




