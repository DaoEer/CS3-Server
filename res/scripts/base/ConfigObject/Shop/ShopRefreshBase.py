# -*- coding: utf-8 -*-
#

import KBEngine
from KBEDebug import *
import time
import datetime

class ShopRefreshBase:
	"""
	商店物品刷新基类
	"""
	def __init__( self ):
		"""
		virtual method.
		"""
		pass

	def onGet( self, config, item, params ):
		"""
		virtual method.
		请求数量前
		"""
		return True

	def onSell( self, shop, slot, item ):
		"""
		virtual method.
		出售后
		"""
		return True

	def refresh( self, amount, item ):
		"""
		刷新
		"""
		item["startTime"] = time.mktime(datetime.date.today().timetuple())
		item["amount"] = amount
		return True