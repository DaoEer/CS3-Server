# -*- coding: utf-8 -*-


import ObjectScript.Monster.Monster as Monster
class MonsterExtCanPush( Monster.Monster ):
	"""
	可以被玩家推动的怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )