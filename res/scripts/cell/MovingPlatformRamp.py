# -*- coding: utf-8 -*-


import KBEDebug
import csdefine
import Functions
#cell
from MovingPlatformShade import MovingPlatformShade

class MovingPlatformRamp( MovingPlatformShade ):
	"""
	移动平台 显示——透明——销毁
	"""
	def __init__( self ):
		MovingPlatformShade.__init__( self )
		object = self.getScript()
		if object.displayTime > 0:
			self.addTimerCallBack( object.displayTime, "beginShade", () )

	def startMove( self ):
		"""
		开始移动
		"""
		if self.patrolRoute:
			patrolRouteInfo = self.getCurrentSpacePatrolnfo(self.patrolRoute)
			self.startPatrol(self.getSpeed(), True, ( patrolRouteInfo, self.patrolPathNode, csdefine.MOVE_PATROL_MODE_GOTO_POSITION_NOT_FACE ) )
		
	def startShaderMove( self ):
		pass
		
	def delayShade( self ):
		pass
			
	def beginShade( self ):
		"""开始渐变过程"""
		object = self.getScript()
		if object.rampTime > 0:
			self.shadeTime = "1|" + str( Functions.getTime( object.rampTime ) )
			self.addTimerCallBack( object.rampTime + object.endRampTime, "destroySelf", () )
			
	def showAgain( self ):
		"""
		销毁自身
		"""
		pass
		
	def onWitnessed( self, isWitnessed ):
		"""
		玩家视野范围内才开始执行
		"""
		pass
