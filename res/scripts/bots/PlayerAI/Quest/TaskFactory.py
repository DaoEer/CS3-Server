# -*- coding: utf-8 -*-
#
import sys

import KBEngine
from KBEDebug import *
from Singleton import Singleton
import PlayerAI.Quest.Task as Task


class TaskFactory( Singleton ):
	"""
	"""
	def __init__(self):
		pass
		
	def createTask(self, questID, config):
		"""
		根据配置初始化一个task
		"""
		task = SCRIPT_MAPPING[config["TaskClass"]](questID, config)
		return task

g_taskFactory = TaskFactory()

	
SCRIPT_MAPPING = {}
def initTaskClass():
	"""
	初始化Task，在这里创建的原因是为了解决交叉（循环）引用的问题
	"""
	SCRIPT_MAPPING.clear()
	SCRIPT_MAPPING["QuestTaskGetTo"] 				= Task.QuestTaskGetTo
	SCRIPT_MAPPING["QuestTaskTalkWithNPC"] 			= Task.QuestTaskTalkWithNPC
	SCRIPT_MAPPING["QuestTaskLearnSkill"] 			= Task.QuestTaskLearnSkill
	SCRIPT_MAPPING["QuestTaskEventTrigger"] 		= Task.QuestTaskEventTrigger
	SCRIPT_MAPPING["QuestTaskKillMonster"] 			= Task.QuestTaskKillMonster
	SCRIPT_MAPPING["QuestTaskGetItem"] 				= Task.QuestTaskGetItem
	SCRIPT_MAPPING["QuestTaskMountPet"] 			= Task.QuestTaskMountPet
	SCRIPT_MAPPING["QuestTaskConjurePet"] 			= Task.QuestTaskConjurePet
	SCRIPT_MAPPING["QuestUseCommitItem"] 			= Task.QuestUseCommitItem
	SCRIPT_MAPPING["QuestTaskPlayerLevel"] 			= Task.QuestTaskPlayerLevel
	SCRIPT_MAPPING["QuestTaskUseSkill"] 			= Task.QuestTaskUseSkill
	SCRIPT_MAPPING["QuestTaskXiuweiLevel"] 			= Task.QuestTaskXiuweiLevel
	SCRIPT_MAPPING["QuestTaskEnterChuanChengCopy"] 	= Task.QuestTaskEnterChuanChengCopy
	SCRIPT_MAPPING["QuestTaskEnterPotentialCopy"] 	= Task.QuestTaskEnterPotentialCopy
	SCRIPT_MAPPING["QuestTaskPlayerTitle"] 			= Task.QuestTaskPlayerTitle
	
initTaskClass()
