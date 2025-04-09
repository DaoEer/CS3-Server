# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import KST
import Functions
import csdefine
import csstatus
import ItemFactory
from MsgLogger import g_logger
from ConfigObject.Store.StoreMgr import g_storeMgr
from StoreRecordData import StoreBuyRecordData
from StoreRecordData import StorePresentRecordData
from StoreGiftBoxData import StoreGiftBoxData
from ConfigObject.Store.StoreRuleBase import StoreLimitTime
from ConfigObject.Store.StoreRuleBase import StoreDiscountTime

# 商品类型对应支付类型
STORE_PAY_TYPE = {
	csdefine.STORE_GOODS_TYPE_HOME			:	csdefine.STORE_TYPE_XIANSHI,
	csdefine.STORE_GOODS_TYPE_APPEARANCE	:	csdefine.STORE_TYPE_XIANSHI,
	csdefine.STORE_GOODS_TYPE_PET			:	csdefine.STORE_TYPE_XIANSHI,
	csdefine.STORE_GOODS_TYPE_SUNDRIES		:	csdefine.STORE_TYPE_XIANSHI,
	csdefine.STORE_GOODS_TYPE_XUANSHI		:	csdefine.STORE_TYPE_XUANSHI,
}

class RoleStoreInterface:
	"""
	玩家商城接口类(新)
	"""
	def __init__( self ):
		self.prepayment = {
							csdefine.STORE_TYPE_XIANSHI : 0,
							csdefine.STORE_TYPE_LINGSHI : 0,
							csdefine.STORE_TYPE_XUANSHI : 0,
							csdefine.STORE_TYPE_JINQIAN : 0,
		}  # 预支付

	def initClientData( self ):
		KBEngine.globalData["StoreManager"].initClientData(self, self.databaseID)

	def requestOpenStoreUI(self, goodsType, itemType, cfgTime):
		"""
		exposed method
		申请打开某一页商城
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].onUpdateStoreGoods(self, goodsType, itemType, cfgTime)
		
	def getStoreNewGoods(self, goodsType, cfgTime):
		"""
		exposed method
		获得某类型的新品数据
		"""
		if not self.validateClientCall():
			return	
		KBEngine.globalData["StoreManager"].getStoreNewGoods(self, goodsType, cfgTime)

	def getGoodsListByIDList(self, goodsIDList):
		"""
		exposed method
		通过ID列表获得商品列表
		"""
		if not self.validateClientCall():
			return
		goodsList = []
		for ID in goodsIDList:
			goods = g_storeMgr.getGoodsByID(ID)
			if goods != None:
				goodsList.append(goods)
		self.client.CLIENT_OnGetGoodsListByIDList({"Datas" : goodsList })

	def getRecommentGoods(self, goodsIDList):
		"""
		exposed method
		通过ID列表获得推荐首页商品列表
		"""
		if not self.validateClientCall():
			return
		goodsList = []
		for ID in goodsIDList:
			goods = g_storeMgr.getGoodsByID(ID)
			if goods != None:
				goodsList.append(goods)
		self.client.CLIENT_OnGetRecommentGoods({"Datas" : goodsList })


	def requestStoreLimitGoodsList(self):
		"""
		exposed method
		查询数量限制
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].requestStoreLimitGoodsList(self, self.databaseID)

	def onRequestStoreLimitGoodsList(self, goodsIDList, amountList):
		"""
		<defined method>
		查询数量限制的回调
		"""
		self.client.CLIENT_OnRequestStoreLimitGoodsList(goodsIDList, amountList)


#-----------------------------------------购买-----------------------------------------
	def requestBuyStoreGoods(self, goodsID, amount):
		"""
		exposed method
		申请购买
		"""
		if not self.validateClientCall():
			return

		KBEngine.globalData["StoreManager"].requestBuyStoreGoods(self, self.databaseID, goodsID, amount)


	def onRequestBuyStoreGoods(self, goodsID, amount):
		"""
		<defined method>
		申请购买回调
		"""
		goods = g_storeMgr.getGoodsByID(goodsID)

		# 判断时间限制
		if not StoreLimitTime().verity(goods, amount):
			self.statusMessage(csstatus.STORE_BALANCE_FAILED)
			return

		# 判断是否是折扣时间
		actualPrice = goods.DiscountPrice
		if not StoreDiscountTime().verity(goods, amount):
			actualPrice = goods.Price
		

		# 金钱不足返回
		price = actualPrice * amount
		if STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI) == csdefine.STORE_TYPE_JINQIAN:
			self.cell.isEnoughMoney(goodsID, goods.ItemID, amount, price)
			return
		
		if not self.isEnoughMoney( STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI), price ):
			if STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI) == csdefine.STORE_TYPE_LINGSHI:
				lingshi = price - self.lingshi
				xianshi = lingshi
				self.inquireMessage(csstatus.STORE_NO_ENOUGH_XIANSHI_REPALCE_LINGSHI, [xianshi, lingshi], "isBuyStoreGoods", goodsID, goods.ItemID, amount, price, csdefine.STORE_TYPE_LINGSHI)
			else:
				self.statusMessage(csstatus.STORE_NO_ENOUGH_XIANSHI, "")
			return
		
		# 判断背包是否放的下
		self.cell.buyStoreGoods(goodsID, goods.ItemID, amount, price, STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI))

	def isBuyStoreGoods(self, reply, goodsID, ItemID, amount, price, priceType):
		if reply:
			lingshi = price - self.lingshi
			xianshi = lingshi
			if xianshi > self.xianshi:
				self.statusMessage(csstatus.STORE_NO_ENOUGH_XIANSHI_AND_LINGSHII, "")
				return
			self.prepayment[priceType] += price
			self.cell.buyStoreGoods(goodsID, ItemID, amount, price, priceType)

	def onBuyStoreGoods(self, goodsID, amount, price, priceType):
		"""
		<defined method>
		购买回调
		"""
		goods = g_storeMgr.getGoodsByID(goodsID)
		#灵石不够时，可通过仙石进行支付，不返利
		self.paymentStoreGoods(priceType, price)
		self.addBuyRecords(goods, amount, price, priceType, goods.ItemID)
		self.statusMessage(csstatus.STORE_BUY_SUCCESS)
		KBEngine.globalData["StoreManager"].onBuyStoreGoods(self.databaseID, goodsID, amount)
		if hasattr(self, "client") and self.client:
			self.client.OnStoreBuyComplete()

	def queryBuyRecords(self):
		"""
		<exposed method>
		查询购买记录
		"""
		if not self.validateClientCall():
			return

		self.client.CLIENT_OnUpdateBuyRecords({"Datas" : self.buyRecords})

	def addBuyRecords(self, goods, amount, price, priceType, itemID):
		"""
		添加购买记录
		"""
		data = StoreBuyRecordData()
		data.goodsID = goods.ID
		data.amount = amount
		data.goodsType = priceType
		data.price = price
		data.itemID = itemID
		self.buyRecords.append( data )
		
		if hasattr(self, "client") and self.client:
			self.client.CLIENT_OnUpdateBuyRecords({"Datas" : [data]})

	def deleteBuyRecord(self, uid):
		"""
		<exposed method>
		删除一条购买记录
		"""
		if not self.validateClientCall():
			return
		for i in self.buyRecords:
			if i.uid == uid:
				self.buyRecords.remove(i)
				break
		self.client.CLINET_OnDeleteBuyRecord(uid)

	def deleteBuyRecords(self):
		"""
		<exposed method>
		清空购买记录
		"""
		if not self.validateClientCall():
			return
		self.buyRecords.clear()
		self.client.CLINET_OnDeleteBuyRecords()
		
	def _getPriceByType(self, priceType, price):
		"""
		"""
		lst = [csdefine.STORE_TYPE_XIANSHI, csdefine.STORE_TYPE_LINGSHI, csdefine.STORE_TYPE_XUANSHI, csdefine.STORE_TYPE_JINQIAN]
		return tuple([ price if e == priceType else 0 for e in lst ])

#-----------------------------------------赠送-----------------------------------------
	def requestPresentGift(self, goodsID, amount, receiverName, receiverDBID, message):
		"""
		exposed method
		赠送
		"""	
		if not self.validateClientCall():
			return
		query = "select sm_roleState from tbl_Role where sm_playerName = '%s'"%receiverName
		KBEngine.executeRawDatabaseCommand( query, Functions.Functor( self.queryRequestPresentGift, goodsID, amount, receiverName, receiverDBID, message) )

	def queryRequestPresentGift(self, goodsID, amount, receiverName, receiverDBID, message, resultSet, rows, insertid, errstr):
		if errstr is not None:
			KBEDebug.ERROR_MSG( errstr )
			return
		if not resultSet:
			self.statusMessage(csstatus.STORE_ROLE_NOT_EXIST)
			return	
		if int( resultSet[0][0] ) == csdefine.ROLE_STATE_DELETE:
			self.statusMessage(csstatus.STORE_ROLE_NOT_EXIST)
			return
		self.continueRequestPresentGift(goodsID, amount, receiverName, receiverDBID, message)	

	def continueRequestPresentGift(self, goodsID, amount, receiverName, receiverDBID, message):
		"""
		继续赠送
		"""
		# 不是好友无法赠送
		if not self.hasFriend( receiverName ):
			self.statusMessage( csstatus.STORE_ROLE_NOT_FRIEND, "")
			return

		goods = g_storeMgr.getGoodsByID(goodsID)
		# 仙石商品才可以赠送
		if STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI) != csdefine.STORE_TYPE_XIANSHI:
			return
		# 已下架的商品不能赠送
		if goods.GoodsState == csdefine.STORE_GOODS_STATE_SOLD_OUT:
			self.statusMessage(csstatus.STORE_GOODS_SOLD_OUT, "")
			return

		# 判断时间限制
		if not StoreLimitTime().verity(goods, amount):
			self.statusMessage(csstatus.STORE_BALANCE_FAILED)
			return

		# 判断是否是折扣时间
		actualPrice = goods.DiscountPrice
		if not StoreDiscountTime().verity(goods, amount):
			actualPrice = goods.Price

		# 金钱不足
		price = actualPrice * amount
		if not self.isEnoughMoney( STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI), price ):
			# self.client.CLIENT_StoreNotEnoughMoney( STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI) )
			self.statusMessage(csstatus.STORE_NO_ENOUGH_XIANSHI, "")
			return
		
		presentRecord = self.pickPresentRecord(goodsID, amount, self.playerName, receiverName, price, self.databaseID, receiverDBID, goods.ItemID)
		KBEngine.globalData["StoreManager"].setPresentRecords(self, [presentRecord])
		giftBox = self.pickGiftBoxData(self.playerName, self.databaseID, goodsID, amount, receiverName, receiverDBID, price, message, goods.ItemID)
		KBEngine.globalData["StoreManager"].requestPresentGift(self, giftBox) 
		rebateValue = int(price * goods.RebateRate)
		self.paymentStoreGoods(csdefine.STORE_TYPE_XIANSHI, price, rebateValue)
		self.statusMessage(csstatus.STORE_PRESENT_SUCCESS, "")
		
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(goods.ItemID, amount)
		moneyList = self._getPriceByType(STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI), price)
		g_logger.tradeGivingGoodLog(self.databaseID, self.playerName, receiverDBID, receiverName, goods.ItemID, itemInst.getItemDir("ItemName"), amount, moneyList[0], moneyList[1], moneyList[2], moneyList[3], itemInst)
		KBEngine.lookUpEntityByDBID( "Role", int(receiverDBID), Functions.Functor( self.onReceivePresent, [presentRecord]) )

	def pickGiftBoxData(self, senderName, senderDBID, goodsID, amount, receiverName, receiverDBID, price, message, itemID):
		"""
		打包礼品盒
		"""
		data = StoreGiftBoxData()
		data.goodsID = goodsID
		data.amount = amount
		data.receiverName = receiverName
		data.receiverDBID = str(receiverDBID)
		data.senderName = senderName
		data.senderDBID = str(senderDBID)
		data.price = price
		data.message = message
		data.itemID = itemID
		return data

	def pickPresentRecord(self, goodsID, amount, senderName, receiverName, price, senderDBID, receiverDBID, itemID):
		data = StorePresentRecordData()
		data.goodsID = goodsID
		data.amount = amount
		data.sender = senderName
		data.receiver = receiverName
		data.price = price
		data.receiverDBID = str(receiverDBID)
		data.senderDBID = str(senderDBID)
		data.itemID = itemID
		return data

	def queryPresentRecords(self):
		"""
		exposed method
		查询赠送记录
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].queryPresentRecords(self, str(self.databaseID))

	def deletePresentRecord(self, uid):
		"""
		exposed method
		删除赠送记录
		"""
		if not self.validateClientCall():
			return
		
		KBEngine.globalData["StoreManager"].deletePresentRecord(str(self.databaseID), uid)
		self.client.CLINET_OnDeletePresentRecord(uid)	

	def deletePresentRecords(self):
		"""
		exposed method
		清空赠送记录
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].deletePresentRecords(str(self.databaseID))
		self.client.CLINET_OnDeletePresentRecords()

#-----------------------------------------礼品盒-----------------------------------------
	def requestOpenGiftBox(self):
		"""
		exposed method
		申请打开礼品盒
		"""
		if not self.validateClientCall():
			return
			
		KBEngine.globalData["StoreManager"].requestOpenGiftBox(self, str(self.databaseID))

	def acceptGift(self, uid):
		"""
		exposed method
		接受礼品
		"""
		if not self.validateClientCall():
			return
		
		KBEngine.globalData["StoreManager"].acceptGift(self, str(self.databaseID), uid)

	def onAcceptGift(self, itemID, amount, uid):
		"""
		<defined method>
		收礼
		"""
		self.cell.onAcceptGift( itemID, amount, uid)
		
	def onAcceptGiftOver(self, uid):
		"""
		<defined method>
		收礼完成回调
		"""
		KBEngine.globalData["StoreManager"].onAcceptGiftOver( self, str(self.databaseID), uid )

	def acceptGifts(self):
		"""
		exposed method
		全部接受礼品
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].acceptGifts(self, str(self.databaseID))

	def onAcceptGifts(self, itemIDList, amountList):
		"""
		<defined method>
		全部收取
		"""
		self.cell.onAcceptGifts( itemIDList, amountList)

	def onAcceptGiftsOver(self):
		"""
		<defined method>
		全部收礼完成回调
		"""
		KBEngine.globalData["StoreManager"].onAcceptGiftOvers(self, str(self.databaseID))

	def refuseGift(self, uid):
		"""
		<exposed method>
		拒礼
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].refuseGift(self, str(self.databaseID), uid)

	def refuseGifts(self):
		"""
		exposed method
		全部拒礼
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].refuseGifts(self, str(self.databaseID))

	def deleteGiftBoxReceiveRecord(self, uid):
		"""
		<exposed method>
		删除收礼记录
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].removeGiftBoxRecord(2, self, str(self.databaseID), uid )

	def deleteGiftBoxReceiveRecords(self):
		"""
		<exposed method>
		清空收礼记录
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].removeAllGiftBoxRecord(2, self, str(self.databaseID))

	def getBackGift(self, uid):
		"""
		<exposed method>
		取回礼品
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].getBackGift(self, str(self.databaseID), uid)

	def onGetBackGift(self, itemID, amount, uid ):
		"""
		<defined method>
		取回礼品
		"""
		self.cell.onGetBackGift( itemID, amount, uid)

	def onGetBackGiftOver(self, uid):
		"""
		<defined method>
		取回礼品完成回调
		"""
		KBEngine.globalData["StoreManager"].onGetBackGiftOver(self, str(self.databaseID), uid )

	def getBackGifts(self):
		"""
		<exposed method>
		全部取回礼品
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].getBackGifts(self, str(self.databaseID))

	def onGetBackGifts(self, itemIDList, amountList):
		"""
		<defined method>
		全部收取
		"""
		self.cell.onGetBackGifts( itemIDList, amountList)

	def onGetBackGiftsOver(self):
		"""
		<defined method>
		取回礼品完成回调
		"""
		KBEngine.globalData["StoreManager"].onGetBackGiftsOver(self, str(self.databaseID))

	def deleteGiftBoxSendRecord(self, uid):
		"""
		<exposed method>
		删除送礼记录
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].removeGiftBoxRecord(1, self, str(self.databaseID), uid )

	def deleteGiftBoxSendRecords(self):
		"""
		<exposed method>
		删除送礼记录
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].removeAllGiftBoxRecord(1, self, str(self.databaseID))

	def transferPresent(self, uid, receiverName, receiverDBID, message):
		"""
		<exposed method>
		转增
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["StoreManager"].transferPresent(self, str(self.databaseID), uid, receiverName, receiverDBID, message)

	def onTransferPresent(self, giftBox):
		"""
		<defined method>
		转增回调
		"""
		presentRecord = self.pickPresentRecord(giftBox.goodsID, giftBox.amount, self.playerName, giftBox.receiverName, giftBox.price, self.databaseID, giftBox.receiverDBID, giftBox.itemID)
		KBEngine.globalData["StoreManager"].setPresentRecords(self, [presentRecord])
		self.statusMessage(csstatus.STORE_PRESENT_SUCCESS, "")
		
		goods = g_storeMgr.getGoodsByID(giftBox.goodsID)
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(goods.ItemID, giftBox.amount)
		moneyList = self._getPriceByType(STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI), giftBox.price)
		g_logger.tradeGivingGoodLog(self.databaseID, self.playerName, giftBox.receiverDBID, giftBox.receiverName, goods.ItemID, itemInst.getItemDir("ItemName"), giftBox.amount, moneyList[0], moneyList[1], moneyList[2], moneyList[3], itemInst)
		KBEngine.lookUpEntityByDBID( "Role", int(giftBox.receiverDBID), Functions.Functor( self.onReceivePresent, [presentRecord]) )

	def onShowGiftBoxRedPoint(self, type):
		"""
		<exposed method>
		显示完小红点
		"""
		if not self.validateClientCall():
			return

		KBEngine.globalData["StoreManager"].onShowGiftBoxRedPoint(self, self.databaseID, type)	

#-----------------------------------------购物车---------------------------------------------
	def buyStoreCartGoods(self, goodsIDList, amountList):
		"""
		<exposed method>
		购物车批量购买商品
		"""
		if not self.validateClientCall():
			return
		
		KBEngine.globalData["StoreManager"].buyStoreCartGoods(self, self.databaseID, goodsIDList, amountList)

	def onBuyStoreCartGoods(self, goodsIDList, amountList):
		"""
		<defined method>
		购物车批量购买商品回调
		"""
		index = 0
		itemIDList = []
		priceList = []
		price = 0
		GoodsType = csdefine.STORE_TYPE_XIANSHI
		for goodsID in goodsIDList:
			amount = amountList[index]
			goods = g_storeMgr.getGoodsByID(goodsID)
			GoodsType = STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI)	
			itemIDList.append(goods.ItemID)

			# 判断时间限制
			if not StoreLimitTime().verity(goods, amount):
				self.statusMessage(csstatus.STORE_BALANCE_FAILED)
				return

			# 判断是否是折扣时间
			actualPrice = goods.DiscountPrice
			if not StoreDiscountTime().verity(goods, amount):
				actualPrice = goods.Price

			priceList.append(actualPrice * amount)
			price += actualPrice * amount

			index += 1

		# 金钱不足返回	
		if GoodsType == csdefine.STORE_TYPE_JINQIAN:
			self.cell.isEnoughMoneyByCart(goodsIDList, itemIDList, amountList, priceList, price)
			return

		if not self.isEnoughMoney( GoodsType, price ):
			if GoodsType == csdefine.STORE_TYPE_LINGSHI:
				lingshi = price - self.lingshi
				xianshi = lingshi
				self.inquireMessage(csstatus.STORE_NO_ENOUGH_XIANSHI_REPALCE_LINGSHI, [xianshi, lingshi], "isBuyStoreCartGoods", goodsIDList, itemIDList, amountList, priceList, price, GoodsType)
			else:
				self.statusMessage(csstatus.STORE_NO_ENOUGH_XIANSHI, "")
			return	
			
		# 判断背包是否放的下
		self.cell.buyStoreCartGoods(goodsIDList, itemIDList, amountList, priceList, price, GoodsType)

	def isBuyStoreCartGoods(self, reply, goodsIDList, itemIDList, amountList, priceList, price, priceType):
		if reply:
			lingshi = price - self.lingshi
			xianshi = lingshi
			if xianshi > self.xianshi:
				self.statusMessage(csstatus.STORE_NO_ENOUGH_XIANSHI_AND_LINGSHII, "")
				return
			self.prepayment[priceType] += price
			self.cell.buyStoreCartGoods(goodsIDList, itemIDList, amountList, priceList, price, priceType)

	def onBuyStoreCartGoodsOver(self, goodsIDList, amountList, priceList, price, priceType):
		"""
		<defined method>
		购买购物车完成
		"""
		index = 0
		GoodsType = csdefine.STORE_TYPE_XIANSHI
		for goodsID in goodsIDList:
			goods = g_storeMgr.getGoodsByID(goodsID)
			amount = amountList[index]
			actualPrice = priceList[index]
			GoodsType = STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI)
			self.addBuyRecords(goods, amount, actualPrice, priceType, goods.ItemID )
			index += 1
		
		#灵石不够时，可通过仙石进行支付，不返利
		self.paymentStoreGoods(priceType, price)
		self.statusMessage(csstatus.STORE_BUY_SUCCESS)
		if hasattr(self, "client") and self.client:
			self.client.OnStoreBuyComplete()

	def presentStoreCartGoods(self, goodsIDList, amountList, receiverName, receiverDBID, message):
		"""
		exposed method
		购物车批量赠送商品
		"""	
		if not self.validateClientCall():
			return
		if len(goodsIDList) == 0:
			return
		query = "select sm_roleState from tbl_Role where sm_playerName = '%s'"%receiverName
		KBEngine.executeRawDatabaseCommand( query, Functions.Functor( self.queryPresentStoreCartGoods, goodsIDList, amountList, receiverName, receiverDBID, message) )

	def queryPresentStoreCartGoods(self, goodsIDList, amountList, receiverName, receiverDBID, message, resultSet, rows, insertid, errstr):
		"""
		查询角色状态回调
		"""
		if errstr is not None:
			KBEDebug.ERROR_MSG( errstr )
			return
		if not resultSet:
			self.statusMessage(csstatus.STORE_ROLE_NOT_EXIST)
			return	
		if int( resultSet[0][0] ) == csdefine.ROLE_STATE_DELETE:
			self.statusMessage(csstatus.STORE_ROLE_NOT_EXIST)
			return		
		self.continuePresentStoreCartGoods(goodsIDList, amountList, receiverName, receiverDBID, message)		

	def continuePresentStoreCartGoods(self, goodsIDList, amountList, receiverName, receiverDBID, message):
		"""
		继续购物车批量赠送商品
		"""

		# 不是好友无法赠送
		if not self.hasFriend( receiverName ):
			self.statusMessage( csstatus.STORE_ROLE_NOT_FRIEND, "")
			return

		index = 0
		totalPrices = 0
		rebateValue = 0 
		presentRecords = []
		for goodsID in goodsIDList:
			goods = g_storeMgr.getGoodsByID(goodsID)
			amount = amountList[index]
			# 仙石商品才可以赠送
			if STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI) != csdefine.STORE_TYPE_XIANSHI:
				return

			# 已下架的商品不能赠送
			if goods.GoodsState == csdefine.STORE_GOODS_STATE_SOLD_OUT:
				self.statusMessage(csstatus.STORE_GOODS_SOLD_OUT, "")
				return

			# 判断时间限制
			if not StoreLimitTime().verity(goods, amount):
				self.statusMessage(csstatus.STORE_BALANCE_FAILED)
				return

			# 判断是否是折扣时间
			actualPrice = goods.DiscountPrice
			if not StoreDiscountTime().verity(goods, amount):
				actualPrice = goods.Price
				
			# 金钱不足
			price = actualPrice * amount
			totalPrices += price
			rebateValue += int(price * goods.RebateRate)
			if not self.isEnoughMoney( STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI), price ):
				# self.client.CLIENT_StoreNotEnoughMoney( STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI) )
				self.statusMessage(csstatus.STORE_NO_ENOUGH_XIANSHI, "")
				return

			presentRecord = self.pickPresentRecord(goodsID, amount, self.playerName, receiverName, price, self.databaseID, receiverDBID, goods.ItemID)
			presentRecords.append(presentRecord)
			giftBox = self.pickGiftBoxData(self.playerName, str(self.databaseID), goodsID, amount, receiverName, receiverDBID, price, message, goods.ItemID)
			KBEngine.globalData["StoreManager"].requestPresentGift(self, giftBox)
			index += 1
			
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(goods.ItemID, amount)
			moneyList = self._getPriceByType(STORE_PAY_TYPE.get(goods.GoodsType, csdefine.STORE_TYPE_XIANSHI), price)
			g_logger.tradeGivingGoodLog(self.databaseID, self.playerName, receiverDBID, receiverName, goods.ItemID, itemInst.getItemDir("ItemName"), amount, moneyList[0], moneyList[1], moneyList[2], moneyList[3], itemInst)
		
		self.paymentStoreGoods(csdefine.STORE_TYPE_XIANSHI, totalPrices, rebateValue)
		self.statusMessage(csstatus.STORE_PRESENT_SUCCESS, "")
		KBEngine.globalData["StoreManager"].setPresentRecords(self, presentRecords)
		KBEngine.lookUpEntityByDBID( "Role", int(receiverDBID), Functions.Functor( self.onReceivePresent, presentRecords) )

	def onReceivePresent(self, presentRecords, target ):
		if target is False:
			return
		if target is True:
			return
		if target.client:
			target.statusMessage(csstatus.STORE_RECEIVE_GIFT, "")
			target.client.CLIENT_OnUpdatePresentRecords({"Datas" : presentRecords})

	def addStoreCartGoods(self, goodsType, goodsID, amount):
		"""
		exposed method
		将某商品添加到购物车
		购物车里的goodsType指的是payType支付类型
		"""
		if not self.validateClientCall():
			return
		goods = g_storeMgr.getGoodsByID(goodsID)

		# 已下架的商品不能添加到购物车
		if goods.GoodsState == csdefine.STORE_GOODS_STATE_SOLD_OUT:
			self.statusMessage(csstatus.STORE_GOODS_SOLD_OUT, "")
			return

		if goodsType not in self.storeCart:
			self.storeCart[goodsType] = {}

		if goodsID not in self.storeCart[goodsType]:
			self.storeCart[goodsType][goodsID] = 0

		self.storeCart[goodsType][goodsID] += amount
		self.client.CLIENT_OnAddStoreCartGoods( goodsType, goodsID, amount )

		
	def deleteStoreCartGoods(self, goodsType, goodsID):
		"""
		exposed method
		将某商品从购物车删除
		"""
		if not self.validateClientCall():
			return
		if goodsType in self.storeCart:
			self.storeCart[goodsType].pop(goodsID, None)
		self.client.CLIENT_OnDeleteStoreCartGoods( goodsType, goodsID)

	def deleteSoldOutStoreCartGoods( self, goodsType, goodsIDs ):
		"""
		exposed method
		将已下架的商品从购物车删除
		"""
		if goodsType in self.storeCart:
			for goodsID in goodsIDs:
				if goodsID in self.storeCart[goodsType].keys():
					self.storeCart[goodsType].pop(goodsID, None)
		self.client.OnDeleteSoldOutStoreCartGoods( goodsType, goodsIDs )

	def clearStoreCartGoods(self, goodsType):
		"""
		exposed method
		清空某专区的购物车
		"""
		if not self.validateClientCall():
			return
		self.storeCart.pop(goodsType, None)
		self.client.CLIENT_OnClearStoreCartGoods(goodsType)

	def synStoreCartGoods(self, goodsType, goodsIDList, amountList):
		"""
		exposed method
		将客户端的购物车数据更新到服务器(一般是玩家下线的同步)
		"""
		if not self.validateClientCall():
			return

		if goodsType not in self.storeCart:
			return

		index = 0
		for ID in goodsIDList:
			self.storeCart[goodsType].update({ID:amountList[index]})
			index += 1

	def openStoreCart(self):
		"""
		exposed method
		打开购物车
		"""
		goodsList = []
		for goodsType in self.storeCart:
			for goodsID, amount in self.storeCart[goodsType].items():
				goods = g_storeMgr.getGoodsByID(goodsID)
				if goods != None:
					goodsList.append(goods)
		self.client.CLIENT_OnGetGoodsListByIDList({"Datas" : goodsList })
		List = self.storeCart.getList()
		self.client.CLIENT_UpdateStoreCart( {"Datas" : List })


#--------------------------------商城支付---------------------------------------
	def isEnoughMoney(self, goodsType, value):
		"""
		判断金钱是否足够
		"""
		result = False
		if goodsType == csdefine.STORE_TYPE_XIANSHI:
			if self.xianshi >= (value + self.prepayment[goodsType]):
				result = True
		elif goodsType == csdefine.STORE_TYPE_LINGSHI:
			if self.lingshi >= (value + self.prepayment[goodsType]):
				result = True
		elif goodsType == csdefine.STORE_TYPE_XUANSHI:
			if self.xuanshi >= (value + self.prepayment[goodsType]):
				result = True
			else:
				self.statusMessage(csstatus.STORE_NO_ENOUGH_XUANSHI, "")
		if result:
			self.prepayment[goodsType] += value	
		return result
		
	def isEnoughMoney2(self, goodsType, value):
		"""
		"""
		result = self.isEnoughMoney(goodsType, value)
		if not result:
			if goodsType == csdefine.STORE_TYPE_LINGSHI:
				if self.xianshi >= value:
					return True, csdefine.STORE_TYPE_XIANSHI
			return False, goodsType
		
		return True, goodsType

	def paymentStoreGoods(self, goodsType, value, rebateValue = 0):
		"""
		付款
		"""
		if goodsType == csdefine.STORE_TYPE_XIANSHI:
			self.paymentByXianShi( value, rebateValue, csdefine.CHANGE_XIANSHI_BY_SHOP_CONSUME )
		elif goodsType == csdefine.STORE_TYPE_LINGSHI:
			if self.lingshi < value:
				xianshi = value - self.lingshi
				lingshi = self.lingshi
				self.payXianShi(xianshi, csdefine.CHANGE_XIANSHI_BY_SHOP_CONSUME)
				self.payLingShi(self.lingshi, csdefine.CHANGE_LINGSHI_BY_SHOP_CONUSUME)
			else:
				self.payLingShi(value, csdefine.CHANGE_LINGSHI_BY_SHOP_CONUSUME)
		elif goodsType == csdefine.STORE_TYPE_XUANSHI:
			self.payXuanShi(value, csdefine.CHANGE_XUANSHI_SHOP_CONUSUME)
		self.prepayment[goodsType] -= value	

	def onStoreFailureDeal(self, goodsType, price ):
		"""
		<define method>
		商城交易失败
		"""
		if goodsType == csdefine.STORE_TYPE_JINQIAN:
			return
		self.prepayment[goodsType] -= price	

	def paymentByXianShi(self, value, rebateValue, reason):
		"""
		<define method>
		用仙石付款--返利玄石
		"""
		self.payXianShi(value, reason)
		if not rebateValue: return
		
		self.gainXuanShi(rebateValue, csdefine.CHANGE_XUANSHI_SHOP_REBATE)