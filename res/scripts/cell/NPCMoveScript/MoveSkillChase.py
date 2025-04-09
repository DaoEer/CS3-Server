# -*- coding: utf-8 -*-
import KBEngine
import Math

from NPCMoveScript import MoveBase
import csdefine

class MoveSkillChase( MoveBase.MoveBase ):
	def _chaseEntity( self, entity, chaseEntityID, distance ):
		"""
		追击目标
		"""
		chaseEntity = KBEngine.entities.get( chaseEntityID )
		moveControlID = 0
		if chaseEntity:
			#如果有浮空标志位，设置为不贴地直接移动到点（CST-2421）
			if entity.hasFlag(csdefine.FLAG_CAN_FLY):
				moveControlID = entity.moveToPointExt(Math.Vector3(chaseEntity.position), entity.moveSpeed, distance, True, True )
			else:
				moveControlID = entity.navigatePointExt( Math.Vector3( chaseEntity.position ), entity.moveSpeed, distance )
		
		return moveControlID
	
	def start( self, entity, chaseEntityID, distance, skill ):
		"""
		开始移动
		"""
		return self._chaseEntity( entity, chaseEntityID, distance )
	
	def tick( self, entity, chaseEntityID, distance, skill ):
		"""
		移动循环
		"""
		return self._chaseEntity( entity, chaseEntityID, distance )
	
	def stop( self, entity, chaseEntityID, distance, skill ):
		"""
		vitural  method
		移动中断
		"""
		player = KBEngine.entities.get( chaseEntityID )
		skill.onSkillChaseOver(entity, False)
		if entity.getSyncPosClient() != 0:
			entity.setSyncPosClient( 0 )
			if not entity.isOutOwnerAOI( player ):	# 同时停止客户端的移动
					player.clientEntity( entity.id ).OnStopMoving()
	
	def over( self, entity, chaseEntityID, distance, skill ):
		chaseEntity = KBEngine.entities.get( chaseEntityID )
		if chaseEntity:
			skill.onSkillChaseOver(entity, True)
			# if entity.position.flatDistTo( chaseEntity.position ) <= distance + 0.1: #追击完成
			# 	entity.changeDefaultMove()
	
	def getTickTime( self ):
		"""
		vitural  method
		移动心跳时间，0则为不开启
		"""
		return 0.1