# -*- coding: utf-8 -*-
import Math
import random
import KBEngine
import KBEDebug
import Functions
from NPCMoveScript import MoveBase

import csdefine

class MoveRandom( MoveBase.MoveBase ): 
	#随机移到一个点
	def start( self, entity ):
		k = 1
		while k < 5:
			k += 1
			positionList = entity.getRandomPoints( entity.spawnPos, float(entity.randomWalkRange), 1, entity.layer, 0xFFFF )
			#取到点了，退出循环
			if len( positionList ) != 0:
				break
				
		if positionList:
			randomPoint = positionList[0]
			return entity.navigatePointExt(Math.Vector3(randomPoint), entity.moveSpeed, 0.5)
		return 0

	def over( self, entity ):
		"""
		移动循环
		"""

		self.startDormancy( entity, float(random.randint(3,10)) ) #开始移动休眠

	def onDormancy( self, entity):
		"""
		移动休眠结束
		"""
		k = 1
		while k < 5:
			k += 1
			positionList = entity.getRandomPoints( entity.spawnPos, float(entity.randomWalkRange), 1, entity.layer, 0xFFFF )
			#取到点了，退出循环
			if len( positionList ) != 0:
				break
				
		if positionList:
			randomPoint = positionList[0]
			return entity.navigatePointExt(Math.Vector3(randomPoint), entity.moveSpeed, 0.5)
		return 0