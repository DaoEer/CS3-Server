# -*- coding: utf-8 -*-
import Math

import csdefine
from NPCMoveScript import MoveBase

class MoveFlyToPoint( MoveBase.MoveBase ):
	def start( self, entity, targetPosition, distance = 0.0, faceMovement = True, moveVertically = True ):
		"""
		vitural  method
		开始移动
		"""
		if not entity.hasFlag(csdefine.FLAG_CAN_FLY):
			entity.addFlag(csdefine.FLAG_CAN_FLY)
		return entity.moveToPointExt( Math.Vector3( targetPosition ), entity.moveSpeed, distance, faceMovement, moveVertically )

	def over( self, entity, targetPosition, distance = 0.0, faceMovement = True, moveVertically = True ):
		entity.stopMovingForType(csdefine.MOVE_TYPE_STOP)