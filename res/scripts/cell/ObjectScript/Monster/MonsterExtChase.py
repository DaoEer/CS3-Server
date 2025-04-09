# -*- coding: utf-8 -*-


import KBEngine
import KBEDebug
#script
import Monster
import time
import csarithmetic
import csdefine
import Const

class MonsterExtChase( Monster.Monster ):
	"""
	追击目标怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )