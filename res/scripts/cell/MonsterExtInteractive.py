# -*- coding: utf-8 -*-


"""
usage:
	怪物基类

attribute:
	modelNumber

member function:
	getModelNumber
	setModelNumber

callback:
	pass

"""


#python
#engine
import KBEngine
import KBEDebug
#script
import Monster
import csdefine


class MonsterExtInteractive( Monster.Monster ):
	"""
	F键交互怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_INTERACTIVE)

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		player = KBEngine.entities.get( srcEntityID )
		if not player or not player.getClient():
			return
		player.clientEntity( self.id ).AddInitiativeTrap()

	def interactiveWith(self, srcEntityID):
		"""
		<exposed method>
		客户端左键双击事件
		"""
		triggerEntity = KBEngine.entities.get( srcEntityID, None )
		self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_ON_GOSSIP_WITH_MONSTER, (srcEntityID, "", "Interactive"),triggerEntity)
