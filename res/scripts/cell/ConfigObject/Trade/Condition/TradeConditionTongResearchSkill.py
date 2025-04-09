# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

from ConfigObject.Trade.TradeConditionBase import TradeConditionBase

class TradeConditionTongResearchSkill( TradeConditionBase ):
	"""
	帮会技能是否研发（cell不存数据，此处不作判断）
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
			return True
		return False