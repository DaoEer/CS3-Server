# -*- coding: utf-8 -*-
#
import json
import Singleton

import KBEngine
import KBEDebug

from LoadModule import openJsonPathConfig

QUEST_PATH = "Quest/"
class QuestLoader( Singleton.Singleton ):
	"""
	"""
	def __init__( self ):
		self._quests = {}
		
	def getAllQuest(self):
		"""
		"""
		return self._quests
	
	def loadQuest(self):
		"""
		"""
		self._quests = openJsonPathConfig(QUEST_PATH)
		
	def getQuest(self, id):
		"""
		"""
		quest = self._quests.get(str(id), None)
		if quest is None: return None
		return quest[str(id)]
		
	
g_quests = QuestLoader()
g_quests.loadQuest()