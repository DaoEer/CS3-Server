# -*- coding: utf-8 -*-
import random

import KBEngine
from KBEDebug import *

import KST_Config
from Extra.QuestLoader import g_quests
from PlayerAI.State.AI_Run import CRun
from PlayerAI.State.AI_Attack import CAttack
from PlayerAI.State.AI_Dead import CDeadToRevive
from PlayerAI.State.AI_Teleport import CTeleport
from PlayerAI.State.CStateInterface import eAIState
from PlayerAI.State.AI_System import CNull, CPetAISys
from PlayerAI.State.AI_Run import CRunRandomAndUseSkill
from PlayerAI.Base.AIBase import AIBase

class QuestTestAI( AIBase ):
	"""
	主线任务AI
	"""
	def __init__(self):
		AIBase.__init__(self)
		
		self.actionStatus[eAIState.NULL] = CNull(self)
		self.actionStatus[eAIState.Pet] = CPetAISys(self)
		self.actionStatus[eAIState.Dead] = CDeadToRevive(self)
		self.actionStatus[eAIState.Attack] = CAttack(self)
		self.actionStatus[eAIState.Teleport] = CTeleport(self)
		self.actionStatus[eAIState.Run] = CRunRandomAndUseSkill(self)
		
		self.quest = None
		self.hasSetQuest = False
		self.attackTarget = None
		
		self.loopQuestID = 0
		self.reAcceptQuestCallBackID = 0
		if len(KST_Config.loopQuestID):
			self.loopQuestID = random.choice(KST_Config.loopQuestID)
		
	def onEnterWorld( self ):
		"""
		"""
		self.owner.eventObj.registerEvent("Event_OnAcceptQuest", self)
		self.owner.eventObj.registerEvent("Event_onQuestComplete", self)
		self.owner.eventObj.registerEvent("Event_onUpdateQuestTask", self)
		self.owner.eventObj.registerEvent("Event_onQuestCommit", self)
		self.owner.eventObj.registerEvent("Event_OnHPChanged", self)
		self.owner.eventObj.registerEvent("Event_OnMPChanged", self)
		
	def onLeaveWorld( self ):
		"""
		""" 
		self.owner.eventObj.unregisterEvent("Event_OnAcceptQuest", self)
		self.owner.eventObj.unregisterEvent("Event_onQuestComplete", self)
		self.owner.eventObj.unregisterEvent("Event_onUpdateQuestTask", self)
		self.owner.eventObj.unregisterEvent("Event_onQuestCommit", self)
		self.owner.eventObj.unregisterEvent("Event_OnHPChanged", self)
		self.owner.eventObj.unregisterEvent("Event_OnMPChanged", self)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		self.think()
		
	def think(self):
		"""
		"""	
		#有目标，攻击目标
		if self.attackTarget:
			self.changeAIState(eAIState.Attack)
			return
			
		#任务还未初始化
		if not self.owner.hasInitQuest:
			return
		
		if self.loopQuestID:
			config = g_quests.getQuest(self.loopQuestID)
			if config is None:
				ERROR_MSG("NOT found start quest[%d]" %(self.loopQuestID))
				return
				
			if len(self.owner.questTable) > 0:
				if list(self.owner.questTable.values())[0].id != self.loopQuestID:
					#放弃当前所有任务
					self.owner.resetQuest()
					
					#如果等级不够，先设置等级
					if config["level"] > self.owner.level:
						self.owner.GMCommand(self.owner, "setLevel", "{}".format(config["level"]))
					self.owner.acceptQuest(self.loopQuestID)
					return
		
		#没有任务了
		self.changeAIState(eAIState.NULL)
		if len(self.owner.questTable) <= 0:
			self.owner.outputMsg("All QUEST is Done")
			if not self.loopQuestID:
				return
			
			#清理所有任务标记
			self.owner.GMCommand(self.owner, "remove_completed_quest")
			self.owner.acceptQuest(self.loopQuestID)
			return
		
		if self.quest is None:
			quests = list(self.owner.questTable.values())
			while len(quests):
				self.quest = quests.pop(0)
				if self.quest.isDone():continue
				break
		
		if self.quest is None:
			ERROR_MSG("No Quest")
			return
		
		#获取优先级最高且还未完成的任务目标
		task = self.quest.getCurTask()
		if not task:
			self.owner.cell.requestToCommitQuest(str(self.quest.id))
			self.quest = None
			return
		
		task.do(self.owner)
	
	def onAcceptQuest(self, questID):
		"""
		接受任务
		"""
		self.think()
		
	def onCompleteQuest(self, questID):
		"""
		任务完成
		"""
		if self.quest:
			if questID == self.quest.id:
				self.quest = None
				return
				
	def onCommitQuest(self, questID):
		"""
		提交任务回调
		"""
		pass
		
	def onUpdateQuestTask(self, questID, taskID):
		"""
		更新任务目标进度
		"""
		self.think()
	
	def onMonsterDead(self, scriptID, id):
		"""
		"""
		if self.attackTarget:
			if self.attackTarget.id == id:
				self.attackTarget = None
		
	def callback(self, t):
		"""
		"""
		self.resetCallBack()
		self.reAcceptQuestCallBackID = KBEngine.callback(t, self.onCallback)
	
	def onCallback(self):
		self.think()

	def resetCallBack(self):
		if self.reAcceptQuestCallBackID:
			KBEngine.cancelCallback(self.reAcceptQuestCallBackID)
			self.reAcceptQuestCallBackID = 0


AIBase.setClass("QuestTestAI", QuestTestAI)		
	