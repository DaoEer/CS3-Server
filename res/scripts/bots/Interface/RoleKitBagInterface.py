# -*- coding: utf-8 -*-
import KBEDebug
import KBEngine
import ItemTypeEnum
from configObject import Item
class RoleKitBagInterface:
	"""
	"""
	def __init__(self):
		self.items = {}
		self.equipBag = []
		self.commonBag = []
		self.questBag = []
		self.initKitBag = False
		
	def getBagTypeByOrder(self, itemorder):
		if itemorder < ItemTypeEnum.BAG_COMMONSTART:
			return ItemTypeEnum.BAG_EQUIP
		elif itemorder < ItemTypeEnum.BAG_QUESTSTART:
			return ItemTypeEnum.BAG_COMMON
		elif itemorder < ItemTypeEnum.BAG_SPARSTART:
			return ItemTypeEnum.BAG_QUEST
		elif itemorder < ItemTypeEnum.BAG_STORESTART:
			return ItemTypeEnum.BAG_SPAR
		elif itemorder <= ItemTypeEnum.BAG_STOREEND:
			return ItemTypeEnum.BAG_STORE
		elif itemorder <= ItemTypeEnum.BAG_TONG_STORE_END:
			return ItemTypeEnum.BAG_TONG_STORE
		elif itemorder <= ItemTypeEnum.BAG_SPACECOPY_END:
			return ItemTypeEnum.BAG_SPACE_COPY  #副本专用背包
		elif itemorder <= ItemTypeEnum.BAG_APPEARANCES_END:
			return ItemTypeEnum.BAG_APPEARANCE  # 外观隐藏背包
		return None
		
	def CLIENT_endInitKitBag(self):
		self.initKitBag = True
		self.eventObj.fireEvent("Event_CItemAISys_onInitKitBag")
		
	def kitbagInit( self, datas ):
		for data in datas:
			self.addItem(data, None)
		
	def addItem(self, data, reason):
		item = Item.Item()
		item.init(data)
		self.items[item.itemOrder] = item
		
		if self.getBagTypeByOrder(item.itemOrder) == ItemTypeEnum.BAG_EQUIP:
			self.equipBag.append(item.itemOrder)
		elif self.getBagTypeByOrder(item.itemOrder) == ItemTypeEnum.BAG_COMMON:
			self.commonBag.append(item.itemOrder)
		elif self.getBagTypeByOrder(item.itemOrder) == ItemTypeEnum.BAG_QUEST:
			self.questBag.append(item.itemOrder)
		
		self.eventObj.fireEvent("Event_CItemAISys_onAddItem", item.itemOrder)
	
	def CLIENT_removeItem(self, index):
		if index in self.items:
			self.items.pop(index)
			
			if self.getBagTypeByOrder(index) == ItemTypeEnum.BAG_EQUIP:
				if index in self.equipBag: self.equipBag.remove(index)
			elif self.getBagTypeByOrder(index) == ItemTypeEnum.BAG_COMMON:
				if index in self.commonBag: self.commonBag.remove(index)
			elif self.getBagTypeByOrder(index) == ItemTypeEnum.BAG_QUEST:
				if index in self.questBag: self.questBag.remove(index)
		
		self.eventObj.fireEvent("Event_CItemAISys_onRemoveItem")
	
	def endSort(self):
		pass
	def OnStoreMoneyChange( self, p1 ):
		pass
	def OnUnLockStoreGridNumChange( self, p1 ):
		pass
	def requestOpenStoreWindow( self, p1, p2, p3 ):
		pass
	def FKB_addItemCbBySplit( self, p1 ):
		pass
	def ShowNextLevelGift( self, p1, p2 ):
		pass
	def ShowLevelGift( self, p1, p2 ):
		pass
	def FKB_addStoreItemCb( self, p1 ):
		pass
	def FKB_removeStoreItemCb( self, p1 ):
		pass
	def FKB_swapStoreItemAC( self, p1, p2 ):
		pass
	def FKB_swapItemFromBagToStore( self, p1, p2 ):
		pass
	def FKB_addTongStoreItemCb( self, p1 ):
		pass
	def FKB_removeTongStoreItemCb( self, p1 ):
		pass
	def FKB_swapItemFromBagToTongStore( self, p1, p2 ):
		pass
	def CLIENT_addItemBySplit( self, p1 ):
		pass
	def CLIENT_swapItemAC( self, p1, p2 ):
		pass
	def CLIENT_addStoreItem( self, p1 ):
		pass
	def CLIENT_removeStoreItem( self, p1 ):
		pass
	def CLIENT_swapStoreItemAC( self, p1, p2 ):
		pass
	def CLIENT_swapItemFromBagToStore( self, p1, p2 ):
		pass
	def CLIENT_updateTongStoreItem( self, p1 ):
		pass
	def CLIENT_removeTongStoreItem( self, p1 ):
		pass
	def CLIENT_swapTongStoreItemAC( self, p1, p2 ):
		pass
	def CLIENT_swapItemFromBagToTongStore( self, p1, p2 ):
		pass
	def CLIENT_requestSortKitBagCB( self, p1, p2, p3 ):
		pass
	def CLIENT_openInputKBPW( self ):
		pass
	def CLIENT_hideKBLockWin( self ):
		pass
	def CLIENT_AddToItemUseAmountArray( self, p1, p2, p3 ):
		pass
	def CLIENT_UpdateItemUseAmount( self, p1, p2, p3 ):
		pass
	def CLIENT_endSort( self ):
		pass
	def CLIENT_requestOpenStoreWindow( self, p1, p2, p3 ):
		pass
	def CLIENT_OnUnLockStoreGridNumChange( self, p1 ):
		pass
	def CLIENT_OnStoreMoneyChange( self, p1 ):
		pass
	def CLIENT_ShowNextLevelGift( self, p1, p2 ):
		pass
	def CLIENT_ShowLevelGift( self, p1, p2 ):
		pass
	def CLIENT_GreyItem( self, p1 ):
		pass
	def CLIENT_ClearGreyItem( self, p1 ):
		pass
	def CLIENT_OnSetGridEnabledByOrderID( self, p1, p2 ):
		pass
	def OnBeforeRemoveItemBP( self, p1 ):
		pass
	def CLIENT_ShowItemListIcon( self, p1 ):
		pass
	def CLIENT_SetGiftItemsDescribe( self, p1, p2 ):
		pass
	def addStoreItem( self, p1 ):
		pass
	def updateTongStoreItem( self, p1 ):
		pass
	def addShengJieItemNotify( self ):
		pass
