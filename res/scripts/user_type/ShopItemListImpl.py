# -*- coding: utf-8 -*-
import KBEDebug
import json
import KBEngine
import time
import datetime
import random
import csdefine
import csconst
if KBEngine.component == "baseapp":
	from ConfigObject.Shop.ShopMgr import g_shopMgr


class ShopShareItems( dict ):
	"""
	"""
	def __init__( self ):
		self.shopID = ""
		self.shopItems = {}
		
	def initConfig( self, shopItemDatas, isShared ):
		"""纠正配置表的修改"""
		for slot in list(self.shopItems.keys()):
			if slot in shopItemDatas:
				if self[slot]["isShared"] == isShared and shopItemDatas[slot]["buyLimit"] > 0:
					continue
				self.remove(slot)
		
	def getLimitItem(self, shopData):
		"""获取上限物品"""
		if self.shopItems:
			g_shopMgr.onGet( self.shopID, self.shopItems)
		else:
			for slot, shopItem in shopData.items():
				self.shopItems[slot] = {"id" : shopItem["id"], "amount" : shopItem["buyLimit"], "startTime":time.mktime(datetime.date.today().timetuple())}
				
		return self.shopItems
		
	def reduceItem(self, slot, amount):
		""""""
		if slot in self.shopItems:
			if self.shopItems[slot]["amount"] >= amount:
				self.shopItems[slot]["amount"] -= amount
				return True
		return False
		
	def returnBuyItem(self, slot, amount):
		""""""
		if slot in self.shopItems:
			self.shopItems[slot]["amount"] += amount
		return False
		
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		data = {}
		data["shopID"] = self.shopID
		data["shareItems"] = []
		for items in obj.values():
			data["shareItems"].append( items )
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = self.__class__()
		obj.shopID = dict["shopID"]
		for item in dict["shareItems"]:
			obj.shopItems.update( item )
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return True
		return isinstance( obj, ShopShareItems )

class ShopShareItemList( dict ):
	"""
	"""
	def initConfig( self, isShared = True ):
		"""纠正配置表的修改"""
		oldShopIDList = list(self.keys())
		shopData = g_shopMgr.getAll()
		for shopID, shopItemDatas in shopData.items():
			if shopID in oldShopIDList:
				oldShopIDList.remove(shopID)
				self[shopID].initConfig( shopItemDatas, isShared )
			
		for shopID in oldShopIDList:
			self.pop( shopID )
	
	def getLimitItem(self, shopID, shopData):
		"""获取上限物品"""
		if not shopID in self:
			obj = ShopShareItems()
			obj.shopID = shopID
			self[shopID] = obj
		return self[shopID].getLimitItem(shopData)
	
	def reduceItem(self, shopID, slot, amount):
		""""""
		if shopID in self:
			return self[shopID].reduceItem(slot, amount)
		return False
		
	def returnBuyItem(self, shopID, slot, amount):
		""""""
		if shopID in self:
			return self[shopID].returnBuyItem(slot, amount)
		return False
	
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		data = {}
		data["items"] = []
		for o in obj.values():
			data["items"].append( o )
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = self.__class__()
		for data in dict["items"]:
			obj.update( { data["shopID"] : data } )
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return True
		return isinstance( obj, ShopShareItemList )
		
class ShopRandomItemList( ShopShareItemList ):
	"""
	随机物品，重写getLimitItem
	"""
	def getRandItem(self, shopID):
		"""获取随机物品"""
		if not shopID in self:
			obj = ShopShareItems()
			obj.shopID = shopID
			self[shopID] = obj
			randomTime = random.randrange(csconst.RANDOM_REFLASH_TIME_BEGIN, csconst.RANDOM_REFLASH_TIME_END)\
				* 3600 + time.mktime(datetime.date.today().timetuple())
			obj.shopItems = self.generalRandomItems( shopID, randomTime )
		else:
			obj = self[shopID]
			
		startTime = time.localtime( obj.shopItems[ list( obj.shopItems.keys() )[0]]["startTime"] )
		newTime = time.localtime( time.time() )
		if startTime.tm_year != newTime.tm_year or startTime.tm_mon != newTime.tm_mon or startTime.tm_mday != newTime.tm_mday:
			randomTime = random.randrange(csconst.RANDOM_REFLASH_TIME_BEGIN, csconst.RANDOM_REFLASH_TIME_END)\
				* 3600 + time.mktime(datetime.date.today().timetuple())
			startTime = time.localtime( randomTime )
			obj.shopItems = self.generalRandomItems( shopID, randomTime )
		
		# 持续半小时
		isSellAll = True
		t = obj.shopItems[ list( obj.shopItems.keys() )[0]]["startTime"]
		if t <= time.time() and time.time() < t + csconst.RANDOM_REFLASH_TIME_LAST:
			for item in obj.shopItems.values():
				if item["amount"] > 0:						# 只要有一个没卖完
					isSellAll = False
					break
			if not isSellAll:
				return obj.shopItems
		
		return {}
		
	def GM_generalRandomItems( self, shopID, startTime ):
		"""商店生成随机物品"""
		if not shopID in self:
			obj = ShopShareItems()
			obj.shopID = shopID
			self[shopID] = obj
		else:
			obj = self[shopID]
		obj.shopItems = self.generalRandomItems( shopID, startTime )
		
	def generalRandomItems( self, shopID, startTime ):
		"""商店生成随机物品"""
		shopDatas = g_shopMgr.getRandomItems( shopID )
		calDict = {}
		retDict = {}
		for slot, shopItem in shopDatas.items():
			if not shopItem["slotIndex"] in calDict:
				calDict[shopItem["slotIndex"]] = 0
			calDict[shopItem["slotIndex"]] += shopItem["probability"]
		for index, probability in calDict.items():
			randNum = random.uniform(0, probability)
			for slot, shopItem in shopDatas.items():
				if index == shopItem["slotIndex"]:
					randNum -= shopItem["probability"]
					if randNum <= 0:
						retDict[slot] = {"id":slot, "amount":shopItem["buyLimit"], "startTime":startTime}
						break
		return retDict
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return True
		return isinstance( obj, ShopRandomItemList )
		
class ShopLimitItems( dict ):
	"""
	"""
	def __init__( self ):
		self.playerDbid = 0
		self.limitItems = {}
	
	def initConfig( self ):
		"""纠正配置表的修改"""
		for shopDatas in self.limitItems.values():
			shopDatas.initConfig( False )
		
	def getLimitItem(self, shopID, shopData):
		"""获取上限物品"""
		if not shopID in self.limitItems:
			self.limitItems[shopID] = ShopShareItemList()
		return self.limitItems[shopID].getLimitItem( shopID, shopData )
		
	def reduceItem(self, shopID, slot, amount):
		""""""
		if shopID in self.limitItems:
			return self.limitItems[shopID].reduceItem(shopID, slot, amount)
		return False
		
	def returnBuyItem(self, shopID, slot, amount):
		""""""
		if shopID in self.limitItems:
			return self.limitItems[shopID].returnBuyItem(shopID, slot, amount)
		return False
		
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		data = {}
		data["playerDbid"] = self.playerDbid
		data["limitItems"] = []
		for playerDbid, items in obj.items():
			data["limitItems"].append( items )
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = self.__class__()
		obj.playerDbid = dict["playerDbid"]
		for item in dict["limitItems"]:
			obj.limitItems.append(item)
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return True
		return isinstance( obj, ShopLimitItems )

class ShopLimitItemList( dict ):
	"""
	"""
	def initConfig( self ):
		"""纠正配置表的修改"""
		for DBID, shopItem in self.items():
			shopItem.initConfig()
	
	def getLimitItem(self, playerDbid, shopID, shopData):
		"""获取上限物品"""
		if not playerDbid in self:
			obj = ShopLimitItems()
			obj.playerDbid = playerDbid
			self[playerDbid] = obj
		return self[playerDbid].getLimitItem( shopID, shopData )
		
	def reduceItem(self, playerDbid, shopID, slot, amount):
		""""""
		if playerDbid in self:
			return self[playerDbid].reduceItem(shopID, slot, amount)
		return False
		
	def returnBuyItem(self, playerDbid, shopID, slot, amount):
		""""""
		if playerDbid in self:
			return self[playerDbid].returnBuyItem(shopID, slot, amount)
		return False
	
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		data = {}
		data["items"] = []
		for o in obj.values():
			data["items"].append( o )
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = self.__class__()
		for data in dict["items"]:
			obj.update( data )
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return True
		return isinstance( obj, ShopLimitItemList )



g_ShopShareItem = ShopShareItems()
g_ShopShareItems = ShopShareItemList()
g_ShopRandomItems = ShopRandomItemList()
g_ShopLimitItem = ShopLimitItems()
g_ShopLimitItems = ShopLimitItemList()