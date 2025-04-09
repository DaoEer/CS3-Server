# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import Math
import csdefine
import KBEDebug

class MonsterGhostEye( Monster.Monster ):
	"""
	鬼瞳之眼
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		player = KBEngine.entities.get(srcEntityID,None)
		if player:
			self.controlledBy = player.base
		self.moveSpeed = self.getScript().getWalkSpeed( self )