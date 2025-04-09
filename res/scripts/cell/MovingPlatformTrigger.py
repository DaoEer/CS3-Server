# -*- coding: utf-8 -*-
import KBEDebug
import KBEngine
import csdefine
#cell
from MovingPlatform import MovingPlatform

class MovingPlatformTrigger( MovingPlatform ):
	"""
	炼狱之塔移动石柱
	"""
	def __init__( self ):
		MovingPlatform.__init__( self )
		self.playMoveAction()

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
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
		self.allClients.CLIENT_OnPlayAction( action, time )

	def onMovingPlatformTrigger(self, player):
		if not self.getScript().triggerBuffs:
			return
		for buffID in self.getScript().triggerBuffs:
			buff = player.findBuffsByBuffID(buffID)
			if buff:
				continue
			else:
				player.addBuff(player, buffID)

	def onMovingPlatformTriggerStart(self, player):
		if not self.getScript().startBuffs:
			return
		for buffID in self.getScript().startBuffs:
			buff = player.findBuffsByBuffID(buffID)
			if buff:
				continue
			else:
				player.addBuff(player, buffID)