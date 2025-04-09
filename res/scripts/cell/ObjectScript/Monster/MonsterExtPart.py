# -*- coding: utf-8 -*-

import KBEngine
import Math
import csdefine
import ObjectScript.Monster.Monster as Monster

class MonsterExtPart( Monster.Monster ):
	"""
	联合怪物：副怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )







	


