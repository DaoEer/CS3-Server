# -*- coding: utf-8 -*-
import KBEngine
import csstatus
from KBEDebug import *

from ConfigObject.Trade.TradeConditionBase import TradeConditionBase

class TradeConditionLevel( TradeConditionBase ):
	"""
	交易货币基础类
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
		if avatar.level >= value:
			return True
		else:
			avatar.statusMessage( csstatus.CANOT_BUY_GOODS_AS_LEVEL,"" )
			return False