# -*- coding: utf-8 -*-
import KBEngine
from Interface.NPCBaseObject import SpellObject
class SpellBox(
	KBEngine.Entity,
	SpellObject,
	):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		SpellObject.__init__(self)
	def CLIENT_RefreshBoxStatus( self ):
		pass
	def CLIENT_SetBoxStatus( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_SpellBoxInterrupted( self ):
		pass
	def CLIENT_OnHoldRadiusFog( self, p1, p2, p3, p4, p5 ):
		pass
