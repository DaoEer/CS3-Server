# -*- coding: utf-8 -*-
import Math

import csdefine
from NPCMoveScript import MoveBase

class MoveNavigatePoint( MoveBase.MoveBase ):
	def start( self, entity, targetPosition, distance = 1.0, faceMovement = True, layer = 0 ):
		"""
		vitural  method
		开始移动
		lineToPoint: 直线移动，不走导航
		"""
		return entity.navigatePointExt( Math.Vector3( targetPosition ), entity.moveSpeed, distance, faceMovement, 0xFFFF, layer )


	def getMovePosition( self, entity, targetPosition, distance = 1.0, faceMovement = True, layer = 0 ):
		"""
		vitural  method
		获得目标位置
		"""
		return Math.Vector3( targetPosition )