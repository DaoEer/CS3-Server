# -*- coding: utf-8 -*-
import KBEngine
import random
import Math
import math

import Functions

import csconst

class AmbulantInterface( object ):
	"""
	可移动对象基类
	"""
	def __init__( self ):
		object.__init__( self )
		self.initSpeed()
		
	def getSpeed( self ):
		return (self.speed * csconst.RunRatio) / 100.0
	
	def setSpeed( self,  val ):
		"""
		设置移动速度
		"""
		pass
	
	def initSpeed( self ):
		"""
		override
		"""
		pass
	
	#--------------------------------取点方法-------------------------------------------
	def getTargetNearPosition( self, targetPosition, moveDst ):
		"""
		获取目标位置附近的点
		"""
		moveDir = targetPosition - self.position
		moveDir.normalise()
		newTargetPosition = self.position + moveDir * moveDst
		raycastList = self.navmeshRaycast( self.position, newTargetPosition )
		if raycastList:
			newTargetPosition = raycastList[0]
		
		return newTargetPosition
	
	def getTargetAroundPosition( self,  targetPosition, maxRadians ):
		"""
		获取环绕着目标位置的一个点
		"""
		radian = random.uniform( -maxRadians, maxRadians )
		if radian < 0:
			radian = math.pi * 2 + radian
		point = Functions.rotate( (targetPosition[0], targetPosition[2],), (self.position[0], self.position[2] ), radian )
		newTargetPosition = Math.Vector3( (point[0], self.position[1], point[1]) )
		dist = (newTargetPosition-self.position).length
		raycastList = self.navmeshRaycast( self.position, newTargetPosition )
		if raycastList:
			newTargetPosition = raycastList[0]
			
		return newTargetPosition
	
	def getTargetAwayPosition( self,  targetPosition, moveDst = 0.0, distance = 0.0 ):
		"""
		获取远离目标的一个位置
		"""

		moveDir = self.position - targetPosition
		moveDir.normalise()

		if moveDir:
			newTargetPosition = self.position + moveDir * moveDst
		else:
			yaw = self.direction.z
			newTargetPosition = Math.Vector3(self.position.x + moveDst*math.sin(yaw), self.position.y, self.position.z + moveDst*math.cos(yaw))
		raycastList = self.navmeshRaycast( self.position, newTargetPosition )
		if raycastList:
			newTargetPosition = raycastList[0]
		
		return newTargetPosition
