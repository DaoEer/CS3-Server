# -*- coding: utf-8 -*-

"""
usage:
	状态接口类

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
import csconst
import csstatus
import Const
import time



from CoreInterface.ActionFlagInterface import ActionFlagInterface


class StateInterface(ActionFlagInterface):
	"""
	状态基类
	"""
	def __init__( self ):
		"""
		初始化状态。要在Fight初始化之前
		"""
		self.lastState = 0 # 保存上一次的状态
		self.hasStateFlag = True
		ActionFlagInterface.__init__(self)
		self.initOnEnterState()
		self.actCounterIncList( self.stateActionFlags[self.state] )		# 恢复存盘过的状态计数
		self.effectCounter = [0] * len( csdefine.EFFECT_STATE_LIST )
		self.effectState = 0

	def getEnterMethod(self, state):
		"""
		"""
		try:
			enterMethod = getattr( self, self.stateMethodMap.get( state )[0] )
		except ( KeyError, IndexError ) as errorMsg:
			enterMethod = None
			KBEDebug.ERROR_MSG( "getEnterMethod canot find the enter(%i) method, please check STATE_CHANGE_CALL_METHODS_MAPPING!!error:%s" %( old, errorMsg ) )
		return enterMethod

	def getLeaveMethod(self, state):
		"""
		"""
		try:
			leaveMethod = getattr( self, self.stateMethodMap.get( state )[1] )
		except ( KeyError, IndexError ) as errorMsg:
			leaveMethod = None
			KBEDebug.ERROR_MSG( "getLeaveMethod canot find the leave(%i) method, please check STATE_CHANGE_CALL_METHODS_MAPPING!!error:%s" %( old, errorMsg ) )
		return leaveMethod

	def initOnEnterState(self):
		"""
		初始化的时候onEnter初始状态
		"""
		enterMethod = self.getEnterMethod(self.state)
		if enterMethod:
			enterMethod()

	def changeState( self, newState ):
		"""
		<Define method>
		改变状态。
		@param newState	:	新的状态
		@type newState	:	integer
		"""
		KBEDebug.DEBUG_MSG( "Entity id:%s state change from %s to %s." %( self.id, self.state, newState ) )
	
		if self.state == newState:
			return
		self.changeStateBefore( newState, self.state )
		self.lastState = self.state
		self.state = newState
		self.changeStateOver( self.state, self.lastState )

	def changeStateBefore( self, newState, oldState ):
		"""
		状态更新前
		"""
		# 减少原状态的行为限制记数
		self.actCounterDecList( self.stateActionFlags[oldState] )
	
	def changeStateOver( self, newState, oldState ):
		"""
		状态更新后
		"""
		# 增加新状态的行为限制记数
		self.actCounterIncList( self.stateActionFlags[newState] )
		#状态更新回调
		self.onStateChanged( self.state, oldState )

	def onStateChanged( self, new, old ):
		"""
		状态切换。
			@param new	:	更改以后的状态
			@type new	:	integer
			@param old	:	更改以前的状态
			@type old	:	integer
		"""
		leaveMethod = self.getLeaveMethod(old)
		if leaveMethod:
			leaveMethod()
		
		enterMethod = self.getEnterMethod(new)
		if enterMethod:
			enterMethod()
			
		self.triggerSkillEvent( csdefine.SKILL_EVENT_STATE_CHANGE, self.id, {"oldState":old, "newState": new})	
		
	def getState( self ):
		"""
		获取状态。
			@return :	当前状态
			@rtype	:	integer
		"""
		return self.state
		
	def getLastState( self ):
		"""
		获取当前状态之前的状态
		"""
		return self.lastState
		
	def isState( self, state ) :
		"""
		判断是否在某种状态下
		@param			state : MACRO DEFINATION
		@type			state : states defined in csdefine.py
		@rtype				  : bool
		@return				  : 在指定状态下则返回 True
		"""
		return state == self.state

# ----------------------------------------------------------------------------------------------------
	# 效果状态	
	# ----------------------------------------------------------------------------------------------------
	
	def effectStateChanged( self, estate, disabled ):
		"""
		效果改变.
			@param estate		:	效果标识(非组合)
			@type estate		:	integer
			@param disabled		:	效果是否生效
			@param disabled		:	bool
		"""
		self.triggerSkillEvent( csdefine.SKILL_EVENT_EFFECT_STATE_CHANGE, self.id, {"effectState":estate, "disabled": disabled})
		
	def effectStateInc( self, estate ):
		"""
		<Define method>
		添加一个效果状态到记数器
		"""
		try:
			self.effectCounter[estate] += 1		# Counter不得大于255
			if self.effectCounter[estate] == 1:
				self.effectState |=  1<<estate
				self.actCounterIncList( csconst.EFFECT_STATE_TO_ACTION_FLAGS[estate] )
				self.effectStateChanged( estate, True )
		except Exception as e:
			KBEDebug.ERROR_MSG("estate = %d, error:%s"%(estate,e))

	def effectStateIncList( self, estateList ):
		"""
		<Define method>
		添加一个效果状态到记数器
		"""
		for estate in estateList:
			self.effectStateInc(estate)

				
	def effectStateDec( self, estate ):
		"""
		<Define method>
		删除一个效果状态到记数器
		"""
		try:
			if self.effectCounter[estate]>=1:
				self.effectCounter[estate] -= 1
				if self.effectCounter[estate] == 0:
					self.effectState &= ~(1<<estate)
					self.actCounterDecList( csconst.EFFECT_STATE_TO_ACTION_FLAGS[estate] )
					self.effectStateChanged( estate, False )
		except Exception as e:
			KBEDebug.ERROR_MSG("estate = %d, error:%s"%(estate,e))
					
	def effectStateDecList( self, estateList ):
		"""
		<Define method>
		删除一个效果状态到记数器
		"""
		for estate in estate:
			self.effectStateDec(estate) 

	
	def hasEffectState( self, effectState ):
		"""
		是否存在效果状态。
			@return	:	True or False
			@rtype	:	bool
		"""
		try:
			return self.effectCounter[effectState]
		except:
			return False
