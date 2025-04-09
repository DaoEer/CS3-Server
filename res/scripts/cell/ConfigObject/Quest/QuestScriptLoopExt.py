# -*- coding: utf-8 -*-
#

import csdefine
from KBEDebug import *
from ConfigObject.Quest.QuestBase.QuestScript import QuestScript

from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader


class QuestScriptLoopExt( QuestScript ):
	"""
	环任务
	1、不会增加环任务次数
	2、没有额外的奖励
	"""

	def __init__(self):
		QuestScript.__init__(self)
		self._type = csdefine.QUEST_TYPE_LOOP
		
	def getQuestDataByTalk( self, player ):
		"""
		点击任务选项后将任务数据发送到客户端以显示任务界面内容
		"""
		talkQuestData = QuestScript.getQuestDataByTalk( self, player )
		talkQuestData["LoopQuestNum"] = player.loopQuest["loopQuestNum"] - 1
		
		return talkQuestData
		
	def packQuestStream( self, player ):
		"""
		打包任务数据
		"""
		questInfo = QuestScript.packQuestStream( self, player )
		questInfo["loopQuestNum"] = player.loopQuest["loopQuestNum"] - 1
		return questInfo
		
