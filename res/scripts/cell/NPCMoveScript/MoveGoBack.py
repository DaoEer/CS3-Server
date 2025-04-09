# -*- coding: utf-8 -*-
import Math
from NPCMoveScript import MoveBase

import csdefine

import KBEDebug

class MoveGoBack( MoveBase.MoveBase ):
	def start( self, entity ):
		"""
		开始移动
		"""
		spawnPosition = (0,0,0)
		if entity.parent:
			spawnPosition = Math.Vector3( entity.parent.positionLocalToWorld( entity.spawnPos ) )
		else:
			spawnPosition = Math.Vector3( entity.spawnPos )
		
		#CST-10996
		if entity.moveSpeed <= 0.0:
			return 0
		
		movingControlID = 0
		if entity.hasFlag(csdefine.FLAG_CAN_FLY):
			movingControlID = entity.moveToPointExt( spawnPosition,  entity.moveSpeed,  0.0, True )
		else:
			movingControlID = entity.navigatePointExt( spawnPosition,  entity.moveSpeed, 0.0, True )
		
		return movingControlID


	def over( self, entity ):
		"""
		移动结束
		"""
		spawnPosition = (0,0,0)
		if entity.parent:
			spawnPosition = Math.Vector3( entity.parent.positionLocalToWorld( entity.spawnPos ) )
		else:
			spawnPosition = Math.Vector3( entity.spawnPos )
		
		if entity.position.flatDistTo( spawnPosition ) > 0.0: #没有移动回原点，直接设置坐标
			entity.position = spawnPosition
		if entity.gobackTimer:
			entity.popTimer(entity.gobackTimer)
			entity.gobackTimer = 0
		entity.stopMoving( csdefine.MOVE_TYPE_GOBACK )
		#默认是走回出生点重置出生点朝向
		if not entity.hasFlag(csdefine.FLAG_NOT_RESET_SPAWNDIR):
			entity.changeDirection(entity.spawnDir, csdefine.REASON_CHANGE_DIR_FORCE)
		if entity.isState( csdefine.ENTITY_STATE_RESET ):
			entity.changeState( csdefine.ENTITY_STATE_FREE )


	def getMovePosition( self, entity, *args ):
		"""
		vitural  method
		获得目标位置
		"""
		spawnPosition = (0,0,0)
		if entity.parent:
			spawnPosition = Math.Vector3( entity.parent.positionLocalToWorld( entity.spawnPos ) )
		else:
			spawnPosition = Math.Vector3( entity.spawnPos )

		return spawnPosition
		
	
		
