# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug

import csdefine
import Extra.Extend as Extend
from PlayerAI.State.CStateInterface import CStateBase

class CDeadToRevive(CStateBase):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.callbackID = 0
		self.controllerID = 0
	
	def enter(self):
		#复活
		self.callbackID = KBEngine.callback(1, self.onCallBack)
		self.ai.owner.eventObj.registerEvent("Event_OnStateChanged", self)
		
	def leave(self):
		self.ai.owner.eventObj.unregisterEvent("Event_OnStateChanged", self)
		
		# 离开之前，对自身进行复活(主动离开的话，应该是进入到新的地图中去了)
		if self.ai.owner.state == csdefine.ENTITY_STATE_DEAD:
			self.ai.owner.GMCommand(self.ai.owner, "revive")
		
		if self.callbackID > 0:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
			
		if self.controllerID > 0:
			self.ai.owner.cancelController(self.controllerID)
			self.controllerID = 0
	
	def onEvent(self, name, *argv):
		if name == "Event_OnStateChanged":
			self.onStateChanged(*argv)
	
	def onStateChanged(self, newState, oldState):
		if (oldState == csdefine.ENTITY_STATE_DEAD or oldState == csdefine.ENTITY_STATE_WARN) and newState == csdefine.ENTITY_STATE_FREE :
			self.ai.think()

	def onCallBack(self):
		self.callbackID = 0
		self.ai.owner.GMCommand(self.ai.owner, "revive")
		
	