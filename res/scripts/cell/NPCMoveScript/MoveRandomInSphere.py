# -*- coding: utf-8 -*-
import math
import Math
import KBEngine
import KBEDebug
import Functions
import csdefine
import random
import csarithmetic
from NPCMoveScript import MoveBase

class MoveRandomInSphere( MoveBase.MoveBase ): 
	"""
	在球形里随机移动
	"""
	def start( self, entity, centerPosition, radius, aiCmd1, aiCmd2, maxTime, minTime):

		#entity.setTemp("MoveRandomInSpherePos",Math.Vector3(centerPosition))
		# 改成在球内接正方体的8个顶点随机移动
		length = 2 * radius/math.sqrt(3)
		SpherePosList = [Math.Vector3(centerPosition.x-length, centerPosition.y-length, centerPosition.z-length ), Math.Vector3(centerPosition.x+length, centerPosition.y-length, centerPosition.z-length),\
		Math.Vector3(centerPosition.x+length, centerPosition.y-length, centerPosition.z-length), Math.Vector3(centerPosition.x+length, centerPosition.y-length, centerPosition.z+length),\
		Math.Vector3(centerPosition.x-length, centerPosition.y+length, centerPosition.z-length), Math.Vector3(centerPosition.x+length, centerPosition.y+length, centerPosition.z-length),\
		Math.Vector3(centerPosition.x-length, centerPosition.y+length, centerPosition.z+length), Math.Vector3(centerPosition.x+length, centerPosition.y+length, centerPosition.z+length)]

		entity.setTemp("SpherePosList",SpherePosList)
		#randomPoint = csarithmetic.getPositionBySphere(centerPosition, radius)
		random.shuffle(SpherePosList)
		randomPoint = SpherePosList[0]
		
		faceMovement = True
		if entity.hasFlag(csdefine.FLAG_CANT_ROTATE):
			faceMovement = False	
		if entity.hasFlag(csdefine.FLAG_CAN_FLY):
			return entity.moveToPointExt( Math.Vector3(randomPoint), entity.moveSpeed, 0.5, faceMovement )
		else:
			return entity.navigatePointExt( Math.Vector3(randomPoint), entity.moveSpeed, 0.5 )

	def over( self, entity, centerPosition, radius, aiCmd1, aiCmd2, maxTime, minTime):
		"""
		移动循环
		"""
		entity.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (entity.id, entity.scriptID, aiCmd1))
		dormancyTime = random.uniform(minTime, maxTime)
		self.startDormancy( entity, dormancyTime ) #开始移动休眠

	def onDormancy( self, entity, centerPosition, radius, aiCmd1, aiCmd2, maxTime, minTime):
		"""
		移动休眠结束
		"""
		entity.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (entity.id, entity.scriptID, aiCmd2))
		#randomPoint = csarithmetic.getPositionBySphere(entity.queryTemp("MoveRandomInSpherePos"), radius)
		length = 2 * radius/math.sqrt(3)
		tempList = list(entity.queryTemp("SpherePosList", []))
		for i in list(tempList):
			if entity.position.distTo(i) <= length + 0.5:
				tempList.remove(i)
		random.shuffle(tempList)
		randomPoint = tempList[0]
		moveControlID = 0
		faceMovement = True
		if entity.hasFlag(csdefine.FLAG_CANT_ROTATE):
			faceMovement = False
		if entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveControlID =  entity.moveToPointExt( Math.Vector3(randomPoint), entity.moveSpeed, 0.5, faceMovement )
		else:
			moveControlID =  entity.navigatePointExt( Math.Vector3(randomPoint), entity.moveSpeed, 0.5 )

		entity.moveControlID = moveControlID