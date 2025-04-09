# -*- coding: utf-8 -*-
import csdefine
import KBEngine
import Math
import csarithmetic

from NPCMoveScript import MoveBase

class MoveChaseOptimize( MoveBase.MoveBase ):	
	def start( self, entity, chaseEntityID, distance ):
		"""
		vitural  method
		开始移动
		"""
		return entity.moveToEntityExt( chaseEntityID, distance )
	
	def stop( self, entity, chaseEntityID, distance ):
		"""
		vitural  method
		移动结束
		"""
		#配合录像表现 停止移动时，设置怪物转向追击目标
		
		targetEntity = KBEngine.entities.get(chaseEntityID, None)
		if targetEntity:
			entity.direction.z  = csarithmetic.getYawByVector3(targetEntity.position - entity.position)