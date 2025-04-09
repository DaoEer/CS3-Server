# -*- coding: utf-8 -*-
#
from KBEDebug import *
from ConfigObject.Quest.QuestBase.QuestScript import QuestScript


class QuestScriptTTD( QuestScript ):
	"""
	通天塔任务
	"""
	def __init__(self):
		QuestScript.__init__(self)
		self._type = csdefine.QUEST_TYPE_TTD