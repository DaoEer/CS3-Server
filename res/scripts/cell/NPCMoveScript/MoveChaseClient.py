# -*- coding: utf-8 -*-
import csdefine
import KBEngine
import Math
import KBEDebug
import csarithmetic
import random
import math

from NPCMoveScript import MoveBase


class MoveChaseClient( MoveBase.MoveBase ):	


	def start( self, entity, chaseEntityID, distance ):
		"""
		开始移动
		"""
		return True
	
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
		self.isUpdateMoveTargetPosFromClient = False
		chaseEntity = KBEngine.entities.get( chaseEntityID )
		if chaseEntity:
			if entity.position.flatDistTo( chaseEntity.position ) <= distance: #追击完成
			 	entity.changeDefaultMove()
	
	def getTickTime( self ):
		"""
		vitural  method
		移动心跳时间，0则为不开启
		"""
		return 0.0

	
	def getMovePosition(self, entity, chaseEntityID, distance):
		"""
		vitural  method
		获得目标位置
		"""
		chaseEntity = KBEngine.entities.get( chaseEntityID )
		if not chaseEntity:
			return None
		return chaseEntity.position

	def updateMoveTargetPosFromClient(self, entity, moveTargetPos):
		"""
		"""
		if not entity.canMoveCheck():
			return
		pos = moveTargetPos
		if entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveControlID = entity.moveToPointExt(moveTargetPos, entity.moveSpeed, 0.0, True, True )
		else:
			moveControlID = entity.navigatePointExt( moveTargetPos, entity.moveSpeed, 0.0 )