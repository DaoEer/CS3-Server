# -*- coding: utf-8 -*-
import Math

from NPCMoveScript import MoveBase

class MoveAround( MoveBase.MoveBase ):
	def start( self, entity, targetPosition, distance, targetID ):
		moveControlID = entity.navigatePointExt(  Math.Vector3( targetPosition ), entity.moveSpeed, distance, True )
		if moveControlID:
			entity.turnToPos(targetPosition)
			entity.allClients.CLIENT_OnWalkAroundTarget(targetID)
		
		return moveControlID
	
	def stop(  self, entity, targetPosition, distance, targetID ):
		entity.allClients.CLIENT_OnWalkAroundTargetEnd()

	def getMovePosition( self, entity, targetPosition, distance, targetID ):
		"""
		vitural  method
		获得目标位置
		"""
		return Math.Vector3( targetPosition )