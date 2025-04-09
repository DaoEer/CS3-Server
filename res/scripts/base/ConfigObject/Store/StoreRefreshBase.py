# -*- coding: utf-8 -*-
import KBEngine
import time
import datetime

class StoreRefreshBase:

	def __init__( self ):
		"""
		virtual method.
		"""
		pass

	def onGet(self, limitGood, isSverLimit):
		"""
		virtual method.
		获得
		"""
		return True

	def onBuy( self, playerDBID, amount, goods ):
		"""
		virtual method.
		购买
		"""
		return True


	def refresh( self, amount, goods ):
		"""
		刷新
		"""
		goods["startTime"] = time.mktime(datetime.date.today().timetuple())
		goods["amount"] = amount
		return True