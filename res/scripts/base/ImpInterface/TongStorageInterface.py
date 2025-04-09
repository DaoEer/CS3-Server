# -*- coding: utf-8 -*-

import Functions
import csconst
import KBEDebug
import csstatus
import csdefine
import ItemTypeEnum

class TongStorageInterface( object ):
	def __init__( self ):
		pass
		
	def addTongStoreCapacity( self, capacity ):
		"""帮会仓库增加容量"""
		self.storeCapacity += capacity
		
	def enterTongStorage( self, playerDBID, NpcID ):
		"""
		define method
		申请打开仓库
		"""
		mailbox = self.members[playerDBID].baseMailBox
		if not mailbox:return
		mailbox.client.OpenTongStore( NpcID, self.storeCapacity )
		for order, item in self.storeBags.items():
			self.updateItemToClient( order, item, mailbox )
				
	def reFreshBag( self, mailBox, srcorder ):
		"""刷新客户端数据, 只刷新当前order对应包裹的数据"""
		bag = int( (srcorder - ItemTypeEnum.BAG_TONG_STORE_START)/csconst.TONG_STORE_BAG_CAPACITY )
		min = ItemTypeEnum.BAG_TONG_STORE_START + bag * csconst.TONG_STORE_BAG_CAPACITY
		max = min + csconst.TONG_STORE_BAG_CAPACITY
		for order in range(min, max):
			if order in self.storeBags:
				self.updateItemToClient( order, self.storeBags[order], mailBox )
	
	def requestSaveTongItem( self, playerMB, playerName, srcorder, srcItem, bagID ):
		"""
		define method
		仓库存物品
		"""
		if srcItem is None:return
		if self._doStackItem( playerMB, srcItem ):
			playerMB.onRequestSaveTongItem( srcorder, 0, True )
			self.addStoreRecord(csdefine.TONG_STORE_EVENT_STORE, playerName, srcItem.getItemDir("ItemName"), str(srcItem.amount))
			return
			
		order = self.getFreeOrder( bagID )
		if not order:
			playerMB.onRequestSaveTongItem( srcorder, 0, False )
			playerMB.client.statusMessage( csstatus.STORE_MSG_FULL, "" )
			return
		srcItem.setOrder(order)
		self.storeBags[order] = srcItem
		playerMB.onRequestSaveTongItem( srcorder, order, True )
		self.updateItemToClient(order, srcItem, playerMB)
		self.addStoreRecord(csdefine.TONG_STORE_EVENT_STORE, playerName, srcItem.getItemDir("ItemName"), str(srcItem.amount))

	def _doStackItem( self, playerMB, itemInst ):
		"""叠加单个物品到仓库"""
		if itemInst.canStack():
			itemList = []
			amount = itemInst.getAmount()
			for order, item in self.storeBags.items():
				if item.id == itemInst.id and item.isBinded() == itemInst.isBinded() and itemInst.canStack():
					itemList.append( item )
					amount += item.amount
					# 如果可以堆叠所有的数量，才进行堆叠
					if amount <= itemInst.getMaxAmount() * len( itemList ):
						for item in itemList:
							if amount <= 0:
								break
							if amount <= item.getMaxAmount():
								item.setAmount( None, amount )
								amount = 0
							else:
								amount -= item.getMaxAmount()
								item.setAmount( None, item.getMaxAmount())
							self.updateOneDataToClient("amount", item.getAmount(), item, playerMB)
						return True
			
		return False
	
	def requestTakeTongItem( self, playerMB, playerName, srcorder ):
		"""
		define method
		帮会仓库取物品
		"""
		if srcorder in self.storeBags:
			srcItem = self.storeBags.pop( srcorder )
			playerMB.onRequestTakeTongItem( srcorder, srcItem, True )
			self.addStoreRecord(csdefine.TONG_STORE_EVENT_OBTAIN, playerName, srcItem.getItemDir("ItemName"), str(srcItem.amount))
			return
		self.reFreshBag( playerMB, srcorder )
	
	def onRequestTakeTongItemFail( self, srcorder, srcItem ):
		"""
		define method
		仓库取物品失败
		"""
		self.storeBags[srcorder] = srcItem
	
	def swapTongItemAC( self, playerMB, srcorder, dstorder ):
		"""
		define method
		互换格子
		"""
		if srcorder in self.storeBags and dstorder in self.storeBags:
			srcItem = self.storeBags[srcorder]
			dstItem = self.storeBags[dstorder]
			if srcItem.id == dstItem.id  and dstItem.canStack(1):	# 处理叠加情况
				if srcItem.isBinded() != dstItem.isBinded():
					srcItem.setBindType( playerMB )
					dstItem.setBindType( playerMB )
				if dstItem.overlyingMax >= ( dstItem.amount + srcItem.amount ):
					dstItem.setAmount( None, dstItem.amount + srcItem.amount )
					self.updateOneDataToClient("amount", dstItem.getAmount(), dstItem, playerMB)
					self.storeBags.pop( srcorder )
					playerMB.client.CLIENT_removeTongStoreItem( srcorder )
				else:
					srcItem.setAmount( None, dstItem.amount + srcItem.amount - dstItem.overlyingMax)
					self.updateOneDataToClient("amount", srcItem.getAmount(), srcItem, playerMB)
					dstItem.setAmount( None, dstItem.overlyingMax )
					self.updateOneDataToClient("amount", dstItem.getAmount(), dstItem, playerMB)
			else:
				dstItem.setOrder( srcorder )
				self.storeBags[srcorder] = dstItem
				srcItem.setOrder( dstorder )
				self.storeBags[dstorder] = srcItem
				playerMB.client.CLIENT_swapTongStoreItemAC( srcorder, dstorder )
			return
		elif srcorder in self.storeBags:
			popOrder = srcorder
			addOrder = dstorder
		elif dstorder in self.storeBags:
			popOrder = dstorder
			addOrder = srcorder
		else:
			self.reFreshBag( playerMB, srcorder )
		item = self.storeBags.pop( popOrder )
		item.setOrder( addOrder)
		self.storeBags[addOrder] = item
		playerMB.client.CLIENT_swapTongStoreItemAC( popOrder, addOrder )
	
	def swapItemFromBagToTongStore( self, playerMB, playerName, srcorder, dstorder, srcItem ):
		"""
		define method
		将背包物品拖曳到仓库
		"""
		if srcItem is None:
			KBEDebug.ERROR_MSG("Player(%d) swap item from bag(%d) to tong store(%d),bagItem is None!"%(playerMB.id,srcorder,dstorder))
			return
		if dstorder in self.storeBags and self.storeBags[dstorder]:
			dstItem = self.storeBags[dstorder]
			# 如果可以叠加，优先叠加
			if dstItem.id == srcItem.id and dstItem.canStack() and srcItem.canStack():
				srcItem_amount = srcItem.amount
				if dstItem.isBinded() != srcItem.isBinded():
					dstItem.setBindType( playerMB )
					srcItem.setBindType( playerMB )
				if dstItem.getMaxAmount() >= ( dstItem.getAmount() + srcItem.getAmount() ):
					dstItem.setAmount( None, dstItem.getAmount() + srcItem.getAmount() )
					self.updateOneDataToClient("amount", dstItem.getAmount(), dstItem, playerMB)
				else:
					bagID = int( (dstorder - ItemTypeEnum.BAG_TONG_STORE_START)/csconst.TONG_STORE_BAG_CAPACITY )
					order = self.getFreeOrder( bagID )
					srcItem.setOrder(order)
					srcItem.setAmount( None, dstItem.getAmount() + srcItem.getAmount() - srcItem.getMaxAmount() )
					playerMB.client.CLIENT_removeItem( srcorder )
					self.storeBags[order] = srcItem
					self.updateItemToClient(None, self.storeBags[order], playerMB)
					dstItem.setAmount( None, dstItem.getMaxAmount() )
					self.updateOneDataToClient("amount", dstItem.getAmount(), dstItem, playerMB)
				self.addStoreRecord(csdefine.TONG_STORE_EVENT_STORE, playerName, srcItem.getItemDir("ItemName"), str(srcItem_amount))
				srcItem = None
				playerMB.onStackItemToStore( srcorder, srcItem )
				return
			else:					# 否则交换位置
				dstItem = self.storeBags.pop(dstorder)
				srcItem.setOrder( dstorder )
				self.storeBags[dstorder] = srcItem
				self.addStoreRecord(csdefine.TONG_STORE_EVENT_STORE, playerName, srcItem.getItemDir("ItemName"), str(srcItem.amount))
				self.addStoreRecord(csdefine.TONG_STORE_EVENT_OBTAIN, playerName, dstItem.getItemDir("ItemName"), str(dstItem.amount))
		else:
			dstItem = None
			srcItem.setOrder(dstorder)
			self.storeBags[dstorder] = srcItem
			self.addStoreRecord(csdefine.TONG_STORE_EVENT_STORE, playerName, srcItem.getItemDir("ItemName"), str(srcItem.amount))
		playerMB.onSwapItemToTongStore( srcorder, dstorder, dstItem )
	
	def swapItemFromTongStoreToBag( self, playerMB, playerName, srcorder, dstorder, dstItem ):
		"""
		define method
		将仓库物品拖曳到背包
		"""
		srcItem = self.storeBags[ srcorder ]
		if dstItem:
			if srcItem.id == dstItem.id and dstItem.canStack() and srcItem.canStack():
				if srcItem.isBinded() != dstItem.isBinded():
					srcItem.setBindType( playerMB )
					dstItem.setBindType( playerMB )
				if dstItem.getMaxAmount() >= ( dstItem.getAmount() + srcItem.getAmount() ):
					dstItem.setAmount( None, dstItem.getAmount() + srcItem.getAmount() )
					self.updateOneDataToClient("amount", dstItem.getAmount(), dstItem, playerMB)
					self.storeBags.pop( srcorder )
					playerMB.client.CLIENT_removeTongStoreItem( srcorder )
					self.addStoreRecord(csdefine.TONG_STORE_EVENT_OBTAIN, playerName, srcItem.getItemDir("ItemName"), str(srcItem.amount))
				else:
					take_amount = srcItem.getAmount()
					srcItem.setAmount( None, dstItem.getAmount() + srcItem.getAmount() - dstItem.getMaxAmount() )
					self.updateOneDataToClient("amount", srcItem.getAmount(), srcItem, playerMB)
					dstItem.setAmount( None, dstItem.getMaxAmount() )
					self.updateOneDataToClient("amount", dstItem.getAmount(), dstItem, playerMB)
					item = self.storeBags.pop( srcorder )
					playerMB.onRequestTakeTongItem( srcorder, item, True )
					self.addStoreRecord(csdefine.TONG_STORE_EVENT_OBTAIN, playerName, srcItem.getItemDir("ItemName"), str(take_amount))
				playerMB.onStackItemToStore( dstorder, dstItem )
			else:
				self.storeBags.pop( srcorder )
				dstItem.setOrder(srcorder)
				self.storeBags[srcorder] = dstItem
				playerMB.onSwapItemToTongStore( dstorder, srcorder, srcItem )
				self.addStoreRecord(csdefine.TONG_STORE_EVENT_OBTAIN, playerName, srcItem.getItemDir("ItemName"), str(srcItem.amount))
				self.addStoreRecord(csdefine.TONG_STORE_EVENT_STORE, playerName, dstItem.getItemDir("ItemName"), str(dstItem.amount))
			return
		else:
			self.storeBags.pop( srcorder )
			self.addStoreRecord(csdefine.TONG_STORE_EVENT_OBTAIN, playerName, srcItem.getItemDir("ItemName"), str(srcItem.amount))
		playerMB.onSwapItemToTongStore( dstorder, srcorder, srcItem )
		playerMB.client.CLIENT_removeTongStoreItem( srcorder )
	
	def getFreeOrder( self, bagID ):
		"""获取包裹空余位置"""
		if self.storeCapacity / csconst.TONG_STORE_BAG_CAPACITY - 1 >= bagID:
			min = ItemTypeEnum.BAG_TONG_STORE_START + bagID *csconst.TONG_STORE_BAG_CAPACITY
			max = min + csconst.TONG_STORE_BAG_CAPACITY
			for order in range( min, max ):
				if not order in self.storeBags:
					return order
		else:
			KBEDebug.ERROR_MSG("bagID(%d) is not activate!"%bagID)
		return None
	
	def sortTongStoreItem( self, playerMB, bagID ):
		"""
		define method
		帮会仓库分类
		"""
		if self.storeCapacity / csconst.TONG_STORE_BAG_CAPACITY - 1 >= bagID:
			min = ItemTypeEnum.BAG_TONG_STORE_START + bagID*csconst.TONG_STORE_BAG_CAPACITY
			max = min + csconst.TONG_STORE_BAG_CAPACITY
			temp = {}
			for order in range( min, max ):
				if order in self.storeBags:
					temp[order] = self.storeBags.pop( order )
					playerMB.client.CLIENT_removeTongStoreItem( order )
			items = list( temp.values() )
			items = sorted( items, key = lambda item: item.getSortIndex(), reverse = True )
			for order in range( min, min+len(items)):
				items[order - min].setOrder(order)
				self.storeBags[order] = items[order - min]
			self.reFreshBag( playerMB, min )
		else:
			KBEDebug.ERROR_MSG("bagID(%d) is not activate!"%bagID)
			
	def requestRemoveTongStoreItem( self, playerMB, UID ):
		"""
		define method
		帮会仓库移除物品	
		"""
		order = self.getItemOrderByUid( UID )
		if order == None:
			return
		item = self.storeBags[order]
		item.setLock( True )
		playerMB.client.CLIENT_OnSetGridEnabledByOrderID(order,False)
		playerMB.inquireMessage( csstatus.ITEM_DESTROY, [item.getItemDir("ItemName")], "replyRemoveTongStoreItem", [order, playerMB] )

	def removeTongStoreItem( self, reply, order, playerMB):
		"""
		移除物品
		"""
		if order not in self.storeBags:
			return
		item = self.storeBags[order]
		item.setLock(False)
		if reply:
			playerMB.client.CLIENT_removeTongStoreItem( order )
			del self.storeBags[order]

	def getItemOrderByUid( self, UID ):
		"""
		"""
		for order, item in self.storeBags.items():
			if item.uid == UID:
				return order
		return None
	
	def updateItemToClient( self, order, itemInst, playerMB ):
		"""更新物品数据到客户端"""
		playerMB.client.updateTongStoreItem( itemInst.getDictForClient( None ) )
		
	def updateOneDataToClient(self, propertyname, propertyvalue, itemInst, playerMB):
		"""
		更新一条属性到客户端
		"""
		uid = str(itemInst.uid)
		type_ = type(propertyvalue)
		if type_ == type(1):		#整形
			type_ = "INT"
		elif type_ == type(1.0):	#浮点数
			type_ = "FLOAT"
		elif type_ == type(""):		#字符串
			type_ = "STRING"
		else:						#其它
			type_ = "STRING"
		value = type_ + "|#|" + uid + "|#|" + propertyname[0].upper() + propertyname[1:]  + "|#|" + str(propertyvalue)
		playerMB.client.CLIENT_SetFStringPropertyByKey("DynamicProperty", value)
		
	def calcItemListAmount(self, itemList):
		"""
		计算列表中物品的总数量
		"""
		amount = 0
		if not itemList:	return amount
		for item in itemList:
			amount += item.getAmount()
		return amount