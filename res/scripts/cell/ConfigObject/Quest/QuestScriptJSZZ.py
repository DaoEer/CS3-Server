# -*- coding: utf-8 -*-
#
from KBEDebug import *
from ConfigObject.Quest.QuestBase.QuestScript import QuestScript
from ConfigObject.Quest.QuestRewards import QuestRewardChooseItem
import csdefine

class QuestScriptJSZZ( QuestScript ):
	"""
	金树种子
	"""
	def __init__(self):
		QuestScript.__init__(self)
		self._type = csdefine.QUEST_TYPE_JSZZ

	def packQuestStream( self, player ):
		"""
		打包任务数据
		"""
		status = player.queryQuestStatus(self._id)
		
		questInfo = {}
		# 任务目标数据
		taskClass = []
		taskParam1 = []
		taskParam2 = []
		taskParam3 = []
		goal = []
		taskName = []
		taskID = []
		progress = []
		priority = []
		navigateData = []
		#奖励数据
		rewards = {}

		if self._taskClasses:
			# 根据任务ID获取任务实例
			quest = player.questTable.get(self._id)

			for tClass, taskData in self._taskClasses:
				# 根据任务实例可以获取到该任务的进度
				if quest is not None:
					QP = quest.taskProgress(taskData["id"])
				else:
					QP = 0
				progress.append( QP )

				taskClass.append( taskData["TaskClass"] )
				if taskData["id"] == 1:
					firstTaskData = quest.getFirstTaskData()
					firstTaskNumber = quest.getFirstTaskNumber()
					taskParam1.append(firstTaskData[0])
					taskParam2.append(firstTaskData[1])
					taskParam3.append(firstTaskData[2])
					navigateData.append( firstTaskNumber + "#" + firstTaskData[0] )
				else:
					taskParam1.append( taskData["param1"] )
					taskParam2.append( taskData["param2"] )
					taskParam3.append( taskData["param3"] )
					navigateData.append( taskData["navigateData"])
				goal.append( taskData["goal"] )
				taskName.append( taskData["name"] )
				taskID.append( taskData["id"] )
				priority.append( taskData["priority"])

		if self._rewards:
			for reward in self._rewards:
				if isinstance( reward, QuestRewardChooseItem ):
					if str(csdefine.QUEST_REWARD_TYPE_ITEM_CHOOSE) not in rewards:
						rewards.update( {str(csdefine.QUEST_REWARD_TYPE_ITEM_CHOOSE): []} )
					rewards[str(csdefine.QUEST_REWARD_TYPE_ITEM_CHOOSE)].append( reward.sendClientData( player ) )
				else:
					rewards.update( reward.sendClientData( player ) )

		questInfo = {
				"id":str(self._id),
				"name":self.query("title"),
				"type":str(self.type),
				"description":self.query("description"),
				"taskLogDes":self.query("taskLogDes"),
				"status":str(status),
				"taskClass":taskClass,
				"taskParam1":taskParam1,
				"taskParam2":taskParam2,
				"taskParam3":taskParam3,
				"rewards":rewards,
				"goal":goal,
				"taskName":taskName,
				"taskID":taskID,
				"progress":progress,
				"priority":priority,
				"navigateData":navigateData,
				"isAutoAccept":str( self.query("isAutoAccept") ),
				"isAutoCommit":str( self.query("isAutoCommit") ),
				"finish_by":str(self._finish_by),
			}
		# 根据任务ID获取任务实例
		quest = player.questTable.get( self._id )
		if quest:
			quest.showFirstTaskToClient(player)
			quest.showSecondTaskToClient(player)
		return questInfo

	def abandonBy(self, player, params = {}):
		QuestScript.abandonBy(self, player, params = {})
		if player.isInSpacePlane():
			player.gotoExitSpacePos()
