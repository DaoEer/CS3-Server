# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug

import KST_Config
from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.AI_Run import CRunRandom
from PlayerAI.State.AI_System import CPetAISys, CTeamAISys
from PlayerAI.State.CStateInterface import eAIState

class RandWalkAI( AIBase ):
	"""
	"""
	def __init__(self):
		AIBase.__init__(self)
		
		self.actionStatus[eAIState.Run] = CRunRandom(self)
		self.actionStatus[eAIState.Pet] = CPetAISys(self)
		self.actionStatus[eAIState.Team] = CTeamAISys(self)
		
	def onEnterWorld(self):
		"""
		"""
		pass
		
	def onEnterSpace(self):
		"""
		KBEngine method
		entity 进入一个新的space
		"""
		pass
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		if not self.enterDefaultMap:
			self.enterDefaultSpace()
			return
		
		self.think()
		
	def think(self):
		"""
		"""
		spaceInfo = KST_Config.walk_map
		spaceScriptID = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if spaceScriptID != spaceInfo[0]:
			self.owner.GMCommand(self.owner, "goto", "{} {}".format(spaceInfo[0], spaceInfo[1]))
			return
		
		if KST_Config.pet and self.owner.currentPetUID == 0:
			self.changeAIState(eAIState.Pet)
			return
			
		if KST_Config.walk_create_team and self.owner.teamID == 0:
			self.changeAIState(eAIState.Team)
			return

		#watch状态下宠物不出战
		if KST_Config.walk_watch_flag and not KST_Config.pet:
			self.owner.GMCommand(self.owner, "watch")
		self.changeAIState(eAIState.Run)
		
	def getLoop(self):
		return KST_Config.walk_loop
		
	def getWalkRadius(self):
		return KST_Config.walk_radius
		
AIBase.setClass("RandWalkAI", RandWalkAI)