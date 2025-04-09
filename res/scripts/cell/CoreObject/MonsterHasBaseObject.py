# -*- coding: utf-8 -*-

"""
用于有base类型的怪物派出基类
"""

from CoreObject import MonsterObject

class MonsterHasBaseObject(  MonsterObject.MonsterObject ):
	def __init__( self ):
		MonsterObject.MonsterObject.__init__( self )
		
		
	def doEnterSpace( self ):
		"""
		进入一个空间调用
		"""
		MonsterObject.MonsterObject.doEnterSpace( self )

	def doLeaveSpace( self ):
		"""
		离开一个空间调用（在doEnterSpace之后）
		"""
		MonsterObject.MonsterObject.doEnterSpace( self )