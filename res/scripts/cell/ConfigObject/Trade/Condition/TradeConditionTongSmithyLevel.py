# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

from ConfigObject.Trade.TradeConditionBase import TradeConditionBase

class TradeConditionTongSmithyLevel( TradeConditionBase ):
	"""
	帮会铁匠铺等级
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
		if avatar.tongMB:
			return avatar.tongSmithyLevel >= value
		return False