# -*- coding: utf-8 -*-
import time
import csdefine
from KBEDebug import *

from Extra.QuestLoader import g_quests
from PlayerAI.Quest.TaskFactory import g_taskFactory

class Quest:
	
	def __init__(self):
		self.id = 0
		self.status = csdefine.QUEST_NOT_ACCEPT
		self.rewards = {}
		self.tasks = {}
		self.acceptTime = 0
		self.currentTask = None
		
	def init(self, role, questData):
		self.id = int(questData["id"])
		self.status = int(questData["status"])
		
		for i in range(len(questData["taskID"])):
			taskID = questData["taskID"][i]
			task = self._getTask(taskID)
			if task is None:continue
			task.updateProgress(role, questData["progress"][i])
			self.tasks[taskID] = task
			task.doBeforeBegine(role)
		self.rewards = questData["rewards"]
		self.acceptTime = int(time.time())
		
	def getQuestInfo(self):
		"""
		"""
		info = "questID:{}".format(self.id)
		for id, task in self.tasks.items():
			info += " task:{}:{}".format(id, task.progress)
		return info
		
	def updateTaskProgress(self, role, taskID, progress):
		"""
		"""
		if taskID not in self.tasks:
			task = self._getTask(taskID)
			self.tasks[taskID] = task
		
		self.tasks[taskID].updateProgress(role, progress)
		
	def isDone(self):
		"""
		"""
		for id, task in self.tasks.items():
			if not task.isDone():
				return False
		return True
		
	def _getTask(self, taskID):
		"""
		"""
		config = g_quests.getQuest(self.id)
		if config is None:
			ERROR_MSG("not found quest[%d]" %(self.id))
			return None
			
		for cfg in config["tasks"]:
			if cfg["id"] != taskID:
				continue
		
			task = g_taskFactory.createTask(self.id, cfg)
			return task
		return None

	def getCurTask(self):
		"""
		"""
		if self.currentTask:
			if not self.currentTask.isDone():
				return self.currentTask
			self.currentTask = None
		
		priority = 999
		for _taskID, _task in self.tasks.items():
			if _task.isDone():
				continue
			
			#根据优先级来选任务目标
			if _task.priority < priority:
				self.currentTask = _task
				priority = _task.priority
		
		#没有
		if self.currentTask is None:
			pass
			#ERROR_MSG("Quest[%d] has done" %(self.id))
		return self.currentTask