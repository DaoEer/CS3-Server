# -*- coding: utf-8 -*-
#
import csdefine
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
import KBEngine
from KBEDebug import *
from LoadModule import *

class QuestTrigger:

	_instance = None

	def __init__(self):
		assert self._instance is None
		self._normalQuests = {}			# 非日常任务 { 等级: [任务脚本] }
		self._dailyQuests = {}			# 日常任务 { 等级: [任务脚本] }

	@staticmethod
	def instance():
		if QuestTrigger._instance is None:
			QuestTrigger._instance = QuestTrigger()
		return QuestTrigger._instance

	def classifyQuests(self, questScripts):
		"""分类任务"""
		for questScript in questScripts:
			if questScript.type == csdefine.QUEST_TYPE_DAILY:
				# 日常任务
				questSet = self._dailyQuests
			else:
				# 非日常任务
				questSet = self._normalQuests

			level = questScript.level
			if level in questSet:
				questSet[level].append(questScript)
			else:
				questSet[level] = [questScript]

	def triggerOnLevelRange(self, player, start, end):
		"""触发某个等级范围的任务"""
		questScripts = self.findNormalQuestsByLevel(start, end)
		for questScript in questScripts:
			self.letAcceptQuest(player, questScript)

	def triggerNextQuest(self, player, questID):
		"""触发某个任务的后续任务"""
		questScript = self.findQuestByID(questID)
		nextQuestID = questScript.getNextQuest( player )
		if nextQuestID:
			self.letAcceptQuest(player, self.findQuestByID(nextQuestID))

	def triggerDailyQuests(self, player):
		"""触发日常任务"""
		questScripts = self.findDailyQuestsByLevel(player.level, player.level)
		for questScript in questScripts:
			self.letAcceptQuest(player, questScript)

	def findQuestByID(self, questID):
		"""根据任务ID查找任务"""
		return g_QuestLoader.getScript(questID)

	def findNormalQuestsByLevel(self, start, end):
		"""查找某个等级段的非日常任务"""
		result = []
		for level in range(start, end + 1):
			if level in self._normalQuests:
				result.extend(self._normalQuests[level])
		return result

	def findDailyQuestsByLevel(self, start, end):
		"""查找某个等级段的日常任务"""
		result = []
		for level in range(start, end + 1):
			if level in self._dailyQuests:
				result.extend(self._dailyQuests[level])
		return result

	def findQuestByOperation(self, operation):
		"""根据操作查找任务"""
		return None

	@staticmethod
	def letAcceptQuest(player, questScript):
		"""触发后续任务 弹出后续任务的接受任务界面"""
		if player.requirementCheck(questScript):
			player.sendApplyQuestDataByClick( questScript.id, 0 )
			if questScript.type == csdefine.QUEST_TYPE_MAILLINE:
				# 根据任务ID获取任务基础数据
				player.showMessagePlaySound(questScript._data["description"])


g_QuestTrigger = QuestTrigger.instance()