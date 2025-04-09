# -*- coding: utf-8 -*-

from NPCMoveScript import MoveBase

LOOP_ROTATOR_DYC_DIR_TICK = 0.1
class MoveLoopRotator( MoveBase.MoveBase ):
	def rotator( self, entity,  rotatorSpeed ):
		"""
		转一次
		"""
		entity.direction = entity.direction		#底层不会自动同步direction到客户端，必须脚本层手动赋值
		moveControlID = entity.addYawRotator( entity.direction[2] + rotatorSpeed * LOOP_ROTATOR_DYC_DIR_TICK * 2, rotatorSpeed, 0 )
		return moveControlID
		
	def start( self, entity, rotatorSpeed ):
		return self.rotator( entity, rotatorSpeed  )
	
	def tick( self, entity, rotatorSpeed ):
		return self.rotator( entity, rotatorSpeed  )
	
	def getTickTime( self ):
		"""
		vitural  method
		移动心跳时间，0则为不开启
		"""
		return LOOP_ROTATOR_DYC_DIR_TICK

	def isStartTick(self, isCanMove):
		"""
		是否开启心跳
		"""
		return False if self.getTickTime()<=0 else True