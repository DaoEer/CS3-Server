# -*- coding: utf-8 -*-
from Interface.CombatInterface import CombatInterface
from Interface.MonsterOwnerInterface import MonsterOwnerInterface
class MonsterControlledByClientCombatInterface(
	CombatInterface, 
	MonsterOwnerInterface, ):
	def __init__(self):
		CombatInterface.__init__(self) 
		MonsterOwnerInterface.__init__(self) 
	def CLIENT_PlayDeadEffect( self ):
		pass
