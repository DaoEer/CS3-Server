# -*- coding: utf-8 -*-
#
from ConfigObject.Quest.QuestBase.QuestRequirement import QuestRequirementBase
import csdefine


# ----------------------------------------------------------
# 可接取任务前提条件类型扩展 继承父类QuestRequirementBase
# ----------------------------------------------------------
class QuestRequirementMoney( QuestRequirementBase ):
	"""
	金币限制
	"""
	def __init__( self ):
		pass

	def init( self, data ):
		"""
		"""
		self._money = int(data["param1"])

	def query( self, player ):
		"""
		"""
		return player.money >= self._money

	def getDetail( self ):
		"""
		"""
		return ""

class QuestRequirementProfession( QuestRequirementBase ):
	"""
	职业限制
	"""
	def __init__( self ):
		pass

	def init( self, data ):
		"""
		"""
		self._profession = data["param1"].split("|")

	def query( self, player ):
		"""
		"""
		professionList = []
		for profession in self._profession:
			professionList.append(int(profession))

		return player.profession in professionList

	def getDetail( self ):
		"""
		"""
		return ""

class QuestRequirementCamp( QuestRequirementBase ):
	"""
	阵营限制
	"""
	def __init__( self ):
		pass

	def init( self, data ):
		"""
		"""
		self._camp = int(data["param1"])

	def query( self, player ):
		"""
		"""
		return player.getFinalCamp() == self._camp

	def getDetail( self ):
		"""
		"""
		return ""

class QuestRequirementMissionCompleted( QuestRequirementBase ):
	"""
	完成任务(完成且提交某个任务才能显示可接任务)
	"""
	def __init__( self ):
		pass

	def init( self, data ):
		"""
		"""
		questIDList = data["param1"].split("|")
		self._questIDList = [ int( questID) for questID in data["param1"].split("|") ]

	def query( self, player ):
		"""
		"""
		# 根据任务ID获取该任务的状态
		for questID in self._questIDList:
			if player.queryQuestStatus(questID) == csdefine.QUEST_HAD_FINISH:
				return True

		return False

	def getDetail( self ):
		"""
		"""
		return ""

class QuestRequirementLevel( QuestRequirementBase ):
	"""
	玩家等级限制
	"""
	def __init__( self ):
		self._minLevel = 0
		self._maxLevel = 0

	def init( self, data ):
		"""
		"""
		self._minLevel = int(data["param1"])
		if data["param2"]:
			self._maxLevel = int( data["param2"] )

	def query( self, player ):
		"""
		"""
		level = player.level
		if self._maxLevel:
			return self._minLevel <= level and level <= self._maxLevel
		else:
			return level >= self._minLevel

	def getDetail( self ):
		"""
		"""
		return ""
