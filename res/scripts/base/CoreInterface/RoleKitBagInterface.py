
import KBEDebug
import KBEngine
import csdefine
import csconst
import csstatus
import ItemTypeEnum
import ItemFactory
import Functions
from MsgLogger import g_logger

class RoleKitBagInterface:
	"""
	"""
	def __init__(self):
		#背包是否被锁
		self.kbLockStatus = self.cellData["kbLockStatus"]
		
	def onGetCell( self ):
		"""
		cell创建成功
		"""
		if self.client:
			self.client.CLIENT_OnUnLockStoreGridNumChange(self.storeItems.unLockStoreGridNum)

	def unLockGrid(self, Xinshicost, Itemcost ,index):
		"""
		<define method>
		请求查询解锁格子所需仙石是否足够
		"""
		#之前是消耗仙石，现在已修改为消耗金币，所以此方法不再调用，在此备注(CST-11653)
		if self.payShiTou(Xinshicost, csdefine.CHANGE_XIANSHI_UNLOCKBAGGRID):	#足够支付
			if Itemcost > 0:
				self.cell.unLockGridRemoveItem( Itemcost ) 						#支付完物品后支付物品
			self.cell.unLockGridCB(index, True)
		else:
			self.cell.unLockGridCB(index, False)
	
	def unLockStoreGrid( self, index ):
		"""
		exposed method
		解锁仓库格子
		"""
		if not self.validateClientCall():
			return
		index = int(index)
		
		self.cell.CELL_unLockStoreGrid(index, self.storeItems.unLockStoreGridNum)
		
	def unLockStoreGridCB(self, unLockGridNum):
		"""
		define method
		解锁仓库格子回调
		"""
		self.storeItems.setUnLockGridNum(unLockGridNum)
		self.client.CLIENT_OnUnLockStoreGridNumChange(self.storeItems.unLockStoreGridNum)
		self.unLockStoreGrid(ItemTypeEnum.BAG_STORESTART + ItemTypeEnum.STORE_CAPACITY)
		
	def setPWKitBagLock(self, status):
		"""
		<Define method>
		设置背包锁状态
		"""
		self.kbLockStatus = status

	def isPWKitBagLock(self):
		"""
		判断是背包是否处理于密码锁定
		True表示背包已经使用了安全锁加锁了
		False表示已经解开安全锁或未使用安全锁
		"""
		return self.kbLockStatus == csdefine.LOCK_KB_WITH_PW
		
	def requestOpenStoreWindow( self, npcID ):
		"""
		define method
		打开仓库
		"""
		self.client.CLIENT_requestOpenStoreWindow( npcID, self.storeItems.unLockStoreGridNum, str(self.storeMoney) )
		for item in self.storeItems.values():
			self.addItemToClient( item )
		
	def addStoreMoney( self, money ):
		"""添加仓库金钱"""
		self.storeMoney += money
		self.client.CLIENT_OnStoreMoneyChange( str( self.storeMoney ) )
		
	def subStoreMoney( self, money ):
		"""减少仓库金钱"""
		self.storeMoney -= money
		self.client.CLIENT_OnStoreMoneyChange( str( self.storeMoney ) )
		
	def requestSaveMoney( self, money ):
		"""
		define method
		仓库存钱
		"""
		if self.storeMoney >= csconst.LIMIT_STORE_MONEY:
			self.cell.onRequestSaveMoney(0)
			self.statusMessage( csstatus.STORE_MSG_FULL )
			return
		if self.storeMoney + money > csconst.LIMIT_STORE_MONEY:
			money = csconst.LIMIT_STORE_MONEY - self.storeMoney
			self.statusMessage( csstatus.STORE_MSG_LIMIT_MONEY )
		self.addStoreMoney( money )
		self.cell.onRequestSaveMoney( money )
		
	def requestTakeMoney( self, money ):
		"""
		define method
		仓库取钱
		"""
		if self.storeMoney < money:
			self.cell.onRequestTakeMoney( 0 )
			self.statusMessage( csstatus.STORE_NO_STOREMONEY )
			return
		self.subStoreMoney( money )
		self.cell.onRequestTakeMoney( money )
			
	def requestSaveItem( self, srcorder, srcItem ):
		"""
		define method
		仓库存物品
		"""
		if srcItem is None:return
		order = self.storeItems.getFreeOrder(ItemTypeEnum.BAG_STORE)
		# 先执行叠加(有叠加，优先叠加满)
		if self._doStackItem( srcItem, srcorder, order ):
			return
		
		if not order:
			self.cell.onRequestSaveItem( srcorder, 0, False )
			self.statusMessage( csstatus.STORE_MSG_FULL )
			return
		
		srcItem.setOrder(order)
		srcItem.setLock( False )
		self.storeItems[order] = srcItem
		self.cell.onRequestSaveItem( srcorder, order, True )
		
	def _doStackItem( self, itemInst, srcorder, dstorder ):
		"""叠加单个物品到仓库"""
		if itemInst.canStack():
			itemList = []
			amount = itemInst.getAmount()
			for order, item in self.storeItems.items():
				if item.id == itemInst.id and item.isBinded() == itemInst.isBinded() and itemInst.canStack():
					itemList.append( item )
					amount += item.amount
					# 如果可以堆叠所有的数量，进行堆叠
					if amount <= itemInst.getMaxAmount() * len( itemList ):
						for item in itemList:
							if amount <= item.getMaxAmount():
								item.setAmount( self, amount )
							else:
								amount -= item.getMaxAmount()
								item.setAmount( self, item.getMaxAmount())
						
						self.cell.onRequestSaveItem( srcorder, 0, True )
						return True
			
			#如果能堆叠部分数量，进行堆叠
			if itemList:
				if not dstorder: return False
				amount = itemInst.getAmount()
				
				for item in itemList:
					amount -= (item.getMaxAmount() - item.getAmount())
					item.setAmount( self, item.getMaxAmount())
				
				itemInst.setAmount(self, amount)
				itemInst.setOrder(dstorder)
				itemInst.setLock( False )
				self.storeItems[dstorder] = itemInst
				#self.addItemToClient(itemInst)
				self.cell.onRequestSaveItem( srcorder, dstorder, True )
				return True
		return False
		
	def requestTakeItem( self, srcorder ):
		"""
		define method
		仓库取物品
		"""
		if srcorder in self.storeItems:
			srcItem = self.storeItems.pop(srcorder)
			self.cell.onRequestTakeItem( srcorder, srcItem, True )
			return
#		self.cell.onRequestTakeItem( srcorder, None, False )
		
	def onRequestTakeItemFail( self, srcorder, srcItem ):
		"""
		define method
		仓库取物品失败
		"""
		srcItem.setOrder(srcorder)
		srcItem.setLock( False )
		self.storeItems[srcorder] = srcItem
		
	def swapItemAC( self, srcorder, dstorder ):
		"""
		define method
		互换格子
		"""
		if not self.isValidStoreIndex(dstorder):
			return
		if srcorder in self.storeItems and dstorder in self.storeItems:
			srcItem = self.storeItems[srcorder]
			dstItem = self.storeItems[dstorder]
			if srcItem.id == dstItem.id and dstItem.canStack(1) and srcItem.canStack(1):	# 处理叠加情况
				if srcItem.isBinded() != dstItem.isBinded():
					srcItem.setBindType( self )
					dstItem.setBindType( self )
				if dstItem.getMaxAmount() >= dstItem.getAmount() + srcItem.getAmount():
					dstItem.setAmount( self, dstItem.getAmount() + srcItem.getAmount() )
					self.removeItemToClient(srcItem)
				else:
					srcItem.setAmount( self, dstItem.getAmount() + srcItem.getAmount() - dstItem.getMaxAmount() )
					dstItem.setAmount( self, dstItem.getMaxAmount() )
			else:
				dstItem.setOrder( srcorder )
				dstItem.setLock( False )
				self.storeItems[srcorder] = dstItem
				srcItem.setOrder( dstorder )
				srcItem.setLock( False )
				self.storeItems[dstorder] = srcItem
				self.client.CLIENT_swapStoreItemAC( srcorder, dstorder )
			return
		elif srcorder in self.storeItems:
			popOrder = srcorder
			addOrder = dstorder
		elif dstorder in self.storeItems:
			popOrder = dstorder
			addOrder = srcorder
		else:
			return
		item = self.storeItems.pop( popOrder )
		item.setOrder( addOrder )
		self.storeItems[addOrder] = item
		self.client.CLIENT_swapStoreItemAC( popOrder, addOrder )
		
	def swapItemFromBagToStore( self, srcorder, dstorder, srcItem ):
		"""
		define method
		将背包物品拖曳到仓库
		"""
		if not self.checkSwapItem( srcorder, dstorder ):return
		if srcItem is None:
			KBEDebug.ERROR_MSG("Player(%s,%d) swap item from bag(%d) to store(%d),bagItem is None!"%(self.playerName,self.id,srcorder,dstorder))
			return
		if not self.isValidStoreIndex(dstorder):
			return
		if dstorder in self.storeItems and self.storeItems[dstorder]:
			dstItem = self.storeItems[dstorder]
			# 如果可以叠加，优先叠加
			if dstItem.id == srcItem.id and dstItem.canStack() and srcItem.canStack():
				if dstItem.isBinded() != srcItem.isBinded():
					dstItem.setBindType( self )
					srcItem.setBindType( self )
				if dstItem.getMaxAmount() >= dstItem.getAmount() + srcItem.getAmount():
					dstItem.setAmount( self, dstItem.getAmount() + srcItem.getAmount() )
					srcItem = None
				else:
					srcItem.setAmount( self, dstItem.getAmount() + srcItem.getAmount() - dstItem.getMaxAmount() )
					dstItem.setAmount( self, dstItem.getMaxAmount() )
				self.cell.onStackItemToStore( srcorder, srcItem )
				return
			else:					# 否则交换位置
				dstItem = self.storeItems.pop(dstorder)
				srcItem.setOrder( dstorder )
				srcItem.setLock( False )
				self.storeItems[dstorder] = srcItem
		else:
			dstItem = None
			srcItem.setOrder( dstorder )
			srcItem.setLock( False )
			self.storeItems[dstorder] = srcItem
		self.cell.onSwapItemToStore( srcorder, dstorder, dstItem )
		
	def swapItemFromStoreToBag( self, srcorder, dstorder, dstItem ):
		"""
		define method
		将仓库物品拖曳到背包
		"""
		if not self.checkSwapItem( dstorder, srcorder ):return
		assert srcorder in self.storeItems,"Player(%s,%d) swap item from store(%d) to bag(%d),StoreItem is None!"%(self.playerName,self.id,srcorder,dstorder)
		if not self.isValidStoreIndex(srcorder):
			return
		srcItem = self.storeItems[ srcorder ]
		if srcItem is None:return
		if dstItem:
			# 如果可以叠加，优先叠加
			if srcItem.id == dstItem.id and dstItem.canStack() and srcItem.canStack():
				if srcItem.isBinded() != dstItem.isBinded():
					srcItem.setBindType( self )
					dstItem.setBindType( self )
				if dstItem.getMaxAmount() >= dstItem.getAmount() + srcItem.getAmount():
					dstItem.setAmount( self, dstItem.getAmount() + srcItem.getAmount() )
					self.removeItemToClient( srcItem )
				else:
					srcItem.setAmount( self, dstItem.getAmount() + srcItem.getAmount() - dstItem.getMaxAmount() )
					dstItem.setAmount( self, dstItem.getMaxAmount() )
				self.cell.onStackItemToStore( dstorder, dstItem )
				return
			else:					# 否则交换位置
				srcItem = self.storeItems.pop(srcorder)
				dstItem.setOrder( srcorder )
				dstItem.setLock( False )
				self.storeItems[srcorder] = dstItem
		else:			# 背包，不一定有物品
			self.storeItems.pop(srcorder)
		
		self.cell.onSwapItemToStore( dstorder, srcorder, srcItem )
			
	def checkSwapItem( self, bagOrder, storeOrder ):
		""""""
		assert storeOrder >= ItemTypeEnum.BAG_STORESTART and storeOrder <= ItemTypeEnum.BAG_STOREEND, \
		"Store order must in store start - end!!"
		if storeOrder in self.storeItems:
			dstItem = self.storeItems[storeOrder]
			bagType = self.getBagTypeByOrder(bagOrder)
			if dstItem.getKitBagType() != bagType:
				if bagType == ItemTypeEnum.BAG_COMMON:
					msgID = csstatus.STORE_NORMAL_ITEM_TO_NORMAL_BAG
				elif bagType == ItemTypeEnum.BAG_SPAR:
					msgID = csstatus.STORE_CRYSTAL_ITEM_TO_CRYSTAL_BAG
				elif bagType == ItemTypeEnum.BAG_QUEST:
					msgID = csstatus.STORE_QUESAT_ITEM_TO_QUEST_BAG
				else:
					msgID = csstatus.STORE_ERROR
				self.statusMessage( msgID, "" )
				return False
		return True

	def isValidStoreIndex( self, index ):
		"""是否合法的index"""
		if self.getBagTypeByOrder( index ) == ItemTypeEnum.BAG_STORE:
			# 仓库需要验证格子的有效性
			if index < ItemTypeEnum.BAG_STORESTART or index > ItemTypeEnum.BAG_STORESTART + ItemTypeEnum.STORE_CAPACITY + self.storeItems.unLockStoreGridNum - 1:
				return False
		return True

	def requestRemoveStoreItem( self, sUID ):
		"""
		exposed method
		移除物品
		"""
		if not self.validateClientCall():
			return

		UID = int( sUID )
		order = self.getItemOrderByUid( UID )
		if order == None:
			KBEDebug.ERROR_MSG( "Remove store item err!cannot find uid = %d"%UID )
			return
		item = self.storeItems[order]
		self.inquireMessage( csstatus.ITEM_DESTROY, [item.getItemDir("ItemName")] ,"replyRemoveStoreItem",order )
		item.setLock( True )
		if hasattr(self, "client") and self.client:
			self.client.CLIENT_OnSetGridEnabledByOrderID(order,False)

	def replyRemoveStoreItem( self, reply,order):
		"""
		"""
		if order not in self.storeItems:
			return
		item = self.storeItems[order]
		item.setLock(False)
		if hasattr(self, "client") and self.client:
			self.client.CLIENT_OnSetGridEnabledByOrderID(item.order,True)
		if reply:
			self.removeItemToClient( self.storeItems[order] )
		
	def splitStoreItem(self, order, amount):
		"""
		<Exposed method>
		分开一个可叠加的道具。
		"""
		if not self.validateClientCall():
			return
		if order in self.storeItems and self.storeItems[order]:
			item = self.storeItems[order]
		if amount < 1:
			return
		if item.getAmount()-amount < 1:
			return
		if item.getMaxAmount() <= 1:
			return
		freeOrder = self.storeItems.getFreeOrder(ItemTypeEnum.BAG_STORE)
		if freeOrder == None:
			self.statusMessage( csstatus.CIB_MSG_FULL )
			return
		dstItem = ItemFactory.ItemFactoryInst.createDynamicItem(item.id, amount)
		item.setAmount(self, item.getAmount() - amount)
		dstItem.setBindType(self, item.bindType)
		dstItem.ownerID = self.databaseID
		dstItem.setOrder( freeOrder )
		self.storeItems[freeOrder] = dstItem
		self.addItemToClient(dstItem)
		
	def requestSortStoreBag( self ):
		"""
		define method
		整理仓库背包
		"""
		self._doStackItems()
		items = sorted(self.storeItems.values(), key = lambda item: item.getSortIndex(), reverse = True)
		oldOrders = []
		for item in items:
			oldOrders.append( item.order )
			
		startIndex = ItemTypeEnum.BAG_STORESTART
		newOrders = [order for order in range( startIndex, startIndex + len(items) )]
		self.storeItems.clear()
		for order in newOrders:
			item = items.pop(0)
			item.setOrder(order)
			self.storeItems[order] = item
		self.client.CLIENT_requestSortKitBagCB( ItemTypeEnum.BAG_STORE, oldOrders, newOrders )
		
	def _doStackItems( self ):
		"""
		根据叠加上限，自动叠加可以叠加的物品
		策略：找出可以叠加的物品
			根据最高叠加物品，直接设置几个为最大叠加数量，剩余的全给另外一个物品，多余的物品就删除
		"""
		if not self.storeItems:
			return
		result = {True:{},False:{}}		#True的value表示是绑定的物品数据，False表示的是未绑定的物品数据
		for order, item in self.storeItems.items():
			if item.canStack():
				iBind = item.isBinded()
				if item.id not in result[iBind]:
					result[iBind].update({item.id:[item]})
				else:
					result[iBind][item.id].append(item)
		for iBind, itemDatas in result.items():
			for itemList in itemDatas.values():
				self._stackItemList( itemList )
	
	def _stackItemList( self, itemlist ):
		"""叠加列表"""
		itemGrids = len(itemlist)	#物品格子数
		if itemGrids <= 1:
			return
		curListAmount = self.calcItemListAmount(itemlist)
		maxStackGrid = curListAmount // itemlist[0].overlyingMax		#可以放满的格子数
		liftAmount = curListAmount % itemlist[0].overlyingMax		#剩余的数量（不足放满一个格子的）
		KBEDebug.DEBUG_MSG("itemGrids[%d], curListAmount[%d], maxStackGrid[%d], liftAmount[%d], overlyingMax[%d]"%(itemGrids,curListAmount,maxStackGrid,liftAmount, itemlist[0].overlyingMax))
		for index in range(0, itemGrids):
			if index < maxStackGrid:
				itemlist[index].setAmount(self, itemlist[index].getMaxAmount())	#更新数量
			elif index == maxStackGrid:
				if liftAmount != 0:
					itemlist[index].setAmount(self, liftAmount)	#更新数量
				else:
					#删除物品
					self.removeItemToClient( itemlist[index] )
			else:
				#删除物品
				self.removeItemToClient( itemlist[index] )
		
	def calcItemListAmount(self, itemList):
		"""
		计算列表中物品的总数量
		"""
		amount = 0
		if not itemList:	return amount
		for item in itemList:
			amount += item.getAmount()
		return amount
		
	def getItemOrderByUid( self, uid ):
		for order, item in self.storeItems.items():
			if item.uid == uid:
				return order
		return None
		
	def getBagTypeByOrder(self, itemorder):
		"""
		根据位置获取背包的类型
		"""
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
		elif itemorder <= ItemTypeEnum.BAG_TEMP_EQUIP_END:
			return ItemTypeEnum.BAG_TEMP_EQUIP  # 吃鸡副本临时装备背包
		return None
		
	def addItemToClient( self, itemInst ):
		"""
		通过cell添加物品到客户端
		"""
		self.cell.addItemToStoreClient( itemInst )
		
	def updateOneDataToClient(self, propertyname, propertyvalue, itemInst):
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
		self.client.CLIENT_SetFStringPropertyByKey("DynamicProperty", value)

	def removeItemToClient( self, itemInst ):
		"""
		通知客户端删除物品
		"""
		del self.storeItems[itemInst.order]
		self.client.CLIENT_removeStoreItem( itemInst.order )
		