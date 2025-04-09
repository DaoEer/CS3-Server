# -*- coding: utf-8 -*-

import json
import time
import datetime
import KBEngine
import KBEDebug
if KBEngine.component == "baseapp":
	from ConfigObject.Store.StoreMgr import g_storeMgr


class StoreServerLimitGoods( dict ):
	"""
	"""
	def initConfig(self):
		"""
		"""
		oldList = list(self.keys())
		goodsDatas = g_storeMgr.getAll()
		for goodsID, goods in goodsDatas.items():
			if goods.ServeLimitAmount <= 0:
				continue
			if goodsID in oldList:
				amount = self[goodsID]["amount"]
				oldList.remove(goodsID)
			else:
				amount = goods.ServeLimitAmount
			self[goodsID] = {"goodsID": goods.ID, "amount": amount, "startTime":time.mktime(datetime.date.today().timetuple())}
		
		for oldID in oldList:
			self.pop(oldID, None)

	def getLimitGoods(self, goodsDatas):
		"""
		获取上限物品
		"""
		if self:
			g_storeMgr.onGet(self, True)
		else:
			for goods in goodsDatas:
				self[goodsData["ID"]] = {"goodsID":goods.ID, "amount": goods.ServeLimitAmount, "startTime":time.mktime(datetime.date.today().timetuple())}

		return self

	def getLimitGoodsAmount(self):
		"""
		获得有数量上限的物品ID和对应的数量
		"""
		if self:	
			g_storeMgr.onGet(self, True)
		IDlist = []
		amountList = []
		for key, value in self.items():
			IDlist.append(key)
			amountList.append(value["amount"])

		return IDlist, amountList

	def reduceGoods(self, goodsID, amount):
		"""
		减少可购买数量
		"""
		if goodsID in self:
			if self[goodsID]["amount"] >= amount:
				self[goodsID]["amount"] -= amount
				return True
		return False

	def isNoLimitAmount(self, goodsID, amount):
		"""	

		"""
		if goodsID in self:
			if self[goodsID]["amount"] < amount:
				return False
		return True

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		"""
		data = {}
		data["items"] = []
		for i in obj.values():
			data["items"].append( i )
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		"""
		obj = self.__class__()
		for data in dict["items"]:
			obj[data["goodsID"]] = data
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		"""
		if obj is None: return True
		return isinstance( obj, StoreServerLimitGoods )

class StorePlayerLimitGoods( dict ):
	"""
	"""
	def __init__( self ):	
		self.playerDbid = 0
		self.limitGoods = {}

	def initConfig(self):
		"""
		"""
		removeList = []
		for goodsID, LimitGoods in self.limitGoods.items():
			goods = g_storeMgr.getGoodsByID(goodsID)
			if goods.LimitAmount < 0:
				removeList.append(goodsID)
				continue
			self.limitGoods[goodsID] = {"goodsID":goods.ID, "amount":self.limitGoods[goodsID]["amount"], "startTime":time.mktime(datetime.date.today().timetuple())}

		for removeID in removeList:
			self.limitGoods.pop(removeID, None)

	def getLimitGoods(self, goodsID, goodsData):
		"""
		获取上限物品
		"""
		if goodsID in self.limitGoods:
			amount = self.limitGoods[goodsID]["amount"]
		else:
			amount = goodsData.LimitAmount
		self.limitGoods[goodsID] = {"goodsID":goodsData.ID, "amount":amount, "startTime":time.mktime(datetime.date.today().timetuple())}
		return self.limitGoods

	def reduceGoods(self, goodsID, amount):
		""""""
		if goodsID in self.limitGoods:
			if self.limitGoods[goodsID]["amount"] >= amount:
				self.limitGoods[goodsID]["amount"] -= amount
				return True
		return False

	def isNoLimitAmount(self, goodsID, amount):
		"""	

		"""
		if goodsID in self.limitGoods:
			if self.limitGoods[goodsID]["amount"] < amount:
				return False
		return True

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		"""
		data = {}
		data["playerDbid"] = self.playerDbid
		data["limitGoods"] = []
		for i in obj.limitGoods.values():
			data["limitGoods"].append( i )
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		"""
		obj = self.__class__()
		obj.playerDbid = dict["playerDbid"]
		for data in dict["limitGoods"]:
			obj.limitGoods[data["goodsID"]] = data
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		"""
		if obj is None: return True
		return isinstance( obj, StorePlayerLimitGoods )

class StorePlayerLimitGoodsList( dict ):
	"""
	"""
	def initConfig(self):
		"""
		"""
		for DBID, limitGoods in self.items():
			limitGoods.initConfig()

	def getLimitGoods(self, playerDbid, goodsData):
		"""
		获取上限物品
		"""
		if not playerDbid in self:
			obj = StorePlayerLimitGoods()
			obj.playerDbid = playerDbid
			self[playerDbid] = obj
		return self[playerDbid].getLimitGoods( goodsData.ID , goodsData )

	def getLimitGoodsAmount(self,  playerDbid ):
		"""
		获得有数量上限的物品ID和对应的数量
		"""
		IDlist = []
		amountList = []
		if playerDbid not in self:
			return IDlist, amountList
			
		if self:	
			g_storeMgr.onGet(self[playerDbid], False)
		if playerDbid in self:
			for key, value in self[playerDbid].items():
				IDlist.append(key)
				amountList.append(value["amount"])

		return IDlist, amountList

	def reduceGoods(self, playerDbid, goodsID, amount):
		"""
		"""
		if playerDbid in self:
			return self[playerDbid].reduceGoods(goodsID, amount)	
		return False

	def isNoLimitAmount(self, playerDbid, goodsID, amount):
		"""	

		"""
		if playerDbid in self:
			return self[playerDbid].isNoLimitAmount(goodsID, amount)
		return True

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		"""
		data = {}
		for key,value in obj.items():
			temp = {}
			for i,j in value.items(): 
				temp[i]= j
			data[key] = temp
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		"""
		obj = self.__class__()
		for data in dict["items"]:
			temp = {}
			for i in data["limitGoods"]:
				temp[i["goodsID"]] = i
			obj[data["playerDbid"]] = temp
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		"""
		if obj is None: return True
		return isinstance( obj, StorePlayerLimitGoodsList )

g_StoreServerLimitGoods = StoreServerLimitGoods()
g_StorePlayerLimitGoods = StorePlayerLimitGoods()
g_StorePlayerLimitGoodsList = StorePlayerLimitGoodsList()