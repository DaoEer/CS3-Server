
from KBEDebug import *
import ItemTypeEnum
import math
import csdefine
import csstatus

class KitBagTypeImpl:
	"""
	"""
	def __init__( self ):
		self._dataList = {}						# { order : itemInst }
		self._uid2order = {}					# { itemUID : order }
	
	def __len__( self ):
		"""
		获得当前背包有几个道具

		@return: 当前背包容纳的道具数量
		@rtype:  INT16
		"""
		return len( self._uid2order )

	def __getitem__( self, key ):
		return self._dataList.get( key )
		
	def keys(self):
		return self._dataList.keys()
		
	def values(self):
		return self._dataList.values()
		
	def items(self):
		return self._dataList.items()
	
	def getOrderID( self, uid ):
		"""
		通过uid获取orderID
		"""
		try:
			return self._uid2order[uid]
		except KeyError:
			return -1
			
	def getItemByID( self, itemID ):
		"""物品ID"""
		itemList = []
		for item in self._dataList.values():
			if item.id == itemID:
				itemList.append( item )
		return itemList
			
	def getItemByIDList(self, idList):
		""""""
		itemList = []
		for item in self._dataList.values():
			if item.id in idList:
				itemList.append( item )
		return itemList
			
	def getRelationItem( self, itemInst ):
		"""
		获取与添加物品相关的数据
		优化遍历次数
		"""
		unLockItemList = []
		lockItemList = []
		for item in self._dataList.values():
			if item.id == itemInst.id:
				if item.bindType == ItemTypeEnum.BINDED_STATE:
					lockItemList.append(item)
				else:
					unLockItemList.append(item)
		return unLockItemList, lockItemList
	
	def addItem( self, itemInst ):
		"""背包添加物品"""
		order = itemInst.order
		uid = itemInst.uid
		assert order not in self._dataList and uid not in self._uid2order,\
		"Can not add item to bag!same order(%s) or same uid(%ss)"%(order in self._dataList, uid in self._uid2order)
		self._dataList[order] = itemInst
		self._uid2order[uid] = order
	
	def removeByUID( self, uid ):
		"""移除物品"""
		return self.removeByOrder( self.getOrderID(uid) )
	
	def removeByOrder( self, order ):
		"""将物品从背包移除"""
		if order in self._dataList:
			itemInst = self._dataList.pop(order)
			self._uid2order.pop( itemInst.uid )
			return True
		return False
	
	def swapOrder( self, selfEntity, srcOrder, dstOrder ):
		"""交换两个位置上的道具"""
		if self.wieldEquip( selfEntity, srcOrder, dstOrder ) or self.wieldYCJMDEquip(selfEntity, srcOrder, dstOrder):
			return True
		srcItem = self[srcOrder]
		dstItem = self[dstOrder]
		# 可叠加，优先处理叠加
		if srcItem and dstItem and srcItem.id == dstItem.id and srcItem.canStack() and dstItem.canStack():
			if dstItem.canStack(srcItem.amount):
				dstItem.setAmount( selfEntity, srcItem.amount + dstItem.amount)
				if srcItem.isBinded() != dstItem.isBinded():
					dstItem.setBindType(selfEntity, ItemTypeEnum.BINDED_STATE)
				self.removeByOrder(srcItem.order)
				selfEntity.client.CLIENT_removeItem(srcItem.order)
			else:
				leftAmount = srcItem.amount + dstItem.amount - dstItem.overlyingMax
				srcItem.setAmount(selfEntity, leftAmount)
				dstItem.setAmount(selfEntity, dstItem.overlyingMax)
				if srcItem.isBinded() != dstItem.isBinded():
					dstItem.setBindType(selfEntity, ItemTypeEnum.BINDED_STATE)
					srcItem.setBindType(selfEntity, ItemTypeEnum.BINDED_STATE)
			if srcItem.isLimitTimeItem():  # 同ID限时道具堆叠时，取剩余时间较少的作为限时依据
				if int(srcItem.getItemEndTime()) > int(dstItem.getItemEndTime()):
					srcItem.setItemEndTime(selfEntity, dstItem.getItemEndTime())
				elif int(srcItem.getItemEndTime()) < int(dstItem.getItemEndTime()):
					dstItem.setItemEndTime(selfEntity, srcItem.getItemEndTime())
			return True
		# 有可能是空闲的位置
		
			
		if srcItem:
			self.removeByOrder( srcOrder )
		if dstItem:
			self.removeByOrder( dstOrder )
		if srcItem:
			srcItem.setOrder( dstOrder )
			self.addItem( srcItem )
		if dstItem:
			dstItem.setOrder( srcOrder )
			self.addItem(dstItem )
		selfEntity.client.CLIENT_swapItemAC(srcOrder, dstOrder)
		
	def wieldEquip( self, selfEntity, srcOrder, dstOrder ):
		"""穿戴装备"""
		srcBagType = selfEntity.getBagTypeByOrder(srcOrder)
		dstBagType = selfEntity.getBagTypeByOrder(dstOrder)
		
		if srcBagType == ItemTypeEnum.BAG_EQUIP or dstBagType == ItemTypeEnum.BAG_EQUIP:
			if selfEntity.isState(csdefine.ENTITY_STATE_FIGHT):
				selfEntity.statusMessage( csstatus.CAN_NOT_EQUIP_IN_COMBAT )
				return True
			srcItem = self[srcOrder]
			dstItem = self[dstOrder]
			if srcItem.isEquip():
				if dstBagType == ItemTypeEnum.BAG_EQUIP:	#穿上装备
					if not srcItem.canWield(selfEntity):return True
					if srcItem and srcItem.getType() != ItemTypeEnum.ITEM_TYPE_RING:
						if not dstItem and srcItem.getEquipPart() != dstOrder:
							return True
						if dstItem and srcItem.getEquipPart() != dstItem.getEquipPart():
							return True

				if srcItem:
					self.removeByOrder( srcOrder )
				if dstItem:
					self.removeByOrder( dstOrder )
				if srcItem:
					srcItem.setOrder( dstOrder )
					self.addItem( srcItem )
				if dstItem:
					dstItem.setOrder( srcOrder )
					self.addItem(dstItem )
					
				if srcBagType == ItemTypeEnum.BAG_EQUIP:		# 卸下装备
					srcItem.unWield(selfEntity)
				else:
					if dstItem:									#已经有装备
						dstItem.unWield(selfEntity)
					srcItem.wield(selfEntity)
				selfEntity.client.CLIENT_swapItemAC(srcOrder, dstOrder)
			return True
		return False

	def wieldYCJMDEquip(self, selfEntity, srcOrder, dstOrder):
		"""
		穿戴副本临时装备
		"""
		srcBagType = selfEntity.getBagTypeByOrder(srcOrder)
		dstBagType = selfEntity.getBagTypeByOrder(dstOrder)
		
		if srcBagType == ItemTypeEnum.BAG_TEMP_EQUIP or dstBagType == ItemTypeEnum.BAG_TEMP_EQUIP:
			if selfEntity.isState(csdefine.ENTITY_STATE_FIGHT):
				selfEntity.statusMessage( csstatus.CAN_NOT_EQUIP_IN_COMBAT )
				return True
			srcItem = self[srcOrder]
			dstItem = self[dstOrder]
			if not srcItem:
				return True
			if srcItem.isTempEquip():
				#如果源目标是临时装备
				if srcBagType == ItemTypeEnum.BAG_TEMP_EQUIP:
					#目前不允许临时装备换位置
					if dstBagType == ItemTypeEnum.BAG_TEMP_EQUIP:
						return True
					if dstBagType == ItemTypeEnum.BAG_SPACE_COPY:
						#如果是从临时装备栏卸载到副本背包，并且目标位置不为空时
						if dstItem:
							return True
				#如果源目标是副本背包的物品
				if srcBagType == ItemTypeEnum.BAG_SPACE_COPY:
					#从副本背包装备到临时装备栏
					if dstBagType == ItemTypeEnum.BAG_TEMP_EQUIP:
						if dstItem:
							if dstItem.getEquipPart()!= srcItem.getEquipPart():
								return True
						elif dstOrder!=srcItem.getEquipPart():
							return True

				if srcItem:
					self.removeByOrder( srcOrder )
				if dstItem:
					self.removeByOrder( dstOrder )
				if srcItem:
					srcItem.setOrder( dstOrder )
					self.addItem( srcItem )
				if dstItem:
					dstItem.setOrder( srcOrder )
					self.addItem(dstItem )
					
				if srcBagType == ItemTypeEnum.BAG_TEMP_EQUIP:		# 卸下装备
					srcItem.unWield(selfEntity)
				else:
					if dstItem:									#已经有装备
						dstItem.unWield(selfEntity)
					srcItem.wield(selfEntity)
				selfEntity.client.CLIENT_swapItemAC(srcOrder, dstOrder)
				return True
		return False

	
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		return { "items" : list( obj._dataList.values() ) }

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		inst = KitBagTypeImpl()
		for item in dict["items"]:
			#防止物品配置被删除，导致后续初始化无法继续下去 (CST-13029)
			if item is None:
				continue
			
			inst._dataList[item.order] = item
			inst._uid2order[item.uid] = item.order
		return inst

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return True
		return isinstance( obj, KitBagTypeImpl )


instance = KitBagTypeImpl()

