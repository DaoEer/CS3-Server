# -*- coding: utf-8 -*-


import KBEDebug
import KBEngine

import Const
import csdefine

from ObjectScript.SpellBox import SpellBox
from ConfigObject.SpellBoxAdvancedState.SpellBoxAdvancedStateBase.SpellBoxAdvancedStateMgr import g_spellBoxAdvancedStateMgr

class SpellBoxAdvanced( SpellBox.SpellBox ):
	"""
	"""
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )

	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		SpellBox.SpellBox.initData( self, data )
		
	def onInit( self, selfEntity ):
		"""
		"""
		#先初始化相关的配置
		self.getGroupState(selfEntity).initEntity(selfEntity)
		#再设置初始化的状态，因为进入初始状态时，可能需要根据配置在初始状态中处理一些事情
		selfEntity.onSetInitState()
		
	def getGroupState( self, selfEntity ):
		"""
		"""
		return g_spellBoxAdvancedStateMgr.getSpellBoxAdvancedGroupState(selfEntity)

	def interruptProgress(self, selfEntity):
		"""
		"""
		selfEntity.changeInteractiveState(csdefine.INTERACTIVE_STATE_REOPEN)
		

#-----------------------------------state--------------------------
	def onEnterCreate( self, selfEntity ):
		"""
		virtual method
		进入创建状态
		"""
		self.getGroupState(selfEntity).onEnter(selfEntity)
		
	def onLeaveCreate( self, selfEntity ):
		"""
		virtual method
		离开创建状态
		"""
		self.getGroupState(selfEntity).onLeave(selfEntity)
	
	def onEnterOpen( self, selfEntity ):
		"""
		virtual method
		进入开启状态
		"""
		self.getGroupState(selfEntity).onEnter(selfEntity)
		selfEntity.addTimerCallBack(0.5, "reTrigger", ())
		
	def onLeaveOpen( self, selfEntity ):
		"""
		virtual method
		离开开启状态
		"""
		self.getGroupState(selfEntity).onLeave(selfEntity)
	
	def onEnterInprogress( self, selfEntity ):
		"""
		virtual method
		进入处理状态
		"""
		self.getGroupState(selfEntity).onEnter(selfEntity)
		
	def onLeaveInprogress( self, selfEntity ):
		"""
		virtual method
		进入解决状态
		"""
		self.getGroupState(selfEntity).onLeave(selfEntity)

	def onEnterResolved( self, selfEntity ):
		"""
		virtual method
		离开解决状态
		"""
		self.getGroupState(selfEntity).onEnter(selfEntity)
		
	def onLeaveResolved( self, selfEntity ):
		"""
		virtual method
		离开完成状态
		"""
		self.getGroupState(selfEntity).onLeave(selfEntity)
		
	def onEnterAccept( self, selfEntity ):
		"""
		virtual method
		进入查收状态
		"""
		self.getGroupState(selfEntity).onEnter(selfEntity)
		if selfEntity.destroyTime >= 0:
			selfEntity.addTimerCallBack( selfEntity.destroyTime, "changeInteractiveState", (csdefine.INTERACTIVE_STATE_CLOSED,) )
		
	def onLeaveAccept( self, selfEntity ):
		"""
		virtual method
		离开结算状态
		"""
		self.getGroupState(selfEntity).onLeave(selfEntity)
		
	def onEnterClosed( self, selfEntity ):
		"""
		virtual method
		进入关闭状态
		"""
		self.getGroupState(selfEntity).onEnter(selfEntity)
		
	def onLeaveClosed( self, selfEntity ):
		"""
		virtual method
		离开关闭状态
		"""
		self.getGroupState(selfEntity).onLeave(selfEntity)

	def onEnterReopen( self, selfEntity ):
		"""
		virtual method
	    进入重启状态
		"""
		self.getGroupState(selfEntity).onEnter(selfEntity)

	def onLeaveReopen( self, selfEntity ):
		"""
		virtual method
		离开重启状态
		"""
		self.getGroupState(selfEntity).onLeave(selfEntity)
		
		
# #----------------------------------------------------------------		
	def tick( self, selfEntity ):
		"""
		"""
		self.getGroupState(selfEntity).tick(selfEntity)
		
	def stateTick( self, selfEntity ):
		"""
		状态内定时器
		"""
		self.getGroupState(selfEntity).stateTick(selfEntity)
		
	def trigger(self, selfEntity, eventType, args, triggerEntity):
		"""
		"""
		self.getGroupState(selfEntity).trigger(selfEntity, eventType, args, triggerEntity)
		
	def destroyForTimeOut(self, selfEntity):
		"""
		"""
		if selfEntity.isInteractiveState(csdefine.INTERACTIVE_STATE_ACCEPT) or selfEntity.isInteractiveState(csdefine.INTERACTIVE_STATE_CLOSED):
			return
		
		self.getGroupState(selfEntity).overTime(selfEntity)
		selfEntity.changeInteractiveState(csdefine.INTERACTIVE_STATE_CLOSED)
		
# #---------------------------------------------------------------
	def startInteractive( self, selfEntity, srcEntity ):
		"""
		开始交互
		"""
		playerEntity = KBEngine.entities.get(srcEntity)
		if playerEntity is None:
			return
		
		#坐骑状态下是否能交互
		if not self.canMountPetGossip and playerEntity.isMountOnPet():
			playerEntity.transformPet( playerEntity.id )
		
		self.getGroupState(selfEntity).startInteractive(selfEntity, playerEntity)
		
	def interruptInteractive( self, selfEntity, srcEntity ):
		"""
		中断交互
		"""
		playerEntity = KBEngine.entities.get(srcEntity)
		if playerEntity is None:
			return
		
		#不在交互列表中
		if srcEntity not in selfEntity.interactiveTargets:
			return
		
		self.getGroupState(selfEntity).interruptInteractive(selfEntity, playerEntity)
		selfEntity.removeInteractiveTarget(srcEntity)
		


