# -*- coding: utf-8 -*-
#
# python
import time
import random
#common
import csdefine
import csstatus
import Const
from KBEDebug import *

from LoadModule import *
import Functions
import KBEngine
import QuestEventDefine
import QuestAIIDSImpl
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
from ConfigObject.Quest.QuestBase.QuestTrigger import g_QuestTrigger
from ConfigObject.SpaceEffect.SpaceEffectLoader import g_spaceEffectLoader
import Quest.QuestConfigs.WhisperQuestConfig as WhisperQuestConfig
from MsgLogger import g_logger


class RoleQuestInterface:

	def __init__(self):
		"""
		Defined Properties:
		self.questTable = {}
		self.questLogger = QuestLogger()
		self.questEventMgr = QuestEventManager()
		"""

	def triggerQuestEvent(self, eventID, params):
		"""
		<Define method>
		@type	eventID: UINT16
		@param	eventID: 事件ID，在QuestEventDefine定义
		@type	params: PYTHON
		@param	params: 事件参数，具体格式由事件决定
		"""
		if self.questEventMgr.hasEvent(eventID):
			autoQuests = []
			for questID, taskID in self.questEventMgr.queryObservers(eventID):
				if questID in self.questTable :
					if self.questTable[questID].isDone():
						continue
					self.questTable[questID].updateTask(self, eventID, taskID, params)
				else:
					ERROR_MSG("RoleQuestInterface::triggerQuestEvent: "\
						"Player(name %s, id %i) dosen't has quest %i, event is %i." %\
						(self.playerName, self.id, questID, eventID))

	def questTaskIncreaseState( self, questID, taskID ):
		"""
		<define method>
		被通知指定任务有一个任务目标被完成
		"""
		self.forceQuestTaskIncreaseState( questID, taskID )

	def questTaskResetState( self, questID, taskID ):
		"""
		<define method>
		重置某任务目标
		"""
		if questID not in self.questTable:
			return
		self.questTable[questID].resetOneTask( self, taskID )

	def forceQuestTaskIncreaseState( self, questID, taskID ):
		"""
		强制完成指定任务目标
		"""
		if questID not in self.questTable:
			return
		self.questTable[questID].completeTask( self, taskID, "" )
		if questID not in self.questTable:#这里做这个判断是有可能在完成指定任务时，剧情系统 已经让这个任务给提交 了
			return

	def registerQuestEvent(self, eventID, observer):
		"""
		注册任务事件
		注意，这个方法不支持ghost调用
		"""
		self.questEventMgr.registerEvent(eventID, observer)

	def deregisterQuestEvent(self, eventID, observer):
		"""
		注销任务事件
		注意，这个方法不支持ghost调用
		"""
		self.questEventMgr.deregisterEvent(eventID, observer)

	def initQuest(self):
		"""
		玩家登陆时调用
		"""
		self.questEventMgr.clear()
		for quest in self.questTable.values():
			quest.onPlayerLogin(self)

	def addQuest(self, questID):
		quest = g_QuestLoader.newQuest(questID)
		self.questTable[questID] = quest
		quest.onPlayerAddQuest(self)
		#ERROR_MSG("ROLE:%d QUEST:%d:%d" %(self.id, questID, quest.isDone()))

	def removeQuest(self, questID):
		if questID in self.questTable:
			quest = self.questTable.pop( questID )
			quest.onPlayerRemoveQuest( self )

	def removeQuestType( self, type ):
		"""移除某个类型任务"""
		for quest in list(self.questTable.values()):
			if quest.type == type:
				self.abandonQuest(quest.id)
				return

	def hasQuest(self, questID):
		return questID in self.questTable

	def hasQuestType( self, type ):
		"""是否某个类型任务"""
		for quest in self.questTable.values():
			if quest.type == type:
				return True
		return False

	def questIsDone(self, questID):
		"""是否已经完成某个任务"""
		quest = self.questTable.get(questID)
		if quest is None:
			return False
		else:
			return quest.isDone()

	def logFinishedQuest(self, questID):
		"""记录已完成任务"""
		self.questLogger.log(questID)

	def hadFinishedQuest(self, questID):
		"""是否之前已经做过某个任务"""
		return self.questLogger.query(questID) != 0

	def queryQuestStatus(self, questID):
		"""查询任务状态"""
		quest = self.questTable.get(questID)
		if quest is None:
			if self.hadFinishedQuest(questID):
				return csdefine.QUEST_HAD_FINISH
			else:
				return csdefine.QUEST_NOT_ACCEPT
		else:
			if quest.isDone():
				return csdefine.QUEST_DONE
			else:
				return csdefine.QUEST_NOT_DONE

	def queryTaskStatus(self, questID, taskID):
		"""查询任务的某个任务目标的状态"""
		quest = self.questTable.get(questID)
		if quest is None:
			if self.hadFinishedQuest(questID):
				return csdefine.QUEST_HAD_FINISH
			else:
				return csdefine.QUEST_NOT_ACCEPT
		else:
			if quest.taskIsDone(taskID):
				return csdefine.TASK_DONE
			else:
				return csdefine.TASK_NOT_DONE

	def canAcceptQuest(self, questID, params = {}):
		"""检查是否可以接受某个ID的任务"""
		if self.hasQuest(questID):
			return False

		#任务脚本接任务规则检查
		return g_QuestLoader.getScript(questID).canAcceptBy(self, params)

	def requirementCheck(self, questScript, params = {}):
		"""检查是否可以接受某个脚本的任务"""
		if not questScript:
			return False
		if self.hasQuest(questScript.id):
			return False

		return questScript.requirementCheck(self)

	def acceptQuest(self, questID, params = {}):
		"""接受任务"""
		if self.hasQuest(questID):
			ERROR_MSG("RoleQuestInterface::acceptQuest: Player(name %s, id %i) still has quest %i."\
				% (self.playerName, self.id, questID))
			return False

		questScript = g_QuestLoader.getScript(questID)
		if questScript is None:
			ERROR_MSG("RoleQuestInterface::acceptQuest: Quest with id %i dosen't exist!" % questID)
			return False

		if questScript.canAcceptBy(self, params):
			self.addQuest(questID)
			questScript.acceptedBy(self, params)
			# 通知客户端(一些任务在接取后，就已经满足了任务完成条件，并且任务配置为了自动提交)
			if questID in self.questTable and self.client is not None:
				dataStream = self.getQuestDataByQuestID(questID)
				#ERROR_MSG("Role[%d] onAcceptQuest [%d]" %(self.id, questID))
				self.client.onAcceptQuest( dataStream )
			questScript.afterClientAccepted(self, params)
			#添加日志
			g_logger.acceptQuestLog(self.playerDBID, self.getName(), questID, questScript.getTitle(), self.getLevel(), self.grade)
			
			return True
		else:
			ERROR_MSG("RoleQuestInterface::acceptQuest: Player(name %s, id %i) accept "\
				"quest %i fail on canAcceptBy check." % (self.playerName, self.id, questID))
			return False

	def commitQuest(self, questID, params = {}):
		"""提交任务"""
		quest = self.questTable.get(questID)
		if quest is None:
			ERROR_MSG("RoleQuestInterface::commitQuest: Player(name %s, id %i) dosen't "\
				"has quest %i." % (self.playerName, self.id, questID))
			return False

		if quest.isDone():
			if quest.getScript().tryToReward(self, params):
				self.removeQuest(questID)
				# 记录完成任务
				self.logFinishedQuest(questID)
				quest.getScript().committedBy(self, params)
				# 通知客户端
				if self.client is not None:
					self.client.onCommitQuest( questID )

				quest.getScript().afterClientCommitted(self, params)
				# 触发后续任务
				g_QuestTrigger.triggerNextQuest(self, questID)
				return True
			else:
				INFO_MSG("RoleQuestInterface::commitQuest: Quest %i rewards to "\
				"Player(name %s, id %i) fail." % (questID, self.playerName, self.id))
		else:
			ERROR_MSG("RoleQuestInterface::commitQuest: Player(name %s, id %i) has not "\
				"finished quest %i." % (self.playerName, self.id, questID))
		return False

	

	def abandonQuest(self, questID, params = {}):
		"""放弃任务"""
		quest = self.questTable.get(questID)

		if quest is None:
			ERROR_MSG("RoleQuestInterface::abandonQuest: Player(name %s, id %i) dosen't "\
				"has quest %i." % (self.playerName, self.id, questID))
			return False

		if quest.getScript().canAbandonBy(self, params):
			#记录放弃的任务
			self.addAbandonQuestList( questID )
			self.removeQuest(questID)
			quest.getScript().abandonBy(self, params)
			# 通知客户端
			if self.client is not None:
				self.client.onAbandonQuest( questID )

			quest.getScript().afterClientAbandon(self, params)
			self.removeQuestRecordAIIDS(questID)								#放弃某任务时清任务下保存的AI数据
			#添加日志
			g_logger.abandonQuestLog( self.playerDBID, self.getName(), questID, quest.getScript().getTitle(), self.getLevel(), self.grade )
			return True
		else:
			INFO_MSG("RoleQuestInterface::abandonQuest: Quest %i can't be abandon by "\
			"player(name %s, id %i)." % (questID, self.playerName, self.id))
			return False

	def rquestToAcceptQuest(self, srcEntityID, questID):
		"""
		<Exposed method>
		客户端请求接受一个任务
		@type	questID: STRING(参数类型定义为STRING类型是为了方便在客户端的蓝图中调用)
		@param	questID: 任务ID
		"""
		if not self.validateClientCall( srcEntityID ):
			WARNING_MSG("Cheat detected: src %i, this %i" % (srcEntityID, self.id))
			return

		self.acceptQuest(int(questID))

	def requestToCommitQuest(self, srcEntityID, questID):
		"""
		<Exposed method>
		@type	questID: STRING(参数类型定义为STRING类型是为了方便在客户端的蓝图中调用)
		@param	questID: 任务ID
		"""
		if not self.validateClientCall( srcEntityID ):
			WARNING_MSG("Cheat detected: src %i, this %i" % (srcEntityID, self.id))
			return

		questStatus = self.queryQuestStatus(int(questID))
		if questStatus != csdefine.QUEST_DONE:
			ERROR_MSG("RoleQuestInterface::requestToCommitQuest: Player(name %s, id %i) has not "\
				"finished quest %i." % (self.playerName, self.id, int(questID)))
			return

		self.commitQuest(int(questID))

	def requestToAbandonQuest(self, srcEntityID, questID):
		"""
		<Exposed method>
		请求放弃任务
		@type	questID: STRING(参数类型定义为STRING类型是为了方便在客户端的蓝图中调用)
		@param	questID: 任务ID
		"""
		if not self.validateClientCall( srcEntityID ):
			WARNING_MSG("Cheat detected: src %i, this %i" % (srcEntityID, self.id))
			return

		if not self.hasQuest(int(questID)):
			ERROR_MSG("RoleQuestInterface::requestToAbandonQuest: Player(name %s, id %i) do not has quest %i."\
				% (self.playerName, self.id, int(questID)))
			return

		if not self.abandonQuest(int(questID)):
			INFO_MSG("RoleQuestInterface::requestToAbandonQuest: Quest %i can't be abandon by "\
				"player(name %s, id %i)." % (int(questID), self.playerName, self.id))

	def sendApplyQuestDataByClick( self, questID, npcID ):
		"""
		点击任务选项后将任务数据发送到客户端以显示任务界面内容
		"""
		id = int( questID )
		questScript = g_QuestLoader.getScript( id )
		talkData = questScript.getQuestDataByTalk( self )
		talkData.update( { "questNpcID" : str( npcID ) } )
		
		self.client.onSetQuestContent( Functions.toJsonString( talkData ))
		
	def getQuestDataByQuestID(self, questID):
		"""
		根据任务ID获取任务相关的数据(包含任务目标、奖励等数据)
		@param 		questID: 任务ID
		@type 		questID: INT32
		"""
		questScript = g_QuestLoader.getScript( questID )
		if questScript is None:
			WARNING_MSG( "Can not find questID(%d) script!!"%questID )
			return ""
			
		# 获取任务的状态
		questInfo = questScript.packQuestStream( self )
		return Functions.toJsonString(questInfo)

	def sendQuestDataToClient(self):
		"""将任务数据发送到客户端 用于任务列表显示"""
		needToDelQuests = []
		for quest in self.questTable.values():
			if quest.checkQuestIsTimeOut():
				needToDelQuests.append(quest.id)
				continue
			dataStream = self.getQuestDataByQuestID(quest.id)

			if self.client is not None:
				self.client.onAddQuest( dataStream )
		
		for questID in needToDelQuests:
			self.questTable.pop(questID)

		if not self.questLogger.isEmpty():
			stringStream = ""
			for questID in self.questLogger.values():
				stringStream += str(questID) + "|"
			self.client.onRecvQuestLog(stringStream)
			
		if self.client:
			self.client.OnQuestInitNotity()

	def broadcastQuestEvent(self, srcEntityID, questID, taskID):
		"""
		<Exposed method>
		玩家达到某区域触发任务目标完成
		"""
		if not self.validateClientCall( srcEntityID ):
			WARNING_MSG("Cheat detected: src %i, this %i" % (srcEntityID, self.id))
			return
		
		# 因为到达某地是客户端触发完成，如果使用事件通知。可能会导致其他任务完成。无法判断是哪个任务
#		self.triggerQuestEvent( QuestEventDefine.EVENT_GET_TO, taskID )
		qID = int( questID )
		tID = int( taskID )
		if qID in self.questTable:
			self.questTable[qID].updateTask(self, QuestEventDefine.EVENT_GET_TO, tID, taskID)

	def addQuestRecordAIIDS(self,questID,aiid):
		"""
		<Define Method>
		记录已经对目标使用过的AIID，此数据是为了在某任务ID重置或者放弃时重置该任务下保存的ai数据
		"""
		exists = False
		for data in self.questResetAIIDS:
			if questID == data.questID:
				exists = True
				if not aiid in data.aiIDS:
					aiIDS = data.aiIDS
					aiIDS.append(aiid)
					data.aiIDS = aiIDS

		if not exists:
			data = QuestAIIDSImpl.QuestAIIDSImpl()
			data.questID = questID
			data.aiIDS = [aiid]
			self.questResetAIIDS.append(data)

	def removeQuestRecordAIIDS(self,questID):
		"""
		<Define method>
		删除某任务ID下已经记录对目标使用过的AIID
		"""
		temp = -1
		for index,data in enumerate(self.questResetAIIDS):
			if questID == data.questID:
				temp = index
				break

		if temp >= 0 :
			self.questResetAIIDS.pop(temp)

	def clearQuestReordAIIDS( self ):
		"""
		清除所有在玩家身上保存的AIIDS数据
		"""
		self.questResetAIIDS = []

	def setAbandonPrimaryFlag( self, flag ):
		"""
		define method
		设置可以放弃全部任务标志
		"""
		self.abandonPrimaryFlag = flag
	
	def questChooseReward( self, srcEntityID, questID, chooseRewardIndex, itemInfo ):
		"""
		Exposed method
		多个奖励选择一个
		"""
		if not self.validateClientCall( srcEntityID ):
			WARNING_MSG("Cheat detected: src %i, this %i" % (srcEntityID, self.id))
			return
			
		quest = self.questTable.get(int(questID))
		if quest is None:
			ERROR_MSG("RoleQuestInterface::questChooseReward: Player(name %s, id %i) dosen't "\
				"has quest %i." % (self.playerName, self.id, questID))
			return False

		quest.getScript().chooseRewardItem( int(chooseRewardIndex), itemInfo )	
	#-----------------------------------------------环任务-------------------------------------------------------------------------
	def onNewDayLogin( self ):
		"""24:00过后清除任务"""
		self.initDailyQuest()
		self.loopQuest["loopQuestList"] = []
		self.loopQuest["isAbandonQuest"] = False
		self.loopQuest["loopQuestNum"] = 0
		self.loopQuest["taskCompleteNum"] = 0
		self.loopQuestProgress = 0
		self.questLogger.clearLoopQuest()
		self.client.onRemoveQuestLogByType("QuestLoop")		#通知客户端将所有记录的questlog进行清除。
		self.removeQuestType( csdefine.QUEST_TYPE_LOOP )

		KBEngine.globalData["RingTaskSpaceMgr"].setCurrentProgress( str( self.playerDBID ), self.loopQuestProgress )
				
	def setLoopQuestTaskCompleteNum( self, num ):
		"""设置 任务目标完成数量（用于计算奖励）"""
		self.loopQuest["taskCompleteNum"] = num

	def addLoopQuestTaskCompleteNum( self, num ):
		"""增加任务目标完成数量（用于计算奖励）"""
		self.loopQuest["taskCompleteNum"] += num

	def randomLoopQuest( self ):
		"""随机选取环任务"""
		if self.loopQuest["loopQuestList"]:
			self.statusMessage( csstatus.TALK_HAS_ACCEPT_LOOP_QUEST,"" )
			return False
		if self.loopQuest["loopQuestNum"] >= Const.LOOP_QUEST_CAN_ACCEPT_NUM:
			self.statusMessage( csstatus.TALK_HAS_FINISH_LOOP_QUEST ,"" )
			return False
			
		self.questLogger.clearLoopQuest()						# 完成一轮，需要重置
		loopQuests = g_QuestLoader.getRandomLoopQuest( self )
		self.loopQuest["loopQuestList"] = loopQuests
		self.loopQuest["isAbandonQuest"] = False
		return True
	
	#-----------------------------------------------帮会日常任务--------------------------------------------------------
	def initDailyQuest( self ):
		""""""
		self.removeQuestType( csdefine.QUEST_TYPE_DAILY )
		if not self.tongDBID:return
		self.dailyQuest.initQuest()
		self.questLogger.clearQuestLogByType( csdefine.QUEST_TYPE_DAILY )	# 每天,清理任务日志
		self.client.onRemoveQuestLogByType("QuestTongDaily")		#通知客户端将所有记录的questlog进行清除。
	
	def requestTongDailyQuest(self, srcEntityID, npcID):
		"""
		<Exposed method>
		请求帮会日常任务树 数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.client.OnRequestTongDailyQuest( self.dailyQuest.getAcceptQuestIndexByDay(), {"data" : self.dailyQuest.finishQuestIndexs}, self.dailyQuest.treeQuestNodes, self.dailyQuest.getNodeMapQuestDatas() )
		self.sendGossipComplete( npcID )
	
	def acceptTongDailyQuest( self, srcEntityID, beforeNode, acceptNode ):
		"""
		Exposed method
		接取帮会日常任务
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.dailyQuest.acceptQuestNode( self, beforeNode, acceptNode )

	def playerAnswerTongQuestion(self, srcEntityID, questID, questionID, answer):
		"""
		exposed method
		帮会日常【见闻拾记】玩家回答问题
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		quest = self.questTable.get(questID)
		quest.getScript().onPlayerAnswer(self, questionID, answer)

	def selectNextTongQuestion(self, srcEntityID, questID):
		"""
		Exposed method
		帮会日常【见闻拾记】选择下一个问题
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		quest = self.questTable.get(questID)
		quest.getScript().sendRandomQuestionToClient(self)

	def stopTongQuestion(self, srcEntityID, questID):
		if not self.validateClientCall( srcEntityID ):
			return
		quest = self.questTable.get(int(questID))
		if quest is None: return
		quest.getScript().onStopTongQuestion(self)
		
	def setTongDailyQuestTaskCompleteNum( self, num ):
		"""
		"""
		self.dailyQuest.taskCompleteNum = num

	#-----------------------------------------------自动任务--------------------------------------------------------
	def questAuto( self, autoID ):
		"""
		<define method>
		自动交接任务
		"""
		questScript = g_QuestLoader.getScript(autoID)
		nextQuestID = questScript.getNextQuest( self )
		self.questAutoCommit( autoID )
		self.acceptQuest( nextQuestID )

	def questAutoCommit( self, questID, params = {} ):
		"""
		自动交任务
		"""
		quest = self.questTable.get(questID)

		if quest is None:
			ERROR_MSG("RoleQuestInterface::commitQuest: Player(name %s, id %i) dosen't "\
				"has quest %i." % (self.playerName, self.id, questID))
			return False
		if quest.isDone():
			if quest.getScript().tryToReward(self, params):
				self.removeQuest(questID)
				# 记录完成任务
				self.logFinishedQuest(questID)
				quest.getScript().committedBy(self, params)
				# 通知客户端
				if self.client is not None:
					self.client.onCommitQuest( questID )

				quest.getScript().afterClientCommitted(self, params)
				return True
			else:
				INFO_MSG("RoleQuestInterface::commitQuest: Quest %i rewards to "\
				"Player(name %s, id %i) fail." % (questID, self.playerName, self.id))
		else:
			ERROR_MSG("RoleQuestInterface::commitQuest: Player(name %s, id %i) has not "\
				"finished quest %i." % (self.playerName, self.id, questID))

		return False

#-----------------------------------------------传话任务--------------------------------------------------------
	def completeWhisperQuest( self, srcEntityID, questID, taskID, isSucced ):
		"""
		Exposed method
		传话游戏结束
		"""
		if not self.validateClientCall( srcEntityID ):
			WARNING_MSG("Cheat detected: src %i, this %i" % (srcEntityID, self.id))
			return
		quest = self.questTable.get( questID )
		if not quest:
			return

		task = quest.getTask(taskID)
		if not task:
			return
		progress = task._progress + 1

		data = None
		datas = WhisperQuestConfig.Datas
		if questID in datas and progress in datas[questID]:
			data = datas[questID][progress]
		if not data:
			return

		if isSucced:
			quest.gmSetTaskDone( self, questID, taskID, 1)
			self.addLoopQuestTaskCompleteNum(1)
			self.showMessagePlaySound( data["succeedSoundID"] )
		else:
			self.showMessagePlaySound( data["failedSoundID"] )
			self.acceptQuest(data["taskQuestID"])
			if data["taskQuestTime"] > 0:
				self.startTimeQuest(data["taskQuestTime"], data["taskQuestID"])
		self.client.OnCompleteWhisperQuest( questID, taskID, isSucced )
				
	def startTimeQuest(self, delayTime, questID):
		"""
		开始任务倒计时
		"""
		strTime = str(Functions.getTime(delayTime))
		self.client.StartTimeQuest(strTime, questID)
		self.addTimerCallBack( delayTime, "onTimeAbandonQuest", ( questID ) )

	def onTimeAbandonQuest(self, questID):
		"""
		任务倒计时到达
		"""
		quest = self.questTable.get( questID )
		if not quest:
			return
		if quest.isDone():
			return
		self.abandonQuest(questID)
		
	def completeWhisperQuestTask( self, questID, taskID, progress ):
		"""
		自定义完成传话任务目标
		"""
		quest = self.questTable.get( questID )
		if not quest:
			ERROR_MSG("%i is not exist quest"%(questID))
			return

		task = quest.getTask(taskID)
		if not task:
			ERROR_MSG("%i is not exist task"%(taskID))
			return
		self.addLoopQuestTaskCompleteNum(progress)
		task._progress += progress
		task.setDone()
		self.client.SetQuestTaskDone(questID, taskID)
		self.client.onUpdateQuestTask(questID, taskID, task._progress)
		quest.onTaskCompleted(taskID, self)

#-----------------------------------------------通天塔任务--------------------------------------------------------
	def addAbandonQuestList( self, questID ):
		"""添加放弃任务"""
		quest = self.questTable.get( questID )
		if quest.type == csdefine.QUEST_TYPE_TTD:
			self.abandonQuestList.append( questID )

	def clearAbandonQuest( self ):
		"""清除放弃任务数据"""
		self.abandonQuestList.clear()
		self.questLogger.clearTongTianDaQuest()

	def isInAbandonQuestList(self, questID ):
		"""是否在放弃任务列表"""
		return questID in self.abandonQuestList
