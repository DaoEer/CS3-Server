# -*- coding: utf-8 -*-
#

import KBEngine
from KBEDebug import *
import csdefine
import time
import datetime
from ConfigObject.Shop.ShopRefreshBase import ShopRefreshBase

class ShopRefreshDay( ShopRefreshBase ):
	"""
	商店物品每日定时刷新
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
		#每天刷新类型
		if config["refreshType"] != csdefine.NPCSHOP_ITEM_REFRESH_DAY:
			return False

		if item["amount"] >= config["buyLimit"]:
			#物品已经是最大数量不需要重制
			self.refresh( config["buyLimit"], item )
			return False
		
		if datetime.date.fromtimestamp(item["startTime"]).year == datetime.date.today().year:
			if datetime.date.fromtimestamp(item["startTime"]).month == datetime.date.today().month:
				if datetime.date.fromtimestamp( item["startTime"] ).day == datetime.date.today().day:
					return False
		
		return self.refresh( config["buyLimit"], item )

	def onSell( self, shop, slot, item ):
		"""
		virtual method.
		出售后
		"""
		return ShopRefreshBase.onSell( self, shop, slot, item )