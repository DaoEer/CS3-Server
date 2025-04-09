# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
from Role import Role, PlayerRole
from Interface.NPCBaseObject import NPCBaseObject
from Interface.CombatInterface import CombatInterface
from Interface.MonsterObject import MonsterObject
class Monster(
	MonsterObject,
	KBEngine.Entity,
	NPCBaseObject,
	CombatInterface,
	):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		MonsterObject.__init__(self)
		NPCBaseObject.__init__(self)
		CombatInterface.__init__(self)
		
	def set_state(self, oldState):
		CombatInterface.set_state(self, oldState)
		if self.state == csdefine.ENTITY_STATE_DEAD:
			for owner in self.owners:
				if owner["type"] == csdefine.DROP_OWNER_TYPE_PERSON:
					player = self.clientapp.entities.get(owner["owner"], None)
					if player and isinstance(player, PlayerRole):
						player.addKillMonsterCounter(self.scriptID)
						player.eventObj.fireEvent("Event_OnMonsterDead", self.scriptID, self.id)
		
	def PlayAdmissionAction(self, actionID):
		pass
		
	def PlayDeadEffect(self):
		pass
	def HideSpecialProgress(self):
		pass
		
	def AddClientAttackTrap(self, int1, str1,f1):
		pass
		
	def CancelClientAttackTrap(self):
		pass
		
	def AddClientInitiativeTrap(self, shape, shapeParam, angle, trapHeight):
		pass
		
	def CancelClientInitiativeTrap(self):
		pass
		
	def CreateFightArea(self):
		pass
		
	def OnLeaveFightArea(self):
		pass
	def OnStopCurrentAction(self):
		pass
	def CloseInitiativeTrapEffect( self ):
		pass
	def OpenInitiativeTrapEffect( self ):
		pass
	def SimulationCircle( self, p1 ):
		pass
	def PlayerReTriggerTrap( self ):
		pass
	def OpenInitiactiveTrapEffect( self, p1, p2, p3, p4 ):
		pass
	def CloseInitiactiveTrapEffect( self ):
		pass
	def StopSimulationCircle( self ):
		pass
	def ShowSpecialProgress( self, p1, p2, p3 ):
		pass
	
	def onLeaveWorld(self):
		self.eventObj.fireEvent("Event_OnMonsterLeaveWorld", self.scriptID, self.id)
		
	def onLeaveSpace(self):
		pass
	def CLIENT_PlayAdmissionAction( self, p1 ):
		pass
	def CLIENT_ShowSpecialProgress( self, p1, p2, p3 ):
		pass
	def CLIENT_HideSpecialProgress( self ):
		pass
	def CLIENT_StartMonsterJump( self ):
		pass
	def CLIENT_EndMonsterJump( self ):
		pass
	def ShowMonsterLocationTwinkle( self ):
		pass
	def ClientMovingReady(self):
		pass
	def OpenMoveShield( self, p1, p2 ):
		pass
	def CloseMoveShield( self, p1 ):
		pass
