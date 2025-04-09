# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
import csstatus
import time
from ConfigObject.ShopMall.ShopMallMgr import g_shopMallMgr
from ConfigObject.Coupon.CouponMgr import g_couponMgr
import json
import csconst
import Functions
from ItemFactory import ItemFactoryInst
from MsgLogger import g_logger




class RoleShopMallInterface:
	"""
	玩家商城接口类
	"""
	def __init__( self ):
		self.givingGoodsData = {}  #玩家赠送数据
		self.receiveGoodsData = {} #玩家接收数据
		self.checkCouponItem()
		
	def onGetCell( self ):
		"""
		"""
		self.cell.updateShiTou(self.xianshi, self.lingshi, self.xuanshi)
	
	def checkCouponItem( self ):
		"""
		检查优惠券是否过期
		"""
		if len( self.couponItems ) <= 0:
			return
		couponItemUID = []
		for key,couponItem in self.couponItems.items():
			couponData = g_couponMgr.getConfig( couponItem["couponId"] ) #获得优惠劵的配置
			if couponData == None:
				return
			if couponData["timeLimit"] > 0:
				currentTime = time.time()
				offsetTime = currentTime - couponItem["createTime"]
				if offsetTime < 0:
					return
				if offsetTime < couponData["timeLimit"]:
					self.addTimerCallBack( couponData["timeLimit"] - offsetTime, "removeCouponItem", (couponItem["uid"],))
				else:
					couponItemUID.append( couponItem["uid"] )
		if len( couponItemUID ) > 0:
			for uid in couponItemUID:
				self.removeCouponItem( uid )

	def initCouponItem( self ):
		"""
		将优惠劵发送到客户端
		"""
		data = {}
		tempData = {}
		for couponItem in self.couponItems:
			tempData[couponItem["uid"]] = {"uid":couponItem["uid"],"couponId":couponItem["couponId"],"createTime:":time.time()}
		data["couponItems"] = tempData
		self.client.InitCouponItem( data )

	def addCouponItem( self, couponItemId ):
		"""
		增加优惠券
		"""
		couponData = g_couponMgr.getConfig( couponItemId )
		if couponData == None:
			KBEDebug.ERROR_MSG(" couponData is None")
			return False
		couponItem = {"couponId":couponData["couponId"],"uid":KBEngine.genUUID64(),"createTime":time.time()}
		uid = couponItem["uid"]
		self.couponItems[uid] = couponItem
		if couponData["timeLimit"] > 0:
			self.addTimerCallBack( couponData["timeLimit"], "removeCouponItem", (uid,))
		tempData = { "couponId":couponData["couponId"],"uid":couponItem["uid"], "createTime:":time.time()}
		self.client.AddCouponItem( tempData )
		return True

	def removeCouponItem( self, couponUID ):
		"""
		移除优惠券
		"""
		if couponUID not in self.couponItems:
			return False
		self.client.RemoveCouponItem( couponUID )
		del self.couponItems[couponUID]
		return True
		
	def requestShopMallItemList( self ):
		"""
		请求打开商城获得商城的所有物品列表
		"""
		if not self.validateClientCall():
			return
		self.initCouponItem()
		KBEngine.globalData["ShopMallManager"].onRoleLoginInitGivingGoodsData( self, self.databaseID )
		KBEngine.globalData["ShopMallManager"].requestShopMallItemList( self )

	def requestBuyShopMallItemCB( self,xianShiPrice,lingShiPrice,xuanShiPrice,isAmountLimitItem, buyDataListStr,couponUID,targetDBID ):
		"""
		商品购买回调
		@param couponUID ：优惠劵的UID   
		@type couponUID：STRING

		@param buyDataListStr ：购买物品数据json格式
		@type buyDataListStr：STRING
		buyDataListStr = '[["1","1",1000,10,1,1], ["1","1",1000,10,1,2]]'
		@param buyDataListStr[0][0]:商城类型
		@type buyDataListStr[0][0]：STRING
		@param buyDataListStr[0][1]：物品位置
		@type buyDataListStr[0][1]：物品位置
		@param buyDataListStr[0][2] : 物品id
		@type buyDataListStr[0][2] : INT32
		@param buyDataListStr[0][3] : 物品数量
		@type buyDataListStr[0][3] : INT32
		@param buyDataListStr[0][4] : 货币类型
		@type buyDataListStr[0][4] : INT32
		@param buyDataListStr[0][5] : 是否永久拥有
		@type buyDataListStr[0][5] : INT32  csdefine.SHOP_GOODS_PERMANENT
		"""
		#是否使用优惠券
		if len(couponUID) == 0:
			totalxianShiPrice = xianShiPrice
			totallingShiPrice = lingShiPrice
			totalxuanShiPrice = xuanShiPrice
		else:
			couponUID = int( couponUID )
			couponItem = self.couponItems.get( couponUID,None ) #该优惠劵不存在
			if couponItem ==None:
				KBEngine.globalData["ShopMallManager"].returnBuyShopMallItem( isAmountLimitItem, buyDataListStr ) #返回商品到商城
				KBEDebug.ERROR_MSG(" couponUID %i is not exit "%couponUID)
				return
			if g_couponMgr.onVerify( couponItem["couponId"],shopMallTypeId,slot,itemID ): #验证是否适用于该商品
				couponData = g_couponMgr.getConfig( couponItem["couponId"] )
				totalxianShiPrice = xianShiPrice * couponData["discount"]
				totallingShiPrice = lingShiPrice * couponData["discount"]
				totalxuanShiPrice = xuanShiPrice * couponData["discount"]
			else:
				KBEngine.globalData["ShopMallManager"].returnBuyShopMallItem( isAmountLimitItem, buyDataListStr )
				KBEDebug.ERROR_MSG(" itemID is not use couponItem ")
				return
		xianShiMoneyAmount = self.getUsableXianShi()
		lingShiMoneyAmount = self.getUsableLingShi()
		xuanShiMoneyAmount  = self.getUsableXuanShi()
		if 	xianShiMoneyAmount < totalxianShiPrice:
			KBEngine.globalData["ShopMallManager"].returnBuyShopMallItem( isAmountLimitItem, buyDataListStr)
			KBEDebug.ERROR_MSG(" money is not enough ")
			return
		if 	lingShiMoneyAmount < totallingShiPrice:
			KBEngine.globalData["ShopMallManager"].returnBuyShopMallItem( isAmountLimitItem, buyDataListStr )
			KBEDebug.ERROR_MSG(" money is not enough ")
			return
		if 	xuanShiMoneyAmount < totalxuanShiPrice:
			KBEngine.globalData["ShopMallManager"].returnBuyShopMallItem( isAmountLimitItem, buyDataListStr )
			KBEDebug.ERROR_MSG(" money is not enough ")
			return
		self.cell.receiveShopMallGoods( int(totalxianShiPrice),int(totallingShiPrice),int(totalxuanShiPrice),isAmountLimitItem, buyDataListStr,couponUID,targetDBID )

	def requestBuyShopMallItem( self, buyShopMallItemList, couponUID, targetDBID ):
		"""
		请求购买物品
		@param couponUID ：优惠劵的UID
		@type couponUID：STRING
		@param targetDBID ：目标DBID
		@type targetDBID：DBID

		@param buyDataListStr ：购买物品数据json格式
		@type buyDataListStr：STRING
		buyDataListStr = '[["1","1",1000,10,1], ["1","1",1000,10,1]]'
		@param buyDataListStr[0][0]:商城类型
		@type buyDataListStr[0][0]：STRING
		@param buyDataListStr[0][1]：物品位置
		@type buyDataListStr[0][1]：物品位置
		@param buyDataListStr[0][2] : 物品id
		@type buyDataListStr[0][2] : INT32
		@param buyDataListStr[0][3] : 物品数量
		@type buyDataListStr[0][3] : INT32
		@param buyDataListStr[0][4] : 货币类型
		@type buyDataListStr[0][4] : INT32

		"""
		if not self.validateClientCall():
			return
		buyDataListStr = self.getBuyDataStr(buyShopMallItemList)
		try:
			buyDataList = json.loads( buyDataListStr )
		except:
			KBEDebug.ERROR_MSG("data is error")
			return
		for buyData in buyDataList:
			if buyData[3] <= 0:  #物品数量
				return
			#使用的货币
			if buyData[4] not in [csdefine.SHOP_MONEY_TYPE_XIANSHI,csdefine.SHOP_MONEY_TYPE_LINGSHI,csdefine.SHOP_MONEY_TYPE_XUANSHI]:
				KBEDebug.ERROR_MSG("Money type is error:%i"% buyData[4])
				return
			#商城判断
			if int(buyData[0]) == csdefine.SHOP_TYPE_XIANSHI:
				if buyData[4] not in [csdefine.SHOP_MONEY_TYPE_XIANSHI,csdefine.SHOP_MONEY_TYPE_LINGSHI]:
					KBEDebug.ERROR_MSG("Money type is error:%i"% buyData[4])
					return
				elif buyData[4] == csdefine.SHOP_MONEY_TYPE_XIANSHI:
					buyData.append(csdefine.SHOP_GOODS_PERMANENT)  #永久购买的标志
				elif buyData[4] == csdefine.SHOP_MONEY_TYPE_LINGSHI:
					buyData.append(csdefine.SHOP_GOODS_TEMPORARY)  #临时购买的标志
			if int(buyData[0]) == csdefine.SHOP_TYPE_LINGSHI:
				if buyData[4] != csdefine.SHOP_MONEY_TYPE_LINGSHI:
					KBEDebug.ERROR_MSG("Money type is error:%i"% buyData[4])
					return
				else:
					buyData.append(csdefine.SHOP_GOODS_PERMANENT)
			if int(buyData[0]) == csdefine.SHOP_TYPE_XUANSHI:
				if buyData[4] != csdefine.SHOP_MONEY_TYPE_XUANSHI:
					KBEDebug.ERROR_MSG("Money type is error:%i"% buyData[4])
					return
				else:
					buyData.append(csdefine.SHOP_GOODS_PERMANENT)
			if int(buyData[0]) == csdefine.SHOP_TYPE_GIFT:
				if buyData[4] == csdefine.SHOP_MONEY_TYPE_XIANSHI:
					buyData.append(csdefine.SHOP_GOODS_PERMANENT)  #永久购买的标志
				else:
					buyData.append(csdefine.SHOP_GOODS_TEMPORARY)
				
		buyDataListStr = json.dumps(buyDataList)
		KBEngine.globalData["ShopMallManager"].requestBuyShopMallItem( buyDataListStr,couponUID,self,targetDBID)

	def getBuyDataStr( self, buyShopMallItemList ):
		"""
		获得购买数据的字符串
		"""
		buyItemListStr = []
		for buyItem in buyShopMallItemList:
			tempArray = []
			tempArray.append(buyItem.shopMallType)
			tempArray.append(buyItem.slot)
			tempArray.append(buyItem.itemID)
			tempArray.append(buyItem.amount)
			tempArray.append(buyItem.moneyType)
			tempArray.append(buyItem.itemType)
			buyItemListStr.append(tempArray)
		return json.dumps(buyItemListStr)

	def receiveShopMallGoodsCB( self,couponUID,totalxianShiPrice,totallingShiPrice,totalxuanShiPrice ):
		"""
		获得商品的回调，减少货币
		@param couponUID ：优惠劵的UID
		@type couponUID：STRING
		"""
		if len(couponUID) > 0: 
			self.removeCouponItem( int(couponUID) )
		if totalxianShiPrice > 0:
			self.payXianShi( totalxianShiPrice, csdefine.CHANGE_XIANSHI_BY_SHOP_CONSUME )
		if totallingShiPrice > 0:
			self.payLingShi( totallingShiPrice, csdefine.CHANGE_LINGSHI_BY_SHOP_CONUSUME )
		if totalxuanShiPrice > 0:
			self.payXuanShi( totalxuanShiPrice, csdefine.CHANGE_XUANSHI_SHOP_CONUSUME )


	def GivingShopMallItemToPlayer(self, giveShopMallItemList, targetDBID):
		"""
		赠送好友商品
		@param targetDBID ：目标DBID
		@type targetDBID：DBID

		@param giveDataListStr ：购买物品数据json格式
		@type giveDataListStr:STRING
		giveDataListStr = '[["1","2",1001,1,1], ["0","1",1000,1,1]]'
		@param buyDataListStr[0][0]:商城类型
		@type buyDataListStr[0][0]：STRING
		@param buyDataListStr[0][1]：物品位置
		@type buyDataListStr[0][1]：物品位置
		@param buyDataListStr[0][2] : 物品id
		@type buyDataListStr[0][2] : INT32
		@param buyDataListStr[0][3] : 物品数量
		@type buyDataListStr[0][3] : INT32
		@param buyDataListStr[0][4] : 货币类型
		@type buyDataListStr[0][4] : INT32
		"""
		if not self.validateClientCall():
			return
		#判断赠送数据是否超过上限
		if len( self.givingGoodsData ) > csconst.ROLE_GIVINGGOODSDATA_UPPER_LIMIT:
			return
		#没有选择赠送目标
		if targetDBID <= 0:
			KBEDebug.ERROR_MSG(" has no player ")
			return
		#是否为好友
		if self.hasFriendBuyPlayerDBID( targetDBID ) == False:
			KBEDebug.ERROR_MSG("false  %i"%targetDBID)
			return
		giveDataListStr = self.getBuyDataStr(giveShopMallItemList)
		try:
			giveDataList = json.loads( giveDataListStr )
		except:
			KBEDebug.ERROR_MSG("data is error")
			return
		for giveData in giveDataList:
			#在灵石商城和仙石商品的物品不能赠送
			if int(giveData[0]) in [csdefine.SHOP_TYPE_LINGSHI,csdefine.SHOP_TYPE_XUANSHI]:
				KBEDebug.ERROR_MSG(" SHOP_TYPE_LINGSHI and SHOP_TYPE_XUANSHI is not allow give item to player")
				return
			#货币只能用仙石
			if giveData[4] != csdefine.SHOP_MONEY_TYPE_XIANSHI:
				return
		self.requestBuyShopMallItem(  giveShopMallItemList, "", targetDBID )

	def createGivingGoodsData( self, targetDBID, itemInstList ):
		"""
		创建一条赠送物品数据
		@param targetDBID ：目标DBID
		@type targetDBID：DBID
		@param itemInstList ：物品列表
		@type itemInstList：ITEMLIST
		"""
		currentTime = time.time()
		goodsData = {"uid":str(KBEngine.genUUID64()), "playerDbid":self.databaseID, "targetDbid":targetDBID,"itemList":itemInstList,"givingTime":currentTime,
		"changeTime":currentTime,"state":csdefine.GIVING_GOODSDATA_WAIT_STATE,"playerIsClear":csdefine.GIVING_GOODSDATA_CLEAR_NO,"targetIsClear":csdefine.GIVING_GOODSDATA_CLEAR_NO}
		#是为了防止在赠送时，对方将你移除了好友
		if self.hasFriendBuyPlayerDBID( targetDBID ) == False:
			return
		playerName = self.getFriendNameBuyPlayerDBID( targetDBID )
		self.givingGoodsData[goodsData["uid"]] = goodsData
		itemName = self.getGoodsDataName(goodsData["itemList"])
		itemAmount = self.getGoodsDataItemAmount(goodsData["itemList"])
		itemID = self.getGoodsDataItemID( goodsData["itemList"] )
		tempData = {"uid":str(goodsData["uid"]),"itemID":itemID,"itemName":itemName,"amount":itemAmount,"time":str(goodsData["givingTime"]),"playerName":playerName,"state":goodsData["state"]}
		self.client.AddGivingGoodsDataRecord( tempData )
		#获得好友的MailBox
		player = self.IsFriendOnLogin(goodsData["targetDbid"])
		if player != None:
			#对方在线
			player.addToReceiveGoodsData( goodsData )
			#直接发送数据信息到玩家客户端
		KBEngine.globalData["ShopMallManager"].addToGivingGoodsData( goodsData )

	def addToReceiveGoodsData( self, goodsData ):
		"""
		添加到接收数据列表
		"""
		self.receiveGoodsData[goodsData["uid"]] = goodsData
		itemName = self.getGoodsDataName(goodsData["itemList"])
		itemAmount = self.getGoodsDataItemAmount(goodsData["itemList"])
		itemID = self.getGoodsDataItemID( goodsData["itemList"] )
		tempData = {"uid":str(goodsData["uid"]),"itemID":itemID,"itemName":itemName,"amount":itemAmount,"time":str(goodsData["givingTime"]),"playerName":self.getFriendNameBuyPlayerDBID( goodsData["playerDbid"] ),"state":goodsData["state"]}
		self.client.AddReceiveGoodsDataRecord( tempData )
	
	def getGoodsDataName( self,itemListData ):
		"""
		获得赠送物品的名称
		"""
		itemList = json.loads(itemListData)
		itemName = ItemFactoryInst.getItemData(itemList[0]["id"]).get("ItemName",None)
		if len(itemList) > 1:
			return "%s..."%itemName
		return "%s"%itemName

	def getGoodsDataItemAmount( self,itemListData ):
		"""
		获得赠送物品的数量
		"""
		itemList = json.loads(itemListData)
		if len(itemList) > 1:
			return -1
		return itemList[0]["amount"]

	def getGoodsDataItemID( self,itemListData ):
		"""
		获得赠送物品的itemID
		"""
		itemList = json.loads(itemListData)
		if len(itemList) > 1:
			return -1
		return itemList[0]["id"]

	def dealReceiveGivingGoodsData( self, goodsDataUIDs, dealGivingGoodsData ):
		"""
		玩家处理赠送的物品数据接口
		@param goodsDataUIDs ：接收物品数据UID列表
		@type goodsDataUIDs：STRING
		@param dealGivingGoodsData ：处理物品标识
		@type dealGivingGoodsData：INT32
		csdefine.AGREE_TO_RECEIVEGIVINGGOODSDATA  同意接收赠送的物品数据
		csdefine.REFUSE_TO_RECEIVEGIVINGGOODSDATA 拒绝接收赠送的物品数据
		"""
		if not self.validateClientCall():
			return
		for goodsDataUID in goodsDataUIDs:
			goodsData = self.receiveGoodsData.get(goodsDataUID,None)
			if goodsData == None:
				KBEDebug.ERROR_MSG(" goodsData is error ")
				return
			#还需判断该数据是否过期 或者 对方已撤回
			if goodsData["state"] == csdefine.GIVING_GOODSDATA_OVERDUE_STATE:
				KBEDebug.ERROR_MSG(" OVERDUE ")
				return
			if goodsData["state"] == csdefine.GIVING_GOODSDATA_WITHDRAW_STATE:
				KBEDebug.ERROR_MSG(" WITHDRAW ")
				return
			#如果不是等待处理的状态
			if goodsData["state"] != csdefine.GIVING_GOODSDATA_WAIT_STATE:
				return
		goodsDataList = []
		currentTime = time.time()
		for goodsDataUID in goodsDataUIDs:
			goodsData = self.receiveGoodsData.get(goodsDataUID,None)
			player = self.IsFriendOnLogin(goodsData["playerDbid"])
			if dealGivingGoodsData == csdefine.AGREE_TO_RECEIVEGIVINGGOODSDATA:
				self.cell.receiveGoodsDataItems(goodsData["itemList"])
				goodsData["state"] = csdefine.GIVING_GOODSDATA_RECEIVE_STATE #好友接收标识
			elif dealGivingGoodsData == csdefine.REFUSE_TO_RECEIVEGIVINGGOODSDATA:
				goodsData["state"] = csdefine.GIVING_GOODSDATA_REFUSE_STATE  #好友拒绝标识
			goodsData["changeTime"] = currentTime
			goodsDataList.append(goodsData)
			if player != None:
				#并改变该条数据
				player.changeGivingGoodsData(goodsDataUID,currentTime,dealGivingGoodsData)
			KBEngine.globalData["ShopMallManager"].dealToGivingGoodsData(goodsDataUID,currentTime,dealGivingGoodsData)
		goodsDataListStr = []
		for goodsData in goodsDataList:
			tempData = {"uid":str(goodsData["uid"]),"state":goodsData["state"],"changeTime":str(goodsData["changeTime"])}
			goodsDataListStr.append( tempData )
		data = {}
		data["dealGivingGoodsData"] = goodsDataListStr
		self.client.DealReceiveGivingGoodsDataCB( data )

	def changeGivingGoodsData( self, goodsDataUID,currentTime,dealGivingGoodsData ):
		"""
		改变赠送的数据
		@param goodsDataUID ：处理赠送物品数据的UID
		@type goodsDataUID：STRING
		@param currentTime ：当前改变这条数据的时间
		@type goodsDataUID：DOUBLE
		@param dealGivingGoodsData ：处理物品标识
		@type dealGivingGoodsData：INT32
		csdefine.AGREE_TO_RECEIVEGIVINGGOODSDATA  同意接收赠送的物品数据
		csdefine.REFUSE_TO_RECEIVEGIVINGGOODSDATA 拒绝接收赠送的物品数据
		"""
		goodsData = self.givingGoodsData.get(goodsDataUID,None)
		if goodsData == None:
			KBEDebug.ERROR_MSG(" goodsData is error ")
			return
		if dealGivingGoodsData == csdefine.AGREE_TO_RECEIVEGIVINGGOODSDATA:
			goodsData["state"] = csdefine.GIVING_GOODSDATA_RECEIVE_STATE
		elif dealGivingGoodsData == csdefine.REFUSE_TO_RECEIVEGIVINGGOODSDATA:
			goodsData["state"] = csdefine.GIVING_GOODSDATA_REFUSE_STATE
		goodsData["changeTime"] = currentTime
		tempData = {"uid":str(goodsData["uid"]),"state":goodsData["state"],"changeTime":str(goodsData["changeTime"])}
		self.client.ChangeGivingGoodsDataCB( tempData )

	def withDrawGiveGoodsData(self,goodsDataUID):
		"""
		玩家撤回赠送的物品数据
		"""
		if not self.validateClientCall():
			return
		goodsData = self.givingGoodsData.get(goodsDataUID,None)
		if goodsData == None:
			KBEDebug.ERROR_MSG("goodsData is error")
			return
		#该条数据已为接收状态
		if goodsData["state"] == csdefine.GIVING_GOODSDATA_RECEIVE_STATE:
			KBEDebug.ERROR_MSG(" RECEIVE ")
			return
		#该条数据已为拒绝状态
		if goodsData["state"] == csdefine.GIVING_GOODSDATA_REFUSE_STATE:
			KBEDebug.ERROR_MSG(" REFUSE ")
			return
		currentTime = time.time()
		goodsData["state"] = csdefine.GIVING_GOODSDATA_WITHDRAW_STATE
		goodsData["changeTime"] = currentTime
		player = self.IsFriendOnLogin(goodsData["targetDbid"])
		if player != None:
			#被赠送的玩家在线
			player.withDrawChangeGivingGoodsData( goodsDataUID,currentTime )
			
		KBEngine.globalData["ShopMallManager"].dealToGivingGoodsData(goodsDataUID,currentTime,csdefine.WITHDRAW_TO_GIVEGOODSDATA)
		tempData = {"uid":str(goodsData["uid"]),"state":goodsData["state"],"changeTime":str(goodsData["changeTime"])}
		self.client.ChangeGivingGoodsDataCB( tempData )

	def withDrawChangeGivingGoodsData( self,goodsDataUID,currentTime ):
		"""
		赠送方撤回赠送的物品，改变自己的接收物品的数据
		"""
		goodsData = self.receiveGoodsData.get( goodsDataUID,None )
		if goodsData == None:
			KBEDebug.ERROR_MSG("withDrawChangeGivingGoodsData goodsData is error ")
			return
		goodsData["state"] = csdefine.GIVING_GOODSDATA_WITHDRAW_STATE
		goodsData["changeTime"] = currentTime
		goodsDataListStr = []
		data = {}
		tempData = {"uid":str(goodsData["uid"]),"state":goodsData["state"],"changeTime":str(goodsData["changeTime"])}
		goodsDataListStr.append(tempData)
		data["dealGivingGoodsData"] = goodsDataListStr
		self.client.DealReceiveGivingGoodsDataCB( data )

	def clearGivingGoodsDataRecord( self,goodsDataUIDs ):
		"""
		清除赠送物品的数据记录
		"""
		if not self.validateClientCall():
			return
		for goodsDataUID in goodsDataUIDs:
			goodsData = self.givingGoodsData.get( goodsDataUID,None )
			if goodsData == None:
				KBEDebug.ERROR_MSG("clearGivingGoodsDataRecord goodsData is error")
				return
			#该条数据状态不为接收状态
			if goodsData["state"] != csdefine.GIVING_GOODSDATA_RECEIVE_STATE:
				KBEDebug.ERROR_MSG("clearGivingGoodsDataRecord goodsData is not allow")
				return
		for goodsDataUID in goodsDataUIDs:
			del self.givingGoodsData[goodsDataUID]
		KBEngine.globalData["ShopMallManager"].clearGivingGoodsDataRecord( goodsDataUIDs,self.databaseID )
		self.client.ClearGivingGoodsDataRecordCB(goodsDataUIDs)

	def clearReceiveGoodsDataRecord( self,goodsDataUIDs ):
		"""
		清除收取物品的数据记录
		"""
		if not self.validateClientCall():
			return
		for goodsDataUID in goodsDataUIDs:
			goodsData = self.receiveGoodsData.get( goodsDataUID,None )
			if goodsData == None:
				KBEDebug.ERROR_MSG("clearReceiveGoodsDataRecord goodsData is error")
				return
			if goodsData["state"] == csdefine.GIVING_GOODSDATA_WAIT_STATE:
				KBEDebug.ERROR_MSG("clearReceiveGoodsDataRecord goodsData is not allow")
				return
		for goodsDataUID in goodsDataUIDs:
			del self.receiveGoodsData[goodsDataUID]
		KBEngine.globalData["ShopMallManager"].clearGivingGoodsDataRecord( goodsDataUIDs,self.databaseID )
		self.client.ClearReceiveGoodsDataRecordCB(goodsDataUIDs)

	def turnGivingShopMallItemToPlayer( self,goodsDataUID,targetDBID ):
		"""
		转增给好友
		"""
		goodsData = self.givingGoodsData.get(goodsDataUID,None)
		if goodsData == None:
			KBEDebug.ERROR_MSG("turnGivingShopMallItemToPlayer goodsData is error")
			return
		if goodsData["state"] == csdefine.GIVING_GOODSDATA_RECEIVE_STATE:
			KBEDebug.ERROR_MSG("turnGivingShopMallItemToPlayer goodsData state is receive")
			return
		if goodsData["state"] == csdefine.GIVING_GOODSDATA_WAIT_STATE:
			KBEDebug.ERROR_MSG("turnGivingShopMallItemToPlayer goodsData state is wait")
			return
		self.createGivingGoodsData(targetDBID,goodsData["itemList"])
		del self.givingGoodsData[goodsDataUID]

	def takeBackGivingGoodsData( self,goodsDataUID ):
		"""
		将赠送的物品数据取回
		"""
		if not self.validateClientCall():
			return
		goodsData = self.givingGoodsData.get(goodsDataUID,None)
		if goodsData == None:
			KBEDebug.ERROR_MSG("takeBackGivingGoodsData goodsData is error")
			return
		if goodsData["state"] == csdefine.GIVING_GOODSDATA_RECEIVE_STATE:
			KBEDebug.ERROR_MSG("takeBackGivingGoodsData goodsData state is receive")
			return
		if goodsData["state"] == csdefine.GIVING_GOODSDATA_WAIT_STATE:
			KBEDebug.ERROR_MSG("takeBackGivingGoodsData goodsData state is wait")
			return
		#添加到自己的背包
		#if self.cell.receiveItemToBag(goodsData["itemList"],csdefine.SHOP_GOODS_PERMANENT):
		#	goodsData["state"] = csdefine.GIVING_GOODSDATA_RECEIVE_STATE


	def sharedToGivingGoodsData( self,goodsDataUID,goodsData ):
		"""
		同步赠送的物品数据
		"""
		if goodsData["playerIsClear"] == csdefine.GIVING_GOODSDATA_CLEAR_NO:
			self.givingGoodsData[goodsDataUID] = goodsData

	def sharedToReceiveGoodsData( self,goodsDataUID,goodsData ):
		"""
		同步接收的物品数据
		"""
		if goodsData["targetIsClear"] == csdefine.GIVING_GOODSDATA_CLEAR_NO:
			self.receiveGoodsData[goodsDataUID] = goodsData

	#-----------------------------仙石，灵石，玄石-----------------------------
	def payShiTou( self, value, reason, order = "" ):
		"""
		支付灵石（仙石）！先支付绑定的灵石，如果不够再支付仙石
		除了商城中，特定的物品！其他消耗，都要条此接口
		"""
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
			
		if self.hasEnoughShiTou(value):
			self._payShiTou(value, reason, order)
			return True
		
		return False
		
	def payShiTouFromCell( self, value, reason, order ):
		"""
		define method
		支付灵石（仙石）
		"""
		if self.hasEnoughShiTou(value):
			self._payShiTou(value, reason, order)
		else:
			#如果还是不够则清零（一般不会出现这种情况）
			self.payXianShi(self.xianshi, reason, order)
			self.payLingShi(self.lingshi, csconst.PAY_XIANSHI_USE_LINGSHI[reason], order)
		
	def _payShiTou( self, value, reason, order = "" ):
		if self.lingshi >= value:
			self.payLingShi( value, csconst.PAY_XIANSHI_USE_LINGSHI[reason], order ) 
			return
		
		if not self.hasEnoughShiTou(value):
			KBEDebug.ERROR_MSG("Role[%d:%d] pay xianshi[%d]/lingshi[%d] error" %(self.id, self.databaseID, self.xianshi, self.lingshi))
			return
		
		if self.lingshi:
			value -= self.lingshi
			self.payLingShi( self.lingshi, csconst.PAY_XIANSHI_USE_LINGSHI[reason], order )
		self.payXianShi( value, reason, order ) 
		
	def hasEnoughShiTou( self, value ):
		"""是否有足够的灵石（仙石）消耗"""
		return self.xianshi + self.lingshi >= value
	
	def addXianShi(self, value, reason = None, order = ""):
		"""
		增减仙石
		"""
		self.accountEntity.addXianShi( value, reason, order )

	def payXianShi(self, value, reason, order = ""):
		"""
		付仙石
		"""
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		
		if self.getUsableXianShi() - value < 0:
			return False
		
		self.addXianShi( -value, reason, order )
		return True
		
	def payXianShiFromCell(self, value, reason, order):
		"""
		define method
		付仙石
		"""
		if self.getUsableXianShi() >= value:
			self.addXianShi(-value, reason, order)
		else:
			#如果还是不够则清零（一般不会出现这种情况）
			self.addXianShi(self.getUsableXianShi(), reason, order)
		
	def gainXianShi(self, value, reason = None):
		"""
		给玩家仙石
		"""
		if self.xianshi + value > csconst.ROLE_XIANSHI_UPPER_LIMIT:
			return False
		self.addXianShi( value,reason )
		return True

	def setXianShi(self, value, reason = None):
		"""
		define method
		GM指令设置玩家的仙石
		"""
		value = min( value, csconst.ROLE_XIANSHI_UPPER_LIMIT ) - self.xianshi
		self.accountEntity.addXianShi( value, reason )

	def updateXianShi(self, value, reason = None):
		"""
		更新玩家的仙石
		"""
		if self.xianshi < value:
			messageID = csstatus.ACCOUNT_ADD_XIAN_SHI
			cValue = value - self.xianshi
		else:
			messageID = csstatus.ACCOUNT_DEL_XIAN_SHI
			cValue = self.xianshi - value
		self.xianshi = value
		
		if hasattr(self, "cell") and self.cell: self.cell.updateShiTou(self.xianshi, self.lingshi, self.xuanshi)
		self.statusMessage( messageID, str(cValue) )
		

	def getUsableXianShi(self ):
		"""
		获得玩家可用的仙石
		"""
		return self.xianshi

	def addLingShi( self, value, reason, order = ""):
		"""
		增减玩家灵石
		"""
		if self.lingshi + value > csconst.ROLE_LINGSHI_UPPER_LIMIT:
			return False
		old = self.lingshi
		new = self.lingshi + value  
		self.updateLingShi(new, reason)

		playerDBID = self.databaseID
		name = self.playerName
		g_logger.lingshiChangeLog( self.accountEntity.databaseID, playerDBID, name, old, new, reason, order )
		return True

	def payLingShi(self, value, reason, order = ""):
		"""
		付灵石
		"""
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		
		if self.getUsableLingShi() - value < 0:
			return False
		
		self.addLingShi( -value, reason, order )
		return True
		
	def payLingShiFromCell(self, value, reason, order):
		"""
		define method
		付灵石
		"""
		if self.getUsableLingShi() >= value:
			self.addLingShi(-value, reason, order)
		else:
			#如果还是不够则清零（一般不会出现这种情况）
			self.addLingShi(self.getUsableLingShi(), reason, order)

	def gainLingShi(self, value, reason = None):
		"""
		给玩家灵石
		"""
		if self.lingshi + value > csconst.ROLE_LINGSHI_UPPER_LIMIT:
			return False
		self.addLingShi( value, reason )
		return True

	def setLingShi(self, value, reason = None):
		"""
		define method
		GM指令设置玩家的灵石
		"""
		value = min( value, csconst.ROLE_LINGSHI_UPPER_LIMIT )
		self.updateLingShi( value, reason )

	def updateLingShi(self, value, reason = None):
		"""
		更新玩家的灵石
		"""
		if self.lingshi < value:
			messageID = csstatus.ACCOUNT_ADD_LING_SHI
			cValue = value - self.lingshi
		else:
			messageID = csstatus.ACCOUNT_DEL_LING_SHI
			cValue = self.lingshi - value
		self.lingshi = value
	
		if hasattr(self, "cell") and self.cell: self.cell.updateShiTou(self.xianshi, self.lingshi, self.xuanshi)
		self.statusMessage( messageID, str(cValue) )

	def getUsableLingShi(self ):
		"""
		获得玩家可用的灵石
		"""
		return self.lingshi


	def addXuanShi(self, value, reason = None, order=""):
		"""
		增减玄石
		"""
		self.accountEntity.addXuanShi( value, reason )

	def payXuanShi(self, value, reason = None):
		"""
		付玄石
		"""
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		
		if self.getUsableXuanShi() - value < 0:
			return False
		
		self.addXuanShi( -value, reason )
		return True
	
	def payXuanShiFromCell(self, value, reason, order):
		"""
		define method
		付玄石
		"""
		if self.getUsableXuanShi() >= value:
			self.addXuanShi(-value, reason, order)
		else:
			#如果还是不够则清零（一般不会出现这种情况）
			self.addXuanShi(self.getUsableXuanShi(), reason, order)

	def gainXuanShi(self, value, reason = None):
		"""
		给玩家玄石
		"""
		if self.xuanshi + value > csconst.ROLE_XUANSHI_UPPER_LIMIT:
			return False
		self.addXuanShi( value, reason )
		return True

	def setXuanShi(self, value, reason = None):
		"""
		define method
		GM指令设置玩家的玄石
		"""
		value = min( value, csconst.ROLE_XUANSHI_UPPER_LIMIT )
		self.accountEntity.addXuanShi( value - self.xuanshi, reason )

	def updateXuanShi(self, value, reason = None):
		"""
		更新玩家的玄石
		"""
		if self.xuanshi < value:
			messageID = csstatus.ACCOUNT_ADD_XUAN_SHI
			cValue = value - self.xuanshi
		else:
			messageID = csstatus.ACCOUNT_DEL_XUAN_SHI
			cValue = self.xuanshi - value
		self.xuanshi = value
		
		if hasattr(self, "cell") and self.cell: self.cell.updateShiTou(self.xianshi, self.lingshi, self.xuanshi)
		self.statusMessage( messageID, str(cValue) )

	def getUsableXuanShi(self ):
		"""
		获得玩家可用的玄石
		"""
		return self.xuanshi

