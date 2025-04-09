# -*- coding: utf-8 -*-

import csdefine
import time
import datetime
from ConfigObject.Store.StoreRefreshBase import StoreRefreshBase

class StoreRefreshDay( StoreRefreshBase ):
	"""
	商城商品每日定时刷新
	"""
	def __init__( self ):
		StoreRefreshBase.__init__( self )

	def onGet(self, goodsData, limitGood, isSverLimit):
		"""
		virtual method.
		获得限制商品数量
		"""
		LimitAmount = 0
		if isSverLimit:
			LimitAmount = goodsData.ServeLimitAmount
		else:
			LimitAmount = goodsData.LimitAmount

		if LimitAmount < 0:
			return False

		#每天刷新类型
		if goodsData.RefreshType != csdefine.NPCSHOP_ITEM_REFRESH_DAY:
			return False

		if limitGood["amount"] >= LimitAmount:
			#物品已经是最大数量不需要重制
			self.refresh( LimitAmount, limitGood )
			return False

		if datetime.date.fromtimestamp(limitGood["startTime"]).year == datetime.date.today().year:
			if datetime.date.fromtimestamp(limitGood["startTime"]).month == datetime.date.today().month:
				if datetime.date.fromtimestamp( limitGood["startTime"] ).day == datetime.date.today().day:
					return False

		return self.refresh( LimitAmount, limitGood )