# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TradeConditionBase:
	"""
	交易条件基础类
	"""
	def __init__( self ):
		"""
		virtual method.
		初始化
		"""
		pass

	def verify( self, avatar, value ):
		"""
		virtual method.
		验证
		"""
		return True