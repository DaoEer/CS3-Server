# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import csstatus
import time
import Const
import random
from ConfigObject.Shop.ShopMgr import g_shopMgr

class RoleLunHuiMiJinInterface:
	"""
	玩家轮回秘境接口
	"""
	def __init__( self ):
		self.shopID = ""					# 商店ID
#		self.autoReflashLHMJShopTime = 0			# 商品刷新时间
#		self.lhmjShopDatas = {}				# 轮回秘境商品

	def requestLHMJShop( self, NPCID, shopID ):
		"""
		<define method>
		请求轮回秘境商店数据
		"""
		self.shopID = shopID
		if time.time() - self.autoReflashLHMJShopTime >= Const.LHMJ_SHOP_REFLASH_TIME:
			self.autoReflashLHMJShopTime = time.time()
			self.reflashfLHMJShop()
		self.client.CLIENT_InitLHMJShopData( NPCID, shopID, self.lhmjShopDatas )
			
	def reflashfLHMJShop( self ):
		"""刷新轮回秘境物品"""
		self.lhmjShopDatas.clear()
		shopItems = g_shopMgr.getShopConfig(self.shopID)
		randNum = min( Const.LHMJ_SHOP_REFLASH_NUM, len(shopItems))
		randList = random.sample(list(shopItems), randNum)
		for index in randList:
			item = shopItems[index]
			self.lhmjShopDatas[item["id"]] = {"id":item["id"], "itemID" : item["itemID"], "amount" : item["buyLimit"] }
			
	def requestReflashLHMJShop(self):
		"""
		<define method>
		玩家请求刷新
		"""
		self.reflashfLHMJShop()
		self.client.CLIENT_reflashLHMJShopData( self.lhmjShopDatas )
		
	def BASE_autoReflashLHMJShop(self):
		"""
		<exposed method>
		自动刷新
		"""
		if time.time() - self.autoReflashLHMJShopTime >= Const.LHMJ_SHOP_REFLASH_TIME:
			self.autoReflashLHMJShopTime = time.time()
			self.reflashfLHMJShop()
		self.client.CLIENT_autoReflashLHMJShopData(self.lhmjShopDatas )
		
	def checkItemNum(self, slot, num):
		"""检查物品数量"""
		if not slot in self.lhmjShopDatas:
			KBEDebug.ERROR_MSG("Can not find slot(%s) in LHMJ Shop!"%slot)
			return False
		if self.lhmjShopDatas[slot]["amount"] >= num:
			return True
		return False
		
	def reduceLHMJItem(self, slot, num):
		"""减少物品数量"""
		self.lhmjShopDatas[slot]["amount"] -= num