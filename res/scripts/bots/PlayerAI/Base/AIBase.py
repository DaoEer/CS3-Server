# -*- coding: utf-8 -*-

import random
import weakref

import KBEngine
import KBEDebug

import csdefine
import KST_Config
from PlayerAI.State.CStateInterface import eAIState

class AIBase:
	"""
	"""
	_AI_CALSS = {}
	def __init__(self):
		self.aistate = eAIState.NULL
		self.actionStatus = {}
		self.enterDefaultMap = False
		self.spaceInfo = KST_Config.default_map
		
		self.tickSpace = 1
		self.tempTickSpace = 0
		
	@classmethod
	def setClass( SELF, className, classObj ):
		SELF._AI_CALSS[ className ] = classObj
	
	@classmethod
	def getClassObj( SELF, className ):
		if className in SELF._AI_CALSS:
			return SELF._AI_CALSS[ className ]( )
		return None
		
	def attache(self, owner):
		"""
		"""
		self.tempTickSpace = self.tickSpace
		self.owner = weakref.proxy(owner)
		self.owner.eventObj.registerEvent("Event_OnStateChanged", self)
		
	def getAction(self):
		"""
		"""
		return self.actionStatus[self.aistate]
		
	def think(self):
		"""
		virtual method
		思考
		"""
		pass
		
	def changeAIState(self, aistate):
		"""
		改变AI状态
		"""
		if self.aistate == aistate:
			self.actionStatus[self.aistate].reEnter()
			return
			
		if self.aistate != eAIState.NULL:
			self.actionStatus[self.aistate].leave()
			
		self.aistate = aistate
		
		if self.aistate != eAIState.NULL:
			self.actionStatus[self.aistate].enter()
	
	def onEvent(self, name, *argv):
		if name == "Event_OnStateChanged":
			self.onStateChanged(*argv)
		elif name == "Event_OnMonsterDead":
			self.onMonsterDead(*argv)
		elif name == "Event_OnHPChanged":
			self.OnHPChanged(*argv)
		elif name == "Event_OnAcceptQuest":
			self.onAcceptQuest(*argv)
		elif name == "Event_onQuestComplete":
			self.onCompleteQuest(*argv)
		elif name == "Event_onUpdateQuestTask":
			self.onUpdateQuestTask(*argv)
		elif name == "Event_onQuestCommit":
			self.onCommitQuest(*argv)
		elif name == "Event_OnMPChanged":
			self.OnMPChanged(*argv)
		elif name == "Event_CItemAISys_onAddItem":
			self.onAddItem(*argv)
		elif name == "Event_OnxianshiChanged":
			self.onXianShiChanged(*argv)
		elif name == "Event_OnlingshiChanged":
			self.onLingShiChanged(*argv)
		elif name == "Event_OnxuanshiChanged":
			self.onXuanShiChanged(*argv)
		elif name == "Event_OnMoneyChanged":
			self.onMoneyChanged(*argv)
		elif name == "Event_OnControlMonster":
			self.onControlMonster(*argv)
	
	def onStateChanged(self, newState, oldState):
		"""
		"""
		if oldState != csdefine.ENTITY_STATE_DEAD and newState == csdefine.ENTITY_STATE_DEAD:
			self.changeAIState(eAIState.Dead)
			
	def onMonsterDead(self, scriptID, id):
		"""
		"""
		pass
		
	def OnHPChanged(self, curHP):
		"""
		"""
		if float(curHP / self.owner.HP_Max) <= 0.5:
			self.owner.GMCommand(self.owner, "full")
		
	def OnMPChanged(self, curMP):
		"""
		"""
		if float(curMP / self.owner.MP_Max) <= 0.5:
			self.owner.GMCommand(self.owner, "full")
		
	def onAcceptQuest(self, questID):
		"""
		"""
		pass
		
	def onCompleteQuest(self, questID):
		"""
		"""
		pass
		
	def onUpdateQuestTask(self, questID, taskID):
		"""
		"""
		pass
		
	def onCommitQuest(self, questID):
		"""
		"""
		pass
		
	def onAddItem(self, itemOrder):
		"""
		"""
		pass
		
	def onXianShiChanged(self, xianshi):
		"""
		"""
		pass
		
	def onLingShiChanged(self, lingshi):
		"""
		"""
		pass
		
	def onXuanShiChanged(self, xuanshi):
		"""
		"""
		pass
		
	def onMoneyChanged(self, money):
		"""
		"""
		pass
		
	def onControlMonster(self, entityID):
		"""
		"""
		pass
		
	def onMoveOver( self, controllerID, userData ):
		"""
		"""
		if self.aistate == eAIState.NULL:
			return
			
		self.actionStatus[self.aistate].onMoveOver(controllerID, userData)
	
	def onMoverFailure( self, controllerID, userData ):
		"""
		"""
		if self.aistate == eAIState.NULL:
			return

		self.actionStatus[self.aistate].onMoverFailure(controllerID, userData)
		
	def onEnterWorld( self ):
		"""
		"""
		if self.aistate == eAIState.NULL:
			return
			
		self.actionStatus[self.aistate].onEnterWorld()
		
	def onLeaveWorld( self ):
		"""
		"""
		if self.aistate == eAIState.NULL:
			return
		
		self.actionStatus[self.aistate].onLeaveWorld()
		
	def onSetSpaceData( self ):
		"""
		"""
		currentSpace = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		#KBEDebug.INFO_MSG("AIBase:onSetSpaceData:[%d]:[%s][%s:%s]" %(self.owner.id, self.owner.playerName, currentSpace, self.owner.position))
		self.owner.cell.OnPlayerMoveChange(0, 1)
		self.owner.outputMsg("OnPlayerMoveChange")
		
	def onEnterSpace( self ):
		"""
		"""
		if self.aistate == eAIState.NULL:
			return
			
		self.actionStatus[self.aistate].onEnterSpace()
		
	def onLeaveSpace( self ):
		"""
		"""
		if self.aistate == eAIState.NULL:
			return
		
		self.actionStatus[self.aistate].onLeaveSpace()
	
	def enterDefaultSpace( self ):
		"""
		"""
		if not self.enterDefaultMap:
			self.enterDefaultMap = True
			spaceScriptID = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
			if spaceScriptID != self.spaceInfo[0]:
				self.owner.GMCommand(self.owner, "goto", "{} {}".format(self.spaceInfo[0], self.spaceInfo[1]))
				return
			else:
				KBEngine.callback(3, self.onSetSpaceData)
				
	def useSkill( self, skillID, targetID ):
		"""
		"""
		if KST_Config.close_skill:
			return
		
		self.owner.useSkillForTarget( skillID, targetID )
		
	def startAction(self, key, param):
		"""
		"""
		pass
		
	def onTickCallBack(self, tick):
		"""
		"""
		self.tempTickSpace -= 1
		if self.tempTickSpace <= 0:
			self.tempTickSpace = self.tickSpace
		else:
			return
		
		if self.aistate == eAIState.NULL:
			return
		
		self.actionStatus[self.aistate].onTickCallBack(tick)
		
	def setTickSpace(self, value):
		"""
		设置tick执行间隔
		1个tick为60S，执行一次onTickCallBack
		"""
		tick = int(value)
		if tick < 0:
			return
			
		self.tickSpace = tick