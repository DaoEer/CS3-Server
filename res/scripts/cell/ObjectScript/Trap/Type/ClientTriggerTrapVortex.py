# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
import Math
from ObjectScript.Trap.Type.ClientTriggerTrap import ClientTriggerTrap

class ClientTriggerTrapVortex( ClientTriggerTrap ):
	"""
	旋涡 将玩家吸入陷阱中心
	"""
	def __init__( self ):
		ClientTriggerTrap.__init__( self )

	def onEnterTrap(self, selfEntity, enterID):
		"""
		"""
		ClientTriggerTrap.onEnterTrap(self, selfEntity, enterID)
		player = KBEngine.entities.get(enterID, None)
		if not player:
			return

		player.client.CLIENT_AddTrapVortex(selfEntity.id, self.vortexSpeed)


	def onLeaveTrap(self, selfEntity, enterID):
		"""
		"""
		ClientTriggerTrap.onLeaveTrap(self, selfEntity, enterID)
		player = KBEngine.entities.get(enterID, None)
		if not player:
			return
		player.client.CLIENT_RemoveTrapVortex(selfEntity.id)