# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug

from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase import SpellBoxAdvancedSubState
from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase import SpellBoxAdvancedBehaviorInstance

# 状态组
class SpellBoxAdvancedGroupState:
	"""
	"""
	def __init__( self, scriptID ):
		"""
		"""
		self._scriptID = scriptID
		self._tickTime = 0
		self._subStates = {}
		self._holdEffectIDs = []
		self._lifeTime = 0
		self._complete = 0
		
		#交互相关
		self._tickInstances = []
		self._overTimeInstances = []
		self._startInteractiveInstances = []
		self._interruptInteractiveInstances = []
	
	def getScriptID( self ):
		"""
		"""
		return self._scriptID
	
	def initData( self, data ):
		"""
		初始化数据
		"""
		#持有效果
		self._holdEffectIDs = data["HoldEffectIDs"]
		#生命时间
		self._lifeTime = data["lifeTime"]
		#完成度
		self._complete = data["complete"]
		
		#心跳间隔
		self._tickTime = data["tickTime"]
		for section in data["tickInst"]:
			obj = SpellBoxAdvancedBehaviorInstance.SpellBoxAdvancedBehaviorInstance()
			obj.initData( section["behavior"] )
			self._tickInstances.append(obj)
		
		#交互
		for section in data["startInteractive"]:
			obj = SpellBoxAdvancedBehaviorInstance.SpellBoxAdvancedBehaviorInstance()
			obj.initData( section["behavior"] )
			self._startInteractiveInstances.append(obj)
		for section in data["interruptInteractive"]:
			obj = SpellBoxAdvancedBehaviorInstance.SpellBoxAdvancedBehaviorInstance()
			obj.initData( section["behavior"] )
			self._interruptInteractiveInstances.append(obj)
			
		#超时结束将要执行的行为
		for section in data["overTimeInst"]:
			obj = SpellBoxAdvancedBehaviorInstance.SpellBoxAdvancedBehaviorInstance()
			obj.initData( section["behavior"] )
			self._overTimeInstances.append(obj)
		
		#加截数据
		subStateDatas = data["subState"]
		for stateID, stateSec in subStateDatas.items():
			obj = SpellBoxAdvancedSubState.SpellBoxAdvancedSubState( stateID )
			obj.initData( stateSec )
			self._subStates[ stateID ] = obj

#----------------------------自身处理-----------------------------------------------			
	def initEntity( self, entity ):
		"""
		"""
		#加载持有效果
		for holdEffectID in self._holdEffectIDs:
			entity.addFixIDHoldEffect(holdEffectID, entity)
		
		#开启心跳
		if self._tickTime > 0:
			entity.addTimerRepeat(self._tickTime, "tick", ())
			
		#生命时间
		if self._lifeTime > 0:
			entity.addTimerCallBack( self._lifeTime, "destroySelfForTimeOut", () )
			
	def tick( self, entity ):
		"""
		tick循环
		"""
		for behaviorInst in self._tickInstances:
			if behaviorInst.check( entity, "" ):
				behaviorInst.do(entity)
				
	def overTime( self, entity ):
		"""
		超时结束
		"""
		for behaviorInst in self._overTimeInstances:
			if behaviorInst.check( entity, "" ):
				behaviorInst.do(entity)

#----------------------相应状态中进行处理-------------------------------------------------		
	def onEnter( self, entity ):
		"""
		进入状态(函数本身不对状态进行切换，只执行配置的行为)
		"""
		state = entity.getInteractiveState()
		if state not in self._subStates:
			return
		
		self._subStates[state].onEnter(entity)
		
	def onLeave( self, entity ):
		"""
		离开状态(函数本身不对状态进行切换，只执行配置的行为)
		"""
		state = entity.getInteractiveState()
		if state not in self._subStates:
			return
		
		self._subStates[state].onLeave(entity)
	
	def trigger( self, entity, eventType, eventArgs, triggerEntity ):
		"""
		触发事件
		"""
		state = entity.getInteractiveState()
		if state not in self._subStates:
			return
		
		self._subStates[state].trigger( entity, eventType, eventArgs, triggerEntity )
	
	def stateTick( self, entity ):
		"""
		状态内定时器
		"""
		state = entity.getInteractiveState()
		if state not in self._subStates:
			return
		
		self._subStates[state].stateTick(entity)

#---------------------------交互-------------------------------------------------		
	def startInteractive(self, entity, srcEntity):
		"""
		开始交互
		"""
		for behaviorInst in self._startInteractiveInstances:
			if behaviorInst.check( entity, "", srcEntity ):
				behaviorInst.do(entity, srcEntity)
		
	def interruptInteractive(self, entity, srcEntity):
		"""
		中断交互
		"""
		for behaviorInst in self._interruptInteractiveInstances:
			if behaviorInst.check( entity, "", srcEntity ):
				behaviorInst.do(entity, srcEntity)