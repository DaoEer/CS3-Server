# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
from ObjectScript.SpellBox import SpellBoxAdvanced
import csstatus
import Const

class SpellBoxAdvancedZhenYan( SpellBoxAdvanced.SpellBoxAdvanced ):
	"""
	阵眼
	"""
	def __init__( self ):
		SpellBoxAdvanced.SpellBoxAdvanced.__init__( self )

	def onInit(self, selfEntity):
		"""
		"""
		SpellBoxAdvanced.SpellBoxAdvanced.onInit(self, selfEntity)
		master = selfEntity.getMaster()
		if master:
			master.addFollower(selfEntity.id)
			
		if selfEntity.isInteractiveState(csdefine.INTERACTIVE_STATE_CREATE):
			selfEntity.changeInteractiveState(csdefine.INTERACTIVE_STATE_OPEN)
			
#---------------------------------------------------------------
	def onEnterInprogress( self, selfEntity ):
		"""
		virtual method
		进入处理状态
		"""
		SpellBoxAdvanced.SpellBoxAdvanced.onEnterInprogress(self, selfEntity)
		#更新自身进度
		selfEntity.updateProgress()
		
	def onEnterResolved( self, selfEntity ):
		"""
		virtual method
		进入解决状态
		"""
		SpellBoxAdvanced.SpellBoxAdvanced.onEnterResolved(self, selfEntity)
		
		#阵眼通知法阵更新进度
		master = selfEntity.getMaster()
		if master:
			master.updateProgress()
			
	def onEnterClosed( self, selfEntity ):
		"""
		virtual method
		进入关闭状态
		"""
		SpellBoxAdvanced.SpellBoxAdvanced.onEnterClosed(self, selfEntity)
		selfEntity.interruptAllInteractive()
		selfEntity.removeAllFixIDHoldEffect()
		
		#移除自身
		master = selfEntity.getMaster()
		if master:
			master.removeFollower(selfEntity.id)
		
		selfEntity.destroySelf()

#---------------------------------------------------------------
	def interruptProgress(self, selfEntity):
		"""
		"""
		master = selfEntity.getMaster()
		if master and master.isInteractiveState(csdefine.INTERACTIVE_STATE_CLOSED):
			selfEntity.changeInteractiveState(csdefine.INTERACTIVE_STATE_CLOSED)
		else:
			selfEntity.changeInteractiveState(csdefine.INTERACTIVE_STATE_REOPEN)

	def updateProgress(self, selfEntity):
		"""
		更新进度
		"""
		selfEntity.completeProgress()

			