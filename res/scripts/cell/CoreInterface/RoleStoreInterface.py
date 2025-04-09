# -*- coding: utf-8 -*-
import KBEDebug
import csdefine
import csstatus
from MsgLogger import g_logger
from ItemFactory import ItemFactoryInst as g_itemFactory

class RoleStoreInterface:
	"""
	玩家商城接口类(新)
	"""
	def __init__( self ):
		pass

	def isEnoughMoney(self, goodsID, itemID, amount, price):
		"""
		<define method>
		金币是否足够
		"""
		price *= 10000
		if self.money < price:
			money = int((price - self.money)/10000)
			xianshi = money
			self.inquireMessage(csstatus.STORE_NO_ENOUGH_XIANSHI_REPALCE_MONEY, [xianshi, money], "buyStoreGoodsUseXianshi", goodsID, itemID, amount, price)
			return

		if self.buyStoreGoods( goodsID, itemID, amount, price, csdefine.STORE_TYPE_JINQIAN):
			self.subMoney(price, csdefine.MONEY_SUB_REASON_SHOP_BUY)
			
	def _getPriceByType(self, priceType, price):
		"""
		"""
		lst = [csdefine.STORE_TYPE_XIANSHI, csdefine.STORE_TYPE_LINGSHI, csdefine.STORE_TYPE_XUANSHI, csdefine.STORE_TYPE_JINQIAN]
		return tuple([ price if e == priceType else 0 for e in lst ])
	
	def buyStoreGoodsUseXianshi(self, reply, goodsID, itemID, amount, price ):
		if reply:
			if price > self.money + (self.xianshiForCell) * 10000:
				self.statusMessage(csstatus.STORE_NO_ENOUGH_XIANSHI_AND_MONEY, "")
				return
			if self.buyStoreGoods( goodsID, itemID, amount, price, csdefine.STORE_TYPE_JINQIAN):
				xianshi = int((price - self.money)/10000)
				self.payXianShi(xianshi, csdefine.CHANGE_XIANSHI_BY_SHOP_CONSUME, "")
				self.subMoney(self.money, csdefine.MONEY_SUB_REASON_SHOP_BUY)

	def buyStoreGoods(self, goodsID, itemID, amount, price, priceType ):
		"""
		<define method>
		购买物品
		"""
		# 背包空间不够，购买失败
		result, itemInst = self.addItemByID(itemID, amount, csdefine.ITEM_ADD_BY_SHOPMALLTRADE )
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(csstatus.STORE_NO_ENOUGH_ROOM, "")
			self.base.onStoreFailureDeal(priceType, price)
			return False
		
		self.base.onBuyStoreGoods(goodsID, amount, price, priceType)
		moneyList = self._getPriceByType(priceType, price)
		g_logger.tradeShopBuyLog(self.playerDBID, self.playerName, itemID, itemInst.uid, itemInst.getItemDir("ItemName"), amount, moneyList[0], moneyList[1], moneyList[2], moneyList[3], self.grade, itemInst)
		return True

	def isEnoughMoneyByCart(self, goodsIDList, itemIDList, amountList, priceList, price):
		"""
		<define method>
		金币是否足够
		"""
		price *= 10000
		if self.money < price:
			money = int((price - self.money)/10000)
			xianshi = money
			self.inquireMessage(csstatus.STORE_NO_ENOUGH_XIANSHI_REPALCE_MONEY, [xianshi, money], "buyStoreCartGoodsUseXianshi", goodsIDList, itemIDList, amountList, priceList, price)
			return

		if self.buyStoreCartGoods( goodsIDList, itemIDList, amountList, priceList, price, csdefine.STORE_TYPE_JINQIAN):
			self.subMoney(price, csdefine.MONEY_SUB_REASON_SHOP_BUY)

	def buyStoreCartGoodsUseXianshi(self, reply, goodsIDList, itemIDList, amountList, priceList, price ):
		if reply:		
			if price > self.money + (self.xianshiForCell) * 10000:
				self.statusMessage(csstatus.STORE_NO_ENOUGH_XIANSHI_AND_MONEY, "")
				return
			if self.buyStoreCartGoods( goodsIDList, itemIDList, amountList, priceList, price, csdefine.STORE_TYPE_JINQIAN):
				xianshi = int((price - self.money)/10000)
				self.payXianShi(xianshi, csdefine.CHANGE_XIANSHI_BY_SHOP_CONSUME, "")				
				self.subMoney(self.money, csdefine.MONEY_SUB_REASON_SHOP_BUY)

	def buyStoreCartGoods(self, goodsIDList, itemIDList, amountList, priceList, price, priceType):
		"""
		<defined method>
		购买购物车
		"""
		result, itemInsts = self.addItemByIDList( itemIDList, amountList, csdefine.ITEM_ADD_BY_SHOPMALLTRADE)
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(csstatus.STORE_BAG_HAS_ENOUGH, "")
			self.base.onStoreFailureDeal(priceType, price)
			return False
		
		self.base.onBuyStoreCartGoodsOver(goodsIDList, amountList, priceList, price, priceType)
		
		#记录购物日志
		for i in range(len(itemInsts)):
			itemInst = itemInsts[i]
			moneyList = self._getPriceByType(priceType, priceList[i])
			g_logger.tradeShopBuyLog(self.playerDBID, self.playerName, itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, moneyList[0], moneyList[1], moneyList[2], moneyList[3], self.grade, itemInst)
		return True

	def onAcceptGift(self, itemID, amount, uid):
		"""
		<defined method>
		收礼
		"""
		# 背包空间不够，购买失败
		result, _ = self.addItemByID(itemID, amount, csdefine.ITEM_ADD_BY_SHOPMALLTRADE )
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(csstatus.STORE_BAG_HAS_ENOUGH, "")
			return
		self.base.onAcceptGiftOver(uid)

	def onAcceptGifts(self, itemIDList, amountList):
		"""
		<defined method>
		全部收取
		"""
		result, _ = self.addItemByIDList( itemIDList, amountList, csdefine.ITEM_ADD_BY_SHOPMALLTRADE)
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(csstatus.STORE_BAG_HAS_ENOUGH, "")
			return
		self.base.onAcceptGiftsOver()

	def onGetBackGift(self, itemID, amount, uid ):
		"""
		<defined method>
		取回礼品
		"""
		# 背包空间不够，购买失败
		result, _ = self.addItemByID(itemID, amount, csdefine.ITEM_ADD_BY_SHOPMALLTRADE )
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(csstatus.STORE_BAG_HAS_ENOUGH, "")
			return
		self.base.onGetBackGiftOver( uid)

	def onGetBackGifts(self, itemIDList, amountList):
		"""
		<defined method>
		全部取回
		"""
		result, _ = self.addItemByIDList( itemIDList, amountList, csdefine.ITEM_ADD_BY_SHOPMALLTRADE)
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(csstatus.STORE_BAG_HAS_ENOUGH, "")
			return
		self.base.onGetBackGiftsOver()


	def initStoreAppearance(self):
		"""
		初始化玩家商城外观
		"""
		for i in self.hasStoreAppearances:
			self.client.AddHasStoreAppearance(i)
		for i in self.storeAppearances:
			self.client.AddStoreAppearance(i)
		for k,v in self.storeBackAdornParam.items():
			self.client.UpdateStoreBackAdornParam(int(k), v)

	def setStoreBackAdornParam( self, srcEntityID, itemID, paramStr ):
		"""
		Exposed method
		更新背饰参数数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.storeBackAdornParam[str(itemID)] = paramStr

		self.client.UpdateStoreBackAdornParam(itemID, paramStr)

	def onUseStoreAppearance(self, itemID):
		"""
		使用商城外观物品回调
		"""
		if itemID not in self.hasStoreAppearances:
			self.hasStoreAppearances.append(itemID)
			self.client.AddHasStoreAppearance(itemID)

		item = g_itemFactory.getItemData( itemID )
		appearancesType = int(item["Param1"])
		for i in self.storeAppearances:
			temp = g_itemFactory.getItemData( i )
			if int(temp["Param1"]) == appearancesType:
				self.storeAppearances.remove(i)
				self.client.RemoveStoreAppearance(i)
				break
		self.storeAppearances.append(itemID)
		self.client.AddStoreAppearance(itemID)

	def putOnStoreAppearance(self, srcEntityID, aType, value, itemID):
		"""	
		<Exposed method>
		换上商城外观
		"""
		self.setStoreAppearanceByType(aType, value, itemID)
		self.onUseStoreAppearance(itemID)

	def takeOffStoreAppearance(self, srcEntityID, aType, value, itemID):
		"""	
		<Exposed method>
		脱掉商城外观
		"""
		self.setStoreAppearanceByType(aType, "", itemID)
		if itemID in self.storeAppearances:
			self.storeAppearances.remove(itemID)
			self.client.RemoveStoreAppearance(itemID)