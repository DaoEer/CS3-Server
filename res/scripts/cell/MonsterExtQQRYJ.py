# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import KBEDebug
import csdefine
import csarithmetic

class MonsterExtQQRYJ( Monster.Monster ):
	"""
	巧取熔岩晶 ---骑乘推动怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		
	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_QQRYJ)

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		player = KBEngine.entities.get( srcEntityID )
		if not player or not player.getClient():
			return
		player.clientEntity( self.id ).AddAlternatelyRange()
		
	def CELL_OnPlayerBeginPush( self, srcEntityID ):
		"""
		Exposed Method
		玩家开始推动
		"""
		triggerEntity = KBEngine.entities.get( srcEntityID, None )
		if triggerEntity:
			self.direction.z = csarithmetic.getYawByVector3( self.position - triggerEntity.position )
			self.setSyncPosClient( srcEntityID )
			self.monsterAITriggerEvent( csdefine.ENTITY_EVENT_ON_PLAYER_BEGIN_PUSH, [], triggerEntity )
			
		
	def CELL_OnPlayerEndPush( self, srcEntityID ):
		"""
		Exposed Method
		玩家结束推动
		"""
		self.setSyncPosClient(0)
		triggerEntity = KBEngine.entities.get( srcEntityID, None )
		self.monsterAITriggerEvent( csdefine.ENTITY_EVENT_ON_PLAYER_END_PUSH, [], triggerEntity )

	def alternatelyResults( self, srcEntityID ):
		"""
		<exposed method>
		交互结果
		"""
		triggerEntity = KBEngine.entities.get( srcEntityID, None )
		self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_ON_GOSSIP_WITH_MONSTER, (srcEntityID, "", "alternately"),triggerEntity)