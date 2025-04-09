# -*- coding: utf-8 -*-
import csdefine
import KBEngine
import Math

from NPCMoveScript import MoveBase


class MoveChase( MoveBase.MoveBase ):	
	def _chaseEntity( self, entity, chaseEntityID, distance ):
		"""
		追击目标
		"""
		chaseEntity = KBEngine.entities.get( chaseEntityID )
		entity.cancelController( "Movement" )
		moveControlID = 0
		if chaseEntity:
			#如果有浮空标志位，设置为不贴地直接移动到点（CST-2421）
			if entity.hasFlag(csdefine.FLAG_CAN_FLY):
				moveControlID = entity.moveToPointExt(Math.Vector3(chaseEntity.position), entity.moveSpeed, distance, True, True )
			else:
				moveControlID = entity.navigatePointExt( Math.Vector3( chaseEntity.position ), entity.moveSpeed, distance )

		return moveControlID

	def start( self, entity, chaseEntityID, distance ):
		"""
		开始移动
		"""
		return self._chaseEntity( entity, chaseEntityID, distance )
	
	def tick( self, entity, chaseEntityID, distance ):
		"""
		移动循环
		"""
		chaseEntity = KBEngine.entities.get(chaseEntityID,None)
		if chaseEntity:
			return self._chaseEntity( entity, chaseEntityID, distance )
		else:
			entity.stopMoving(csdefine.MOVE_TYPE_CHASE)
			return 0
	
	def stop( self, entity, chaseEntityID, distance ):
		"""
		vitural  method
		移动结束
		"""
		player = KBEngine.entities.get( chaseEntityID )
		if entity.getSyncPosClient() != 0:
			entity.setSyncPosClient( 0 )
			if not entity.isOutOwnerAOI( player ):	# 同时停止客户端的移动
				player.clientEntity( entity.id ).OnStopMoving()
	
	def over( self, entity, chaseEntityID, distance ):
		"""
		移动结束
		"""
		if entity.moveControlID == 0 and entity.moveTimerID == 0:
			entity.changeDefaultMove()
		chaseEntity = KBEngine.entities.get( chaseEntityID )
		if chaseEntity:
			if entity.position.flatDistTo( chaseEntity.position ) <= distance + 0.1: #追击完成
				entity.changeDefaultMove()
	
	def getTickTime( self ):
		"""
		vitural  method
		移动心跳时间，0则为不开启
		"""
		return 0.3

	
	def getMovePosition(self, entity, chaseEntityID, distance):
		"""
		vitural  method
		获得目标位置
		"""
		chaseEntity = KBEngine.entities.get( chaseEntityID )
		if not chaseEntity:
			return None
		return chaseEntity.position