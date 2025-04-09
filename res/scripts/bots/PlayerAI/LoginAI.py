# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug

import KST_Config
from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.AI_System import CChatAISys
from PlayerAI.State.AI_Dead import CDeadToRevive
from PlayerAI.State.CStateInterface import eAIState

class LoginAI( AIBase ):
	"""
	"""
	def __init__(self):
		AIBase.__init__(self)
		
		self.actionStatus[eAIState.CChat] = CChatAISys(self)
		self.actionStatus[eAIState.Dead] = CDeadToRevive(self)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		self.owner.GMCommand(self.owner, "set_level", "35")
		self.setTickSpace(KST_Config.Login_talk_tick)
		self.think()
		
	def think(self):
		"""
		"""
		self.changeAIState(eAIState.CChat)
		
AIBase.setClass("LoginAI", LoginAI)