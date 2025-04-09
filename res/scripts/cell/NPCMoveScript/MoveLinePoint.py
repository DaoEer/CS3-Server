# -*- coding: utf-8 -*-
import Math

import csdefine
from NPCMoveScript import MoveBase

class MoveLinePoint( MoveBase.MoveBase ):
	def start( self, entity, targetPosition, distance = 0.0, faceMovement = True, moveVertically = True ):
		"""
		vitural  method
		开始移动
		"""
		return entity.moveToPointExt( Math.Vector3( targetPosition ), entity.moveSpeed, distance, faceMovement, moveVertically )