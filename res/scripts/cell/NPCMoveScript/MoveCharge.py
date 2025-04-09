# -*- coding: utf-8 -*-
import Math
import KBEMath
import csdefine
from NPCMoveScript import MoveBase

class MoveCharge( MoveBase.MoveBase ):
	def start( self, entity, targetPosition, distance ):
		"""
		开始
		"""
		if entity.hasFlag(csdefine.FLAG_CAN_FLY):
			movingControlID = entity.moveToPointExt( Math.Vector3(targetPosition), entity.moveSpeed, distance, False )
		else:
			movingControlID = entity.navigatePointExt( Math.Vector3(targetPosition), entity.moveSpeed, distance, False )

		# if movingControlID:
		# 	targetPosition = KBEMath.KBEngine2UnrealPosition( targetPosition )
		# 	entity.allClients.OnChargeToPosition(targetPosition[0], targetPosition[1], targetPosition[2], entity.moveSpeed )
		return movingControlID
		
	def stop( self, entity, targetPosition, distance ):
		"""
		vitural  method
		移动结束
		"""
		#entity.allClients.onEndChargeToPosition()
		pass
	
	def getMovePosition( self, entity, targetPosition, distance ):
		"""
		vitural  method
		获得目标位置
		"""
		return Math.Vector3(targetPosition)