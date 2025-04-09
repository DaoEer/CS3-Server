# -*- coding: utf-8 -*-
import Math
import KBEngine
import Monster
import csdefine
import Const
import KBEDebug

class MonsterFollowRole( Monster.Monster ):
	"""
	客户端AI测试怪(跟随玩家)
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_MONSTER_FOLLOW_ROLE)
		
	def syncEntityTarget(self, srcEntityID, targetID):
		"""
		Exposed method
		同步entity的目标
		"""
		if srcEntityID != self.controlEntityID:
			return
		
		entity = KBEngine.entities.get(targetID)
		if entity is None: return
		self.enemyID = targetID
		
	def CELL_onSetControlledBy(self, srcEntityID):
		"""
		Exposed method
		设置被玩家控制
		"""
		if srcEntityID != self.controlEntityID:
			return
		
		entity = KBEngine.entities.get(srcEntityID)
		if entity is None: return
		self.controlledBy = entity.base
	
	def setSyncPos(self, position):
		"""
		"""
		self.curPosition = position
		
	def setSyncDire(self, direction):
		"""
		"""
		self.curDirection = direction
		
		
	