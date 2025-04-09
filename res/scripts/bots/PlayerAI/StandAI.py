# -*- coding: utf-8 -*-
import Math
import KBEngine
from KBEDebug import *

import KST_Config
import Extra.Extend as Extend
from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.AI_System import CNull
from PlayerAI.State.AI_Dead import CDeadToRevive
from PlayerAI.State.CStateInterface import eAIState

g_row = 0		#行
g_line = 0		#列


class StandAI( AIBase ):
	"""
	"""
	def __init__(self):
		AIBase.__init__(self)
		
		self.walkToPos = False
		self.controllerID = 0
		self.xyPos = self.getStandXYPos()
		self.spaceInfo = KST_Config.stand_map
		self.actionStatus[eAIState.NULL] = CNull(self)
		self.actionStatus[eAIState.Dead] = CDeadToRevive(self)
		
	def onEnterSpace(self):
		"""
		"""
		self.owner.eventObj.registerEvent("Event_OnHPChanged", self)
		self.owner.eventObj.registerEvent("Event_OnMPChanged", self)
	
	def onLeaveSpace(self):
		"""
		"""
		self.owner.eventObj.unregisterEvent("Event_OnHPChanged", self)
		self.owner.eventObj.unregisterEvent("Event_OnMPChanged", self)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		if not self.enterDefaultMap:
			spaceScriptID = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
			if spaceScriptID != self.spaceInfo[0]:
				self.owner.GMCommand(self.owner, "set_level", "35")
				self.owner.GMCommand(self.owner, "goto", "{} {}".format(self.spaceInfo[0], self.spaceInfo[1]))
				return
			
		self.enterDefaultMap = True
		if not self.walkToPos:
			self.walkToDefaultPos()
			return
		
		self.think()
		
	def think(self):
		"""
		"""
		self.changeAIState(eAIState.NULL)
		
	def walkToDefaultPos( self ):
		"""
		"""
		uePos = self.spaceInfo[1].split(" ")
		pos = Extend.Unreal2KBEnginePosition(Math.Vector3(self.xyPos[0], self.xyPos[1], uePos[2]))
		if (self.owner.position - pos).length <= 2:
			self.walkToPos = True
			self.onSetSpaceData()
			return
		
		if not self.controllerID:
			self.controllerID = self.owner.moveToPos(pos)
		
	def getStandXYPos( self ):
		"""
		"""
		global g_row
		global g_line
		
		uePos = self.spaceInfo[1].split(" ")
		if abs(self.getOffset(g_line)) <= abs(self.getOffset(g_row)):
			g_line += 1
			g_row = 0
			return (int(uePos[0]) + 800 * g_line, int(uePos[1]) + 800 * g_row)
		
		g_row += 1
		return (int(uePos[0]) + 800 * g_line, int(uePos[1]) + 800 * g_row)
	
	def getOffset( self, index ):
		"""
		"""
		return index / 2 * -1 if index % 2 == 0 else (index + 1) / 2
		
	def onMoveOver( self, controllerID, userData ):
		"""
		"""
		self.controllerID = 0
		self.walkToDefaultPos()
	
	def onMoverFailure( self, controllerID, userData ):
		"""
		"""
		self.controllerID = 0
		self.walkToDefaultPos()
		
AIBase.setClass("StandAI", StandAI)