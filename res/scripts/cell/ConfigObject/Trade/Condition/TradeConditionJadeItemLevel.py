# -*- coding: utf-8 -*-
import KBEngine
import csstatus
import csdefine
from KBEDebug import *

from ConfigObject.Trade.TradeConditionBase import TradeConditionBase

class TradeConditionJadeItemLevel( TradeConditionBase ):
	"""
	玲珑玉令等级
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
		if avatar.getLHMJBuildLevel(csdefine.LHMJ_BUIILD_LING_QUAN) >= value:
			return True
		else:
			avatar.statusMessage( csstatus.CANOT_BUY_ITEM_JADE_LEVEL_DOWN,"" )
			return False