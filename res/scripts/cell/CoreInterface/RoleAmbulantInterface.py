# -*- coding: utf-8 -*-
import csconst
import csdefine

from CoreInterface import AmbulantInterface

class RoleAmbulantInterface( AmbulantInterface.AmbulantInterface  ):
	def __init__( self ):
		AmbulantInterface.AmbulantInterface.__init__( self )
		self.initSpeed()
	
	def initSpeed( self ):
		"""
		override
		"""
		self.setSpeed(  (self.speed * csconst.RunRatio) / 100.0 )

	def canMoveCheck( self, isForceMove = False ):
		"""
		@param isForceMove:	是否受迫移动
		能否移动检测
		"""
		if self.state == csdefine.ENTITY_STATE_DEAD:
			return False
		if self.actionForbidSign( csdefine.ACTION_FORBID_MOVE ) and not isForceMove:
			return False
		return True

	def stopMoving( self, moveScriptID ):
		"""
		停止移动
		"""
		if self.roleMoveType == csdefine.MOVE_TYPE_BACK or self.roleMoveType == csdefine.MOVE_TYPE_TRACE:
			return False
		self.client.CLIENT_NotifyStopMoving()
		return True
	
	def stopMovingForType( self, moveType ):
		if self.roleMoveType == csdefine.MOVE_TYPE_BACK or self.roleMoveType == csdefine.MOVE_TYPE_TRACE:
			return False
		if self.getClient():
			self.client.CLIENT_NotifyStopMoving()
		return True

	def setSpeed( self,  val ):
		"""
		设置移动速度
		"""
		if self.tempSpeed != 0:
			self.moveSpeed = (self.tempSpeed * 1.0)/100
		else:
			self.moveSpeed = val
	
	def timerRemoveAxternalVelocity( self, winDir0, winDir1, winDir2, speed ):
		self.allClients.RemoveAxternalVelocity( winDir0, winDir1, winDir2, speed )