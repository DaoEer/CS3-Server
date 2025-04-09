# -*- coding: utf-8 -*-
import KBEngine
import Monster
import csdefine
import Const
import KBEDebug

class MonsterClientBase( Monster.Monster ):
	"""
	客户端AI怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_MONSTER_CLIENT_BASE)

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		Monster.Monster.CELL_onClientReady( self, srcEntityID )
		self.getScript().setUpMonsterBaseDatas( self )
		self.moveSpeed = self.getScript().getWalkSpeed( self )

	def CELL_onAttackTarget( self, srcEntityID ):
		"""
		<Expose method>
		攻击玩家
		"""
		self.setTargetID( srcEntityID )
		spellList = []
		for skillID in self.attcakSkills:
			tempList = [ skillID, self.getTargetID(),True ]
			spellList.append(tempList)
		self.behAdds(csdefine.BEHAVIOUR_TYPE_SPELL, spellList,csdefine.BEHAVIOUR_LOOP)

	def CELL_onSetControlledBy( self, srcEntityID ):
		"""
		在玩家视野范围内才设置controlledBy
		"""
		player = KBEngine.entities.get( srcEntityID, None )
		if player and player.isEntityInView( self ):
			self.controlledBy = player.base

	def CELL_startFalling( self, srcEntityID ):
		"""
		开始掉落
		"""
		self.destroySelf()

