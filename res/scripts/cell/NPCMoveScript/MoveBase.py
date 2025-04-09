# -*- coding: utf-8 -*-
import Vector
import Math
import math
import random

import csconst
import csdefine

from ConfigObject import PatrolRouteLoader

class MoveBase( object ):
	def __init__( self, moveScriptID ):
		object.__init__( self )
		self.moveScriptID = moveScriptID
	
	def getScriptID( self ):
		return self.moveScriptID
		
	def start( self, entity, *args ):
		"""
		vitural  method
		开始移动
		"""
		return 0
	
	def failure( self, entity, *args ):
		"""
		vitural  method
		移动失败，不能打断当前移动, 并没有改变entity的移动模式
		"""
		pass
	
	def stop( self, entity, *args ):
		"""
		vitural  method
		移动被打断
		"""
		pass
	
	def over( self, entity, *args ):
		"""
		vitural  method
		移动结束
		"""
		pass
	
	def tick( self, entity, *args ):
		"""
		vitural  method
		移动循环
		必需getTickTime有返回时间才会回调这里
		"""
		return 0
	
	def startDormancy( self, entity, dormancyTime ):
		"""
		开启移动休眠
		"""
		entity.moveStartDormancy( dormancyTime )
	
	def onDormancy( self, entity, *args ):
		"""
		vitural  method
		移动休眠
		"""
		pass
	
	def isCanBreak( self, entity, newMoveType ):
		"""
		是否能打断当前移动
		"""
		if  csconst.MOVE_TYPE_DICT[ newMoveType ] > csconst.MOVE_TYPE_DICT[ self.getScriptID() ]:
			return False
			
		return True

	def getTickTime( self ):
		"""
		vitural  method
		移动心跳时间，0则为不开启
		"""
		return 0

	def isStartTick(self, isCanMove):
		"""
		是否开启心跳
		"""
		if not isCanMove:
			return False
		return False if self.getTickTime()<=0 else True


	def getMovePosition( self, entity, *args ):
		"""
		vitural  method
		获得目标位置
		"""
		return (0.0, 0.0, 0.0)

	#----------------------巡逻路线------------------------------
	
	def getCurrentSpacePatrolnfo( self, spaceScriptID, patrolRoute ):
		"""
		获取当前地图的某条巡逻路线
		"""
		if patrolRoute:
			return PatrolRouteLoader.g_patrolRouteLoader.getPatrolRoute( spaceScriptID, patrolRoute )
			
		return None

	def updateMoveTargetPosFromClient(self, entity, moveTargetPos):
		"""
		vitural  method
		"""
		pass