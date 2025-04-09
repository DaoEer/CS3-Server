# -*- coding: utf-8 -*-
#
# 将任务ID映射到数据位上，用于记录该任务是否已经完成。
#
# 设计思想：考虑到游戏的任务ID是一系列连续的整数，采用
# 位来记录已完成任务会比用列表记录任务ID消耗更少存储空
# 间，也利于减少在服务器和客户端之间传输的带宽占用。
#
# 用query查询任务是否被记录，如果返回值是零，表示没有
# 记录，非零值表示已记录。
#
# 用values返回所有已经记录的任务ID

import csdefine
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader

class QuestLogger:

	bitSize = 64

	def __init__(self):
		self._logs = {}			# {index: int64}

	def initFromStream(self, data):
		"""从数据流恢复"""
		for log in data["logs"]:
			self._logs[log["index"]] = log["value"]

	def packStreamData(self):
		"""打包传输数据"""
		logs = []
		for index, value in self._logs.items():
			logs.append({"index": index, "value": value})
		return {"logs": logs}

	def log(self, questID):
		"""记录一个任务"""
		index, pos = divmod(questID, self.bitSize)

		if index in self._logs:
			self._logs[index] |= 1 << pos
		else:
			self._logs[index] = 1 << pos

	def erase(self, questID):
		"""擦除一个任务记录"""
		index, pos = divmod(questID, self.bitSize)

		if index in self._logs:
			self._logs[index] &= ~(1 << pos)
			if self._logs[index] == 0:
				del self._logs[index]

	def query(self, questID):
		"""查询任务是否被记录，如果没有被记录，则返回0，
		否则返回非零值"""
		index, pos = divmod(questID, self.bitSize)

		if index in self._logs:
			return self._logs[index] & (1 << pos)
		else:
			return 0

	def isEmpty(self):
		"""是否为空"""
		return len(self._logs) == 0

	def values(self):
		"""返回所有记录的任务ID"""
		result = set()

		for index, value in self._logs.items():
			pos = 0
			while value:
				if value & 1:
					result.add(index * self.bitSize + pos)
				value >>= 1
				pos += 1

		return result

	def clear(self):
		self._logs.clear()
		
	def clearQuestLogByType( self, type ):
		"""移除任务记录"""
		questList = []
		for questID in self.values():
			quest = g_QuestLoader.getScript( questID )
			if quest and quest.type == type:
				questList.append( questID )
		for questID in questList:
			self.erase( questID )
		
	def clearLoopQuest( self ):
		"""移除环任务记录"""
		loopQuest = []
		for  questID in self.values():
			quest = g_QuestLoader.getScript( questID )
			if quest and quest.type == csdefine.QUEST_TYPE_LOOP:
				loopQuest.append( questID )
		for questID in loopQuest:
			self.erase( questID )

	def clearTongTianDaQuest( self ):
		"""移除通天塔任务记录"""
		tongTianDaQuest = []
		for  questID in self.values():
			quest = g_QuestLoader.getScript( questID )
			if quest and quest.type == csdefine.QUEST_TYPE_TTD:
				tongTianDaQuest.append( questID )
		for questID in tongTianDaQuest:
			self.erase( questID )
			