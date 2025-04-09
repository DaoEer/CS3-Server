# -*- coding: utf-8 -*-
import Math

import csdefine
from NPCMoveScript import MoveBase

class MoveSoldierRect( MoveBase.MoveBase ):
	def start( self, entity, isCmdMove, targetPosition, targetDir, distance = 1.0, faceMovement = True, layer = 0 ):
		"""
		vitural  method
		CST-10221 士兵列阵：矩形移动
		"""
		return entity.navigatePointExt( Math.Vector3( targetPosition ), entity.moveSpeed, distance, faceMovement, 0xFFFF, layer )


	def getMovePosition( self, entity, isCmdMove, targetPosition, distance = 1.0, faceMovement = True, layer = 0 ):
		"""
		vitural  method
		获得目标位置
		"""
		return Math.Vector3( targetPosition )

	def over( self, entity, isCmdMove, targetPosition, targetDir, distance = 1.0, faceMovement = True, layer = 0 ):
		"""
		vitural  method
		移动结束
		"""
		entity.stopMoving(csdefine.MOVE_TYPE_SOLDIER_RECT)

		entity.direction = targetDir
		
		#如果当前移动是指令移动 则重置isCmdMoving
		if isCmdMove:
			entity.isCmdMoving = False
			entity.onCmdMoveOver([csdefine.MOVE_TYPE_SOLDIER_RECT])



	def tick( self, entity, isCmdMove, targetPosition, targetDir, distance = 1.0, faceMovement = True, layer = 0 ):
		"""
		vitural  method
		移动循环
		必需getTickTime有返回时间才会回调这里
		"""
		if entity.position.flatDistTo(targetPosition)<=distance:
			self.over(entity, isCmdMove, targetPosition, targetDir, distance, faceMovement, layer)
		return 0


	def getTickTime( self ):
		"""
		vitural  method
		移动心跳时间，0则为不开启
		"""
		return 1.0