# -*- coding: utf-8 -*-
import KBEngine
import csstatus
from KBEDebug import *

from ConfigObject.Trade.TradeConditionBase import TradeConditionBase

class TradeConditionTongShopLevel( TradeConditionBase ):
	"""
	帮会商店等级
	"""
	def __init__( self ):
		"""
		virtual method.
		初始化
		"""
		TradeConditionBase.__init__( self )

	def verify( self, avatar, value ):
		"""
		virtual method.
		验证
		"""
		#CST-11291
		return True
		"""
		if avatar.tongMB:
			if avatar.tongShopLevel >= value:
				return True
			else:
				avatar.statusMessage( csstatus.TONG_LEVEL_CANNOT_BUY_GOODS,"" )
		return False
		"""