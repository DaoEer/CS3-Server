# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import time
import Functions
import csdefine
import csstatus
import csconst
import Const
import ItemFactory
from ConfigObject.Trade.TradeMgr import g_tradeMgr
from Tong.TongBuildFunc import Datas as tongBuildFunc
import ItemTypeEnum
import ItemFactory
import math
from NPCShopItemListImpl import BuyBackItemDict
from MsgLogger import g_logger

class RoleBuyNPCShopInterface:
	"""
	"""
	def __init__(self):
		#帮会掠夺战商店分页数据
		self.isLockTongShop = False
		self.tongPlunderShopSellStart = False
		self.tongPlunderShopData = []

	def isEnoughBindMoney(self,price):
		"""是否有足够的绑定金币"""
		if self.bindMoney < price:
			return False
		else:
			return True

	def initBuyBackItemList( self ):
		"""
		请求回购物品列表	
		"""
		data = {}
		_buyBack = { "buyBackItemDataList":[] }
		for itemInst in self.buyBack:
			tempdict = {'id':itemInst.id, 'uid':str(itemInst.uid), 'amount':itemInst.amount, 'bindType':itemInst.bindType }
			tempdict.update( itemInst.getClientTipDynamicProperty() )
			buyBackItemData = BuyBackItemDict().createObjFromDict( tempdict )
			_buyBack[ "buyBackItemDataList" ].append( buyBackItemData )
		self.client.CLIENT_OnInitBuyBackItemList(  _buyBack  )

#---------------------------高回购物品（废弃CST-5110）---------------------------------------
	def highBuyBackAdd( self,  itemInst ):
		"""
		添加
		"""
		self.highBuyBack.add( itemInst )
		tempdict = {"id":str(itemInst.id), "uid":str(itemInst.uid),"amount":str(itemInst.amount), "bindType":str(itemInst.bindType),"time":self.highBuyBack[itemInst.uid].time }
		tempdict = Functions.toJsonString( [tempdict] )
		self.client.addHighBuyBackItem(tempdict )
		
		self.highBuyBackFullCheck() #列表检查
	
	def highBuyBackDec( self, uid ):
		"""
		减少
		"""
		self.highBuyBack.pop( uid )
		self.client.subHighBuyBackItem( str(uid) )
	
	def highBuyBackFullCheck( self ):
		"""
		高回购列表检查
		"""
		while len(self.highBuyBack) > csdefine.NPCSHOP_HIGH_BUY_BACK_AMOUNT:
			tempTime = []
			for key in self.highBuyBack:
				tempTime.append(self.highBuyBack[key].time)
			tempTime.sort()
			minTime = tempTime[0]
			for key in self.highBuyBack:
				if self.highBuyBack[key].time == minTime:
					uid = key
			
			self.highBuyBackDec( uid )
	
	def requestBuyBackHighItem( self, roleID, shopID, itemUID ):
		"""
		<exposed method>
		请求回购高级物品
		"""
		if not self.validateClientCall( roleID ):
			return

		if self.isState(csdefine.ENTITY_STATE_DEAD):
			self.statusMessage( csstatus.NPCSHOP_ROLE_DEAD,"" )
			return

		if self.shopID != shopID:
			KBEDebug.ERROR_MSG( "shop id %s != %s"%(self.shopID, shopID) )
			return

		# 验证与NPC的距离
		npc = KBEngine.entities.get( self.ShopNPCID, None )
		if npc == None:
			KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
			return
		if self.position.flatDistTo( npc.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
			KBEDebug.ERROR_MSG( "npc %s distance > 5"%(self.ShopNPCID) )
			return

		timeout = []
		isBuy = False
		itemUID = int( itemUID )
		for itemUID in self.highBuyBack:
			data = self.highBuyBack[itemUID]
			if data.time + csdefine.NPCSHOP_HIGH_BUY_BACK_TIME > time.time():
				itemInst = data.item
				if self.addItemCheck( itemInst ) == csstatus.ITEM_GO_ON:
					if self.subBindMoney( int( itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO), csdefine.MONEY_SUB_REASON_SHOP_BUY ):
						self.addItem( data.item, csdefine.ITEM_ADD_BY_NPCTRADE )
						self.statusMessage( csstatus.NPCSHOP_ROLE_BUY_SUCCESS, "" )
						self.highBuyBackDec( itemUID )
						#添加日志
						g_logger.tradeBuyBackHighLog( self.playerDBID, self.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount,  int( itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO), self.grade, npc.scriptID, self.getCurrentSpaceScriptID(), itemInst )
					else:
						cost = int(itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO)
						self.inquireMessage(csstatus.NPCSHOP_BUY_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(cost)], "replacePayBuyBackHigh", npc.scriptID, cost, itemInst,itemUID)
				isBuy = True
				break
			else:
				timeout.append( itemUID )

		for uid in timeout:
			self.highBuyBackDec( uid )

		if not isBuy:
			KBEDebug.ERROR_MSG( "requestBuyBackItem::no %s item"%(itemUID) )

	def replacePayBuyBackHigh(self, reply, NPCID, cost, itemInst, itemUID):
		if reply:
			if self.subMoney(cost, csdefine.MONEY_SUB_REASON_SHOP_BUY):
				self.addItem(itemInst, csdefine.ITEM_ADD_BY_NPCTRADE)
				self.statusMessage(csstatus.NPCSHOP_ROLE_BUY_SUCCESS, "")
				self.highBuyBackDec(itemUID)
				# 添加日志
				g_logger.tradeBuyBackHighLog(self.playerDBID, self.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, cost, self.grade, NPCID, self.getCurrentSpaceScriptID(), itemInst)
			else:
				self.statusMessage(csstatus.NPCSHOP_ROLE_MONEY_ERROR, "")



#---------------------------NPC购买物品---------------------------------------
	def requestShopItemList( self, NPCID, shopID ):
		"""
		由NPC对话请求打开商店获得商店的列表
		"""
		self.ShopNPCID = NPCID
		self.shopID = shopID
		# 如果有动态数据，就到base上读取！否则读取客户端数据
		if g_tradeMgr.hasLimitItem( shopID ):
			KBEngine.globalData["ShopManager"].requestShopLimitItemList( shopID, self, self.playerDBID )
		else:
			
			npcShopConfig = g_tradeMgr.getShopTypeConfig(shopID)
			if npcShopConfig["isTongDisCount"] and self.tongMB:			# 帮会仓库打折
				discount = float(tongBuildFunc[self.tongSmithyLevel]["discount"])
				self.client.CLIENT_InitNPCShopItemListByDiscount( NPCID, shopID, None, discount )
				return
				
			self.client.CLIENT_InitNPCShopItemList( NPCID, shopID, None )
		
	def onRequestShopLimitItemList( self, shopID, shopItems ):
		"""
		<define method>
		查找商店有上限物品回调
		"""
		npcShopConfig = g_tradeMgr.getShopTypeConfig(shopID)
		if npcShopConfig["isTongDisCount"] and self.tongMB:			# 帮会仓库打折
			discount = float(tongBuildFunc[self.tongSmithyLevel]["discount"])
			self.client.CLIENT_InitNPCShopItemListByDiscount( self.ShopNPCID, shopID, shopItems, discount )
			return
		self.client.CLIENT_InitNPCShopItemList( self.ShopNPCID, shopID, shopItems )

	def requestBuyNPCShopItem( self, roleID, shopID, slot, itemID, amount ):
		"""
		<exposed method>
		请求购买物品
		"""
		if not self.validateClientCall( roleID ):
			return
			
		# 验证与NPC的距离,帮会商店没有NPC
		if shopID != "TongShop":
			npc = KBEngine.entities.get( self.ShopNPCID, None )
			if self.getState() == csdefine.ENTITY_STATE_DEAD:
				return
			if npc == None:
				KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
				return
			if self.position.flatDistTo( npc.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
				KBEDebug.ERROR_MSG( "npc %s distance > 5"%(self.ShopNPCID) )
				return
				
		elif shopID == "TongShop":
			if self.hasLockTongShop(): #帮会商店已被锁定，帮会掠夺战
				return
				
		if not g_tradeMgr.checkCondition(self, shopID, slot, itemID):
			return
			
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount)
		if itemInst is None:
			KBEDebug.ERROR_MSG("Buy item err!!item(%d) not find!"%itemID)
			return
		result = self.addItemCheck(itemInst)
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(result)
			return
		
		if g_tradeMgr.isLimitItem( shopID,slot ):
			KBEngine.globalData["ShopManager"].buyLimintItem(shopID, slot, amount, self, self.playerDBID)
			return
			
		#购买没有上限的物品
		item = g_tradeMgr.getShopItemConfig( shopID, slot )
		if item:
			if item["itemID"] != itemID:
				KBEDebug.ERROR_MSG("Buy NPC item err!slot(%s) item id is not same!(sell itemID:%d,buy itemID:%d)"%(slot,item["itemID"],itemID))
				return
			
			#计算总金额
			payItems = dict(item["price"])
			for key, value in payItems.items():
				payItems[key] = value * amount
			
			npcShopConfig = g_tradeMgr.getShopTypeConfig(shopID)
			if npcShopConfig["isTongDisCount"] and self.tongMB:			# 帮会仓库打折
				discount = tongBuildFunc[self.tongSmithyLevel]["discount"]
				for key, value in payItems.items():
					payItems[key] = int( value * discount * 0.1 )

			if csdefine.TRADE_PAY_ITEM_BIND_MONEY in payItems:			#如果支付方式为绑金，计算绑金是否足够支付。
				if not self.isEnoughBindMoney(payItems[csdefine.TRADE_PAY_ITEM_BIND_MONEY]):
					cost = payItems[csdefine.TRADE_PAY_ITEM_BIND_MONEY] - self.bindMoney
					payItems[csdefine.TRADE_PAY_ITEM_BIND_MONEY] = self.bindMoney
					payItems[csdefine.TRADE_PAY_ITEM_MONEY] = cost
					self.inquireMessage(csstatus.NPCSHOP_BUY_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(cost)], "replacePay", csdefine.TRADE_TYPE_NPC_SHOP,self.ShopNPCID, payItems, shopID, slot, itemID, amount)
					return
				
			self.requestPay(csdefine.TRADE_TYPE_NPC_SHOP, self.ShopNPCID, payItems, shopID, slot, itemID, amount)
		else:
			KBEDebug.ERROR_MSG("Buy NPC item err!shopItems(%s,%s) is None"%(shopID,slot))

	def requestBuyTongPlunderShopItem(self, roleID, slot, itemID, amount):
		"""
		<exposed method>
		请求购买帮会商店掠夺战分页的物品
		"""
		if not self.validateClientCall( roleID ):
			return
			
		if self.tongMB:
			self.tongMB.requestBuyTongPlunderShopItem(self.playerDBID, slot, itemID, amount)
		else:
			KBEDebug.ERROR_MSG("player is no tong")
			
	def requestBuyTongPlunderShopItemCB(self, slot, itemID, amount):
		"""
		define method
		"""
		shopID = "TongPlunderShop"
		if not self.hastartTongPlunderShopSell(): #帮会掠夺战分页商品还没开售
			return
			
		if not g_tradeMgr.checkCondition(self, shopID, slot, itemID):
			return
			
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount)
		if itemInst is None:
			KBEDebug.ERROR_MSG("Buy item err!!item(%d) not find!"%itemID)
			return
		result = self.addItemCheck(itemInst)
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(result)
			return
		
		if g_tradeMgr.isLimitItem( shopID,slot ):
			KBEngine.globalData["ShopManager"].buyLimintItem(shopID, slot, amount, self, self.playerDBID)
			return
			
		#购买没有上限的物品
		item = g_tradeMgr.getShopItemConfig( shopID, slot )
		if item:
			if item["itemID"] != itemID:
				KBEDebug.ERROR_MSG("Buy NPC item err!slot(%s) item id is not same!(sell itemID:%d,buy itemID:%d)"%(slot,item["itemID"],itemID))
				return
			
			#计算总金额
			payItems = dict(item["price"])
			for key, value in payItems.items():
				payItems[key] = value * amount
			
			if csdefine.TRADE_PAY_ITEM_BIND_MONEY in payItems:			#如果支付方式为绑金，计算绑金是否足够支付。
				if not self.isEnoughBindMoney(payItems[csdefine.TRADE_PAY_ITEM_BIND_MONEY]):
					cost = payItems[csdefine.TRADE_PAY_ITEM_BIND_MONEY] - self.bindMoney
					payItems[csdefine.TRADE_PAY_ITEM_BIND_MONEY] = self.bindMoney
					payItems[csdefine.TRADE_PAY_ITEM_MONEY] = cost
					self.inquireMessage(csstatus.NPCSHOP_BUY_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(cost)], "replacePay", csdefine.TRADE_TYPE_NPC_SHOP,self.ShopNPCID, payItems, shopID, slot, itemID, amount)
					return
				
			self.requestPay(csdefine.TRADE_TYPE_NPC_SHOP, self.ShopNPCID, payItems, shopID, slot, itemID, amount)
		else:
			KBEDebug.ERROR_MSG("Buy NPC item err!shopItems(%s,%s) is None"%(shopID,slot))
		
	def replacePay(self, reply,tradeType, targetID, payDict, *args):
		"""金币代付绑定金币"""
		if reply:
			self.requestPay(tradeType, targetID, payDict, *args)

	def onBuyLimintItem(self, shopID, slot, amount):
		"""
		define method
		购买上限物品回调
		"""
		shopItems = g_tradeMgr.getShopItemConfig( shopID, slot )
		payItems = dict(shopItems["price"])
		itemID = shopItems["itemID"]
		npcShopConfig = g_tradeMgr.getShopTypeConfig(shopID)
		if npcShopConfig["isTongDisCount"] and self.tongMB:			# 帮会仓库打折
			discount = tongBuildFunc[self.tongSmithyLevel]["discount"]
			for key, value in payItems.items():
				payItems[key] = int( value * discount *0.1 )
		
		if csdefine.TRADE_PAY_ITEM_BIND_MONEY in payItems:			#如果支付方式为绑金，计算绑金是否足够支付。
			if not self.isEnoughBindMoney(payItems[csdefine.TRADE_PAY_ITEM_BIND_MONEY]):
				cost = payItems.pop(csdefine.TRADE_PAY_ITEM_BIND_MONEY)
				payItems.update({csdefine.TRADE_PAY_ITEM_MONEY: cost})
				self.inquireMessage(csstatus.NPCSHOP_BUY_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(cost)], "replacePay", csdefine.TRADE_TYPE_NPC_SHOP,self.ShopNPCID, payItems, shopID, slot, itemID, amount)
				return
		
		self.requestPay(csdefine.TRADE_TYPE_NPC_SHOP, self.ShopNPCID, payItems, shopID, slot, itemID, amount)
	
	def onSuccessPayShopItem( self, payDict, shopID, slot, itemID, amount ):
		"""
		成功支付回调
		"""
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount)
		if itemInst is None:
			KBEDebug.ERROR_MSG("Buy item err!!item(%d) not find!"%itemID)
			return
			
		#CST-11672 如果使用绑金购买，则将物品设置为绑定
		if csdefine.TRADE_PAY_ITEM_BIND_MONEY in payDict and payDict[csdefine.TRADE_PAY_ITEM_BIND_MONEY] > 0:
			itemInst.setBindType(self)
			
		self.addItem( itemInst,csdefine.ITEM_ADD_BY_NPCTRADE )
		self.statusMessage( csstatus.NPCSHOP_ROLE_BUY_SUCCESS, "" )
		
		# 对于购买粉色品质以上的装备添加一条动态属性
		if itemInst.isEquip() and itemInst.getQuality() >= ItemTypeEnum.QUALITY_PINK:
			itemInst.setReturnBackTime( time.time() + 10 * 60,self )
			
		
#		KBEngine.globalData["ShopManager"].refreshItem(shopID, slot, self, self.playerDBID)
		self.client.CLIENT_OnSuccessBuyShopItem( shopID, slot, itemID, amount )
		
		config = g_tradeMgr.getRandomLimitShopConfig(shopID, slot)
		if config:
			spaceEntity = self.getCurrentSpace()
			if spaceEntity:
				c = g_tradeMgr.getShopTypeConfig(shopID)
				shopName = c["shopName"] if c else ""
				messageArg = "{}|{}|{}".format(self.getName(), shopName, itemInst.getItemDir("ItemName"))
				spaceEntity.globalWorld(csstatus.ITEM_ADD_BUY_JIYUAN, messageArg)
			
			#if self.getClient():
			#	self.client.CLIENT_PlaySound(Const.SHENGJIE_ITEM_GET_SOUND)
			#	self.client.CLIENT_PlayEffect(Const.SHENGJIE_ITEM_GET_EFFECTID)
			
		if shopID == "TongPlunderShop":
			cost = payDict.get(csdefine.TRADE_PAY_ITEM_BIND_MONEY, 0)
			cost += payDict.get(csdefine.TRADE_PAY_ITEM_MONEY, 0)
			if self.tongMB:
				self.tongMB.onTongPlunderShopSell(slot, itemID, amount, cost)	
	
		#添加日志
		npc = KBEngine.entities.get( self.ShopNPCID, None )
		npcScriptID = ""
		if npc:
			npcScriptID = npc.scriptID
		costMoney = payDict.get(csdefine.TRADE_PAY_ITEM_MONEY, 0)
		costBindMoney = payDict.get(csdefine.TRADE_PAY_ITEM_BIND_MONEY, 0)
		g_logger.tradeNpcBuyLog(self.playerDBID, self.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, costMoney, costBindMoney, self.grade, npcScriptID, self.getCurrentSpaceScriptID(), itemInst)
		
		price = (costMoney + costBindMoney) / itemInst.amount
		g_logger.costLog(self.accountDBID, self.playerDBID, itemInst.id, itemInst.getItemDir("ItemName"), price, itemInst.amount, costMoney, self.getMoney(), costBindMoney, self.getBindMoney(), self.getLevel())
		
	
	def onFailPayShopItem( self, shopID, slot, itemID, amount ):
		"""
		支付失败回调
		"""
		shopItem = g_tradeMgr.getShopItemConfig( shopID, slot )
		if shopItem["buyLimit"]:						# 购买上限物品失败
			KBEngine.globalData["ShopManager"].returnBuyItem( shopID, slot, itemID, amount, self.playerDBID )
	
	def requestSellItem( self, roleID, shopID, itemUID ):
		"""
		<exposed method>
		请求出售物品
		"""
		if not self.validateClientCall( roleID ):
			return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			self.statusMessage( csstatus.NPCSHOP_ROLE_DEAD,"" )
			return

		if self.shopID != shopID:
			KBEDebug.ERROR_MSG( "shop id %s != %s"%(self.shopID, shopID) )
			return

		if shopID != "TongShop":
			# 验证与NPC的距离
			npc = KBEngine.entities.get( self.ShopNPCID, None )
			if npc == None:
				KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
				return
			if self.position.flatDistTo( npc.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
				KBEDebug.ERROR_MSG( "npc %s distance > 5"%(self.ShopNPCID) )
				return
		elif shopID == "TongShop":
			if self.hasLockTongShop(): #帮会商店已被锁定，帮会掠夺战
				return

		itemInst = self.getItemInstByUid( int(itemUID) )
		if not itemInst:
			#防止异步
			return
		if not itemInst.isCanSell():
			# 物品不能出售
			self.statusMessage( csstatus.ITEM_CANSELL,"" )
			return
		if self.doKBOpratorCheck(itemInst) != csdefine.KB_OPRATOR_CAN_GO:
			return

		if not self.isAddBindMoney( int(itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO) ):
			self.statusMessage( csstatus.NPCSHOP_SELL_MONEY_MAX, "" )
			return

		self.removeItemByAmount( itemInst, itemInst.amount, csdefine.ITEM_REMOVE_BY_SELL_TO_NPC )
		self.onRequestSellItem( itemInst )
		#添加日志
		if shopID != "TongShop":
			g_logger.tradeNpcSellLog(self.playerDBID, self.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, int(itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO), self.grade, npc.scriptID, self.getCurrentSpaceScriptID(), itemInst)
		else:
			g_logger.tradeNpcSellLog(self.playerDBID, self.getName(), itemInst.id, itemInst.uid,
									 itemInst.getItemDir("ItemName"), itemInst.amount,
									 int(itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO), self.grade, "",
									 self.getCurrentSpaceScriptID(), itemInst)

	def onRequestSellItem( self, itemInst ):
		"""
		出售物品回调
		"""
		self.addBindMoney( int(itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO), csdefine.MONEY_ADD_REASON_SELL_ITEM )
		self.statusMessage(csstatus.NPCSHOP_SELL_SUCCESS,"")
#		if itemInst.getQuality() <= ItemTypeEnum.QUALITY_BLUE:
		tempdict = {"id":itemInst.id, "uid":str(itemInst.uid),"amount":itemInst.amount, "bindType":itemInst.bindType }
		tempdict.update( itemInst.getClientTipDynamicProperty() )
		buyBackItemDict = BuyBackItemDict().createObjFromDict( tempdict )
		self.buyBack.insert( 0, itemInst )
		while len( self.buyBack ) > csdefine.NPCSHOP_BUY_BACK_AMOUNT:
			itemInst = self.buyBack[len(self.buyBack)-1]
			tempdict = {"id": itemInst.id, "uid":itemInst.uid,"amount": itemInst.amount , "bindType": itemInst.bindType, "dynamicData": itemInst.getDynamicDataForClient( self ) }
			self.client.OnRequestBuyBackItem( tempdict )
			self.buyBack.remove( itemInst )
		self.client.CLIENT_OnRequestSellItem(buyBackItemDict)

	def requestBuyBackItem( self, roleID, shopID, itemUID ):
		"""
		<exposed method>
		请求回购物品
		"""
		if not self.validateClientCall( roleID ):
			return

		if self.isState(csdefine.ENTITY_STATE_DEAD):
			self.statusMessage( csstatus.NPCSHOP_ROLE_DEAD,"" )
			return

		if self.shopID != shopID:
			KBEDebug.ERROR_MSG( "shop id %s != %s"%(self.shopID, shopID) )
			return

		if shopID != "TongShop":
			# 验证与NPC的距离
			npc = KBEngine.entities.get( self.ShopNPCID, None )
			if npc == None:
				KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
				return
			if self.position.flatDistTo( npc.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
				KBEDebug.ERROR_MSG( "npc %s distance > 5"%(self.ShopNPCID) )
				return
		elif shopID == "TongShop":
			if self.hasLockTongShop(): #帮会商店已被锁定，帮会掠夺战
				return
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO:
			return

		itemUID = int( itemUID )
		for itemInst in self.buyBack:
			if itemInst.uid == itemUID:
				result = self.addItemCheck( itemInst )
				if result == csstatus.ITEM_GO_ON:
					if self.subBindMoney( int(itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO), csdefine.MONEY_SUB_REASON_SHOP_BUY ):
						self.addItem( itemInst, csdefine.ITEM_ADD_BY_NPCTRADE )
						self.statusMessage( csstatus.NPCSHOP_ROLE_BUY_SUCCESS, "" )
						self.buyBack.remove( itemInst )
						tempdict = {"id":itemInst.id, "uid":itemInst.uid,"amount":itemInst.amount, "bindType":itemInst.bindType, "dynamicData": itemInst.getDynamicDataForClient( self )}
						self.client.OnRequestBuyBackItem( tempdict )
						#添加日志
						if shopID != "TongShop":
							g_logger.tradeBuyBackLog( self.playerDBID, self.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, int(itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO), self.grade, npc.scriptID, self.getCurrentSpaceScriptID(), itemInst)
						else:
							g_logger.tradeBuyBackLog(self.playerDBID, self.getName(), itemInst.id, itemInst.uid,
													 itemInst.getItemDir("ItemName"), itemInst.amount,
													 int(itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO), self.grade,
													 "", self.getCurrentSpaceScriptID(), itemInst)
						return
					else:
						cost = int(itemInst.getPrice() * csdefine.NPCSHOP_SELL_RATIO)
						if shopID != "TongShop":
							self.inquireMessage(csstatus.NPCSHOP_BUY_MONEY_REPLACE_BIND_MONEY,[Functions.moneyToStr(cost)], "replacePayBuyBack", npc.scriptID, cost, itemInst)
							return
						else:
							self.inquireMessage(csstatus.NPCSHOP_BUY_MONEY_REPLACE_BIND_MONEY,
												[Functions.moneyToStr(cost)], "replacePayBuyBack", "", cost,
												itemInst)
							return
				else:
					self.statusMessage(result,"")
				return

		KBEDebug.ERROR_MSG( "requestBuyBackItem::no %s item"%(itemUID) )


	def replacePayBuyBack(self,reply, NPCID, cost, itemInst):
		"""金币代付绑定金币回购物品"""
		if reply:
			if self.subMoney(cost, csdefine.MONEY_SUB_REASON_SHOP_BUY):
				self.addItem(itemInst, csdefine.ITEM_ADD_BY_NPCTRADE)
				self.statusMessage(csstatus.NPCSHOP_ROLE_BUY_SUCCESS, "")
				self.buyBack.remove(itemInst)
				tempdict = {"id": itemInst.id, "uid": itemInst.uid, "amount":itemInst.amount,
							"bindType": itemInst.bindType}
				self.client.CLIENT_OnRequestBuyBackItem(tempdict)
				# 添加日志
				g_logger.tradeBuyBackLog(self.playerDBID, self.getName(), itemInst.id, itemInst.uid,itemInst.getItemDir("ItemName"), itemInst.amount, cost, self.grade, NPCID, self.getCurrentSpaceScriptID(), itemInst)
			else:
				self.statusMessage(csstatus.NPCSHOP_ROLE_MONEY_ERROR, "")


	def requestReturnItem( self,roleID,shopID,itemUID ):
		"""
		<exposed method>
		请求退货
		"""
		if not self.validateClientCall( roleID ):
			return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			self.statusMessage( csstatus.NPCSHOP_ROLE_DEAD,"" )
			return
		if self.shopID != shopID:
			KBEDebug.ERROR_MSG( "shop id %s != %s"%(self.shopID, shopID) )
			return
		# 验证与NPC的距离
		npc = KBEngine.entities.get( self.ShopNPCID, None )
		if npc == None:
			KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
			return
		if self.position.flatDistTo( npc.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
			KBEDebug.ERROR_MSG( "npc %s distance > 5"%(self.ShopNPCID) )
			return
		itemInst = self.getItemInstByUid( int(itemUID) )
		if itemInst == None:
			return
		if itemInst.getQuality() < ItemTypeEnum.QUALITY_PINK:
			#如果不是粉色品质以上的物品
			self.statusMessage( csstatus.NPCSHOP_SHOP_RETURN_ITEM_QUALITY_LIMIT,"" )
			return
		if not itemInst.checkCanReturnBack():
			#超出10分钟不能退货
			self.statusMessage( csstatus.NPCSHOP_SHOP_RETURN_ITEM_TIME_LIMIT,"" )
			return
#		if not itemInst.canReturn:
#			#不能退货
#			self.statusMessage( csstatus.NPCSHOP_SHOP_ITEM_RETURN_LIMIT,"" )
#			return
		if not self.isAddBindMoney( int(itemInst.getPrice() * csdefine.NPCSHOP_RETURN_RATIO) ):
			self.statusMessage( csstatus.NPCSHOP_SELL_MONEY_MAX, "" )
			return
		self.removeItemByAmount( itemInst, itemInst.amount, csdefine.ITEM_REMOVE_BY_SELL_TO_NPC )
		self.sellItemCallBack( itemInst )
		#添加日志
		g_logger.tradeBuyReturnItemLog( self.playerDBID, self.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount,  int(itemInst.getPrice() * csdefine.NPCSHOP_RETURN_RATIO), self.grade, npc.scriptID, self.getCurrentSpaceScriptID(), itemInst)

#--------------------------------装备修理----------------------------------------------------------------
	def requestRepairOneEquip( self,roleID,shopID,itemUID ):
		"""
		<exposed method>
		单件装备修理
		"""
		if not self.validateClientCall( roleID ):
			return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			self.statusMessage( csstatus.NPCSHOP_ROLE_DEAD,"" )
			return
		if self.shopID != shopID:
			KBEDebug.ERROR_MSG( "shop id %s != %s"%(self.shopID, shopID) )
			return

		npcShopConfig = g_tradeMgr.getShopTypeConfig(shopID)
		if not npcShopConfig["isCanRepair"]:
			return
			
		tongDiscount = 1
		if npcShopConfig["isTongDisCount"]:
			if self.tongMB:
				tongDiscount = tongBuildFunc[self.tongSmithyLevel]["discount"]
			else:
				KBEDebug.ERROR_MSG( "Player(%s) has not join in tong!"%(self.playerName) )
		
		#self.ShopNPCID为0，表示不是通过NPC打开商店
		# 验证与NPC的距离
		if self.ShopNPCID != 0:
			npc = KBEngine.entities.get( self.ShopNPCID, None )
			if npc == None:
				KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
				return
			if self.position.flatDistTo( npc.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
				KBEDebug.ERROR_MSG( "npc %s distance > 5"%(self.ShopNPCID) )
				return
		itemInst = self.getItemInstByUid( int(itemUID) )
		if itemInst == None:
			KBEDebug.ERROR_MSG( " has no  this item(%s) "%itemUID )
			return
		if not itemInst.isEquip():
			self.statusMessage( csstatus.NPCSHOP_SHOP_NOT_REPAIR,"" )
			return
		itemOrder = self.itemsBag.getOrderID( itemUID )
		if itemOrder in range(ItemTypeEnum.BAG_STORE,ItemTypeEnum.BAG_STOREEND+1):
			self.statusMessage( csstatus.NPCSHOP_SHOP_NOT_REPAIR_STORE_EQUIP, "" )
			return
		#是否有损耗的装备
		if itemInst.getHardiness() < 0 or itemInst.getHardiness() >= itemInst.getHardinessMax():
			self.statusMessage( csstatus.NPCSHOP_SHOP_NOT_REPAIR,"" )
			return
		oldHardiness = itemInst.getHardiness()
		#获得品质系数
		repairRate = self.getItemQualityCoefficient(itemInst.getQuality())
		#金币是否足够  	修理价格= 品质系数*（1-（实际耐久度/原始最大耐久度））*道具价格
		#cost = repairRate * (1 - float( itemInst.getHardiness())/float(itemInst.getHardinessMax())) * itemInst.getPrice() * tongDiscount * 0.1
		#目前客户端计算花费没有加入折扣
		cost = repairRate * (1 - float( itemInst.getHardiness())/float(itemInst.getHardinessMax())) * itemInst.getPrice()
		if self.isEnoughBindMoney(math.ceil(cost)):
			self.subBindMoney(math.ceil(cost), csdefine.MONEY_SUB_REASON_EQUIP_REPAIR)
		else:
			self.inquireMessage(csstatus.NPCSHOP_COST_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(math.ceil(cost))], "replacePayRepair", shopID, math.ceil(cost), itemUID)
			return

		itemInst.setHardiness( itemInst.getHardinessMax(),self )
		self.statusMessage( csstatus.NPCSHOP_SHOP_REPAIR_SUCCESS,Functions.bindMoneyToStr(math.ceil(cost)) )
		
		#添加日志
		g_logger.equipRepairLog( self.playerDBID, self.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, oldHardiness, itemInst.getHardiness(), math.ceil(cost), self.getCurrentSpaceScriptID(), shopID, itemInst)

	def replacePayRepair(self, reply, shopID, cost, itemUID):
		"""金币代付绑定金币维修"""
		if reply:
			itemInst = self.getItemInstByUid(int(itemUID))
			oldHardiness = itemInst.getHardiness()
			if not self.subMoney(cost, csdefine.MONEY_SUB_REASON_EQUIP_REPAIR):
				self.statusMessage(csstatus.NPCSHOP_SHOP_REPAIR_FAILURE, "")
				return
			itemInst.setHardiness(itemInst.getHardinessMax(), self)
			self.statusMessage(csstatus.NPCSHOP_SHOP_REPAIR_SUCCESS, Functions.moneyToStr(math.ceil(cost)))
			g_logger.equipRepairLog(self.playerDBID, self.getName(), itemInst.id, itemInst.uid,itemInst.getItemDir("ItemName"), itemInst.amount, oldHardiness,itemInst.getHardiness(), math.ceil(cost), self.getCurrentSpaceScriptID(), shopID, itemInst)

	def requestRepairAllEquip( self,roleID,shopID ):
		"""
		<exposed method>
		修理身上所有装备
		"""
		if not self.validateClientCall( roleID ):
			return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			self.statusMessage( csstatus.NPCSHOP_ROLE_DEAD,"" )
			return
		if self.shopID != shopID:
			KBEDebug.ERROR_MSG( "shop id %s != %s"%(self.shopID, shopID) )
			return
		npcShopConfig = g_tradeMgr.getShopTypeConfig(shopID)
		if not npcShopConfig["isCanRepair"]:
			return
			
		tongDiscount = 1
		if npcShopConfig["isTongDisCount"]:
			if self.tongMB:
				tongDiscount = tongBuildFunc[self.tongSmithyLevel]["discount"]
			else:
				KBEDebug.ERROR_MSG( "Player(%s) has not join in tong!"%(self.playerName) )
		
		#self.ShopNPCID为0，表示不是通过NPC打开商店
		if self.ShopNPCID != 0:
			# 验证与NPC的距离
			npc = KBEngine.entities.get( self.ShopNPCID, None )
			if npc == None:
				KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
				return
			if self.position.flatDistTo( npc.position ) > csdefine.NPCSHOP_BUY_DISTANCE:
				KBEDebug.ERROR_MSG( "npc %s distance > 5"%(self.ShopNPCID) )
				return
		equipItemList = self.sortByRepairAllEquip()
		totalCost = 0
		partCost = 0
		repairIndex = 0
		bCounted = False
		for index, equipItem in enumerate(equipItemList):
			if not equipItem.isEquip():
				continue
			itemOrder = self.itemsBag.getOrderID( equipItem.uid )
			if itemOrder in range(ItemTypeEnum.BAG_STORESTART, ItemTypeEnum.BAG_STOREEND+1):
				continue
			#是否有损耗的装备
			if equipItem.getHardiness() < 0 or equipItem.getHardiness() >= equipItem.getHardinessMax():
				continue
			oldHardiness = equipItem.getHardiness()
			#获得品质系数
			repairRate = self.getItemQualityCoefficient(equipItem.getQuality())
			
			#客户端的耐久度显示方式为： "当前值/最大值"，即"math.ceil(float(equipItem.getHardiness())/10000.0)"/"math.ceil(float(equipItem.getHardinessMax())/10000.0)"，如果显示的当前值和显示的最大值相等，则不需要修理
			if math.ceil(float(equipItem.getHardiness())/10000.0) == math.ceil(float(equipItem.getHardinessMax())/10000.0):
				continue
			
			#金币是否足够  	修理价格= 品质系数*（1-（实际耐久度/原始最大耐久度））*道具价格
			#cost = math.ceil( repairRate * (1 - float( equipItem.getHardiness())/float(equipItem.getHardinessMax())) * equipItem.getPrice() * tongDiscount * 0.1 )
			#目前客户端计算花费没有加入折扣
			cost = math.ceil( repairRate * (1 - float( equipItem.getHardiness())/float(equipItem.getHardinessMax())) * equipItem.getPrice() )

			if not self.isEnoughBindMoney(totalCost + cost) and bCounted == False:
				repairIndex = index
				partCost = totalCost
				bCounted = True
			totalCost += cost

		if not bCounted:
			self.subBindMoney(totalCost, csdefine.MONEY_SUB_REASON_EQUIP_REPAIR)
			for equipItem in equipItemList:
				oldHardiness = equipItem.getHardiness()
				equipItem.setHardiness(equipItem.getHardinessMax(), self)
				g_logger.equipRepairLog(self.playerDBID, self.getName(), equipItem.id, equipItem.uid, equipItem.getItemDir("ItemName"), equipItem.amount, oldHardiness, equipItem.getHardiness(), totalCost, self.getCurrentSpaceScriptID(), shopID, equipItem)
			self.statusMessage(csstatus.NPCSHOP_SHOP_REPAIR_SUCCESS, Functions.bindMoneyToStr(totalCost))
		else:
			self.inquireMessage(csstatus.NPCSHOP_COST_MONEY_REPLACE_BIND_MONEY, [Functions.moneyToStr(totalCost)], "replacePayRepairAll",shopID, partCost ,totalCost, repairIndex, equipItemList)

	def replacePayRepairAll(self, reply, shopID,partCost, totalCost, repairIndex, equipItemList):
		"""金币代付绑定金币修复全部装备"""
		if reply:
			if self.subMoney(totalCost, csdefine.MONEY_SUB_REASON_EQUIP_REPAIR):
				for equipItem in equipItemList:
					oldHardiness=equipItem.getHardiness()
					equipItem.setHardiness(equipItem.getHardinessMax(), self)
					g_logger.equipRepairLog(self.playerDBID, self.getName(), equipItem.id, equipItem.uid,equipItem.getItemDir("ItemName"), equipItem.amount, oldHardiness,equipItem.getHardiness(), totalCost, self.getCurrentSpaceScriptID(), shopID, equipItem)
				self.statusMessage(csstatus.NPCSHOP_SHOP_REPAIR_SUCCESS, Functions.moneyToStr(totalCost))
			else:
				if partCost == 0:
					self.statusMessage(csstatus.NPCSHOP_SHOP_REPAIR_FAILURE, "")
					return
				if self.subBindMoney(partCost, csdefine.MONEY_SUB_REASON_EQUIP_REPAIR):
					for equipItem in equipItemList[:repairIndex]:
						oldHardiness = equipItem.getHardiness()
						equipItem.setHardiness(equipItem.getHardinessMax(), self)
						g_logger.equipRepairLog(self.playerDBID, self.getName(), equipItem.id, equipItem.uid,equipItem.getItemDir("ItemName"), equipItem.amount, oldHardiness,equipItem.getHardiness(), totalCost, self.getCurrentSpaceScriptID(), shopID, equipItem)
					self.statusMessage(csstatus.NPCSHOP_SHOP_REPAIR_APART_SUCCESS, Functions.bindMoneyToStr(partCost))
		else:
			if partCost == 0:
				self.statusMessage(csstatus.NPCSHOP_SHOP_REPAIR_FAILURE, "")
				return
			if self.subBindMoney(partCost, csdefine.MONEY_SUB_REASON_EQUIP_REPAIR):
				for equipItem in equipItemList[:repairIndex]:
					oldHardiness = equipItem.getHardiness()
					equipItem.setHardiness(equipItem.getHardinessMax(), self)
					g_logger.equipRepairLog(self.playerDBID, self.getName(), equipItem.id, equipItem.uid,equipItem.getItemDir("ItemName"), equipItem.amount, oldHardiness,equipItem.getHardiness(), totalCost, self.getCurrentSpaceScriptID(), shopID, equipItem)
				self.statusMessage(csstatus.NPCSHOP_SHOP_REPAIR_APART_SUCCESS, Functions.bindMoneyToStr(partCost))

	def sortByRepairAllEquip( self ):
		"""
		全部修理时,对背包中的物品进行一个排序(武器-头盔-衣服-腰带-护腕-手套-裤子-鞋子)
		"""
		equipItemList = []
		itemList = self.getItemListByKBType( ItemTypeEnum.BAG_EQUIP) + self.getItemListByKBType( ItemTypeEnum.BAG_COMMON)
		equipItemList.extend(Functions.filterEquipParts( ( ItemTypeEnum.EQUIP_WEAPON, ),itemList))  #武器
		equipItemList.extend(Functions.filterEquipParts( ( ItemTypeEnum.EQUIP_HAT, ),itemList))     #头盔
		equipItemList.extend(Functions.filterEquipParts( ( ItemTypeEnum.EQUIP_COAT, ),itemList)) 	#衣服
		equipItemList.extend(Functions.filterEquipParts( ( ItemTypeEnum.EQUIP_WAIST, ),itemList))	#腰带
		equipItemList.extend(Functions.filterEquipParts( ( ItemTypeEnum.EQUIP_WRIST, ),itemList))   #护腕
		equipItemList.extend(Functions.filterEquipParts( ( ItemTypeEnum.EQUIP_SUIT, ),itemList))	#手套
		equipItemList.extend(Functions.filterEquipParts( ( ItemTypeEnum.EQUIP_PANTS, ),itemList))	#裤子
		equipItemList.extend(Functions.filterEquipParts( ( ItemTypeEnum.EQUIP_SHOES, ),itemList))	#鞋子
		return equipItemList

	def getItemQualityCoefficient( self, quality ):
		"""
		获得品质系数
		"""
		if quality == ItemTypeEnum.QUALITY_WHITE:
			return 0.5
		if quality == ItemTypeEnum.QUALITY_BLUE:
			return 1
		if quality == ItemTypeEnum.QUALITY_GOLD:
			return 2
		if quality == ItemTypeEnum.QUALITY_PINK:
			return 3
		if quality in [ItemTypeEnum.QUALITY_GREEN, ItemTypeEnum.QUALITY_GREEN_TIAN, ItemTypeEnum.QUALITY_GREEN_SHENG, ItemTypeEnum.QUALITY_GREEN_SHEN]:
			return 4		

#---------------------------帮会商店---------------------------------------
	def requestTongShopItemList( self, srcEntityID, NPCID, shopID ):
		"""
		exposed method
		打开帮会商店
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.tongMB is None:return
		
		self.ShopNPCID = NPCID
		self.shopID = shopID
		# 如果有动态数据，就到base上读取！否则读取客户端数据
		if g_tradeMgr.hasLimitItem( shopID ):
			KBEngine.globalData["ShopManager"].requestTongShopItemList( shopID, self, self.playerDBID, self.tongMB.id )
		else:
			self.client.CLIENT_InitNPCShopItemList( NPCID, shopID, None )
		
	def tongShopItemListCallBack( self, shopID, shopItems ):
		"""
		define method
		帮会商店 请求商店列表回调
		"""
		self.recordBuyLimitOfItemList( shopID,shopItems )
		self.client.CLIENT_OnRequestTongShop( self.ShopNPCID, shopID, shopItems.getString() )


#------------------------英雄王座 商店-------------------------------------
	def addJade( self, value ):
		"""
		"""
		self.jade += value
		
	def openTraviaShop( self, NPCID ):
		"""打开英雄王座商店"""
		npc = KBEngine.entities.get( NPCID, None )
		if npc == None:
			KBEDebug.ERROR_MSG( "no npc %s"%(NPCID) )
			return
		self.ShopNPCID = NPCID
		
		guardInfo = npc.getGuardInfo( self )
		pagodaInfos = npc.getPagodaInfos( self )
		drugInfo = g_tradeMgr.getDrugInfo()

		self.client.CLIENT_OpenTraviaShop( NPCID, guardInfo, pagodaInfos, drugInfo )
		
	def CELL_requestBuyCombatSoulItem( self, srcEntityID, itemID ):
		"""
		exposed method
		购买战魂
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		soulInfo = g_tradeMgr.getCombatSoulInfo( itemID )
		if soulInfo:
			if self.jade < soulInfo["BuyPrice"]:
				KBEDebug.ERROR_MSG("Not enough HunYu(need:%d,has:%d)"%(soulInfo["BuyPrice"],self.jade))
				return
			itemList = self.getItemInstsByID( itemID )
			if itemList:
				KBEDebug.ERROR_MSG("Has item(%d) already!"%itemID)
				return
			
			preItemID = soulInfo["PreItemID"]
			if preItemID:
				itemInstList = self.getItemInstsByID( int(preItemID) )
				if itemInstList:
					self.removeItemByAmount(itemInstList[0], 1, csdefine.ITEM_REMOVE_BY_SELL_TO_NPC)
#					self.itemsBag.removeByOrder( itemInstList[0].order )
#					self.client.CLIENT_removeItem(itemInstList[0].order)
					preSoulInfo = g_tradeMgr.getCombatSoulInfo( str(preItemID ))
					self.removeBuffByID( preSoulInfo["BuffID"] )
				else:
					KBEDebug.ERROR_MSG("Buy combatSoul item err!cannot find item(%d)"%preItemID)
					return
			
			result, _ = self.addItemByID( int(itemID), 1, csdefine.ITEM_ADD_BY_NPCTRADE)
			if result == csstatus.ITEM_GO_ON:
				self.jade -= soulInfo["BuyPrice"]
				self.addBuff( self, soulInfo["BuffID"] )
				self.client.CLIENT_OnRequestBuyCombatSoulItem( itemID, str(soulInfo["NextItemID"]) )
				self.statusMessage( csstatus.NPCSHOP_ROLE_BUY_SUCCESS, "" )
			else:
				self.statusMessage( result, "" )
	
	def CELL_requestSellCombatSoulItem( self, srcEntityID, itemID ):
		"""
		exposed method
		出售战魂
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		sellSoulInfo = g_tradeMgr.getCombatSoulInfo( itemID )
		itemInstList = self.getItemInstsByID( int(itemID ))
		if itemInstList:
			self.removeItemByAmount( itemInstList[0], 1, csdefine.ITEM_REMOVE_BY_SELL )
			self.removeBuffByID( sellSoulInfo["BuffID"] )
		else:
			KBEDebug.ERROR_MSG("Sell combatSoul item err!cannot find item(%ss)"%itemID)
			return
		self.jade += sellSoulInfo["SellPrice"]
		self.client.CLIENT_OnRequestSellCombatSoulItem( itemID )
			
	def CELL_requestBuyGuardSoul( self, srcEntityID, scriptID, type ):
		"""
		exposed method
		召唤魂卫
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		npc = KBEngine.entities.get( self.ShopNPCID, None )
		if npc == None:
			KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
			return
		guardInfo = g_tradeMgr.getGuardSoulInfo( scriptID )
		cTime = 0
		if guardInfo["maxBuyTime"] > 0:
			cTime = npc.getGuardCallTime( self, scriptID )
			if cTime >= guardInfo["maxBuyTime"]:				# 已经无法再召唤
				self.client.CLIENT_OnRequestBuyGuardSoul(cTime, scriptID )
				return
		space = self.getCurrentSpace()
		passTime = int( (time.time() - space.lifeStartTime)/60 )
		level = g_tradeMgr.getGuardLevelsByTime( scriptID, passTime )
		price = 0
		for prices in guardInfo["buyPrice"].split("|"):
			ltep, ptep = prices.split(":")
			if level == int(ltep):
				price = int(ptep)
				break
		if price == 0:
			KBEDebug.ERROR_MSG( "Guard call max(%d) time %s"%(cTime) )
			return
		
		if self.jade < price:
			KBEDebug.ERROR_MSG("Not enough HunYu(need:%d,has:%d)"%(price,self.jade))
			return
		self.jade -= price
		self.getCurrentSpace().createMonsterByShop( self, scriptID, type, { "levelYXLM": level })
		npc.onCallGuard( self, scriptID )
		if cTime > 0:
			cTime += 1
		self.client.CLIENT_OnRequestBuyGuardSoul(cTime, scriptID )
		
	def CELL_requestUpdatePagodaSoul( self, srcEntityID, srcScriptID, dstScriptID, wayType ):
		"""
		exposed method
		升级魂塔
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		npc = KBEngine.entities.get( self.ShopNPCID, None )
		if npc == None:
			KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
			return
		space = self.getCurrentSpace()
		if space is None:
			return
		
		if not npc.canUpdateGradePagoda( self, srcScriptID, dstScriptID, wayType ):
			return
		
		price = g_tradeMgr.getPriceByPagodaID( dstScriptID, wayType )
		if price == -1:
			KBEDebug.ERROR_MSG("Get pagoda(%s) price ere!"%dstScriptID)
			return
		if self.jade < price:
			KBEDebug.ERROR_MSG("Not enough HunYu(need:%d,has:%d)"%(price,self.jade))
			return
		self.jade -= price
		self.getCurrentSpace().updateGradeBuilding( srcScriptID, dstScriptID, int(wayType) )
		npc.onUpdateGradePagoda( self, srcScriptID, dstScriptID, wayType )
		self.client.CLIENT_OnRequestUpdatePagodaSoul( srcScriptID, dstScriptID, wayType )
		
	def CELL_requestBuyDrugSoulItem( self, srcEntityID, itemID ):
		"""
		exposed method
		购买 药品
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		npc = KBEngine.entities.get( self.ShopNPCID, None )
		if npc == None:
			KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
			return
		shopData = g_tradeMgr.getDrugInfoByItemID( str(itemID ))
		if shopData is None:
			KBEDebug.ERROR_MSG("Can not find itemID(%s) in config DrugSoulShop.json"%itemID)
			return
		price = shopData["buyPrice"]
		if self.jade < price:
			KBEDebug.ERROR_MSG("Not enough HunYu(need:%d,has:%d)"%(price,self.jade))
			return
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, 1, {})
		if itemInst is None:
			return
		result = self.addItemListCheck([itemInst])
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(result)
			return
		self.jade -= price
		self.addItem(itemInst, csdefine.ITEM_ADD_BY_NPCTRADE)
		
	def CELL_requestSellDrugSoulItem( self, srcEntityID, itemID ):
		"""
		exposed method
		出售 药品
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		npc = KBEngine.entities.get( self.ShopNPCID, None )
		if npc == None:
			KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
			return
		shopData = g_tradeMgr.getDrugInfoByItemID( str(itemID ))
		if shopData is None:
			KBEDebug.ERROR_MSG("Can not find itemID(%s) in config DrugSoulShop.json"%itemID)
			return
		price = shopData["sellPrice"]
		itemInstList = self.getItemInstsByID( int(itemID ))
		if itemInstList:
			self.removeItemByAmount(itemInstList[0], 1, csdefine.ITEM_REMOVE_BY_SELL )
			self.jade += price
	
	def openLMNeuralShop( self, NPCID, scriptIDs, times, level ):
		"""打开中立商店"""
		self.ShopNPCID = NPCID
		self.client.CLIENT_openLMNeuralShop( NPCID, scriptIDs, times, level )
	
	def CELL_requestBuyNeuralGuard( self, srcEntityID, scriptID, type ):
		"""
		exposed method
		中立商店 召唤魂卫
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		npc = KBEngine.entities.get( self.ShopNPCID, None )
		if npc == None:
			KBEDebug.ERROR_MSG( "no npc %s"%(self.ShopNPCID) )
			return
		if not npc.canCallMonster( scriptID ):
			self.client.CLIENT_OnBuyNeuralGuard( scriptID )			# 已经被召唤
			return
		guardInfo = g_tradeMgr.getNeuralGuardSoulInfo( scriptID )
		space = self.getCurrentSpace()
		passTime = int( (time.time() - space.lifeStartTime)/60 )
		level = g_tradeMgr.getNeuralGuardLevelsByTime( scriptID, passTime )
		price = 0
		for prices in guardInfo["buyPrice"].split("|"):
			ltep, ptep = prices.split(":")
			if level == int(ltep):
				price = int(ptep)
				break
		if price == 0:
			KBEDebug.ERROR_MSG( "Guard call max(%d) time %s"%(cTime) )
			return
		
		if self.jade < price:
			KBEDebug.ERROR_MSG("Not enough HunYu(need:%d,has:%d)"%(price,self.jade))
			return
		self.jade -= price
		self.getCurrentSpace().createMonsterByShop( self, scriptID, type, { "levelYXLM": level })
		npc.onCallMonster( scriptID )
		self.client.CLIENT_OnBuyNeuralGuard( scriptID )
		
	#------------------------------------------- 神秘商人 -----------------------------------------------
	def requestBuyMysteriousShopItem( self, npcID, slotID, id, amount ):
		"""
		从神秘商人处购买商品,从NPC处过来
		"""
		shopConfig = g_tradeMgr.getMysteriousMerchantConfig()
		item = shopConfig.get(slotID, {}).get(id, None)
		if item is None: return
		
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(item["itemID"], amount)
		if itemInst is None:
			KBEDebug.ERROR_MSG("err!!item(%d) not find!"%item["itemID"])
			return
		
		result = self.addItemCheck(itemInst)
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(result)
			return
		
		#计算总金额
		payItems = dict(item["price"])
		for key, value in payItems.items():
			payItems[key] = value * amount
		
		self.requestPay(csdefine.TRADE_TYPE_MYSTERIOUS_SHOP, npcID, payItems, npcID, slotID, id, amount)
			
	def onSuccessPayMysteriousShopItem( self, npcID, slotID, id, amount ):
		"""
		"""
		shopConfig = g_tradeMgr.getMysteriousMerchantConfig()
		item = shopConfig.get(slotID).get(id)
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(item["itemID"], amount)
		self.addItem( itemInst,csdefine.ITEM_ADD_BY_NPCTRADE )
		self.statusMessage( csstatus.NPCSHOP_ROLE_BUY_SUCCESS, "" )
		
		shopEntity = KBEngine.entities.get(npcID)
		if shopEntity:
			shopEntity.onSuccessBuyShopItem(self.id, slotID, amount)
			
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			messageArg = "{}|神秘商人|{}".format(self.getName(), itemInst.getItemDir("ItemName"))
			spaceEntity.globalWorld(csstatus.ITEM_ADD_BUY_JIYUAN, messageArg)
		
		if self.getClient():
			self.client.CLIENT_PlaySound(Const.SHENGJIE_ITEM_GET_SOUND)
			self.client.CLIENT_PlayEffect(Const.SHENGJIE_ITEM_GET_EFFECTID)
	
#-----------------------------CST-12032 帮会掠夺战------------------------------------------------------
	def lockTongShop(self):
		"""
		define method
		锁定帮会商店
		"""
		self.isLockTongShop = True
		self.client.CLIENT_LockTongShop()
		
	def unLockTongShop(self):
		"""
		define method
		解锁帮会商店
		"""
		self.isLockTongShop = False
		self.client.CLIENT_UnLockTongShop()
		
	def hasLockTongShop(self):
		"""
		"""
		return self.isLockTongShop
		
	def onTongPlunderShopSellStart(self, tongPlunderShopData, endTime):
		"""
		define method
		帮会掠夺战所获商品售卖开始
		"""
		self.tongPlunderShopSellStart = True
		self.client.OnTongPlunderShopSellStart(tongPlunderShopData, endTime)
		
	def onTongPlunderShopSellEnd(self):
		"""
		define method
		帮会掠夺战所获商品售卖结束
		"""
		self.tongPlunderShopSellStart = False
		self.client.CLIENT_TongPlunderShopSellEnd()
		
	def hastartTongPlunderShopSell(self):
		"""
		"""
		return self.tongPlunderShopSellStart
