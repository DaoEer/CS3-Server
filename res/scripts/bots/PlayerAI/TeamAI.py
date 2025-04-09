# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug

import csdefine
import KST_Config

from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.CStateInterface import eAIState
from PlayerAI.State.AI_System import CCleanAISys, CTeamAISys


class TeamAI( AIBase ):
	"""
	"""
	def __init__(self):
		AIBase.__init__(self)
		self.callbackID = 0
		
		self.actionStatus[eAIState.Team] = CTeamAISys(self)
		self.actionStatus[eAIState.CleanSys] = CCleanAISys(self)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		if not self.enterDefaultMap:
			self.owner.GMCommand(self.owner, "setLevel", "30")
			self.enterDefaultSpace()
			return
		
		self.think()
		
	def think(self):
		"""
		"""
		if self.owner.teamID == 0:
			self.changeAIState(eAIState.Team)
		else:
			if self.callbackID == 0:
				self.callbackID = KBEngine.callback(5, self.onCallBack)
	
	def onCallBack(self):
		self.callbackID = 0
		self.changeAIState(eAIState.CleanSys)

		
AIBase.setClass("TeamAI", TeamAI)