# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import Math
import csdefine
from Trap import Trap
from ConfigObject import PatrolRouteLoader
from CoreInterface.NPCAmbulantInterface import NPCAmbulantInterface


class MoveTrap( Trap, NPCAmbulantInterface ):
	"""
	陷阱类
	"""
	def __init__( self ):
		Trap.__init__( self )
		NPCAmbulantInterface.__init__( self )
		
		if self.hasFlag( csdefine.FLAG_AI_TICK ):
			self.addTimerCallBack( 1.0, "startWalk", ())

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MOVE_TRAP)

	def onWitnessed( self, isWitnessed ):
		"""
		玩家视野范围内才开始执行
		"""
		self.getScript().onWitnessed( self, isWitnessed )
		
		if not self.hasFlag( csdefine.FLAG_AI_TICK ):
			if isWitnessed:
				self.startWalk()
			else:
				self.stopMovingForType( csdefine.NORMAL_MOVE )
	
	def getSpeed( self ):
		return self.getScript().moveSpeed
		
	def getPatrolMoveSpeedMax(self):
		"""
		获取最大巡逻速度
		"""
		return self.getMaxSpeed()


	def getMaxSpeed( self ):
		"""
		限制的最大移动速度
		0：未限制
		"""
		return self.getScript().maxMoveSpeed
	
	def startWalk( self ):
		if self.patrolRoute: #有配巡逻路径的不会随机移动
			if self.patrolPathNode:
				patrolNode = self.patrolPathNode
			else:
				patrolNode = PatrolRouteLoader.g_patrolRouteLoader.getNearestRoutePoint(self.getCurrentSpaceScriptID(), self.patrolRoute,Math.Vector3(self.position))
			patrolRouteInfo = self.getCurrentSpacePatrolnfo(self.patrolRoute)
			self.startPatrol(self.getSpeed(), True, ( patrolRouteInfo, patrolNode, self.patrolMoveMode, self.accVelocity ) )
		elif self.randomWalkRange:
			self.startRandomWalk(self.getSpeed(), True)
	
	def moveStart( self, mScriptID, mSpeed, misUpdateSpeed, mArgs  = () ):
		NPCAmbulantInterface.moveStart( self, mScriptID, mSpeed, misUpdateSpeed, mArgs )

	def getPatrolSpeed( self, speedVal ):
		"""
		获取巡逻速度 有移动速度最大值限定
		"""
		if self.getMaxSpeed()>0:
			return min((speedVal + self.moveSpeedExtra), self.getMaxSpeed())
		else:
			return speedVal + self.moveSpeedExtra

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.doMoveOver( self, controllerID, userData )
		

	def onEnterDead( self ):
		"""
		virtual method
		进入死亡状态
		"""
		self.stopMoving(self.moveScriptID)
		Trap.onEnterDead( self )

	def onActionForbid( self, actForbid ):
		"""
		行为禁止时
		"""
		if actForbid == csdefine.ACTION_FORBID_MOVE:
			self.stopMovingForType(csdefine.SYSTEM_MOVE)
			