# -*- coding: utf-8 -*-
#


class QuestTask:

	quest_event = []

	def __init__(self):
		self._id = 0
		self._progress = 0
		self._goal = 0
		self._priority = 0
		self.param = {}

	@property
	def id(self):
		return self._id

	@property
	def progress(self):
		return self._progress

	@property
	def goal(self):
		return self._goal
		
	@property
	def priority(self):
		return self._priority

	def setTempData( self, key, value ):
		"""
		"""
		self.param[key] = value

	def getTempData( self, key ):
		"""
		"""
		if key in self.param:
			return self.param[key]
		return None

	def packStreamData(self):
		return {"id": self._id, "progress": self._progress,"param":self.param}

	def initFromStream(self, data):
		self._progress = data["progress"]
		self.param = data["param"]

	def initFromConfig(self, data):
		self._id = data["id"]
		self._goal = data["goal"]
		self._priority = data["priority"]
		
	def refreshProgress( self, player ):
		"""刷新任务进度"""
		return False
		
	def registerEvent( self, quest, player ):
		for event in self.quest_event:
			player.registerQuestEvent(event, (quest.id, self.id))
			
	def deregisterEvent( self, quest, player ):
		for event in self.quest_event:
			player.deregisterQuestEvent(event, (quest.id, self.id))

	def updateProgress(self, player, eventID, param):
		return False

	def resetProgress(self, player):
		"""任务目标重置"""
		self._progress = 0

	def isDone(self):
		""""""
		return self._goal != 0 and self._progress >= self._goal

	def setDone(self):
		"""设置为完成状态"""
		self._progress = self._goal