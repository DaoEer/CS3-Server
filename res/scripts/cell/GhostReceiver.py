# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import Const
from CoreObject.GhostReceiverObject import GhostReceiverObject


class GhostReceiver( GhostReceiverObject ):
	"""
	技能对象受术者
	"""
	def __init__( self ):
		GhostReceiverObject.__init__( self )
		self.addFlag(csdefine.FLAG_CAN_FLY)
		if self.deathTime > 0:
			self.addTimerCallBack( self.deathTime, "destroySelf", () )
		else:
			self.addTimerCallBack( Const.GHOST_RECEIVER_DEAD_TIME, "destroySelf", () )

	def setOwner(self, ownerID):
		"""
		设置拥有者
		"""
		self.ownerID = ownerID

	def getOwnerEntity(self):
		"""
		获得拥有者
		"""
		player = KBEngine.entities.get( self.ownerID,None )
		return player
