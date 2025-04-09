
import KBEngine
import csdefine
import ItemFactory
import KBEDebug
import ItemTypeEnum
import csstatus
import time

class RoleFacadeBagInterface:
	"""
	玩家外观背包
	"""
	def __init__( self ):
		"""
		目前暂未用到 先注释
		#腰部挂件背包格子容量
		self.waistPendantBagCapacity = ItemTypeEnum.FACADE_BAG_CECAPACITY
		#背部挂件背包格子容量
		self.backPendantBagCapacity  = ItemTypeEnum.FACADE_BAG_CECAPACITY
		#项链背包格子容量
		self.necklaceBagCapacity     = ItemTypeEnum.FACADE_BAG_CECAPACITY
		#手环背包格子容量
		self.braceletBagCapacity     = ItemTypeEnum.FACADE_BAG_CECAPACITY
		#脚饰背包格子容量
		self.footBagCapacity 		 = ItemTypeEnum.FACADE_BAG_CECAPACITY
		#飞行器背包格子容量
		self.aircraftBagCapacity 	 = ItemTypeEnum.FACADE_BAG_CECAPACITY

		self.timerID = 0
		self.checkFacadeBagItem()
		"""
		pass
		
	def initFacadeBagItems( self ):
		"""
		初始化外观中的物品
		"""
		for itemInst in self.facadeItemList:
			pass
			#self.addFacadeBagItemToClient( itemInst )

	def addFacadeBagItemToClient( self,itemInst,itemType ):
		"""
		添加物品到客户端
		@param itemInst ：物品
		@type itemInst：ITEM
		"""
		itemOrder = -1
		if itemType in [ItemTypeEnum.ITEM_PENDANT,ItemTypeEnum.ITEM_DECORATION]:
			itemOrder = self.getFacadeBagItemOrderByUid( itemInst.uid )
		tempdict = {"id":str( itemInst.id ), "uid":str( itemInst.uid ),"amount":str( itemInst.amount ), "bindType":str( itemInst.bindType ), "itemOrder":str(itemOrder),"itemType":itemType}
		#self.client.ReceiveFacadeBagItem( Functions.toJsonString( [tempdict] ) )

	def addItemToFacadeBag( self,itemInst,itemState,itemType ):
		"""
		添加物品
		@param itemInst ：物品
		@type itemInst：ITEM
		@param itemState ：物品状态
		@type itemState：INT32  (永久拥有、临时拥有)
		"""
		if not itemInst:
			return False
		if itemInst in self.facadeItemList:
			#看该物品的状态是否是临时拥有
			itemLifeTime = itemInst.dynamicData["lifeTime"]
			if itemLifeTime <= 0:
				#已经是永久拥有
				return
			if itemState == csdefine.SHOP_GOODS_TEMPORARY:
				#续费
				itemInst.dynamicData["lifeTime"] =  itemLifeTime + 7*3600
			elif itemState == csdefine.SHOP_GOODS_PERMANENT:
				#永久购买
				itemInst.dynamicData["lifeTime"] = 0
			self.popTimer(self.timerID)
			self.updateOneDataToClient("lifeTime",itemInst.dynamicData["lifeTime"],itemInst)
			if self.timerID <= 0:
				self.timerID = self.self.addTimerCallBack( itemInst.dynamicData["lifeTime"] - currentTime,"removeFacadeBagItemByUID",(itemInst.uid,) )
		if itemType in [ItemTypeEnum.ITEM_PENDANT,ItemTypeEnum.ITEM_DECORATION]:
			itemOrder = self.getFreeOrderByItemInst(itemInst)
			if itemOrder: #找到空闲位置
				self.facadeItemOrders.update({itemOrder: itemInst.uid})
				itemInst.ownerID = self.playerDBID
		self.facadeItemList.append(itemInst)
		self.addFacadeBagItemToClient(itemInst,itemType)
		if itemState == csdefine.SHOP_GOODS_TEMPORARY:
			currentTime = time.time()
			itemLifeTime = currentTime + 7 * 3600
			itemInst.dynamicData["lifeTime"] = itemLifeTime
			self.updateOneDataToClient("lifeTime",itemInst.dynamicData["lifeTime"],itemInst)
			if self.timerID == 0:
				self.timerID = self.addTimerCallBack( itemInst.dynamicData["lifeTime"] - currentTime,"removeFacadeBagItemByUID",(itemInst.uid,) )

	def removeFacadeBagItemByUID( self,uid ):
		"""
		移除物品
		"""
		itemInst = self.getFacadeBagItemByUid(uid)
		if itemInst == None:
			KBEDebug.ERROR_MSG("player[%d] want to remove item by uid[%d]"%(self.playerDBID, uid))
			return
		if itemInst in self.facadeItemList:
			itemOrder = self.getFacadeBagItemOrderByUid(uid)
			if itemOrder != None:
				self.facadeItemOrders.pop(itemOrder)
			self.facadeItemList.remove(itemInst)
			self.popTimer(self.timerID)
			itemInst = self.getMinLifeTimeOfItem( self.facadeItemList )
			if itemInst:
				if self.timerID <= 0:
					self.timerID = self.self.addTimerCallBack( itemInst.dynamicData["lifeTime"] - currentTime,"removeFacadeBagItemByUID",(itemInst.uid,) )
			#通知客户端更新

	def checkFacadeBagItem( self ):
		"""
		检查外观背包中的物品是否过期
		"""
		if len( self.facadeItemList ) <= 0:
			return
		itemInstList = []
		currentTime = time.time()
		for facadeItem in self.facadeItemList:
			itemLifeTime = facadeItem.dynamicData["lifeTime"]
			if itemLifeTime > 0:
				if currentTime > itemLifeTime:
					itemInstList.append( facadeItem )
		if len( itemInstList ) > 0:
			for itemInst in itemInstList:
				self.removeFacadeBagItemByUID( itemInst.uid )
		

	def getMinLifeTimeOfItem( self,itemInstList ):
		"""
		获得物品生存时间最小的
		"""
		if len(itemInstList) < 0:
			return None
		itemLifeTimeList = []
		for itemInst in itemInstList:
			itemLifeTime = itemInst.dynamicData["lifeTime"]
			if itemLifeTime > 0:
				itemLifeTimeList.append(itemLifeTime)
		if len(itemLifeTimeList) < 0:
			return None
		itemLifeTimeList.sort()
		for itemInst in itemInstList:
			if itemInst.dynamicData["lifeTime"] == itemLifeTimeList[0]:
				return itemInst
		return None

	def addItemToFacadeBagCheck( self,itemInst ):
		"""
		添加物品检测
		"""
		itemType = itemInst.getType()
		if itemType in [ItemTypeEnum.ITEM_PENDANT,ItemTypeEnum.ITEM_DECORATION]:
			itemOrder = self.getFreeOrderByItemInst(itemInst)
			if itemOrder:
				return True
			else:
				return False
		return True

	def isInFacadeBag( self,itemInst ):
		"""
		判断是否在外观背包中
		"""
		if itemInst in self.facadeItemList:
			if itemInst.dynamicData["lifeTime"] > 0:
				return True
		return False

	def getFreeOrderByItemInst(self, itemInst):
		"""
		根据物品实例获取物品空闲背包位置
		"""
		bagType = itemInst.getKitBagType()
		funs = {
				ItemTypeEnum.BAG_WAIST_PENDANT:       self.getWaistPendantBagFreeOrder,
				ItemTypeEnum.BAG_BACK_PENDANT:		  self.getBackPendantBagFreeOrder,
				ItemTypeEnum.BAG_NECKLACE_DECORATION: self.getNecklaceBagFreeOrder,
				ItemTypeEnum.BAG_BRACELET_DECORATION: self.getBraceletBagFreeOrder,
				ItemTypeEnum.BAG_FOOT_DECORATION:	  self.getFootBagFreeOrder,
				ItemTypeEnum.BAG_AIRCRAFT_DECORATION: self.getAircraftBagFreeOrder,
		}
		return funs[bagType]()

	def getWaistPendantBagFreeOrder( self ):
		"""
		查找腰部挂件背包的空闲位置
		"""
		return self.getFreeOrder(ItemTypeEnum.BAG_WAIST_PENDANT_START, ItemTypeEnum.BAG_WAIST_PENDANT_START + ItemTypeEnum.FACADE_BAG_CECAPACITY + self.unLockWaistGridNum - 1)

	def getBackPendantBagFreeOrder( self ):
		"""
		查找背部挂件背包的空闲位置
		"""
		return self.getFreeOrder(ItemTypeEnum.BAG_BACK_PENDANT_START, ItemTypeEnum.BAG_BACK_PENDANT_START + ItemTypeEnum.FACADE_BAG_CECAPACITY + self.unLockBackGridNum - 1)

	def getNecklaceBagFreeOrder( self ):
		"""
		查找项链背包的空闲位置
		"""
		return self.getFreeOrder(ItemTypeEnum.BAG_NECKLACE_DECORATION_START, ItemTypeEnum.BAG_NECKLACE_DECORATION_START + ItemTypeEnum.FACADE_BAG_CECAPACITY + self.unLockNecklaceGridNum - 1)

	def getBraceletBagFreeOrder( self ):
		"""
		查找手环背包的空闲位置
		"""
		return self.getFreeOrder(ItemTypeEnum.BAG_BRACELET_DECORATION_START, ItemTypeEnum.BAG_BRACELET_DECORATION_START + ItemTypeEnum.FACADE_BAG_CECAPACITY + self.unLockBraceletGridNum - 1)

	def getFootBagFreeOrder( self ):
		"""
		查找脚饰背包的空闲位置
		"""
		return self.getFreeOrder(ItemTypeEnum.BAG_FOOT_DECORATION_START, ItemTypeEnum.BAG_FOOT_DECORATION_START + ItemTypeEnum.FACADE_BAG_CECAPACITY + self.unLockFootGridNum - 1)

	def getAircraftBagFreeOrder( self ):
		"""
		查找飞行器背包的空闲位置
		"""
		return self.getFreeOrder(ItemTypeEnum.BAG_AIRCRAFT_DECORATION_START, ItemTypeEnum.BAG_AIRCRAFT_DECORATION_START + ItemTypeEnum.FACADE_BAG_CECAPACITY + self.unLockAircraftGridNum - 1)

	def getFreeOrder(self, startIndex, endIndex):
		"""
		获取指定区间内的空闲格子
		"""
		if startIndex > endIndex:
			raise IndexError( "startIndex[%d] less then endIndex[%d]"%(startIndex, endIndex) )
		for i in range(startIndex, endIndex+1):
			if i not in self.facadeItemOrders:
				return i
		return None

	def saveFacade( self,srcUids ):
		"""
		保存外观形象
		"""
		if len(srcUids) <= 0:
			return
		for uid in srcUids:
			itemInst = self.getFacadeBagItemByUid(uid)
			if itemInst == None:
		 		return
			if itemInst.isFacade():
				order = itemInst.getWearOrder()  #获得穿戴的部位
				self.facadeItemOrders[order] = uid
				itemInst.Wear(self,True)

	def getFacadeBagItemByOrder( self,order ):
		"""
		根据order获得物品
		"""
		if self.facadeItemOrders.get(order,None):
			uid = self.facadeItemOrders[order]
			return self.getFacadeBagItemByUid(uid)
		return None

	def getFacadeBagTypeByOrder( self,itemOrder ):
		"""
		根据位置获取背包的类型
		"""
		if itemOrder >= ItemTypeEnum.BAG_FACADE_START and itemOrder < ItemTypeEnum.BAG_FACADE_END:
			return ItemTypeEnum.BAG_FACADE
		return None

	def getFacadeBagItemByUid( self,uid ):
		"""
		根据物品uid获取物品实例
		"""
		for item in self.facadeItemList:
			if item.uid == uid:
				return item
		return None

	def getFacadeBagItemOrderByUid( self, uid ):
		"""
		根据物品uid获取物品所在位置
		"""
		for key, value in self.facadeItemOrders.items():
			if value == uid:
				return key
		return None

	def unLockFacadeBagGrid( self, srcEntityID, index, uid, bagType ):
		"""
		<Exposed method>
		index:格子序号
		uid : 物品uid
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		index = int(index)
		itemInst = self.getItemInstByUid(int(uid))
		if itemInst == None:
			return
		self.removeItem( itemInst, csdefine.ITEM_REMOVE_BY_USE )
		self.unLockFacadeBagGridCB( index,bagType )
	
	def unLockFacadeBagGridCB( self, index, bagType ):
		if bagType == ItemTypeEnum.BAG_WAIST_PENDANT:
			self.unLockWaistGridNum = index - (ItemTypeEnum.BAG_WAIST_PENDANT_START + ItemTypeEnum.FACADE_BAG_CECAPACITY) + 1
		elif bagType == ItemTypeEnum.BAG_BACK_PENDANT:
			self.unLockBackGridNum = index - (ItemTypeEnum.BAG_BACK_PENDANT_START + ItemTypeEnum.FACADE_BAG_CECAPACITY) + 1
		elif bagType == ItemTypeEnum.BAG_NECKLACE_DECORATION:
			self.unLockNecklaceGridNum = index - (ItemTypeEnum.BAG_NECKLACE_DECORATION_START + ItemTypeEnum.FACADE_BAG_CECAPACITY) + 1
		elif bagType == ItemTypeEnum.BAG_BRACELET_DECORATION:
			self.unLockBraceletGridNum = index - (ItemTypeEnum.BAG_BRACELET_DECORATION_START + ItemTypeEnum.FACADE_BAG_CECAPACITY) + 1
		elif bagType == ItemTypeEnum.BAG_FOOT_DECORATION:
			self.unLockFootGridNum = index - (ItemTypeEnum.BAG_FOOT_DECORATION_START + ItemTypeEnum.FACADE_BAG_CECAPACITY) + 1
		elif bagType == ItemTypeEnum.BAG_AIRCRAFT_DECORATION:
			self.unLockAircraftGridNum = index - (ItemTypeEnum.BAG_AIRCRAFT_DECORATION_START + ItemTypeEnum.FACADE_BAG_CECAPACITY) + 1




