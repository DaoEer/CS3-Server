# -*- coding: utf-8 -*-
#
#
# 陷阱初始行为

import KBEDebug

class TrapInitActionBase:
	"""
	陷阱触发效果基础类
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def init( selfEntity, args ):
		"""
		"""
		pass

class TrapInitActionAddBuff( TrapInitActionBase ):
	"""
	给自身添加buff
	"""
	def __init__( self ):
		"""
		"""
		pass

	@staticmethod
	def init( selfEntity, args ):
		"""
		"""
		if args:
			selfEntity.addBuff(selfEntity, int(args[0]))