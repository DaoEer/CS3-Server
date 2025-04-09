# -*- coding: utf-8 -*-
#
from KBEDebug import *
from ConfigObject.Quest.QuestBase.QuestScript import QuestScript


class QuestScriptMainline( QuestScript ):
	"""
	主线任务
	"""

	def __init__(self):
		QuestScript.__init__(self)
		self._type = csdefine.QUEST_TYPE_MAILLINE

	def canAcceptBy(self, player, params = {}):
		"""
		主线任务通用规则：不能重复做
		"""
		if player.hadFinishedQuest(self.id):
			return False
		else:
			return QuestScript.canAcceptBy(self, player, params)