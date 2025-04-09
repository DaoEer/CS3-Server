# -*- coding: utf-8 -*-
"""
usage:
	交互状态接口类

attribute:
	pass

member function:
	pass

callback:
	pass

"""


#common
import KBEDebug
import csdefine

STATE_CHANGE_CALL_METHODS_MAPPING = { 
	csdefine.INTERACTIVE_STATE_CREATE :				( "onEnterCreate", "onLeaveCreate" ),
	csdefine.INTERACTIVE_STATE_OPEN : 				( "onEnterOpen", "onLeaveOpen" ),	
	csdefine.INTERACTIVE_STATE_INPROGRESS : 		( "onEnterInprogress", "onLeaveInprogress"),
	csdefine.INTERACTIVE_STATE_RESOLVED : 			( "onEnterResolved", "onLeaveResolved"),
	csdefine.INTERACTIVE_STATE_ACCEPT: 				( "onEnterAccept", "onLeaveAccept"),
	csdefine.INTERACTIVE_STATE_CLOSED :				( "onEnterClosed", "onLeaveClosed"),
	csdefine.INTERACTIVE_STATE_REOPEN :				( "onEnterReopen", "onLeaveReopen"),
}
GET_ENTER_STATE_CALL_METHOD = lambda entity, state:getattr( entity, STATE_CHANGE_CALL_METHODS_MAPPING.get( state )[0] )
GET_LEAVE_STATE_CALL_METHOD = lambda entity, state:getattr( entity, STATE_CHANGE_CALL_METHODS_MAPPING.get( state )[1] )

class InteractiveStateInterface:
	"""
	交互状态接口
	"""

	def __init__( self ):
		"""
		初始化状态
		"""
		pass
		
	def onSetInitState(self):
		"""
		"""
		self.interactiveState = csdefine.INTERACTIVE_STATE_CREATE
		self._enterState(csdefine.INTERACTIVE_STATE_CREATE)

	def changeInteractiveState(self, newState):
		"""
		"""
		if self.interactiveState == newState:
			return
		
		KBEDebug.DEBUG_MSG( "Entity id:%s InteractiveState change from %s to %s." %( self.id, self.interactiveState, newState ) )
		
		oldState = self.interactiveState
		self._changeInteractiveStateBefore( newState, oldState )
		self.interactiveState = newState
		self._changeInteractiveStateOver( newState, oldState )

	def _changeInteractiveStateBefore( self, newState, oldState ):
		"""
		"""
		pass


	def _changeInteractiveStateOver( self, newState, oldState ):
		"""
		状态更新后
		"""
		#状态更新回调
		self.onInteractiveStateChanged( newState, oldState )
	
	def getInteractiveState( self ):
		"""
		获取状态。
			@return :	当前状态
			@rtype	:	integer
		"""
		return self.interactiveState
		
	def getLastInteractiveState( self ):
		"""
		获取当前状态之前的状态
		"""
		return self.lastInteractiveState
		
	def isInteractiveState( self, state ) :
		"""
		判断是否在某种状态下
		@param			state : MACRO DEFINATION
		@type			state : states defined in csdefine.py
		@rtype				  : bool
		@return				  : 在指定状态下则返回 True
		"""
		return state == self.interactiveState

	def onInteractiveStateChanged( self, new, old ):
		"""
		状态切换。
			@param new	:	更改以后的状态
			@type new	:	integer
			@param old	:	更改以前的状态
			@type old	:	integer
		"""
		self._leaveState(old)
		self._enterState(new)

	def _leaveState( self, old ):
		"""
		"""
		try:
			leaveMethod = GET_LEAVE_STATE_CALL_METHOD( self, old )
		except ( KeyError, IndexError ) as errorMsg:
			leaveMethod = None
			KBEDebug.ERROR_MSG( "onInteractiveStateChanged canot find the leave(%i) method, please check STATE_CHANGE_CALL_METHODS_MAPPING!!error:%s" %( old, errorMsg ) )
			
		if leaveMethod:
			self.doLeaveActions(old)
			leaveMethod()
	
	def _enterState( self, new ):
		"""
		"""
		try:
			enterMethod = GET_ENTER_STATE_CALL_METHOD( self, new )
		except ( KeyError, IndexError ) as errorMsg:
			enterMethod = None
			KBEDebug.ERROR_MSG( "onInteractiveStateChanged canot find the enter(%i) method, please check STATE_CHANGE_CALL_METHODS_MAPPING!! error:%s" %( new, errorMsg ) )
			
		if enterMethod:
			self.doEnterActions(new)
			enterMethod()

	def doEnterActions(self, interactiveState):
		"""
		执行进入状态行为
		"""
		#KBEDebug.ERROR_MSG("self.id = %d, interactiveState = %d DoEnteractions!"%(self.id, interactiveState))
		pass

	def doLeaveActions(self, interactiveState):
		"""
		执行离开状态行为
		"""
		#KBEDebug.ERROR_MSG("self.id = %d, interactiveState = %d DoLeaveactions!"%(self.id, interactiveState))
		pass

	def onEnterCreate( self ):
		"""
		virtual method
		进入创建状态
		"""
		self.getScript().onEnterCreate(self)
		
	def onLeaveCreate( self ):
		"""
		virtual method
		离开创建状态
		"""
		self.getScript().onLeaveCreate(self)
	
	def onEnterOpen( self ):
		"""
		virtual method
		进入开启状态
		"""
		self.getScript().onEnterOpen(self)
		
	def onLeaveOpen( self ):
		"""
		virtual method
		离开开启状态
		"""
		self.getScript().onLeaveOpen(self)
	
	def onEnterInprogress( self ):
		"""
		virtual method
		进入处理状态
		"""
		self.getScript().onEnterInprogress(self)
		
	def onLeaveInprogress( self ):
		"""
		virtual method
		离开处理状态
		"""
		self.getScript().onLeaveInprogress(self)
		
	def onEnterResolved( self ):
		"""
		virtual method
		进入解决状态
		"""
		self.getScript().onEnterResolved(self)
		
	def onLeaveResolved( self ):
		"""
		virtual method
		离开解决状态
		"""
		self.getScript().onLeaveResolved(self)
		
	def onEnterAccept( self ):
		"""
		virtual method
		进入查收状态
		"""
		self.getScript().onEnterAccept(self)
		
	def onLeaveAccept( self ):
		"""
		virtual method
		离开查收状态
		"""
		self.getScript().onLeaveAccept(self)
		
	def onEnterClosed( self ):
		"""
		virtual method
		进入关闭状态
		"""
		self.getScript().onEnterClosed(self)
		
	def onLeaveClosed( self ):
		"""
		virtual method
		离开关闭状态
		"""
		self.getScript().onLeaveClosed(self)

	def onEnterReopen( self ):
		"""
		virtual method
		进入重启状态
		"""
		self.getScript().onEnterReopen(self)

	def onLeaveReopen( self ):
		"""
		virtual method
		进入重启状态
		"""
		self.getScript().onLeaveReopen(self)

