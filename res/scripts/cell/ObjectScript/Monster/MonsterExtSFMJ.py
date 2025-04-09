# -*- coding: utf-8 -*-
import ObjectScript.Monster.Monster as Monster
import csdefine
import KBEngine
import KBEDebug

class MonsterExtSFMJ( Monster.Monster ):
	"""
	神风秘境 -- F键交互怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )