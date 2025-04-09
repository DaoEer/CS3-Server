# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine
import time, random
from CoreObject import MgrPersistentObject
from ConfigObject.Shop.ShopMgr import g_shopMgr
from NPCShopItemListImpl import NPCShopItemListImpl
from Functions import Functor
import copy
import csstatus
import csconst
from ConfigObject.Crond.CrondDatas import CrondDatas

g_CrondDatas = CrondDatas.instance()
RANDOM_ITEM_REFRESH_TIME = 40 * 60	#刷新时间间隔

class ShopManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	商店管理类
	"""
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.shareItems.initConfig()					# {shopID: [{"id":slotID, "amount":amount, "startTime":time}] }
		self.limitItems.initConfig()					# {playerDbid: {shopID : [{"id":slotID, "amount":amount, "startTime":time}] } }
		self.randomLimitItems.initConfig()				# {shopID: [{"id":slotID, "amount":amount, "startTime":time}] }
		self.onCompleteInit()
	
	def reload(self):
		"""
		<Define method>
		"""
		self.shareItems.initConfig()
		self.limitItems.initConfig()
		self.randomLimitItems.initConfig()
		
	def requestShopLimitItemList(self, shopID, role, roleDBID):
		"""
		<defined method>
		通过商店id查找到商店
		"""
		shareItem, limitItem = g_shopMgr.getLimitAndShareConfig(shopID)
		items = NPCShopItemListImpl()
		if shareItem:
			items.update( self.shareItems.getLimitItem( shopID, shareItem ) )
		if limitItem:
			items.update(self.limitItems.getLimitItem( roleDBID, shopID, limitItem ))
		
		if g_shopMgr.getRandomItems( shopID ):
			randomItems = self.randomLimitItems.getRandItem( shopID )
			if len(randomItems):
				items.update( randomItems )
				if role and hasattr(role, "client"):
					endTime = int(list(randomItems.values())[0]["startTime"] + csconst.RANDOM_REFLASH_TIME_LAST)
					role.client.onNotifyRandomItemSellEndTime(shopID, endTime)
		
		role.onRequestShopLimitItemList( shopID, items )

	def buyLimintItem( self, shopID, slot, amount, role, roleDBID ):
		"""
		<defined method>
		购买有上限的物品
		"""
		if g_shopMgr.isRandomLimitShareItem(shopID, slot):
			if not self.randomLimitItems.reduceItem(shopID, slot, amount):
				role.statusMessage(csstatus.NPCSHOP_CANNOT_BUY_LIMIT,"")
				return
		elif g_shopMgr.isSharedItem(shopID, slot):
			if not self.shareItems.reduceItem(shopID, slot, amount):
				role.statusMessage(csstatus.NPCSHOP_CANNOT_BUY_LIMIT,"")
				return
		else:
			if not self.limitItems.reduceItem(roleDBID, shopID, slot, amount):
				role.statusMessage(csstatus.NPCSHOP_CANNOT_BUY_LIMIT,"")
				return
		
		role.onBuyLimintItem(shopID, slot, amount)
	
	def returnBuyItem( self, shopID, slot, itemID, amount, roleDBID ):
		"""
		<defined method>
		购买失败，退回物品给商店
		"""
		if g_shopMgr.isRandomLimitShareItem(shopID, slot):
			self.randomLimitItems.returnBuyItem(shopID, slot, amount)
		elif g_shopMgr.isSharedItem(shopID, slot):
			self.shareItems.returnBuyItem(shopID, slot, amount)
		else:
			self.limitItems.returnBuyItem(roleDBID, shopID, slot, amount)

	#-----------------------------帮会商店--------------------------------------------
	def requestTongShopItemList( self, shopID, role, roleDBID, tongID ):
		"""
		defined method
		请求帮会商店物品
		"""
		shareItem, limitItem = g_shopMgr.getLimitAndShareConfig(shopID)
		items = NPCShopItemListImpl()
		if shareItem:
			items.update(self.shareItems.getLimitItem( shopID, shareItem ))
		if limitItem:
			items.update(self.limitItems.getLimitItem( roleDBID, shopID, limitItem ))
		
		#随机限量商品
		if g_shopMgr.getRandomItems( shopID ):
			randomItems = self.randomLimitItems.getRandItem( shopID )
			if len(randomItems):
				items.update( randomItems )
				if role and hasattr(role, "client"):
					endTime = int(list(randomItems.values())["startTime"] + csconst.RANDOM_REFLASH_TIME_LAST)
					role.client.onNotifyRandomItemSellEndTime(shopID, endTime)
			
		# 计算幻兽技能书
#		tong = KBEngine.entities[tongID]					# 因为两个管理器在同一个base，所以可以获得
#		rItems = tong.getResearchMappingItems()
#		skillItems = g_shopMgr.getTongSkillItems( shopID )
#		for itemID in skillItems:
#			if not itemID in rItems:						# 说明帮会还没研发成功
#				for itemData in items.values():
#					if itemData["itemID"] == itemID:
#						itemData["amount"] = 0
#						continue
		role.onRequestShopLimitItemList( shopID, items )
		
		
	#------------------------------GM命令----------------------------------------------
	def GM_openRandomShop( self ):
		"""
		开启随机商店
		"""
		curTime = time.time()
		shopIDList = g_shopMgr.getRandomLimitShopIDs()
		for shopID in shopIDList:
			self.randomLimitItems.GM_generalRandomItems( shopID, curTime )
