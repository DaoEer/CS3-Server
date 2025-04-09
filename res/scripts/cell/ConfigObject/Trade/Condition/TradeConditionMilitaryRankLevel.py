# -*- coding: utf-8 -*-
import KBEngine
import csstatus
from KBEDebug import *

from ConfigObject.Trade.TradeConditionBase import TradeConditionBase

class TradeConditionMilitaryRankLevel( TradeConditionBase ):
	"""
	玩家军衔等级
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
		if avatar.militaryRank >= value:
			return True
		else:
			avatar.statusMessage( csstatus.MILITARY_RANK_LEVEL_NO_ENOUGH,"" )
			return False
		
		