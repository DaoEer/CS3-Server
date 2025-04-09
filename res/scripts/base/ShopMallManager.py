import KBEDebug
import KBEngine
from CoreObject import MgrPersistentObject
from ConfigObject.ShopMall.ShopMallMgr import g_shopMallMgr
from Functions import Functor
import json
import csdefine
import time
import csstatus
import csconst
import Functions


class ShopMallManager( MgrPersistentObject.MgrPersistentObject ):
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.shopMallList = {} 
		self.timerID = 0
		self.tradeTimeID = 0
		self.checkGivingGoodsData()
		
		config = g_shopMallMgr.getAll()
		if len(config) <= 0:
			self.onCompleteInit()
			return
		
		self.initShop = len(config)
		for id, value in config.items():
			query = "select id from tbl_%s where sm_%s = '%s' limit 1" %("ShopMall", "shopMallTypeId" , id)
			KBEngine.executeRawDatabaseCommand( query, Functor(self._onCreateBaseFromDB, id, value) )

	def _onCreateBaseFromDB(self, shopMallTypeId, value, resultSet, rows, insertid,errstr ):
		"""
		查询数据库回调
		"""
		if self.isDestroyed:
			return
			
		if errstr is not None:
			KBEDebug.ERROR_MSG( errstr )
			return	
		
		if len(resultSet) == 0:
			Functor(self._onCreateShopMall, shopMallTypeId, value)(None, 0, True)
		else:
			KBEngine.createEntityFromDBID( "ShopMall", int(resultSet[0][0]), Functor(self._onCreateShopMall, shopMallTypeId, value))

	def _onCreateShopMall( self, shopMallTypeId, shopData, baseRef, databaseID, wasActive ):
		"""
		创建entity回调
		"""
		if self.isDestroyed:
			return
			
		if baseRef == None:
			params = {
				"shopMallTypeId" : shopMallTypeId,
			}
			baseRef = KBEngine.createEntityLocally( "ShopMall", params )

		self.shopMallList[int(shopMallTypeId)] = baseRef
		baseRef.init( shopMallTypeId, shopData )
		baseRef.writeToDB()
		
		self.initShop -= 1
		if self.initShop <= 0:
			self.onCompleteInit()

	def requestShopMallItemList( self,role ):
		"""
		<Define method>
		请求商城的物品列表
		"""
		data = {}
		for shopMallTypeId in self.shopMallList:
			items = self.shopMallList[shopMallTypeId].getShopMallData()
			data[shopMallTypeId] = items.getString()
		role.client.GetShopMallItemList( json.dumps(data) )

	def requestBuyShopMallItem(self, buyDataListStr,couponUID,role,targetDBID ):
		"""
		<Define method>
		请求购买商城中的商品
		"""
		try:
			buyDataList = json.loads( buyDataListStr )
		except:
			KBEDebug.ERROR_MSG("data is error")
			return
		xianShiPrice = 0
		lingShiPrice = 0
		xuanShiPrice = 0
		isAmountLimitItem = False #是否为限量的商品
		for buyData in buyDataList:
			if int(buyData[0]) not in self.shopMallList:
				KBEDebug.ERROR_MSG("requestBuyShopMallItem shopMallTypeId is not in self.shopMallList  ")
				return
			if self.shopMallList[int(buyData[0])].getItemConfig(buyData[1]) == None:
				KBEDebug.ERROR_MSG("This ShopMall is not Open")
				return
			if self.shopMallList[int(buyData[0])].getItemData( buyData[1] ) != None:
				if len( buyDataList ) == 1:
					isAmountLimitItem = True
				else:
					KBEDebug.ERROR_MSG(" AmountLimit item is not allow together to Buy ")
					return
			if isAmountLimitItem:
				if len(couponUID) != 0:
					KBEDebug.ERROR_MSG(" AmountLimit item is not allow to use couponUID ")
					return
				#判断限量的商品是否足够
				if self.shopMallList[int(buyData[0])].reduceShopMallItemCheck( buyData[1],buyData[2],buyData[3] ) == False:
					KBEDebug.ERROR_MSG(" AmountLimit item is not enouth ")
					return
			price = self.shopMallList[int(buyData[0])].requestBuyShopMallItemPrice( buyData[0],buyData[1],buyData[2],buyData[3],buyData[4],couponUID,role )
			if price < 0:
				return
			if buyData[4] == csdefine.SHOP_MONEY_TYPE_XIANSHI:
				xianShiPrice += price
			if buyData[4] == csdefine.SHOP_MONEY_TYPE_LINGSHI:
				lingShiPrice += price
			if buyData[4] == csdefine.SHOP_MONEY_TYPE_XUANSHI:
				xuanShiPrice += price
		role.requestBuyShopMallItemCB( xianShiPrice,lingShiPrice,xuanShiPrice,isAmountLimitItem, buyDataListStr,couponUID,targetDBID )
		
	def returnBuyShopMallItem( self,isAmountLimitItem, buyDataListStr ):
		"""
		<Define method>
		返回商城中的商品
		"""
		try:
			buyDataList = json.loads( buyDataListStr )
		except:
			KBEDebug.ERROR_MSG("data is error")
			return
		if len( buyDataList ) == 1:
			if int(buyDataList[0][0]) not in self.shopMallList:
				KBEDebug.ERROR_MSG("returnBuyShopMallItem shopMallTypeId is not in self.shopMallList  ")
				return
			if isAmountLimitItem:
				if self.shopMallList[int(buyDataList[0][0])].addShopMallItem( buyDataList[0][1],buyDataList[0][2], buyDataList[0][3] ) == False:
					KBEDebug.ERROR_MSG("returnBuyShopMallItem::return buy items id %s, amount %s, is error"%(buyDataList[0][2], buyDataList[0][3]))
			else:
				KBEDebug.INFO_MSG(" This Item is not AmountLimit ")

	def addToGivingGoodsData(self, goodsData ):
		"""
		<Define method>
		赠送好友物品时添加数据
		@param goodsData ：赠送物品数据
		@type goodsData：GOODS_DATA
		"""
		uid = goodsData["uid"]
		if uid in self.givingGoodsData.keys():
			del self.givingGoodsData[uid]
		self.givingGoodsData[uid] = goodsData
		self.writeToDB()
		if self.timerID == 0:
			self.timerID = self.addTimerCallBack( 48*3600 , "overdueFromWaitToDealGivingGoodsData",(uid,) )

	def overdueFromWaitToDealGivingGoodsData(self, goodsDataUID ):
		"""
		过期赠送好友的物品数据
		"""
		goodsData = self.givingGoodsData.get(goodsDataUID,None)
		if goodsData == None:
			return
		goodsData["state"] = csdefine.GIVING_GOODSDATA_OVERDUE_STATE
		goodsData["changeTime"] = time.time()
		self.givingGoodsData[goodsDataUID] = goodsData
		self.popTimer( self.timerID )
		goodsData = self.getMinTimeOfGivingGoodsData( self.givingGoodsData )
		if goodsData:
			if self.timerID <= 0:
				self.timerID = self.addTimerCallBack( 48*3600 - (time.time()-goodsData["givingTime"]),"overdueFromWaitToDealGivingGoodsData",(goodsData["uid"],) )
		self.writeToDB()

	def dealToGivingGoodsData( self, goodsDataUID, currentTime, dealGivingGoodsData):
		"""
		<Define method>
		处理玩家赠送物品数据接口
		"""
		goodsData = self.givingGoodsData.get( goodsDataUID,None )
		if goodsData == None:
			return
		if dealGivingGoodsData == csdefine.AGREE_TO_RECEIVEGIVINGGOODSDATA:
			goodsData["state"] = csdefine.GIVING_GOODSDATA_RECEIVE_STATE
		elif dealGivingGoodsData == csdefine.REFUSE_TO_RECEIVEGIVINGGOODSDATA:
			goodsData["state"] = csdefine.GIVING_GOODSDATA_REFUSE_STATE
		elif dealGivingGoodsData == csdefine.WITHDRAW_TO_GIVEGOODSDATA:
			goodsData["state"] = csdefine.GIVING_GOODSDATA_WITHDRAW_STATE
		goodsData["changeTime"] = currentTime
		self.givingGoodsData[goodsDataUID] = goodsData
		self.writeToDB()

	def clearGivingGoodsDataRecord( self, goodsDataUIDs,roleDBID ):
		"""
		<Define method>
		清除赠送物品数据的记录
		"""
		for goodsDataUID in goodsDataUIDs:
			goodsData = self.givingGoodsData.get(goodsDataUID,None)
			if goodsData == None:
				KBEDebug.ERROR_MSG("clearGivingGoodsDataRecord goodsData is error")
				return
			if goodsData["state"] == csdefine.GIVING_GOODSDATA_WAIT_STATE:
				KBEDebug.ERROR_MSG("clearGivingGoodsDataRecord goodsData is not allow")
				return
		needToDelGoodsDataUIDList = []
		for goodsDataUID in goodsDataUIDs:
			goodsData = self.givingGoodsData.get(goodsDataUID)
			if goodsData["playerDbid"] == roleDBID:
				goodsData["playerIsClear"] = csdefine.GIVING_GOODSDATA_CLEAR_YES
				if goodsData["targetIsClear"] == csdefine.GIVING_GOODSDATA_CLEAR_YES:
					needToDelGoodsDataUIDList.append(goodsDataUID)
			if goodsData["targetDbid"] == roleDBID:
				goodsData["targetIsClear"] = csdefine.GIVING_GOODSDATA_CLEAR_YES
				if goodsData["playerIsClear"] == csdefine.GIVING_GOODSDATA_CLEAR_YES:
					needToDelGoodsDataUIDList.append(goodsDataUID)
		if len( needToDelGoodsDataUIDList ) > 0:
			for goodsDataUID in needToDelGoodsDataUIDList:
				del self.givingGoodsData[goodsDataUID]
		self.writeToDB()

	def onRoleLoginInitGivingGoodsData(self,role,roleDBID):
		"""
		<Define method>
		玩家上线后同步ShopMallManager中的赠送物品的数据
		"""
		#从需要处理数据中同步
		data = {}
		givingData = []
		receiveData = []
		for goodsDataUID,goodsData in self.givingGoodsData.items():
			itemName = role.getGoodsDataName(goodsData["itemList"])
			itemAmount = role.getGoodsDataItemAmount(goodsData["itemList"])
			itemID = role.getGoodsDataItemID(goodsData["itemList"])
			if goodsData["targetDbid"] == roleDBID:
				role.sharedToReceiveGoodsData( goodsDataUID,goodsData )
				if goodsData["targetIsClear"] == csdefine.GIVING_GOODSDATA_CLEAR_NO:
					tempData = {"uid":goodsData["uid"],"itemID":itemID,"itemName":itemName,"amount":itemAmount,"time":str(goodsData["givingTime"]),"playerName":role.getFriendNameBuyPlayerDBID(goodsData["targetDbid"]),"state":goodsData["state"]}
					receiveData.append( tempData )
			if goodsData["playerDbid"] == roleDBID:
				role.sharedToGivingGoodsData( goodsDataUID,goodsData )
				if goodsData["playerIsClear"] == csdefine.GIVING_GOODSDATA_CLEAR_NO:
					tempData = {"uid":goodsData["uid"],"itemID":itemID,"itemName":itemName,"amount":itemAmount,"time":str(goodsData["givingTime"]),"playerName":role.getFriendNameBuyPlayerDBID(goodsData["playerDbid"]),"state":goodsData["state"]}
					givingData.append( tempData )
		data["givingGoodsData"] = givingData
		data["reveiveGoodsData"] = receiveData
		role.client.InitGoodsDataRecord(data)

	def checkGivingGoodsData( self ):
		"""
		检查赠送物品的数据是否过期
		"""
		if len( self.givingGoodsData ) <= 0:
			return
		goodsDataUIDList = []
		for goodsDataUID,goodsData in self.givingGoodsData.items():
			currentTime = time.time()
			deltaTime = currentTime - goodsData["givingTime"]
			if deltaTime > 48*3600:
				goodsDataUIDList.append( goodsDataUID )
		if len( goodsDataUIDList ) > 0:
			for goodsDataUID in goodsDataUIDList:
				self.overdueFromWaitToDealGivingGoodsData( goodsDataUID )

	def getMinTimeOfGivingGoodsData( self,givingGoodsDataList ):
		"""
		获得赠送的物品数据的最小赠送时间的赠送物品数据，用于添加定时器
		"""
		if len(givingGoodsDataList) < 0 :
			return None
		goodsDataTimeList = []
		for goodsDataUID,goodsData in givingGoodsDataList.items():
			goodsDataTimeList.append(goodsData["givingTime"])
		if len(goodsDataTimeList) < 0:
			return None
		goodsDataTimeList.sort()
		for goodsDataUID,goodsData in givingGoodsDataList.items():
			if goodsData["givingTime"] == goodsDataTimeList[0]:
				return goodsData
		return None

#--------------------灵石寄售-------------------------

	def requestGetOrder( self, role, roleDBID ):
		"""
		<Define method>
		获得订单
		"""
		data = {}
		myOrderList = []
		sellOrderList = []
		collectOrderList = []
		for tradeData in self.lingShiTradeData.values():
			tradeData["remainTime"] = str(int(tradeData["endTime"]) - Functions.getTime())
			tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"] * 100,"price":tradeData["price"],"remainTime":tradeData["remainTime"],"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"]}
			if tradeData["playerDbid"] == roleDBID:
				role.addOrder( tradeData )
				myOrderList.append( tempData )
			if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL and int(tradeData["remainTime"]) > 0 and tradeData["amount"] > 0:
				role.addAllLingShiTradeSellOrder( tradeData )
				sellOrderList.append( tempData )
			if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT and int(tradeData["remainTime"]) > 0 and tradeData["amount"] > 0:
				role.addAllLingShiTradeCollectOrder( tradeData )
				collectOrderList.append( tempData )
		data["lingShiTradeOrder"] = myOrderList
		data["allLingShiTradeSellOrder"] = sellOrderList
		data["allLingShiTradeCollectOrder"] = collectOrderList
		data["tax"] = int(csconst.LINGSHI_TRADE_PRICE * 100)
		role.client.GetAllOrderCB( data ) 

	def addLingShiTradeData( self, tradeData, role ):
		"""
		<Define method>
		增加寄售数据
		"""
		uid = tradeData["uid"]
		self.lingShiTradeData[uid] = tradeData
		if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL:
			role.addSellOrderCB(tradeData)
		elif tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
			role.addCollectOrderCB(tradeData)
		self.writeToDB()
		if self.tradeTimeID == 0:
			self.tradeTimeID = self.addTimerCallBack( 72*3600 , "overdueLingShiTradeData",(uid,) )

	def overdueLingShiTradeData( self, tradeDataUID ):
		"""
		寄售数据过期
		"""
		tradeData = self.lingShiTradeData.get( tradeDataUID,None )
		if tradeData == None:
			return
		tradeData["remainTime"] = "-1"
		self.lingShiTradeData[tradeDataUID] = tradeData
		self.popTimer(self.tradeTimeID)
		self.tradeTimeID = 0
		tradeData = self.getMinTimeOfTradeData( self.lingShiTradeData )
		if tradeData == None:
			return
		if self.tradeTimeID <= 0:
			self.tradeTimeID = self.addTimerCallBack( (int(tradeData["endTime"]) - Functions.getTime())/csconst.TIME_ENLARGE_MULTIPLE,"overdueLingShiTradeData",(tradeData["uid"]) )
		self.writeToDB()

	def dealLinShiTradeOrder( self, amount, totalPrice, uid, type, role, roleDBID ):
		"""
		<Define method>
		购买或出让寄售订单
		"""
		tradeData = self.lingShiTradeData.get(uid,None)
		if tradeData == None:
			KBEDebug.ERROR_MSG(" this tradeData is error %s "%uid)
			return
		if tradeData["playerDbid"] == roleDBID:
			KBEDebug.ERROR_MSG(" buy owner Order %i"%roleDBID)
			return
		if tradeData["tradeType"] != type:
			KBEDebug.ERROR_MSG("tradeData is error %i"%tradeData["tradeType"])
			return
		if tradeData["amount"] < amount:
			role.client.statusMessage( csstatus.LINGSHI_TRADE_ORDER_AMOUNT_ERROR,"" )
			#role.base.UpdataSellOrder( tradeData )
			return
		tradeData["amount"] -= amount
		tradeData["earnMoney"] += amount * tradeData["price"] * 100
		if type == csdefine.LINGSHI_TRADE_SELL:
			role.buyLinShiTradeOrderCB( totalPrice )
			role.cell.buyLinShiTradeOrderCB( totalPrice )
		elif type == csdefine.LINGSHI_TRADE_COLLECT:
			role.base.sellLingShiTradeOrderCB( totalPrice )
			role.cell.sellLingShiTradeOrderCB( totalPrice )
		tempData = {"uid":tradeData["uid"],"amount":amount,"price":tradeData["price"],"isSend":0,"tradeType":type}
		self.lingShiTradeSuccessDatas.insert(0,tempData)
		role.updataOrder(tradeData,self.lingShiTradeSuccessDatas[0])
		KBEngine.lookUpEntityByDBID("Role",tradeData["playerDbid"],Functor(self.dealLinShiTradeOrderCallBack,tradeData,self.lingShiTradeSuccessDatas[0]))

	def dealLinShiTradeOrderCallBack( self, tradeData, successTradeData, target ):
		"""
		获得玩家MailBox回调
		"""
		if target is False:
			return
		if target is True:
			return
		for data in self.lingShiTradeSuccessDatas:
			if data.uid == successTradeData.uid:
				data.isSend = 1
		target.updataMyOrderToClient(tradeData,successTradeData)

	def removeLingShiTradeOrder( self, uid, role ):
		"""
		<Define method>
		下架订单
		"""
		tradeData = self.lingShiTradeData.get(uid,None)
		type = tradeData["tradeType"]
		if tradeData == None:
			return
		totalPrice = tradeData["amount"] * tradeData["price"] * 100
		del self.lingShiTradeData[uid]
		role.removeLingShiTradeOrderCB(totalPrice,uid)

	def refreshPlayerOrder( self, role, roleDBID):
		"""
		<Define method>
		更新玩家订单
		"""
		orderList = []
		data = {}
		for tradeData in self.lingShiTradeData.values():
			if tradeData["playerDbid"] == roleDBID:
				role.addOrder( tradeData )
				tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"] * 100,"price":tradeData["price"],"remainTime":str(int(tradeData["endTime"]) - Functions.getTime()),"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"]}
				orderList.append( tempData )
		data["orderData"] = orderList
		role.client.RefreshMyOrderCB( data) 

	def takeOutMoney( self, role,roleDBID ):
		"""
		<Define method>
		取出收益
		"""
		totalPrice = 0
		totalLingshi = 0
		for tradeData in self.lingShiTradeData.values():
			if tradeData["playerDbid"] == roleDBID and tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL:
				totalPrice += tradeData["earnMoney"]
			elif tradeData["playerDbid"] == roleDBID and tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
				totalLingshi += tradeData["earnMoney"]
		role.takeOutMoneyCB( totalPrice,totalLingshi )

	def takeOutMoneyCB( self, totalPirce,totalLingshi,role,roleDBID ):
		"""
		<Define method>
		取出收益回调
		"""
		for tradeData in self.lingShiTradeData.values():
			if tradeData["playerDbid"] == roleDBID:
				tradeData["earnMoney"] = 0
				role.base.updataMyOrder(tradeData)
		role.addMoneyBuySOrder( totalPrice )		
		role.base.addLingShiBuyOrder( totalLingshi )

	def refreshAllSellOrder( self, role, roleDBID ):
		"""
		<Define method>
		刷新所有出售订单
		"""
		orderList = []
		data = {}
		for tradeData in self.lingShiTradeData.values():
			if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL and int(tradeData["remainTime"]) > 0 and tradeData["amount"] > 0:
				role.addAllLingShiTradeSellOrder( tradeData )
				tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"] * 100,"price":tradeData["price"],"remainTime":str(int(tradeData["endTime"]) - Functions.getTime()),"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"]}
				orderList.append( tempData )
		data["orderData"] = orderList
		role.client.RefreshAllSellOrderCB(  data )

	def refreshAllCollectOrder( self, role, roleDBID ):
		"""
		<Define method>
		刷新所有收购订单
		"""
		orderList = []
		data = {}
		for tradeData in self.lingShiTradeData.values():
			if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT and int(tradeData["remainTime"]) > 0 and tradeData["amount"] > 0:
				role.addAllLingShiTradeCollectOrder( tradeData )
				tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"] * 100,"price":tradeData["price"],"remainTime":str(int(tradeData["endTime"]) - Functions.getTime()),"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"]}
				orderList.append( tempData )
		data["orderData"] = orderList
		role.client.RefreshAllCollectOrder( data ) 

	def getMinTimeOfTradeData( self, lingShiTradeDataList ):
		"""
		获得订单的最小下单时间，用于添加定时器
		"""
		if len( lingShiTradeDataList ) < 0:
			return None
		tradeTimeList = []
		for tradeData in lingShiTradeDataList.values():
			remainTime = int(tradeData["endTime"]) - Functions.getTime()
			if remainTime > 0 and tradeData["amount"] > 0:
				tradeTimeList.append(tradeData["endTime"])
		if len(tradeTimeList) <= 0:
			return None
		tradeTimeList.sort()
		for tradeData in lingShiTradeDataList.values():
			if tradeData["endTime"] == tradeTimeList[0]:
				return tradeData
		return None