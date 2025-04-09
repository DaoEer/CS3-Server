# -*- coding: utf-8 -*-

import KBEngine
import Monster
import csdefine

class MonsterExtImpact( Monster.Monster ):
	"""
	撞击怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.isPlayAction = False
		self.addFlag( csdefine.FLAG_MESH_COLLISION )

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		Monster.Monster.CELL_onClientReady( self, srcEntityID )
		if self.isPlayAction:
			self.playMoveAction()

	def playMoveAction(self):
		object = self.getScript()
		if object.playAction:
			if object.delayTime:
				self.addTimerCallBack(object.delayTime, "clientsPlayAction", (object.playAction,-1.0))
			else:
				self.addTimerCallBack(2.0, "clientsPlayAction", (object.playAction,-1.0))
		
		
	def clientsPlayAction( self, action, time ):
		"""
		"""
		self.isPlayAction = True
		self.allClients.CLIENT_OnPlayAction( action, time )

	def onPlayerBeImpact(self, playerID):
		"""
		玩家被撞击后
		"""
		object = self.getScript()
		if not object.buffIDs:
			return
		player = KBEngine.entities.get(playerID, None)
		if not player:
			return
		for buffID in object.buffIDs:
			buff = player.findBuffsByBuffID( buffID )
			if not len(buff):
				player.addBuff( self, buffID )



