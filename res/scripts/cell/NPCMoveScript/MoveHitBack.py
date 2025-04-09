# -*- coding: utf-8 -*-
import Math
import math

import csdefine
from NPCMoveScript import MoveBase

import KBEDebug

class MoveHitBack( MoveBase.MoveBase ):
	def start( self, entity, targetPosition ):
		"""
		开始移动
		"""
		hitPosition = Math.Vector3(0,0,0)
		if entity.parent:
			hitPosition = Math.Vector3( entity.parent.positionLocalToWorld( targetPosition ) )
		else:
			hitPosition = targetPosition

		if entity.hasFlag(csdefine.FLAG_CAN_FLY):
			movingControlID = entity.moveToPointExt( hitPosition,  entity.moveSpeed,  0.1, False )
		else:
			movingControlID = entity.navigatePointExt( hitPosition,  entity.moveSpeed, 0.1, False )
		
		return movingControlID
	
	def over( self, entity, targetPosition ):
		"""
		移动结束
		"""
		pass
	