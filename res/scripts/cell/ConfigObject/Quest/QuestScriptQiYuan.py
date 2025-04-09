# -*- coding: utf-8 -*-
#
import KBEDebug
from ConfigObject.Quest.QuestBase.QuestScript import QuestScript
from ConfigObject.Quest.QuestRewards import QuestRewardChooseItem
import csdefine
import csconst
import KBEMath

class QuestScriptQiYuan( QuestScript ):
	"""
	奇缘任务
	"""
	def __init__(self):
		QuestScript.__init__(self)
		self._type = csdefine.QUEST_TYPE_QIYUAN
		
	def packQuestStream( self, player ):
		"""
		打包任务数据
		"""
		status = player.queryQuestStatus(self._id)
		
		questInfo = {}
		#奖励数据
		rewards = {}
		progress = []
		taskID = []
		navigateData = []
		taskParam1 = []
		taskParam2 = []
		taskParam3 = []
		
		countDown = 0
		isShowTime = 0
		#建造洞府的任务特殊处理一下，需要显示倒计时
		if self._id == csconst.BUILD_DONG_FU_QUESTID:
			isShowTime = 1
			countDown = player.getBuildProtectTime()
	
		# 根据任务ID获取任务实例
		quest = player.questTable.get(self._id)
		if self._taskClasses:
			for tClass, taskData in self._taskClasses:
				# 根据任务实例可以获取到该任务的进度
				if quest is not None:
					QP = quest.taskProgress(taskData["id"])
				else:
					QP = 0
				progress.append( QP )
				taskID.append( taskData["id"] )
				
				param1 = taskData["param1"]
				param2 = taskData["param2"]
				param3 = taskData["param3"]
				
				#导航数据
				nagivate = ""
				if taskData["navigateData"]:
					pos = KBEMath.KBEngine2UnrealPosition(player.getBuildPos())
					posStr = "{} {} {}".format(pos[0], pos[1], pos[2])
					nagivate  = "(" + posStr + ")" + "#" + taskData["navigateData"]
					param2 = posStr
					
				navigateData.append( nagivate )
				taskParam1.append(param1)
				taskParam2.append(param2)
				taskParam3.append(param3)
		
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
			"status":str(status),
			"taskID":taskID,
			"progress":progress,
			"rewards":rewards,
			"type":str(self.type),
			"navigateData":navigateData,
			"countDown":str(countDown),
			"isShowTime":isShowTime,
			"taskParam1":taskParam1,
			"taskParam2":taskParam2,
			"taskParam3":taskParam3,
		}
		return questInfo
		
	def taskCompleteBy( self, player, taskID, params ):
		"""完成任务目标行为"""
		for taskIDs, func in self._taskCompleteFunctions.items():
			if taskID in taskIDs:
				isAllDone = True
				for tid in taskIDs:
					if player.queryTaskStatus( self._id, tid ) == csdefine.TASK_NOT_DONE:
						isAllDone = False
						break
				if self.functionsCheck(func, player, params) and isAllDone:
					self.functionsDo( func, player, params )
		
		status = player.queryQuestStatus( self._id )	
		if self._isAuto and status == csdefine.QUEST_DONE:			# 自动交接任务
			nextQuestID = self.getNextQuest( player )
			if nextQuestID:
				player.questAuto( self._id)
			else:
				player.questAutoCommit( self._id )
