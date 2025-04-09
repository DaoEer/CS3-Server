# -*- coding: utf-8 -*-
#

import KBEngine
from KBEDebug import *
import csdefine
import time
import datetime
from ConfigObject.Shop.ShopRefreshBase import ShopRefreshBase

class ShopRefreshTime( ShopRefreshBase ):
	"""
	商店物品定时刷新(固定时间内进行售卖，超时不再出售)
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		ShopRefreshBase.__init__( self )

	def onGet( self, config, item, params ):
		"""
		virtual method.
		请求数量前
		"""
		if item == None:
			#商店没有这个物品
			ERROR_MSG( "addItemRefreshTimer:: no item %s"%(slot) )
			return False
		
		if item["amount"] < 0:
			#物品没有数量限制不需要刷新
			return False
			
		#固定时间点刷新类型
		if config["refreshType"] != csdefine.NPCSHOP_ITEM_REFRESH_TIME:
			return False
		
		if item["amount"] >= config["buyLimit"]:
			#物品已经是最大数量不需要重制
			self.refresh( config["buyLimit"], item )
			return False
			
		if params["startTime"] <= item["startTime"] and item["startTime"] < params["endTime"]:
			return False
		
		t = int(time.time())
		if params["startTime"] <= t and t < params["endTime"]:
			self.refresh( config["buyLimit"], item )
			return False
		
		return self.refresh( 0, item )

	def onSell( self, shop, slot, item ):
		"""
		virtual method.
		出售后
		"""
		return ShopRefreshBase.onSell( self, shop, slot, item )
		
	def refresh( self, amount, item ):
		"""
		刷新
		"""
		item["startTime"] = time.time()
		item["amount"] = amount
		return True
		