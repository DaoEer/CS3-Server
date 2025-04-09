# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug

import KST_Config
from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.AI_System import CPetAISys, CItemAISys
from PlayerAI.State.AI_Teleport import CTeleportRepeat
from PlayerAI.State.AI_Dead import CDeadToRevive
from PlayerAI.State.CStateInterface import eAIState

class TeleportSpaceAI( AIBase ):
	"""
	"""
	def __init__(self):
		AIBase.__init__(self)
		
		self.defaultFlag = False
		self.actionStatus[eAIState.Dead] = CDeadToRevive(self)
		self.actionStatus[eAIState.Pet] = CPetAISys(self)
		self.actionStatus[eAIState.CItem] = CItemAISys(self)
		self.actionStatus[eAIState.Teleport] = CTeleportRepeat(self)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		self.think()
		
	def think(self):
		"""
		"""
		if not self.defaultFlag:
			self.defaultFlag = True
			self.setTickSpace(KST_Config.teleport_tick)
			
			if KST_Config.teleport_with_item:
				self.changeAIState(eAIState.CItem)
		elif KST_Config.pet and self.owner.currentPetUID == 0:
			self.changeAIState(eAIState.Pet)
		else:
			self.changeAIState(eAIState.Teleport)

AIBase.setClass("TeleportSpaceAI", TeleportSpaceAI)