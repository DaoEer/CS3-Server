# -*- coding: utf-8 -*-
import Math

import csdefine
from NPCMoveScript import MoveBase

import KBEDebug

class MoveReversePatrol( MoveBase.MoveBase ):
	#移动到巡逻路线上反向的一个点
	def start( self, entity, patrolRouteInfo, moveRoutePoint=1, patrolMoveMode = csdefine.MOVE_PATROL_MODE_NAVIGATE_POSITION, accSpeed = 0.0 ):
		"""
		vitural  method
		开始移动
		patrolRoute：巡逻路线id
		moveRoutePoint：移动到巡逻路线上的第几个点
		patrolMoveMode：巡逻方式
			MOVE_PATROL_MODE_NAVIGATE_POSITION	：通过导航数据来进行巡逻
			MOVE_PATROL_MOVE_GOTO_POSITION    		：直接移动到目标点来进行巡逻，无视导航数据
		accSpeed:巡逻加速度 
		"""
		moveControlID = 0
		#entity.setPatrolSpeed( accSpeed ) #设置循环加速度
		if patrolRouteInfo:
			nodeInfo = patrolRouteInfo.get( moveRoutePoint ) #取出巡逻点信息
			if accSpeed!=0:
				if entity.getPatrolMoveSpeedMax() > 0:
					if entity.getPatrolSpeed(entity.moveSpeed)<entity.getPatrolMoveSpeedMax():
						entity.accelerateSpeedTimerID = entity.addTimerRepeat(0.1, "accelerateSpeed", (accSpeed,)) #加速移动
				else:
					entity.accelerateSpeedTimerID = entity.addTimerRepeat(0.1, "accelerateSpeed", (accSpeed,)) #加速移动

			if patrolMoveMode == csdefine.MOVE_PATROL_MODE_GOTO_POSITION_NOT_FACE:
				moveControlID = entity.moveToPointExt( Math.Vector3( nodeInfo[ "position" ] ), entity.getPatrolSpeed(entity.moveSpeed), 0.1, False ) 
				
			elif patrolMoveMode == csdefine.MOVE_PATROL_MODE_NAVIGATE_POSITION_NOT_FACE:
				moveControlID = entity.navigatePointExt( Math.Vector3( nodeInfo[ "position" ] ), entity.getPatrolSpeed(entity.moveSpeed), 0.1, False )
				
			elif patrolMoveMode == csdefine.MOVE_PATROL_MOVE_GOTO_POSITION or  entity.hasFlag(csdefine.FLAG_CAN_FLY):
				moveControlID = entity.moveToPointExt( Math.Vector3( nodeInfo[ "position" ] ), entity.getPatrolSpeed(entity.moveSpeed), 0.1, True ) 
				
			else:
				moveControlID = entity.navigatePointExt( Math.Vector3( nodeInfo[ "position" ] ), entity.getPatrolSpeed(entity.moveSpeed), 0.1, True )
		
		return moveControlID
	
	def over( self, entity, patrolRouteInfo, moveRoutePoint=1, patrolMoveMode = csdefine.MOVE_PATROL_MODE_NAVIGATE_POSITION, accSpeed = 0.0  ):
		"""
		vitural  method
		移动结束
		"""
		if entity.accelerateSpeedTimerID:
			entity.popTimer(entity.accelerateSpeedTimerID)
			entity.accelerateSpeedTimerID = 0
		nodeInfo = patrolRouteInfo[ moveRoutePoint ] #取出巡逻点信息
		stayTime = nodeInfo.get( "stayTime", 0.0 )
		self.startDormancy( entity, stayTime ) #开始移动休眠
	
	def onDormancy( self, entity, patrolRouteInfo, moveRoutePoint=1, patrolMoveMode = csdefine.MOVE_PATROL_MODE_NAVIGATE_POSITION, accSpeed = 0.0 ):
		"""
		移动休眠结束
		"""
		nodeInfo = patrolRouteInfo[ moveRoutePoint ] #取出巡逻点信息
		if min( patrolRouteInfo.keys() ) == moveRoutePoint:	# 在第一个点
			moveRoutePoint = max( patrolRouteInfo.keys() )
		else:
			moveRoutePoint -= 1 #移动到上个点
			
		entity.moveStart( self.getScriptID(), entity.moveSpeed, entity.isUpdateSpeed, ( patrolRouteInfo, moveRoutePoint, patrolMoveMode, accSpeed ) ) #移动到下个点

	def getMovePosition( self, entity, patrolRouteInfo, moveRoutePoint=1, patrolMoveMode = csdefine.MOVE_PATROL_MODE_NAVIGATE_POSITION, accSpeed = 0.0 ):
		"""
		vitural  method
		获得目标位置
		"""
		if patrolRouteInfo:
			nodeInfo = patrolRouteInfo[ moveRoutePoint ] #取出巡逻点信息
			return Math.Vector3( nodeInfo[ "position" ] )
		return None