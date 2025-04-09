# -*- coding: utf-8 -*-

import KBEngine
import Monster
import KBEDebug
import csdefine

class MonsterExtSFMJ( Monster.Monster ):
	"""
	神风秘境 -- F键交互怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_SFMJ)

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		player = KBEngine.entities.get( srcEntityID )
		if not player or not player.getClient():
			return
		player.clientEntity( self.id ).AddInitiativeRange()

	def interactionResults( self, srcEntityID ):
		"""
		<exposed method>
		交互结果
		"""
		triggerEntity = KBEngine.entities.get( srcEntityID, None )
		self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_ON_GOSSIP_WITH_MONSTER, (srcEntityID, "", "interactive"),triggerEntity)