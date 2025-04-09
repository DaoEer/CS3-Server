# -*- coding: utf-8 -*-

import Math
import KBEngine
import KBEDebug
import Functions
import csdefine
from NPCMoveScript import MoveBase

class MoveRandomChoiceFormList( MoveBase.MoveBase ): 
		# 随机移到一个点(该点从列表里随机选)
		# 只适用于MonsterRandomChoiceMove脚本的怪物

	def start( self, entity ):
		randomPoint = entity.getScript().getRandomPosFromPosList( entity )
		if randomPoint == ( 0.0, 0.0, 0.0 ):
			return 0
			
		faceMovement = True
		if entity.hasFlag(csdefine.FLAG_CANT_ROTATE):
			faceMovement = False	
		if entity.hasFlag(csdefine.FLAG_CAN_FLY):
			return entity.moveToPointExt( Math.Vector3(randomPoint), entity.moveSpeed, 0.5, faceMovement )
		else:
			return entity.navigatePointExt( Math.Vector3(randomPoint), entity.moveSpeed, 0.5, faceMovement )

	def over( self, entity ):
		"""
		移动循环
		"""
		self.startDormancy( entity, 1.0 ) #开始移动休眠

	def onDormancy( self, entity):
		"""
		移动休眠结束
		"""
		randomPoint = entity.getScript().getRandomPosFromPosList( entity )
		if randomPoint == ( 0.0, 0.0, 0.0 ):
			return
		moveControlID = 0	
		faceMovement = True
		if entity.hasFlag(csdefine.FLAG_CANT_ROTATE):
			faceMovement = False
		if entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveControlID =  entity.moveToPointExt( Math.Vector3(randomPoint), entity.moveSpeed, 0.5, faceMovement )
		else:
			moveControlID =  entity.navigatePointExt( Math.Vector3(randomPoint), entity.moveSpeed, 0.5, faceMovement )

		entity.moveControlID = moveControlID