# -*- coding: utf-8 -*-
from Interface.NPCBaseObject import NPCBaseObject
from Interface.MonsterCombatInterface import MonsterCombatInterface
from Interface.MonsterAppearInterface import MonsterAppearInterface
from Interface.NPCAmbulantInterface import NPCAmbulantInterface
from Interface.CombatInterface import CombatInterface
class MonsterObject(
	NPCAmbulantInterface,
	NPCBaseObject, 
	MonsterCombatInterface, 
	MonsterAppearInterface, 
	CombatInterface, ):
	def __init__(self):
		NPCAmbulantInterface.__init__(self)
		NPCBaseObject.__init__(self) 
		MonsterCombatInterface.__init__(self) 
		MonsterAppearInterface.__init__(self) 
		CombatInterface.__init__(self) 
	def OnLeaveFightArea( self ):
		pass
	def CreateFightArea( self ):
		pass
	def PlayerReTriggerTrap( self ):
		pass
	def FaceToPlayer( self, p1 ):
		pass
	def onPlsySpeechBubbles( self, p1 ):
		pass
	def onPlaySpeechBubbles( self, p1 ):
		pass
	def CLIENT_CreateFightArea( self ):
		pass
	def CLIENT_OnLeaveFightArea( self ):
		pass
	def CLIENT_PlayerReTriggerTrap( self ):
		pass
	def CLIENT_FaceToPlayer( self, p1 ):
		pass
	def CLIENT_onPlaySpeechBubbles( self, p1 ):
		pass
	def CLIENT_AddClientAttackTrap( self, p1, p2, p3 ):
		pass
	def CLIENT_CancelClientAttackTrap( self ):
		pass
	def CLIENT_AddClientInitiativeTrap( self, p1, p2, p3 ):
		pass
	def CLIENT_CancelClientInitiativeTrap( self ):
		pass
	def CLIENT_OpenInitiactiveTrapEffect( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_SimulationCircle( self, p1, p2 ):
		pass
	def CLIENT_StopSimulationCircle( self ):
		pass
	def CLIENT_CloseInitiactiveTrapEffect( self ):
		pass
	def CLIENT_endMonsterBlow( self ):
		pass
	def CLIENT_addMonsterBlow( self, p1, p2 ):
		pass
