# -*- coding: utf-8 -*-

import KBEDebug
import csdefine
from Singleton import Singleton
from StoreGoodsImpl import StoreGoodsImpl
from LoadModule import *
from ConfigObject.Store.StoreRefreshType.StoreRefreshDay import StoreRefreshDay
from ConfigObject.Store.StoreRefreshType.StoreRefreshWeek import StoreRefreshWeek

class StoreMgr( Singleton ):
	"""
	商城商品处理类
	"""
	def __init__( self ):
		self.mapping = {} 							# {GoodsID:Goods}
		self.typeMapping = {}						# { GoodsType :{ItemType:[Goods1, Goods2...]}}
		self.refreshMap = {
			csdefine.STORE_GOODS_REFRESH_DAY		: StoreRefreshDay(),
			csdefine.STORE_GOODS_REFRESH_WEEK		: StoreRefreshWeek(),
		}

	def init( self ):
		"""
		配置加载
		"""
		configs = openJsonCfg("Store/StoreConfig.json")
		for config in configs:
			if config["GoodsType"] not in self.typeMapping:
				self.typeMapping[config["GoodsType"]] = {}
			if config["ItemType"] not in self.typeMapping[config["GoodsType"]]:
				self.typeMapping[config["GoodsType"]][config["ItemType"]] = [] 
			goods = StoreGoodsImpl.createObjFromDict(config)
			self.typeMapping[config["GoodsType"]][config["ItemType"]].append(goods)
			self.mapping[config["ID"]] = goods

	def getAll( self ):
		return self.mapping

	def getGoodsByType( self, goodsType, ItemType ):
		if goodsType in self.typeMapping:
			if ItemType in self.typeMapping[goodsType]:
				return self.typeMapping[goodsType][ItemType]
		return []

	def getNewGoods( self, goodsType ):
		List = []
		if goodsType in self.typeMapping:
			for j in self.typeMapping[goodsType].values():
				for i in j:
					if i.GoodsState == csdefine.STORE_GOODS_STATE_NEW_PRODUCT:
						List.append(i)
		return List

	def getGoodsByID(self, ID):
		"""
		通过商品ID获得商品数据
		"""
		if ID in self.mapping:
			return self.mapping[ID]
		return None

	def onGet( self, limitGoodss, isSverLimit ):
		for ID, limitGood in limitGoodss.items():
			GoodData = self.getGoodsByID(ID)
			if not GoodData.RefreshType in self.refreshMap:
				continue
			c = self.refreshMap[GoodData.RefreshType]
			c.onGet(GoodData,limitGood, isSverLimit)

g_storeMgr = StoreMgr()