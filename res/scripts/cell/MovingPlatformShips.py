# -*- coding: utf-8 -*-


#python
import Math
#engine
import KBEngine
import KBEDebug
#common
import csdefine
#cell
from CoreObject.PlatformObject import PlatformObject
from CoreInterface.NPCAmbulantInterface import NPCAmbulantInterface

class MovingPlatformShips( PlatformObject, NPCAmbulantInterface ):
	"""
	仙舟渡劫 -- 移动平台
	"""
	def __init__( self ):
		PlatformObject.__init__( self )
		NPCAmbulantInterface.__init__( self )
		spaceEntity = self.getCurrentSpace()
		self.addFlag(csdefine.FLAG_MESH_COLLISION)
		if spaceEntity:
			spaceEntity.addEntityRecord( self.scriptID, self.id )
			spaceEntity.addEntityMailBoxRecord( self.scriptID, self )

	def beforeDestroy( self ):
		"""
		virtual method
		销毁前做一些事
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.delEntityRecord( self.scriptID, self.id )
			spaceEntity.delEntityMailBoxRecord( self.scriptID, self )
		PlatformObject.beforeDestroy( self )
	
	def getNavmeshPath( self ):
		"""
		获取平台寻路数据的路径
		"""
		return self.getScript().navmeshPath
	
	def getSpeed( self ):
		return self.getScript().moveSpeed

	def startMove( self ):
		"""
		开始移动
		"""
		if self.patrolRoute:
			patrolRouteInfo = self.getCurrentSpacePatrolnfo( self.patrolRoute )
			self.startPatrol( self.getSpeed(), True, ( patrolRouteInfo, self.patrolPathNode, csdefine.MOVE_PATROL_MODE_GOTO_POSITION_NOT_FACE ) )
	
	def moveStart( self, mScriptID, mSpeed, misUpdateSpeed, mArgs  = () ):
		NPCAmbulantInterface.moveStart( self, mScriptID, mSpeed, misUpdateSpeed, mArgs )

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.doMoveOver( self, controllerID, userData )
