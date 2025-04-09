# -*- coding: utf-8 -*-
#

from KBEDebug import *
from LoadModule import *
from SmartImport import smartImport
from HotUpdate.Quest import HotUpdateQuest
import random

class QuestLoader:
	_instance = None

	def __init__(self):
		assert self._instance is None
		self._questScripts = {}
		self._loopQuestGroupScripts = {}			# { "35-39" : questScript }
		self._tongDailyQuestList = {}				# 帮会日常任务{ questID : genre}
		self._startByNPC = {}
		self._finishByNPC = {}

	@staticmethod
	def instance():
		if QuestLoader._instance is None:
			QuestLoader._instance = QuestLoader()

		return QuestLoader._instance

	def loadConfig(self, questData):
		for data in questData.values():
			for d in data.values():
				scriptInst = smartImport("ConfigObject.Quest.%s:%s" % (d["script"], d["script"]))()
				scriptInst.initFromConfig(d)
				self._questScripts[scriptInst.id] = scriptInst
				startNPC = d[ "start_by" ].split("#")[0]
				finishNPC = d[ "finish_by" ].split("#")[0]

				#初始化接任务NPC
				if not startNPC in self._startByNPC:
					self._startByNPC[ startNPC ] = []

				self._startByNPC[ startNPC ].append( scriptInst.id )

				#初始化交任务NPC
				if not finishNPC in self._finishByNPC:
					self._finishByNPC[ finishNPC ] = []

				self._finishByNPC[ finishNPC ].append( scriptInst.id )

		DEBUG_MSG("Load quests finished, total: %i" % len(self._questScripts))
		
	def loadLoopQuestConfig( self, questData ):
		"""加载环任务组"""
		for levelSection, data in questData.items():
			quest = scriptInst = smartImport("ConfigObject.Quest.QuestScriptLoopGroup:QuestScriptLoopGroup")()
			quest.initFromConfig(data)
			self._loopQuestGroupScripts[levelSection] = quest
		
	def loadDailyQuestConfig( self, questData ):
		"""加载帮会日常任务"""
		for data in questData:
			self._tongDailyQuestList[data["questID"]] = data["genre"]
	
	def reloadQuestConfig( self, questID ):
		"""
		热加载
		"""
		questDatas = self.getConfig( questID )
		if questDatas:
			for questData in questDatas.values():
				scriptInst = HotUpdateQuest("ConfigObject.Quest.%s:%s" % (questData["script"], questData["script"]))()
				scriptInst.reloadFromConfig(questData)
				self._questScripts[scriptInst.id] = scriptInst
				startNPC = questData[ "start_by" ].split("#")[0]
				finishNPC = questData[ "finish_by" ].split("#")[0]

				self._startByNPC[ startNPC ].append( scriptInst.id )
				self._finishByNPC[ finishNPC ].append( scriptInst.id )
				return True
		return False
			
	def getConfig( self, QuestID ):
		questPath = "Quest/%i.json"%QuestID
		questData = openJsonCfg( questPath )
		if questData:
			return questData
		else:
			ERROR_MSG("Quest::getConfig Can not find questData(questID:%i)"%QuestID)
			return None

	def getScript(self, questID):
		if questID in self._questScripts:
			return self._questScripts[questID]
		else:
			ERROR_MSG("QuestLoader::getScript: Quest with id %i do not exist!" % questID)
			return None
			
	def getLoopQuestScript( self, levelSection ):
		"""获取环任务组"""
		if levelSection in self._loopQuestGroupScripts:
			return self._loopQuestGroupScripts[levelSection]
		else:
			ERROR_MSG("QuestLoader::getLoopQuestScript: script with levelSection(%s) do not exist!"%levelSection)
			return None

	def allScripts(self):
		return list(self._questScripts.values())

	def newQuest(self, questID):
		if questID in self._questScripts:
			return self._questScripts[questID].createNewQuest()
		else:
			ERROR_MSG("QuestLoader::newQuest: Quest with id %i do not exist!" % questID)
			return None

	def newQuestTask(self, questID, taskID):
		if questID in self._questScripts:
			return self._questScripts[questID].createNewTask(taskID)
		else:
			ERROR_MSG("QuestLoader::newQuestTask: Quest with id %i do not exist!" % questID)
			return None

	def getStartNPCQuests( self, npcEntity ):
		"""
		"""
		return [ self._questScripts[ questID ] for questID in self._startByNPC.get( npcEntity.scriptID, [] ) ]

	def getFinishNPCQuests( self, npcEntity ):
		"""
		"""
		return [ self._questScripts[ questID ] for questID in self._finishByNPC.get( npcEntity.scriptID, [] ) ]

	def getRandomLoopQuest( self, player ):
		"""随机获取环任务"""
		for levelSection, questScript in self._loopQuestGroupScripts.items():
			levelList = levelSection.split("-")
			if len( levelList ) < 2:
				CRITICAL_MSG("LoopQuest config(levelSection:%s) is error!!"%levelSection)
				continue
			lowLevel = int(levelList[0])
			topLevel = int(levelList[1])
			level = player.getLevel()
			if lowLevel <= level and level <= topLevel:
				return questScript.getRandomLoopQuest( player )
		CRITICAL_MSG("player(name:%s,level:%d) Can not getRandomLoopQuest!!"%(player.getName(),level))
		return []
	
	def getRandomDailyQuest( self, num ):
		"""随机获取日常任务"""
		qList = []
		if self._tongDailyQuestList:
			totalNum = len( self._tongDailyQuestList )
			if totalNum >= num:
				return random.sample( self._tongDailyQuestList.keys(), num )
			while(num):
				if num - totalNum > 0:
					num -= totalNum
					qList.extend(random.sample( self._tongDailyQuestList.keys(), totalNum))
				else:
					qList.extend(random.sample( self._tongDailyQuestList.keys(), num))
					num = 0
		return qList
	
g_QuestLoader = QuestLoader.instance()