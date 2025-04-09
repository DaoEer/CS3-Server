# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
import Functions
import ItemTypeEnum

class StoreBags( dict ):
	def __init__( self ):
		self.isSendEntityID = 0						# 用于优化重复发送物品到客户端的问题
		self.unLockStoreGridNum = 0
		
	def addToolItem( self, playerMB, item, bagType ):
		"""添加物品"""
		order = self.getFreeOrder(bagType)
		item.order = order
		self[order] = item
		if playerMB and playerMB.client:
			self.addItemToClient(playerMB, item)
	
	def getFreeOrder( self, bagType ):
		"""
		获取指定区间内的空闲格子
		"""
		if bagType == ItemTypeEnum.BAG_STORE:
			start = ItemTypeEnum.BAG_STORESTART
			end = start + ItemTypeEnum.STORE_CAPACITY + self.unLockStoreGridNum
		elif bagType == ItemTypeEnum.BAG_WORK_SHOP_LOCKERS:
			start = ItemTypeEnum.BAG_WORK_SHOP_LOCKERS_START
			end = start + ItemTypeEnum.STORE_LOCKERS_CAPACITY + self.unLockStoreGridNum
		elif bagType == ItemTypeEnum.BAG_ALCHEMIST_LOCKERS:
			start = ItemTypeEnum.BAG_ALCHEMIST_LOCKERS_START
			end = start + ItemTypeEnum.STORE_LOCKERS_CAPACITY + self.unLockStoreGridNum
		for index in range( start , end ):
			if not index in self:
				return index
		return None
			
	def getFreeNum( self, bagType ):
		"""获取空格数量"""
		if bagType == ItemTypeEnum.BAG_WORK_SHOP_LOCKERS:
			start = ItemTypeEnum.BAG_WORK_SHOP_LOCKERS_START
			end = start + ItemTypeEnum.STORE_LOCKERS_CAPACITY + self.unLockStoreGridNum
		elif bagType == ItemTypeEnum.BAG_ALCHEMIST_LOCKERS:
			start = ItemTypeEnum.BAG_ALCHEMIST_LOCKERS_START
			end = start + ItemTypeEnum.STORE_LOCKERS_CAPACITY + self.unLockStoreGridNum
		return end - start - len(self)
			
	def sendItemsToClient(self, playerMB):
		"""发送数据到客户端"""
		if self.isSendEntityID != playerMB.id:
			self.isSendEntityID = playerMB.id
			for item in self.values():
				self.addItemToClient(playerMB, item)
		
	def addItemToClient( self, playerMB, itemInst ):
		"""
		添加物品到客户端
		"""
		if playerMB:
			playerMB.client.addStoreItem( itemInst.getDictForClient( playerMB ) )

	def updateOneDataToClient(self, playerMB, propertyname, propertyvalue, itemInst):
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

	def removeItemToClient( self, playerMB, order ):
		"""
		通知客户端删除物品
		"""
		if order in self and playerMB:
			playerMB.client.CLIENT_removeStoreItem( order )
			return self.pop(order)
		
	def setUnLockGridNum( self, num ):
		self.unLockStoreGridNum = num
	
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		tempDict = {}
		tempDict["bag"] = []
		for order, item in obj.items():
			tempDict["bag"].append( {"order":order, "item":item } )
		tempDict["unLockStoreGridNum"] = obj.unLockStoreGridNum
		return  tempDict
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		解包
		"""
		bags = StoreBags()
		for bagData in proDict["bag"]:
			bags[bagData["order"]] = bagData["item"]
		bags.unLockStoreGridNum = proDict["unLockStoreGridNum"]
		return bags
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, StoreBags )

class AlchemistBags( dict ):
	def addPlayerItem( self, playerMB, playerDBID, item, bagType ):
		"""玩家获得物品"""
		if not playerDBID in self:
			self[playerDBID] = StoreBags()
		self[playerDBID].addToolItem( playerMB, item, bagType )
		
	def getFreeNum(self, playerDBID, bagType):
		"""获取玩家的空闲格子数量"""
		if playerDBID in self:
			return self[playerDBID].getFreeNum(bagType)
		return ItemTypeEnum.STORE_LOCKERS_CAPACITY
		
	def getUnlockNum(self, playerDBID):
		"""获取储物柜中解锁的格子"""
		if playerDBID in self:
			return self[playerDBID].unLockStoreGridNum
		return 0
	
	def pop(self, playerCell, playerDBID, order):
		"""移除物品"""
		if playerDBID in self:
			return self[playerDBID].removeItemToClient(playerCell, order)
		
	def sendItemsToClient(self, playerCell, playerDBID):
		"""发送数据到客户端"""
		if playerDBID in self and playerCell and playerCell.client:
			self[playerDBID].sendItemsToClient(playerCell)
	
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		tempDict = {}
		tempDict["alchemist"] = []
		for playerDBID, bags in obj.items():
			tempDict["alchemist"].append( {"playerDBID":playerDBID, "bags":bags } )
		return  tempDict
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		解包
		"""
		alchemist = AlchemistBags()
		for bagData in proDict["alchemist"]:
			alchemist[bagData["playerDBID"]] = bagData["bags"]
		return alchemist
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, AlchemistBags )



g_StoreBags = StoreBags()
g_AlchemistBags = AlchemistBags()

