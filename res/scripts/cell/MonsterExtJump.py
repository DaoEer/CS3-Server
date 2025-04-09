# -*- coding: utf-8 -*-

#script
import KBEngine
import Monster
import csdefine

class MonsterExtJump( Monster.Monster ):
	"""
	跳跃怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )


	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_JUMP)