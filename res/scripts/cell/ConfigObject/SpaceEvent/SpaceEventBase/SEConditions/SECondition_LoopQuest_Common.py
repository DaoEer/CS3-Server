# -*- coding: utf-8 -*-

#环任务通用 副本事件条件

from ConfigObject.SpaceEvent.SpaceEventBase.SEConditions.SEConditionBase import SEConditionBase

class SECondition56( SEConditionBase ):
	"""
	当前进度的环任务对应任务目标是否完成
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.taskIDList = [ int(i) for i in section["param1"].split("|") ]			#任务目标ID列表
		self.taskStatusList = [ int(i) for i in section["param2"].split("|") ]		#任务目标状态列表
		
	def check( self, spaceEntity, eventParams ):
		if len(spaceEntity._spaceRoles) == 0:
			return False
		roleEntity = spaceEntity._spaceRoles[0]
		questID = roleEntity.loopQuest["loopQuestList"][0]
		for index, taskId in enumerate( self.taskIDList ):
			status = self.taskStatusList[ index ]
			if roleEntity.queryTaskStatus( questID, taskId ) != status:
				return False
		return True

class SECondition57( SEConditionBase ):
	"""
	判断玩家当前的环任务类型
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.typeList = section["param1"].split("|")

	def check( self, spaceEntity, eventParams ):
		if len(spaceEntity._spaceRoles) == 0:
			return False
		roleEntity = spaceEntity._spaceRoles[0]
		questID = roleEntity.loopQuest["loopQuestList"][0]
		quest = roleEntity.questTable.get( questID )
		if str(quest.getScript().complex) in self.typeList:
			return True
		return False

class SECondition58( SEConditionBase ):
	"""
	环任务进度判断
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.loopQuestProgress = int(section["param1"])

	def check( self, spaceEntity, eventParams ):
		if len(spaceEntity._spaceRoles) == 0:
			return False
		roleEntity = spaceEntity._spaceRoles[0]
		if roleEntity.loopQuest["loopQuestList"]:
			if roleEntity.loopQuestProgress == self.loopQuestProgress:
				return True
			return False
		return False

class SECondition67( SEConditionBase ):
	"""
	玩家身上是否没有接环任务
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )

	def check( self, spaceEntity, eventParams ):
		if len(spaceEntity._spaceRoles) == 0:
			return False
		roleEntity = spaceEntity._spaceRoles[0]
		if roleEntity.loopQuest["loopQuestList"]:
			if not roleEntity.hasQuest( roleEntity.loopQuest["loopQuestList"][0] ):
				return True
		return False


SEConditionBase.setConditionClass("SECondition56", SECondition56)
SEConditionBase.setConditionClass("SECondition57", SECondition57)
SEConditionBase.setConditionClass("SECondition58", SECondition58)
SEConditionBase.setConditionClass("SECondition67", SECondition67)