# -*- coding: utf-8 -*-
import KBEngine
import csstatus
from KBEDebug import *

from ConfigObject.Trade.TradeConditionBase import TradeConditionBase

class TradeConditionJingjieLevel( TradeConditionBase ):
	"""
	境界等级
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
		if avatar.jingjieLevel >= value:
			return True
		else:
			avatar.statusMessage( csstatus.CANOT_BUY_GOODS_AS_JINGJIELEVEL,"" )
			return False