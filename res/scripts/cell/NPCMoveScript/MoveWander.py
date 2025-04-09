# -*- coding: utf-8 -*-

import Math

import csdefine
import Const
import Functions

from NPCMoveScript import MoveBase

class MoveWander( MoveBase.MoveBase ):
	def start( self, entity, targetPos ):
		moveControlID = 0
		wanderPos, wanderDire = Functions.getWanderMovePoint( Math.Vector3( entity.position ), Math.Vector3( targetPos ), Const.WANDER_RADIUS[ 0 ], Const.WANDER_RADIUS[ 1 ] )
		entity.wanderDirection = Const.WANDER_YAW_DICT.get( wanderDire, 0.0 )
		moveControlID = entity.navigatePointExt( Math.Vector3( wanderPos ), entity.moveSpeed, 0.5, False )
		return moveControlID
	
	def tick( self, entity ):
		"""
		移动循环
		"""
		if entity.hasFlag( csdefine.FLAG_CANT_ROTATE ):
			return
			
		target = KBEngine.entities.get( entity.targetID )
		if not target: return 0
		yaw = csarithmetic.getYawByVector3( target.position - entity.position )
		direction = entity.direction
		direction.z = yaw
		entity.changeDirection(direction, csdefine.REASON_CHANGE_DIR_VOLUNTARY)
		return 0
	
	def getTickTime( self ):
		"""
		vitural  method
		移动循环时间
		"""
		return 0.1
	