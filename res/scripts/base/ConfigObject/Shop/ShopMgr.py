# -*- coding: utf-8 -*-
import random, time
import datetime
import KBEngine
import KBEDebug
import csdefine
import csconst
from Singleton import Singleton
from ConfigObject.Shop.ShopRefreshType.ShopRefreshWeek import ShopRefreshWeek
from ConfigObject.Shop.ShopRefreshType.ShopRefreshDay import ShopRefreshDay
from ConfigObject.Shop.ShopRefreshType.ShopRefreshSellOut import ShopRefreshSellOut
from ConfigObject.Shop.ShopRefreshType.ShopRefreshTime import ShopRefreshTime

class ShopMgr( Singleton ):
	"""
	商店处理类
	"""
	def __init__( self ):
		self.mapping = {}						# { "shopID" : [ {shopData},{shopData}] }
		self.shopTypeMapping = {}				# 商店属性表
		self.randomLimitMapping = {}			# 随机限量商品
		self.refreshMap = {
			csdefine.NPCSHOP_ITEM_REFRESH_WEEK		: ShopRefreshWeek(),
			csdefine.NPCSHOP_ITEM_REFRESH_DAY		: ShopRefreshDay(),
			csdefine.NPCSHOP_ITEM_REFRESH_SELLOUT	: ShopRefreshSellOut(),
			csdefine.NPCSHOP_ITEM_REFRESH_TIME		: ShopRefreshTime(),
		}

	def init( self, configPath1, configPath2, configPath3 ):
		"""
		配置加载
		@param configPath1: 商店物品配置表
		@type  configPath1: DICT
		@param configPath2: 随机限量商品配置表
		@type  configPath2: DICT
		@return: 一个声明了的方法，没有返回值
		"""
		for key,value in configPath1.items():
			self.mapping[key] = value
		
		for key, value in configPath2.items():
			self.randomLimitMapping[key] = value
		
		for key, value in configPath3.items():
			self.shopTypeMapping[key] = value
		
	def getAll( self ):
		return self.mapping
		
	def getShopConfig(self, shopID):
		"""获取商店的配置"""
		return self.mapping.get(shopID, {})
		
	def getRandomLimitShopIDs(self):
		"""
		"""
		return list(self.randomLimitMapping.keys())
		
	def getShopTypeConfig( self,shopID ):
		"""
		获得某商店配置
		"""
		return self.shopTypeMapping.get(shopID, None)

	def getLimitAndShareConfig( self, id ):
		"""
		给予配置
		@param id: 商店ID
		@type  id: INT32
		@return: 返回商店上限、共享物品
		"""
		shareItem = {}
		limitItem = {}
		if id in self.mapping:
			for shopData, item in self.mapping[id].items():
				if item["buyLimit"] > 0:
					if item["isShared"]:
						shareItem.update({shopData:item})
					else:
						limitItem.update({shopData:item})
		else:
			KBEDebug.ERROR_MSG("requestShopItemList::request shop id %s is error"%(id))
		return shareItem, limitItem
		
	def isRandomLimitShareItem(self, shopID, slot):
		"""是否是随机限量物品"""
		if shopID in self.randomLimitMapping and slot in self.randomLimitMapping[shopID]:
			return True
		return False
		
	def isSharedItem(self, shopID, slot):
		"""是否是 共享物品"""
		if shopID in self.mapping and slot in self.mapping[shopID]:
			return self.mapping[shopID][slot]["isShared"]
		return False
	
	def onGet( self, shopID, shopItems ):
		"""
		获得物品数量处理
		"""
		shopData = self.mapping.get( shopID, None )
		if shopData:
			for slot, shopItem in shopItems.items():
				if not slot in shopData:
					continue
					
				refreshType = shopData[slot]["refreshType"]
				if not refreshType in self.refreshMap:
					KBEDebug.ERROR_MSG("Cannot find refreshType(%s, %s, %d)"%(shopID, slot, refreshType))
					return False
				
				c = self.refreshMap[refreshType]
				c.onGet( shopData[slot], shopItem, {} )
	
	def onSell( self, shop, slot, item ):
		"""
		出售物品后处理
		@param shop: 商店Entity
		@type  shop: Entity
		@param slot: 商店物品id
		@type  slot: INT32
		"""
		if item == None:
			#商店没有这个物品
			KBEDebug.ERROR_MSG( "addItemRefreshTimer:: no item %s"%(slot) )
			return False
		config = shop.getItemConfig( slot )
		if config == None:
			#没有这个物品的配置
			KBEDebug.ERROR_MSG( "addItemRefreshTimer:: no %s item config"%(slot) )
			return False
		
		if not config["refreshType"] in self.refreshMap:
			#类型错误
			return False

		c = self.refreshMap[config["refreshType"]]
		return c.onSell( shop, slot, item )
		
	def getTongSkillItems( self, shopID ):
		"""获取帮会 幻兽技能书"""
		skillList = []
		if shopID in self.mapping:
			for shopItem in self.mapping[shopID]:
				if "paging" in shopItem:
					if shopItem["paging"] == 3:
						skillList.append(  shopItem["itemID"])
				else:
					KBEDebug.ERROR_MSG("Get shop(%s) tong skill err!!"%shopID)
		return skillList
		
	def getRandomItems( self, shopID ):
		"""商店 有随机物品"""
		return self.randomLimitMapping.get( shopID, {} )
		

g_shopMgr = ShopMgr()