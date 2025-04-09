# -*- coding: utf-8 -*-
import Math
import KBEDebug
import KBEngine

import csdefine
from NPCMoveScript import MoveBase

class MoveNavigatePointTest( MoveBase.MoveBase ):
	def __init__( self, moveScriptID ):
		MoveBase.MoveBase.__init__(self, moveScriptID)
		self.navigatePoints = [Math.Vector3((0,0,0)), Math.Vector3((0,0,0)), Math.Vector3((0,0,0))]
	
	def _navigateToPoint( self, entity, targetPosition, distance):
		"""
		vitural  method
		移动到目标点
		"""
		self.navigatePoints[0] = Math.Vector3(self.navigatePoints[1])
		self.navigatePoints[1] = Math.Vector3(self.navigatePoints[2])
		self.navigatePoints[2] = Math.Vector3(entity.position)
		#posList = KBEngine.collideVertical(entity.spaceID, entity.layer, entity.position, 6, -6 )
		#if len(posList) > 0:
		#	tempPos = Math.Vector3(posList[0])
		#	for pos in posList:
		#		posVector = Math.Vector3(pos)
		#		if posVector.distTo(entity.position) < tempPos.distTo(entity.position):
		#			tempPos = posVector
		#	if abs( entity.position.y - tempPos.y ) > 1.0:
		#		entity.position = Math.Vector3(tempPos)
		return entity.navigatePointExt( Math.Vector3( targetPosition ), entity.moveSpeed, distance)

	def start( self, entity, targetPosition, distance):
		"""
		vitural  method
		开始移动
		"""
		self.startPos = Math.Vector3(entity.position)
		return self._navigateToPoint(entity, Math.Vector3( targetPosition ), distance)
		
	def tick(self, entity, targetPosition, distance):
		"""
		移动循环
		"""
		if self.navigatePoints[0].distTo(Math.Vector3((0,0,0))) > 0 and self.navigatePoints[1].distTo(Math.Vector3((0,0,0))) > 0 \
		and self.startPos.distTo(self.navigatePoints[0]) > 0 and self.startPos.distTo(self.navigatePoints[1]) > 0:
			#flatDistTo计算平面距离，distTo计算三维空间距离
			moveDist = entity.moveSpeed * self.getTickTime()
			if entity.position.distTo(targetPosition) > distance + 0.1 and self.navigatePoints[2].distTo(self.navigatePoints[1]) <= 0.2 \
			and self.navigatePoints[1].distTo(self.navigatePoints[0]) <= 0.2:
				KBEDebug.ERROR_MSG("NavigateError:can't go to targetPosition. start(%s) pos1(%s) pos2(%s) target(%s)" %(self.startPos, self.navigatePoints[1], \
				self.navigatePoints[2], targetPosition))
				entity.destroy()
				return 0
				
		return self._navigateToPoint(entity, Math.Vector3( targetPosition ), distance)
	
	def over(self, entity, targetPosition, distance):
		"""
		移动循环
		"""
		if entity.position.distTo(targetPosition) <= distance + 0.1:
			entity.destroy()
		
	def getTickTime( self ):
		"""
		vitural  method
		移动心跳时间，0则为不开启
		"""
		return 0.3

	def getMovePosition( self, entity, targetPosition, distance):
		"""
		vitural  method
		获得目标位置
		"""
		return Math.Vector3( targetPosition )