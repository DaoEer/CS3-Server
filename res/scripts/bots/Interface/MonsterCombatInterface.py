# -*- coding: utf-8 -*-
from Interface.MonsterOwnerInterface import MonsterOwnerInterface
from Interface.BehaviourInterface import BehaviourInterface
from Interface.CombatInterface import CombatInterface
class MonsterCombatInterface(
	BehaviourInterface,
	MonsterOwnerInterface,
	CombatInterface, ):
	def __init__(self):
		BehaviourInterface.__init__(self)
		MonsterOwnerInterface.__init__(self)
		CombatInterface.__init__(self) 
	def CLIENT_PlayDeadEffect( self ):
		pass
	def PlayDeadMortuaryEffect( self ):
		pass
