# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
from ObjectScript.SpellBox import SpellBoxAdvanced
import csstatus
import Const
import Math

class SpellBoxAdvancedFaZhen( SpellBoxAdvanced.SpellBoxAdvanced ):
	"""
	法阵 
	所有阵眼被交互时，法阵交互完成
	"""
	def __init__( self ):
		SpellBoxAdvanced.SpellBoxAdvanced.__init__( self )
	
	def onInit(self, selfEntity):
		"""
		"""
		SpellBoxAdvanced.SpellBoxAdvanced.onInit( self, selfEntity )
		if selfEntity.isInteractiveState(csdefine.INTERACTIVE_STATE_CREATE):
			selfEntity.changeInteractiveState(csdefine.INTERACTIVE_STATE_OPEN)
			
#----------------------------------------------------------------------------
	def onEnterAccept( self, selfEntity ):
		"""
		virtual method
		进入查收状态
		"""
		SpellBoxAdvanced.SpellBoxAdvanced.onEnterAccept(self, selfEntity)
		self.changeFollowersInteractiveState(selfEntity, csdefine.INTERACTIVE_STATE_ACCEPT)

	def onEnterClosed( self, selfEntity ):
		"""
		virtual method
		进入关闭状态
		"""
		#法阵进入关闭状态 
		SpellBoxAdvanced.SpellBoxAdvanced.onEnterClosed(self, selfEntity)
		self.destroyZhenFa(selfEntity)

#--------------------------------------own method---------------------------------------
	def interruptProgress(self, selfEntity):
		"""
		"""
		#直接销毁掉
		selfEntity.changeInteractiveState(csdefine.INTERACTIVE_STATE_CLOSED)

	def updateProgress(self, selfEntity):
		"""
		更新进度
		"""
		amount = 0
		followers = selfEntity.getFollowers()
		for f in followers:
			if f.interactiveState == csdefine.INTERACTIVE_STATE_RESOLVED:
				amount += 1
		
		#超过设定的完成度达标阈值，法阵完成
		complete = amount / len(selfEntity.getFollowers()) * 100
		if complete >= selfEntity.getComplete():
			selfEntity.completeProgress()

	def changeFollowersInteractiveState(self, selfEntity, state):
		"""
		切换阵眼状态
		"""
		for f in selfEntity.getFollowers():
			f.changeInteractiveState(state)

	def destroyZhenFa(self, selfEntity):
		"""
		"""
		followers = selfEntity.getFollowers()
		while len(followers):
			f = followers.pop(0)
			f.changeInteractiveState(csdefine.INTERACTIVE_STATE_CLOSED)
	
		selfEntity.interruptAllInteractive()
		selfEntity.removeAllFixIDHoldEffect()
		selfEntity.destroySelf()
		