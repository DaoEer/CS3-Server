# -*- coding: utf-8 -*-
import time, random

import KBEngine
from KBEDebug import *

from PlayerAI.Base.AIBase import AIBase
from Extra.StoreConfigLoader import g_storeCfgLoader

class ShopAI( AIBase ):
	"""
	商城AI
	"""
	def __init__(self):
		AIBase.__init__(self)
		self.hasReqOpenStore = False
		self.hasReqGetGoodList = False
		self.hasReqLimitGoods = False
		self.hasReqBuyGoods = False
		self.hasReqBuyRecord = False
		self.hasReqDeleteBuyRecord = False
		self.hasReqBuyStoreCartGoods = False
		self.hasReqDelGiftBoxRecord = False
		
		self.hasReqOpenGiftBox = False
		self.hasReqAcceptGift = False
	
	def reset(self):
		"""
		"""
		self.hasReqOpenStore = False
		self.hasReqGetGoodList = False
		self.hasReqLimitGoods = False
		self.hasReqBuyGoods = False
		self.hasReqBuyRecord = False
		self.hasReqDeleteBuyRecord = False
		self.hasReqBuyStoreCartGoods = False
		self.hasReqOpenGiftBox = False
		self.hasReqAcceptGift = False
		self.hasReqDelGiftBoxRecord = False
		
	def onEnterWorld( self ):
		"""
		"""
		self.owner.eventObj.registerEvent("Event_OnxianshiChanged", self)
		self.owner.eventObj.registerEvent("Event_OnlingshiChanged", self)
		self.owner.eventObj.registerEvent("Event_OnxuanshiChanged", self)
		self.owner.eventObj.registerEvent("Event_OnMoneyChanged", self)
		self.owner.eventObj.registerEvent("Event_CItemAISys_onAddItem", self)
		
	def onLeaveWorld( self ):
		"""
		"""
		self.owner.eventObj.unregisterEvent("Event_OnxianshiChanged", self)
		self.owner.eventObj.unregisterEvent("Event_OnlingshiChanged", self)
		self.owner.eventObj.unregisterEvent("Event_OnxuanshiChanged", self)
		self.owner.eventObj.unregisterEvent("Event_OnMoneyChanged", self)
		self.owner.eventObj.unregisterEvent("Event_CItemAISys_onAddItem", self)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		self.onMoneyChanged(0)
		self.onXianShiChanged(0)
		self.onLingShiChanged(0)
		self.onXuanShiChanged(0)
		
		self.think()
		
	def think(self):
		"""
		"""
		t = int(time.time())
		if not self.hasReqOpenStore:
			self.hasReqOpenStore = True
			typeLst = g_storeCfgLoader.getAllType()
			for type in typeLst:
				self.owner.base.requestOpenStoreUI(type[0], type[1], str(t))
			KBEngine.callback(5, self.think)
			self.owner.outputMsg("openStoreUI")
			return
			
		#通过ID列表获取商品列表
		if not self.hasReqGetGoodList:
			self.hasReqGetGoodList = True
			goodsIDList = list(self.owner.storeMapping.keys())
			self.owner.base.getGoodsListByIDList(goodsIDList)
			KBEngine.callback(5, self.think)
			self.owner.outputMsg("getGoodsList")
			return
		
		#查询数量限制
		if not self.hasReqLimitGoods:
			self.hasReqLimitGoods = True
			self.owner.base.requestStoreLimitGoodsList()
			KBEngine.callback(5, self.think)
			self.owner.outputMsg("requestStoreLimitGoodsList")
			return
			
		#购买商品
		if not self.hasReqBuyGoods:
			self.hasReqBuyGoods = True
			goodsIDs = random.sample(list(self.owner.storeMapping.keys()), 5 if len(self.owner.storeMapping) > 5 else len(self.owner.storeMapping))
			for goodsID in goodsIDs:
				self.owner.base.requestBuyStoreGoods(goodsID, 1)
			KBEngine.callback(5, self.think)
			self.owner.outputMsg("requestBuyStoreGoods")
			return
		
		#获取购买记录
		if not self.hasReqBuyRecord:
			self.hasReqBuyRecord = True
			self.owner.base.queryBuyRecords()
			KBEngine.callback(5, self.think)
			self.owner.outputMsg("queryBuyRecords")
			return
			
		#批量购买商品
		if not self.hasReqBuyStoreCartGoods:
			self.hasReqBuyStoreCartGoods = True
			goods = []
			amount = []
			goodsIDs = random.sample(list(self.owner.storeMapping.keys()), 5 if len(self.owner.storeMapping) > 5 else len(self.owner.storeMapping))
			for goodsID in goodsIDs:
				goods.append(goodsID)
				amount.append(10)
			self.owner.base.buyStoreCartGoods(goods, amount)
			KBEngine.callback(5, self.think)
			self.owner.outputMsg("buyStoreCartGoods")
			return
			
		#删除购买记录
		if not self.hasReqDeleteBuyRecord:
			self.hasReqDeleteBuyRecord = True
			if random.choice([True, False]):
				self.owner.base.deleteBuyRecords()	#一次性清空
			else:	
				for uid in self.owner.buyRecords:	#一个个删除
					self.owner.base.deleteBuyRecord(uid)
					
			KBEngine.callback(5, self.think)
			self.owner.outputMsg("deleteBuyRecord")
			return
		
		#打开礼品盒
		if not self.hasReqOpenGiftBox:
			self.hasReqOpenGiftBox = True
			self.owner.base.requestOpenGiftBox()
			KBEngine.callback(5, self.think)
			self.owner.outputMsg("requestOpenGiftBox")
			return
		
		#接受礼物
		if not self.hasReqAcceptGift:
			self.hasReqAcceptGift = True
			if random.choice([True, False]):
				recvGiftList = random.sample(list(self.owner.recvGiftList.keys()), 5 if len(self.owner.recvGiftList) > 5 else len(self.owner.recvGiftList))
				for uid in recvGiftList:		#一个个接受礼物
					self.owner.base.acceptGift(uid)
			else:
				self.owner.base.acceptGifts()			#接受全部礼物
				
			KBEngine.callback(5, self.think)
			self.owner.outputMsg("acceptGifts")
			return
			
		#清空收礼记录
		if not self.hasReqDelGiftBoxRecord:
			self.hasReqDelGiftBoxRecord = True
			self.owner.base.deleteGiftBoxReceiveRecords()
			KBEngine.callback(5, self.think)
			self.owner.outputMsg("deleteGiftBoxReceiveRecords")
			return
		
		self.reset()
		KBEngine.callback(5, self.think)
	
	def onAddItem(self, itemOrder):
		"""
		"""
		#有一种格子被占用了60%以上 就直接清理背包
		if len(self.owner.equipBag) / self.owner.crystalCapacity >= 0.6 or len(self.owner.commonBag) / self.owner.commonCapacity >= 0.6 or  len(self.owner.questBag) / self.owner.questCapacity >= 0.6:
			self.owner.GMCommand(self.owner, "clearBag")
			
	def onXianShiChanged(self, xianshi):
		"""
		"""
		if self.owner.xianshi <= 500:
			self.owner.GMCommand(self.owner, "setXianShi", str(10000))
			
	def onLingShiChanged(self, lingshi):
		"""
		"""
		if self.owner.lingshi <= 500:
			self.owner.GMCommand(self.owner, "setLingShi", str(10000)) 
		
	def onXuanShiChanged(self, xuanshi):
		"""
		"""
		if self.owner.xuanshi <= 500:
			self.owner.GMCommand(self.owner, "setXuanShi", str(10000))
			
	def onMoneyChanged(self, money):
		"""
		"""
		if self.owner.money < 10000:
			self.owner.GMCommand(self.owner, "setMoney", str(1000000))
	
AIBase.setClass("ShopAI", ShopAI)		
	