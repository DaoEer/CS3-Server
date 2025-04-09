# -*- coding: utf-8 -*-
#

import KBEngine
from KBEDebug import *
import csdefine
import time
from ConfigObject.Shop.ShopRefreshBase import ShopRefreshBase

class ShopRefreshSellOut( ShopRefreshBase ):
	"""
	商店物品售罄刷新
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
			# 商店没有这个物品
			ERROR_MSG( "addItemRefreshTimer:: no item %s"%(slot) )
			return False
		if item["amount"] < 0:
			# 物品没有数量限制不需要刷新
			return False
		# 卖完就刷新类型
		if config["refreshType"] != csdefine.NPCSHOP_ITEM_REFRESH_SELLOUT:
			return False

		if item["amount"] > 0:
			# 物品还有
			return False

		return self.onGet( config["buyLimit"], item, params )

	def onSell( self, shop, slot, item ):
		"""
		virtual method.
		出售后
		"""
		return self.onSell( shop, slot, item )