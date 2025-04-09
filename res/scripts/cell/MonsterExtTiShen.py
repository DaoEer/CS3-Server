# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import csstatus
import csdefine
import KBEDebug
import FightRuleMgr

class MonsterExtTiShen( Monster.Monster ):
	"""
	替身怪物类 目前用于玩家
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN)
		
	def calcAttachProperties( self ):
		"""
		重新计算战斗属性
		"""
		pass

	def updateBornHPMP(self):
		"""
		怪物出生满血
		"""
		pass

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		Monster.Monster.CELL_onClientReady( self, srcEntityID )
		player = self.getOwnerEntity()
		if not player:
			return
			
		for entityID in player.enemyList:
			entity = KBEngine.entities.get(entityID, None)
			if entity.getEntityFlag() != csdefine.ENTITY_FLAG_MONSTER and entity.getTargetID() == player.id:
				return
			FightRuleMgr.g_fightMgr.buildEnemyRelation( entity, self )
			entity.setTargetID( self.id )

	def getRelation( self, targetEntity ):
		"""
		"""
		player = self.getOwnerEntity()
		if not player:
			return
		return player.queryRelation(targetEntity)

	def getOwnerEntity( self ):
		"""
		"""
		if not self.ownerID:
			return None
		player = KBEngine.entities.get( self.ownerID,None )
		if player:
			return player
			
		return None

