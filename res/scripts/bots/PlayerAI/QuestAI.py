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

class QuestAI( AIBase ):
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
		self.startQuestID = 0
		self.reAcceptQuestCallBackID = 0
		
		#任务完成后，机器人跳转的地图
		self.space_test = None
		spaces = []
		for k,v in KST_Config.task_done_goto_space_maps.items():
			if v[1] : spaces.append((k, v[0]))
			
		if len(spaces) <= 0:
			KBEDebug.ERROR_MSG("Space error")
			return
		
		self.space_test = random.choice(spaces)
		
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
		self.resetCallBack()
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
		self.resetCallBack()
	
		#有目标，攻击目标
		if self.attackTarget:
			self.changeAIState(eAIState.Attack)
			return
			
		#任务还未初始化
		if not self.owner.hasInitQuest:
			KBEngine.callback(3, self.think)
			return
		
		#如果设置了起始任务的情况
		if not self.hasSetQuest and KST_Config.startQuestID:
			config = g_quests.getQuest(KST_Config.startQuestID)
			if config is None:
				ERROR_MSG("NOT found start quest[%d]" %(KST_Config.startQuestID))
				return
			
			#放弃当前所有任务
			self.owner.resetQuest()
			
			#如果等级不够，先设置等级
			if config["level"] > self.owner.level:
				self.owner.GMCommand(self.owner, "setLevel", "{}".format(config["level"]))
			self.owner.acceptQuest(KST_Config.startQuestID)
			self.hasSetQuest = True
			return
		
		self.changeAIState(eAIState.NULL)
		#没有任务了
		if len(self.owner.questTable) <= 0:
			self.owner.outputMsg("All QUEST is Done")
			self.resetQuestData()
			
			#没有设置循环刷任务,进入指定地图随机移动并释放技能
			if not KST_Config.isLoopQuest:
				if self.space_test is None: 
					return
				
				#跳转到指定的地图
				currentSpace = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
				if currentSpace != self.space_test[1]:
					self.changeAIState(eAIState.Teleport)	
					return
				
				#切换到随机移动
				self.changeAIState(eAIState.Run)		
				return
			
			#如果设置了起始任务，继续从起始任务开始刷
			if KST_Config.startQuestID:
				self.owner.acceptQuest(KST_Config.startQuestID)
				return
		
			#如果未设置起始任务，则从接到的第一个任务重新开始刷
			if self.startQuestID:
				self.owner.acceptQuest(self.startQuestID)
				return
				
			ERROR_MSG("QUEST has done, no startQuestID")
			return
		
		if self.quest is None:
			self.quest = self.owner.getUnaccomplishedQuest()
		
		if self.quest is None:
			self.owner.outputMsg("No Quest error")
			return
		
		#获取优先级最高且还未完成的任务目标
		task = self.quest.getCurTask()
		if not task:
			self.owner.cell.requestToCommitQuest(str(self.quest.id))
			self.quest = None
			self.owner.outputMsg("requestToCommitQuest")
			return
		
		task.do(self.owner)
		
	def resetQuestData(self):
		"""
		"""
		#清理所有任务标记
		self.owner.GMCommand(self.owner, "remove_completed_quest")
		#清理背包
		self.owner.GMCommand(self.owner, "clearBag")
		#回收幻兽
		self.owner.cell.withdrawPet()
		self.owner.outputMsg("withdrawPet")
		#设置等级
		self.owner.GMCommand(self.owner, "setLevel", "1")
		#设置修为
		self.owner.GMCommand(self.owner, "setXiuwei", "1000")
	
	def onAcceptQuest(self, questID):
		"""
		接受任务
		"""
		#如果还没设置起始任务ID，那么接受的第一个任务认为是起始任务ID
		if not self.startQuestID:
			self.startQuestID = questID
		
		self.think()
		
	def onCompleteQuest(self, questID):
		"""
		任务完成
		"""
		#如果还没设置起始任务ID，那么接受的第一个任务认为是起始任务ID
		if not self.startQuestID:
			self.startQuestID = questID
		
		if self.quest:
			if questID == self.quest.id:
				self.quest = None
				return
				
	def onCommitQuest(self, questID):
		"""
		提交任务回调
		"""
		self.callback(5)
		
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

AIBase.setClass("QuestAI", QuestAI)		
	