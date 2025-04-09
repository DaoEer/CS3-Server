# -*- coding: utf-8 -*-
from Interface.MonsterObject import MonsterObject
from Monster import Monster
class MonsterExtCall( Monster ,
	MonsterObject,
	):
	def __init__(self):
		MonsterObject.__init__(self)
	def CancelClientInitiativeTrap( self ):
		pass
	def CloseInitiativeTrapEffect( self ):
		pass
	def CancelClientAttackTrap( self ):
		pass
	def OpenInitiativeTrapEffect( self ):
		pass
	def AddClientAttackTrap( self, p1, p2, p3 ):
		pass
	def AddClientInitiativeTrap( self, p1, p2, p3, p4 ):
		pass
	def OpenInitiactiveTrapEffect( self, p1, p2, p3, p4 ):
		pass
	def CloseInitiactiveTrapEffect( self ):
		pass
