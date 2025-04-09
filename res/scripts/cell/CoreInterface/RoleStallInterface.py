# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
import csconst
import Const
import csstatus
from ItemFactory import ItemFactoryInst
from StallItemListImpl import BuyAndSellList
import time
import ItemTypeEnum
import Functions

class RoleStallInterface:
	"""
	玩家摆摊接口
	"""
	def __init__( self ):
		"""
		"""
		self.stallVerifyID = 0		#def定义参数，不存储到数据库，在查询的时候记录对方玩家entityid，用来做购买验证
		
	def getStallObj( self ):
		from ObjectScript.ObjectScriptFactory import g_objFactory	#防止交叉引用，必须在这里import
		stallObj = g_objFactory.getStallObject( self.spaceScriptID )
#		if stallObj == None:
#			stallObj = g_objFactory.getStallObject( Const.FENG_MING_CHENG_SCRIPTID )
		return stallObj

	def CELL_requestStallItems( self, playerID ):
		"""
		<Exposed method>
		获得上次未收购完成的数据
		"""
		if not self.validateClientCall( playerID ):
			return
		self.remedyStallSellItems()
		for itemData in self.stallSellItems:
			self.setItemLockState( int(itemData.id), True )
		data = {}
		data["stallCollectionItemList"] = self.getStallItemsStringList(self.collectionItems)
		data["stallSellItemList"] = self.getStallItemsStringList(self.stallSellItems)
		#初始化将收购的物品数据发给客户端
		self.client.CLIENT_OnRequestStallItems( self.stallName, data )

	def remedyStallSellItems( self ):
		"""
		重新纠正出售物品
		"""
		delSellData = []
		for itemData in self.stallSellItems:
			itemInst = self.getItemInstByUid(int(itemData.id))
			if itemInst == None or itemInst.isLocking():
				delSellData.append(itemData)
				continue
			if itemInst.amount < itemData.amount:
				itemData.amount = itemInst.amount
		for itemData in delSellData:
			self.stallSellItems.remove(itemData)

	def verifyStallSellItem( self, uid, itemID ,amount, price ):
		"""
		一件出售商品
		"""
		itemInst = self.getItemInstByUid(int(uid))
		if itemInst == None:
			#物品不存在
			return False
		if itemInst.id != itemID:
			return False
		if itemInst.isBinded():
			#物品不能交易
			self.statusMessage(csstatus.STALL_ISBIND_NOSELL,"" )
			return False
		if itemInst.amount < amount:
			#输入的数量超过该物品的叠加数量
			KBEDebug.ERROR_MSG(" (uid=%s)itemInst%i amount%i not more than amount%i "%(uid,itemInst.id,itemInst.amount,amount))
			return False
		if price <= 0:
			#上架的商品还没有价格，请标好价后在上架
			self.statusMessage( csstatus.STALL_MONEY_NONE,"" )
			return False
		totalSellPrice = self.getStallItemTotalSellPrice()
		if not self.isAddMoney( totalSellPrice ):
			self.statusMessage( csstatus.STALL_SELL_MONEY_LIMIT,"" )
			return False
		if len(self.stallSellItems) >= csconst.STALL_ITEM_MAX_COUNT:
			self.statusMessage( csstatus.STALL_ITEM_FULL, "" )
			return False
		return True

	def getStallItemTotalSellPrice( self ):
		"""
		获得出售的总价格
		"""
		totalSellPrice = 0
		for itemData in self.stallSellItems:
			totalSellPrice += itemData.price * itemData.amount
		return totalSellPrice

	def verifyStallCollectItem( self, itemID, amount, price):
		"""
		验证一件收购商品
		"""
		if self.getState() == csdefine.ENTITY_STATE_STALL:
			KBEDebug.ERROR_MSG( "Now state is stall" )
			return False
		tempItem = ItemFactoryInst.createDynamicItem( itemID )
		if tempItem == None:
			KBEDebug.ERROR_MSG(" not has this Item %i"%itemID)
			return
		if tempItem.isEquip():
			self.statusMessage( csstatus.STALL_CAN_NOT_SELL,"" )
			return False
		if tempItem.isBinded():
			KBEDebug.ERROR_MSG( "item (itemID= %i) is Bind"%itemID )
			return False
		if price <= 0:
			#上架的商品还没有价格，请标好价后在上架
			self.statusMessage( csstatus.STALL_MONEY_NONE,"" )
			return False
		#获得背包中空闲格子数
		freeOrder = self.getAllFreeOrder( ItemTypeEnum.BAG_COMMON )
		if len( self.collectionItems ) + 1 > len( freeOrder ):
			self.statusMessage( csstatus.ITEM_SPACE_LESS,"" )
			return False
		if len( self.collectionItems ) + 1 > csconst.STALL_ITEM_MAX_COUNT:
			self.statusMessage( csstatus.STALL_ITEM_FULL, "" )
			return False
		price = self.getCollectionItemTotalPrice()
		if self.money < price:
			self.statusMessage( csstatus.STALL_SELL_MONEY_NOTENOUGH,"" )
			return False
		return True

	def getCollectionItemTotalPrice( self ):
		"""
		获得收购的总价格
		"""
		price = 0
		for collectionItem in self.collectionItems:
			price += collectionItem.price
		return price

	def CELL_addStallCollectionItem( self, playerID, itemID, amount, price ):
		"""
		<exposed method>
		增加收购数据
		"""
		if not self.validateClientCall( playerID ):
			return
		if not self.verifyStallCollectItem( itemID, amount, price ):
			return
		totalPrice = self.getCollectionItemTotalPrice() + amount * price
		if self.money < totalPrice:
			self.statusMessage( csstatus.STALL_SELL_MONEY_NOTENOUGH,"" )
			return
		tempItem = {"id":"", "itemID":itemID,"amount":amount,"price":price }
		self.collectionItems.append( tempItem )
		self.client.CLIENT_AddCollectionItemSuccessCB( tempItem )

	def CELL_addStallSellItem( self, playerID, uid, itemID, amount, price ):
		"""
		<exposed method>
		增加出售数据
		"""
		if not self.validateClientCall( playerID ):
			return
		if not self.verifyStallSellItem(uid,itemID,amount,price):
			return
		if self.isItemLock( int(uid) ):
			KBEDebug.ERROR_MSG("Add item to stall fail!as item(uid : %s, itemID : %d) is locking"%(int(uid), itemID))
			return
		totalSellPrice = self.getStallItemTotalSellPrice() + price * amount
		if not self.isAddMoney( totalSellPrice ):
			self.statusMessage( csstatus.STALL_SELL_MONEY_LIMIT,"" )
			return
		self.setItemLockState( int(uid), True )
		tempItem = {"id":uid, "itemID":itemID,"amount":amount,"price":price}
		self.stallSellItems.append( tempItem )
		self.client.CLIENT_AddStallSellItemSuccessCB( tempItem )

	def CELL_updateStallCollectionItem( self,playerID,slot,itemID,amount,price ):
		"""
		<exposed method>
		更新收购数据
		"""
		if not self.validateClientCall( playerID ):
			return
		itemData = self.getStallCollectionData( slot,itemID )
		if itemData == None:
			KBEDebug.ERROR_MSG( "ItemData is Error" )
		srcAmount = itemData.amount
		srcPrice = itemData.price
		if itemData == None:
			KBEDebug.ERROR_MSG( "update error" )
			return
		self.collectionItems.remove(itemData)
		if not self.verifyStallCollectItem( itemID, amount, price ):
			tempItem = {"id":"", "itemID":itemID,"amount":srcAmount,"price":srcPrice }
			self.collectionItems.insert(slot,tempItem)
			return
		tempItem = {"id":"", "itemID":itemID,"amount":amount,"price":price }
		self.collectionItems.insert(slot,tempItem)
		self.client.CLIENT_UpdateStallCollectionItemCB( slot,tempItem )

	def CELL_updateStallSellItem( self, playerID,slot,itemID, amount,price ):
		"""
		<exposed method>
		更新出售数据
		"""
		if not self.validateClientCall( playerID ):
			return
		itemData = self.getStallSellItemData( slot,itemID )
		srcAmount = itemData.amount
		srcPrice = itemData.price
		id = itemData.id
		if itemData == None:
			KBEDebug.ERROR_MSG( "update error" )
			return
		self.stallSellItems.remove(itemData)
		if not self.verifyStallSellItem( id,itemID,amount,price ):
			tempItem = {"id":id, "itemID":itemID,"amount":srcAmount,"price":srcPrice }
			self.stallSellItems.insert( slot,tempItem)
			return
		tempItem = {"id":id, "itemID":itemID,"amount":amount,"price":price }
		self.stallSellItems.insert(slot,tempItem)
		self.client.CLIENT_UpdateStallSellItemCB( tempItem )
		self.statusMessage(csstatus.STALL_UPDATA_SUCCESSFUL ,"")

	def CELL_removeStallSellItem( self,playerID,slot,itemID ):
		"""
		<Exposed method>
		下架出售物品
		"""
		if not self.validateClientCall( playerID ):
			return
		itemData = self.getStallSellItemData( slot,itemID )
		if itemData == None:
			KBEDebug.ERROR_MSG( "remove error" )
			return False
		self.setItemLockState( int(itemData.id), False )
		del self.stallSellItems[slot]
		self.client.CLIENT_RemoveStallSellItemCB(playerID, slot)
		return True

	def CELL_removeStallCollectionItem( self,playerID,slot,itemID ):
		"""
		<Exposed method>
		下架收购物品
		"""
		if not self.validateClientCall( playerID ):
			return
		itemData = self.getStallCollectionData( slot,itemID )
		if itemData == None:
			KBEDebug.ERROR_MSG( "remove error" )
			return False
		del self.collectionItems[slot]
		self.client.CLIENT_RemoveStallCollectionItemCB( playerID, slot )
		return True

	def CELL_findStallPoint( self, srcEntityID ):
		"""
		<Exposed method>
		查找摆摊点（一个摆摊点对应一个摊位）
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		#玩家等级验证
		if self.level < 20:
			self.statusMessage( csstatus.LEVEL_CANNOT_SATISFY,20 )
			return

		#玩家的状态验证
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			self.statusMessage( csstatus.STALL_FORBIDDEN_STATE,"" )
			return
			
		if self.isPWKitBagLock():
			self.statusMessage( csstatus.STALL_MUST_BE_UNLOCK,"" )
			return
			
		if self.stallPoint:return
		stallObj = self.getStallObj()
		if stallObj == None:
			self.statusMessage( csstatus.STALL_SCRIPTID_NO_POINT,"" )
			return
		number = stallObj.autoFindStallPoint(self)
		if number == None:
			self.statusMessage( csstatus.STALL_POINT_IS_FULL,"" )
			return
		self.stallPoint = number
		stallObj.setStallPoint( self, number )
		self.client.CLIENT_OnFindStallPoint( stallObj.scriptID, number)
	
	def CELL_onNavigateStallFinish( self, srcEntityID ):
		"""
		Exposed method
		到达摆摊目标点
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		stallObj = self.getStallObj()
		if stallObj == None:
			self.statusMessage( csstatus.STALL_SCRIPTID_NO_POINT,"" )
			return
		stallObj.setStallPosAndDir(self,self.stallPoint)
		self.withdrawPetByReason( csdefine.PET_WITHDRAW_STALL )
		
		acts = [csdefine.ACTION_FORBID_MOVE, csdefine.ACTION_FORBID_SPELL,
		csdefine.ACTION_FORBID_JUMP, csdefine.ACTION_FORBID_TRANSLATE_DIRECTION,
		csdefine.ACTION_FORBID_EMERGENCY_EXIT, csdefine.ACTION_FORBID_CONJURE_PET]
		self.actCounterIncList( acts )
	
	def CELL_cancelStall( self, srcEntityID ):
		"""
		Exposed method
		取消摆摊（跟摆摊结束不同）
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		# 摆摊状态不会走这个 流程
		if self.isState( csdefine.ENTITY_STATE_STALL ):
			KBEDebug.ERROR_MSG("Can not calcel stall!as role(%d) is stalling "%self.id)
			return
		acts = [csdefine.ACTION_FORBID_MOVE, csdefine.ACTION_FORBID_SPELL,
		csdefine.ACTION_FORBID_JUMP, csdefine.ACTION_FORBID_TRANSLATE_DIRECTION,
		csdefine.ACTION_FORBID_EMERGENCY_EXIT, csdefine.ACTION_FORBID_CONJURE_PET]
		self.actCounterDecList( acts )
		#若摆摊前幻兽已存在，则摆摊结束后自动召唤出幻兽
		self.conjurePetByWithdraw()
		
		stallObj = self.getStallObj()
		if stallObj == None:
			self.statusMessage( csstatus.STALL_SCRIPTID_NO_POINT,"" )
			return
		self.getStallObj().cancelStallPoint(self)
		self.stallPoint = ""
		for itemData in self.stallSellItems:
			self.setItemLockState( int(itemData.id), False )
	
	def CELL_startStall( self, playerID,stallName ):
		"""
		<exposed method>
		开始摆摊
		"""
		if not self.validateClientCall( playerID ):
			return

		#玩家等级验证
		if self.level < 20:
			self.statusMessage( csstatus.LEVEL_CANNOT_SATISFY,20 )
			return
			
		totalSellPrice = self.getStallItemTotalSellPrice()
		if not self.isAddMoney( totalSellPrice ):
			self.statusMessage( csstatus.STALL_FAIL_FULL_MONEY,"" )
			return
		
		#判断下携带的金钱是否足够
		price = self.getCollectionItemTotalPrice()
		if self.money < price:
			self.statusMessage( csstatus.STALL_SELL_MONEY_NOTENOUGH,"" )
			return
		
		#玩家的状态验证
		if self.getState() == csdefine.ENTITY_STATE_DEAD:
			self.statusMessage( csstatus.STALL_FORBIDDEN_STATE,"" )
			return
		stallObj = self.getStallObj()
		if stallObj == None:
			self.statusMessage( csstatus.STALL_SCRIPTID_NO_POINT,"" )
			return
#		number = stallObj.autoFindStallPoint(self)
#		if number == None:
#			self.statusMessage( csstatus.STALL_POINT_IS_FULL,"" )
#			return
		# 位置验证
		if not stallObj.stallPointVerify( self,self.stallPoint ):
			return

		if len( self.collectionItems ) <= 0 and len( self.stallSellItems ) <= 0:
			self.statusMessage( csstatus.STALL_ITEM_NULL,"" )
			return
		# 摊位名称验证
		if len(stallName) > csconst.STALL_NAME_MAX_LENGTH:
			self.statusMessage( csstatus.STALL_NAME_TOO_LONG,"" )
			return

		#是否在跟随中
		if self.isNormalFollowing():
			self.cancelNormalFollowFC( self.id )

		#收购验证背包空间
		freeOrder = self.getAllFreeOrder( ItemTypeEnum.BAG_COMMON )
		if len( self.collectionItems ) > len( freeOrder ):
			self.statusMessage( csstatus.STORE_BAG_HAS_ENOUGH,"" )
			return

#		stallObj.setStallPosAndDir( self, self.stallPoint )
		self.stallName = stallName
		self.stallSuccess()

	def stallSuccess( self ):
		"""
		摆摊成功回调
		"""
		self.changeState( csdefine.ENTITY_STATE_STALL )
		self.client.CLIENT_StallSuccessCB(int(csconst.ROLE_STALL_PRICE * 100))

	def CELL_endStall( self, playerID ):
		"""
		<Exposed method>
		结束摆摊
		"""
		if not self.validateClientCall( playerID ):
			return
		
		#删除摆摊点
		self.getStallObj().cancelStallPoint(self)
		
		acts = [csdefine.ACTION_FORBID_MOVE, csdefine.ACTION_FORBID_SPELL,
		csdefine.ACTION_FORBID_JUMP, csdefine.ACTION_FORBID_TRANSLATE_DIRECTION,
		csdefine.ACTION_FORBID_EMERGENCY_EXIT, csdefine.ACTION_FORBID_CONJURE_PET]
		self.actCounterDecList( acts )
		
		#改变状态
		if self.getState() == csdefine.ENTITY_STATE_STALL:
			self.changeState( csdefine.ENTITY_STATE_FREE )
		#若摆摊前幻兽已存在，则摆摊结束后自动召唤出幻兽
		self.conjurePetByWithdraw()
		
		self.stallPoint = ""
		self.stallVerifyID = 0
		for itemData in self.stallSellItems:
			self.setItemLockState( int(itemData.id), False )
		
		#如果背包没有空闲位置了，则下架所有未完成收购的物品(CST-8985)
		if len(self.getAllFreeOrder(ItemTypeEnum.BAG_COMMON)) <= 0:
			for slot in range(len(self.collectionItems)):
				self.client.CLIENT_RemoveStallCollectionItemCB(playerID, slot)
			self.collectionItems.clear()

	def CELL_openRoleStall( self, playerID, entityID ):
		"""
		<exposed method>
		打开其他人摊位
		"""
		if not self.validateClientCall( playerID ):
			return
		# 地图验证
		role = KBEngine.entities.get( entityID, None )
		if role == None:
			# 玩家不和你在一个地图内
			KBEDebug.ERROR_MSG( "queryStallRole::stall  role error" )
			return

		if role.spaceID != self.spaceID:
			# 玩家不和你在一个地图内
			KBEDebug.ERROR_MSG( "queryStallRole::stall spaceID role error" )
			return

		# 距离验证
		if role.position.flatDistTo( self.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
			# 距离摆摊位置过远
			self.statusMessage( csstatus.STALL_OPEN_TOO_FAR,"" )
			return

		self.stallVerifyID = entityID
		dct = {}
		dct["stallSellItemList"] = self.getOtherStallSellItemInst(role)
		dct["stallCollectionItemList"] = self.getStallItemsStringList(role.collectionItems)
		data = BuyAndSellList().createObjFromDict(dct)
		self.client.CLIENT_OnReceiveOtherStallItems( entityID, role.stallName, data )

	def getStallItemsStringList( self,stallItems ):
		"""
		获取摆摊数据
		"""
		stringList = []
		for item in stallItems:
			stringList.append(item.getDict())
		return stringList
		
	def getOtherStallSellItemInst( self, role ):
		"""获取目标摆摊出售物品实例数据"""
		stringList = []
		for item in role.stallSellItems:
			tempDict = item.getDict()
			itemInst = role.getItemInstByUid( int(item.id ) )
			if itemInst is None:continue
			tempDict.update( itemInst.getClientTipDynamicProperty() )
			stringList.append(tempDict)
		return stringList

	def CELL_buyStallItem( self, playerID, entityID, slot, itemID, amount ):
		"""
		<exposed method>
		购买摆摊物品
		"""
		if not self.validateClientCall( playerID ):
			return
		if amount < 1:
			KBEDebug.ERROR_MSG("buy amount is error %i"%amount)
			return
		role = KBEngine.entities.get( entityID,None )
		if role == None:
			# 玩家不和你在一个地图内
			KBEDebug.ERROR_MSG( "queryStallRole::stall point role error" )
			return
		if role.spaceID != self.spaceID:
			# 玩家不和你在一个地图内
			KBEDebug.ERROR_MSG( "queryStallRole::stall point role error" )
			return
		# 距离验证
		if role.position.flatDistTo( self.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
			# 距离摆摊位置过远
			self.statusMessage( csstatus.STALL_OPEN_TOO_FAR,"" )
			return
		#状态验证
		if role.getState() != csdefine.ENTITY_STATE_STALL:
			self.statusMessage( csstatus.STALL_END,"" )
			return
		if self.stallVerifyID != entityID:
			KBEDebug.ERROR_MSG( "%i Stall is error (self = %i)"%(entityID,self.id) )
			return
		itemData = role.getStallSellItemData( slot,itemID )
		if itemData == None:
			self.statusMessage( csstatus.STALL_ITEM_SOLD_OUT,"" )
			KBEDebug.ERROR_MSG( "ItemData is Error" )
			return
		if self.anotherRoleTradeEntity != None:
			KBEDebug.ERROR_MSG( "anotherRoleTradeEntity is not None!" )
			return
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO:
			return
		
		#测试一下，是否还能放得下物品
		itemInst = role.getItemInstByUid( int(itemData.id ))
		if self.addItemCheck(itemInst) != csstatus.ITEM_GO_ON:
			self.statusMessage(csstatus.PLAYERTRADE_KITBAG_NOT_ENOUGH)
			return
		
		self.anotherRoleTradeEntity = role
		itemData.num = amount
		payItems = { csdefine.TRADE_PAY_ITEM_BUY_STALLGOODS : itemData}
		self.requestPay(csdefine.TRADE_TYPE_ROLE_STALL, entityID, payItems, role, csdefine.STALL_SELL_ITEM, slot, itemData)
	
	def onSuccessPayStall( self, role, type, slot, itemData ):
		"""
		成功交易回调（出售、购买）
		"""
		self.anotherRoleTradeEntity = None
		itemData.amount -= itemData.num
		
		if itemData.amount == 0:
			if type == csdefine.STALL_SELL_ITEM:
				del role.stallSellItems[slot]
				self.client.CLIENT_RemoveStallSellItemCB( role.id, slot )
				role.client.CLIENT_RemoveStallSellItemCB( role.id, slot )
			else:
				del role.collectionItems[slot]
				self.client.CLIENT_RemoveStallCollectionItemCB(role.id,slot)
				role.client.CLIENT_RemoveStallCollectionItemCB(role.id,slot)
		else:
			self.client.CLIENT_UpdateStallItem( type,slot,role.id, itemData.getDict() )
			role.client.CLIENT_UpdateStallItem( type,slot,role.id, itemData.getDict() )
			dct = {}
			dct["stallSellItemList"] = self.getOtherStallSellItemInst(role)
			dct["stallCollectionItemList"] = self.getStallItemsStringList(role.collectionItems)
			data = BuyAndSellList().createObjFromDict(dct)
			self.client.CLIENT_UpdateOtherStallItems( role.id, data )
			
	def onFailPayStall( self, role, type, slot, itemData ):
		"""
		失败交易回调（出售、购买）
		"""
		self.anotherRoleTradeEntity = None
	
	def getStallSellItemData( self,slot,itemID ):
		"""
		获得出售的商品
		"""
		if len( self.stallSellItems ) > slot:
			itemData = self.stallSellItems[slot]
			if itemData.itemID == itemID:
				return itemData
		return None

	def getStallCollectionData( self,slot,itemID ):
		"""
		获得收购的商品
		"""
		if len( self.collectionItems ) > slot:
			itemData = self.collectionItems[slot]
			if itemData.itemID == itemID:
				return itemData
		return None

	def CELL_sellStallItem( self, playerID, entityID, slot, itemID, amount ):
		"""
		<exposed method>
		出售物品给摊位
		"""
		if not self.validateClientCall( playerID ):
			return
		if amount < 1:
			KBEDebug.ERROR_MSG("sell amount is error %i"%amount)
			return
		role = KBEngine.entities.get( entityID,None )
		if role == None:
			# 玩家不和你在一个地图内
			KBEDebug.ERROR_MSG( "queryStallRole::stall point role error" )
			return
		if role.spaceID != self.spaceID:
			# 玩家不和你在一个地图内
			KBEDebug.ERROR_MSG( "queryStallRole::stall point role error" )
			return
		# 距离验证
		if role.position.flatDistTo( self.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
			# 距离摆摊位置过远
			self.statusMessage( csstatus.STALL_OPEN_TOO_FAR,"" )
			return
		#状态验证
		if role.getState() != csdefine.ENTITY_STATE_STALL:
			self.statusMessage( csstatus.STALL_END,"" )
			return
			
		if self.stallVerifyID != entityID:
			KBEDebug.ERROR_MSG( "%i Stall is error (self = %i)"%(entityID,self.id) )
			return
			
		#卖完了意味着已经下架了。
		itemData = role.getStallCollectionData( slot,itemID )
		if itemData == None:
			self.statusMessage( csstatus.STALL_ITEM_SOLD_OUT,"" )
			KBEDebug.ERROR_MSG( "ItemData is Error" )
			return
		
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO:
			return
		self.anotherRoleTradeEntity = role
		itemData.num = amount
		payItems = { csdefine.TRADE_PAY_ITEM_SELL_STALLGOODS : itemData}
		self.requestPay(csdefine.TRADE_TYPE_ROLE_STALL, entityID, payItems, role, csdefine.STALL_COLLECTION_ITEM, slot, itemData)

