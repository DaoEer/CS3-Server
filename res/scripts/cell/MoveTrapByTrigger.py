# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
from Trap import Trap
from CoreInterface.NPCAmbulantInterface import NPCAmbulantInterface

#MoveTrap是进入玩家视野后开始移动，而MoveTrapByTrigger需要通过某种行为来触发移动
class MoveTrapByTrigger( Trap, NPCAmbulantInterface ):
	"""
	移动陷阱类
	"""
	def __init__( self ):
		Trap.__init__( self )
		NPCAmbulantInterface.__init__( self )
		self._enterIDList = []

	def getSpeed( self ):
		return self.getScript().moveSpeed

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.doMoveOver( self, controllerID, userData )
	
	def CELL_onEnter(self, exposed, enterID):
		"""
		<Exposed Method>
		"""
		if enterID == self.id:
			return
		Trap.CELL_onEnter(self, exposed, enterID)
		self.startWalk(enterID)
		if enterID not in self._enterIDList:
			self._enterIDList.append(enterID)
	
	def CELL_onLeave(self, exposed, enterID):
		"""
		<Exposed Method>
		"""
		if enterID == self.id:
			return
		Trap.CELL_onLeave(self, exposed, enterID)
		
		entity = KBEngine.entities.get(enterID, None)
		if not entity:
			return
		entity.client.onStopMoveByMoveTrap()
		if enterID in self._enterIDList:
			self._enterIDList.remove(enterID)
	
	def startWalk( self, enterID ):
		entity = KBEngine.entities.get(enterID, None)
		if not entity:
			return
		entity.client.onStartMoveByMoveTrap(self.id, self.moveSpeed)
		if not self.isMovingType(csdefine.MOVE_TYPE_PATROL):
			if self.patrolRoute: #有配巡逻路径的不会随机移动
				self.startPatrol(self.getSpeed(), False)
			
	def stopPatrol(self):
		NPCAmbulantInterface.stopPatrol(self)
		for enterID in self._enterIDList:
			entity = KBEngine.entities.get(enterID, None)
			if entity:
				entity.client.onStopMoveByMoveTrap()
		self._enterIDList = []
		
	def stopMoving( self, moveScriptID ):
		"""
		停止移动
		"""
		#如果停止的移动类型和开启的移动类型不一致，并且不是强制停止移动类型，则不能中断当前移动
		return NPCAmbulantInterface.stopMoving( self, moveScriptID )