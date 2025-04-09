# -*- coding: utf-8 -*-
import csdefine
import Math
import math
import KBEngine
import KBEDebug

class EntityDataValidateInterface( object ):
	def __init__( self ):
		object.__init__( self )
		
	def validateClientCall( self ):
		"""
		验证玩家客户端调用自己的方法
		callEntityID:调用客户端ID
		"""
		if self.isDestroyed: #在销毁中
			return False
			
		return True
	