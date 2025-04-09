# -*- coding: utf-8 -*-
#
from SmartImport import smartImport
import csstatus
import csdefine
import KBEDebug
from HotUpdate.Quest import HotUpdateQuest
from ConfigObject.Quest.QuestRewards import QuestRewardChooseItem
from  ConfigObject.Quest.QuestRewardSequence import QuestRewardSequence

class QuestScript:

	def __init__(self):
		self._data = None
		self._id = 0
		self._type = 0
		self._level = 0
		self._canAbandon = 0		#0为不可放弃，1为可以放弃
		self._canShare = 0
		self._nextQuestID = ""

		self._title = ""

		self._QuestClass = None
		self._taskClasses = []			# [(任务目标类, 配置数据), ...]

		self._rewards = []
		self._requirements = []			# 可接取任务显示的必备条件

		self._acceptedFunctions = []
		self._abandonFunctions = []
		self._committedFunctions = []

		self._taskCompleteFunctions = {}
		self._finish_by = ""

	def initFromConfig(self, data):
		self._data = data
		self._id = data["id"]
		self._level = data["level"]
		self._canAbandon = data["canAbandon"]
		self._canShare = data["canShare"]
		self._title = data["title"]
		self._nextQuestID = str(data["nextQuest"])
		self._finish_by = data["finish_by"]
		self._isAuto = data["isAutoQuest"]

		#加载任务类
		self._QuestClass = smartImport("ConfigObject.Quest.%s:%s" % (data["QuestClass"], data["QuestClass"]))

		#加载任务目标类
		for taskData in data["tasks"]:
			TaskClass = smartImport("ConfigObject.Quest.QuestTasks:%s" % taskData["TaskClass"])
			self._taskClasses.append((TaskClass, taskData))

		#加载任务奖励
		for rewardData in data["rewards"]:
			try:
				reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
				reward.init(rewardData)
			except Exception as e:
				KBEDebug.ERROR_MSG( "====>>>quest( ID: %s) QuestRewards Error:%s!!"%( self._id, e ) )
				
			self._rewards.append(reward)

		#加载可接取任务显示的必备条件
		for requirementData in data["requirements"]:
			try:
				requirement = smartImport("ConfigObject.Quest.QuestRequirements:%s" % requirementData["script"])()
				requirement.init(requirementData)
			except Exception as e:
				KBEDebug.ERROR_MSG( "====>>>quest( ID: %s) requirementData Error:%s!!"%( self._id, e ) )
				
			self._requirements.append(requirement)

		#接受任务时的关联功能
		for funcData in data["acceptedFunctions"]:
			try:
				function = smartImport("ConfigObject.Quest.QuestFunctions:%s" % funcData["script"])()
				function.init(funcData)
			except Exception as e:
				KBEDebug.ERROR_MSG( "====>>>quest( ID: %s) acceptedFunctions Error:%s!!"%( self._id, e ) )
			self._acceptedFunctions.append(function)

		#放弃任务时的关联功能
		for funcData in data["abandonFunctions"]:
			try:
				function = smartImport("ConfigObject.Quest.QuestFunctions:%s" % funcData["script"])()
				function.init(funcData)
			except Exception as e:
				KBEDebug.ERROR_MSG( "====>>>quest( ID: %s) abandonFunctions Error:%s!!"%( self._id, e ) )
				
			self._abandonFunctions.append(function)

		#提交任务时的关联功能
		for funcData in data["committedFunctions"]:
			try:
				function = smartImport("ConfigObject.Quest.QuestFunctions:%s" % funcData["script"])()
				function.init(funcData)
			except Exception as e:
				KBEDebug.ERROR_MSG( "====>>>quest( ID: %s) committedFunctions Error:%s!!"%( self._id, e ) )
				
			self._committedFunctions.append(function)

		#完成某个任务目标时的关联功能
		for taskStr, funcDataList in data["taskCompleteFunctions"].items():
			for funcData in funcDataList:
				try:
					function = HotUpdateQuest("ConfigObject.Quest.QuestFunctions:%s" % funcData["script"])()
					function.init(funcData)
				except Exception as e:
					KBEDebug.ERROR_MSG( "====>>>quest( ID: %s) taskCompleteFunctions Error:%s!!"%( self._id, e ) )
				
				taskIDs = tuple( [ int( tid ) for tid in taskStr.split("|") ] )
				if not taskIDs in self._taskCompleteFunctions:
					self._taskCompleteFunctions[ taskIDs ] = []
				self._taskCompleteFunctions[ taskIDs ].append(function)
				
	def reloadFromConfig(self, data):
		self._data = data
		self._id = data["id"]
		self._level = data["level"]
		self._canAbandon = data["canAbandon"]
		self._canShare = data["canShare"]
		self._title = data["title"]
		self._nextQuestID = str(data["nextQuest"])
		self._finish_by = data["finish_by"]
		self._isAuto = data["isAutoQuest"]

		#热更新加载任务类
		self._QuestClass = HotUpdateQuest("ConfigObject.Quest.%s:%s" % (data["QuestClass"], data["QuestClass"]))

		#热更新加载任务目标类
		for taskData in data["tasks"]:
			TaskClass = HotUpdateQuest("ConfigObject.Quest.QuestTasks:%s" % taskData["TaskClass"])
			self._taskClasses.append((TaskClass, taskData))

		#热更新加载任务奖励
		for rewardData in data["rewards"]:
			reward = HotUpdateQuest("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
			reward.init(rewardData)
			self._rewards.append(reward)

		#热更新加载可接取任务显示的必备条件
		for requirementData in data["requirements"]:
			requirement = HotUpdateQuest("ConfigObject.Quest.QuestRequirements:%s" % requirementData["script"])()
			requirement.init(requirementData)
			self._requirements.append(requirement)

		#热更新接受任务时的关联功能
		for funcData in data["acceptedFunctions"]:
			function = HotUpdateQuest("ConfigObject.Quest.QuestFunctions:%s" % funcData["script"])()
			function.init(funcData)
			self._acceptedFunctions.append(function)

		#热更新放弃任务时的关联功能
		for funcData in data["abandonFunctions"]:
			function = HotUpdateQuest("ConfigObject.Quest.QuestFunctions:%s" % funcData["script"])()
			function.init(funcData)
			self._abandonFunctions.append(function)

		#热更新提交任务时的关联功能
		for funcData in data["committedFunctions"]:
			function = HotUpdateQuest("ConfigObject.Quest.QuestFunctions:%s" % funcData["script"])()
			function.init(funcData)
			self._committedFunctions.append(function)

		#热更新完成某个任务目标时的关联功能
		for taskStr, funcDataList in data["taskCompleteFunctions"].items():
			for funcData in funcDataList:
				function = HotUpdateQuest("ConfigObject.Quest.QuestFunctions:%s" % funcData["script"])()
				function.init(funcData)
				taskIDs = tuple( [ int( tid ) for tid in taskStr.split("|") ] )
				if not taskIDs in self._taskCompleteFunctions:
					self._taskCompleteFunctions[ taskIDs ] = []
				self._taskCompleteFunctions[ taskIDs ].append(function)
	@property
	def id(self):
		return self._id

	@property
	def type(self):
		return self._type

	@property
	def level(self):
		return self._level

	@property
	def title(self):
		return self._title

	def query(self, key, default = None):
		""""""
		if key in self._data:
			return self._data[key]
		else:
			return default

	def createNewTask(self, taskID):
		""""""
		for TaskClass, taskData in self._taskClasses:
			if taskData["id"] == taskID:
				task = TaskClass()
				task.initFromConfig(taskData)
				return task
		return None

	def createNewQuest(self):
		""""""
		quest = self._QuestClass()

		tasks = []
		for TaskClass, taskData in self._taskClasses:
			task = TaskClass()
			task.initFromConfig(taskData)
			tasks.append(task)

		quest.initFromConfig(self._id, tasks, self._data)

		return quest
	
	def getQuestDataByTalk( self, player ):
		"""
		点击任务选项后将任务数据发送到客户端以显示任务界面内容
		"""
		talkQuestData = {}
		rewards = {}
		
		status = player.queryQuestStatus( self._id )
		
		
		for reward in self._rewards:
			if isinstance( reward, QuestRewardChooseItem ):
				if str(csdefine.QUEST_REWARD_TYPE_ITEM_CHOOSE) not in rewards:
					rewards.update( {str(csdefine.QUEST_REWARD_TYPE_ITEM_CHOOSE): []} )
				rewards[str(csdefine.QUEST_REWARD_TYPE_ITEM_CHOOSE)].append( reward.sendClientData( player ) )
			else:
				rewards.update( reward.sendClientData( player ) )
				
		talkQuestData["id"] = str( self._id )
		talkQuestData["type"] = self.type
		talkQuestData["rewards"] = rewards
		talkQuestData["status"] = str( status )
		

		return talkQuestData
		
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
				taskID.append( taskData["id"] )

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

		}
		return questInfo
	
	def chooseRewardItem( self, index, itemInfo ):
		"""
		多个物品选择一个
		"""
		for reward in self._rewards:
			if getattr( reward, "chooseItem", None ) and reward.getIndex() == index:
				reward.chooseItem( itemInfo )
				return
	
	def rewardCheck(self, player, params = {}):
		"""奖励检查"""
		for reward in self._rewards:
			if not reward.check(player, params):
				return False
		return True

	def reward(self, player, params = {}):
		"""给与玩家排序后的奖励"""
		QuestRewardSequence().doGiveReward(player,self._rewards,self, params)

	def tryToReward(self, player, params = {}):
		"""必须保证所有奖励都可以成功发放，才发放奖励"""
		if self.rewardCheck(player, params):
			self.reward(player, params)
			return True
		else:
			return False

	def requirementCheck(self, player):
		"""判断玩家的条件是否满足可接取任务的显示要求"""
		for requirement in self._requirements:
			if not requirement.query(player):
				return False
		return True

	def canAcceptBy(self, player, params = {}):
		""""""
		return self.functionsCheck(self._acceptedFunctions, player, params)

	def canCommitBy(self, player, params = {}):
		return self.functionsCheck(self._committedFunctions, player, params)

	def canAbandonBy(self, player, params = {}):
		if self._canAbandon or player.abandonPrimaryFlag:
			return self.functionsCheck(self._abandonFunctions, player, params)
		else:
			player.statusMessage(csstatus.QUEST_CANNOT_ABANDON, "")
			return False

	def acceptedBy(self, player, params = {}):
		self.functionsDo(self._acceptedFunctions, player, params)

	def afterClientAccepted(self, player, params = {}):
		"""接了任务之后（通知了客户端），部分任务需要做处理"""
		player.questStatusChangeSkyBox()
		
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
			player.questAuto( self._id)

	def committedBy(self, player, params = {}):
		self.functionsDo(self._committedFunctions, player, params)

	def afterClientCommitted(self, player, params = {}):
		"""提交任务之后（通知了客户端），部分任务需要做处理"""
		player.questStatusChangeSkyBox()

	def abandonBy(self, player, params = {}):
		self.functionsDo(self._abandonFunctions, player, params)

	def afterClientAbandon(self, player, params = {}):
		"""放弃任务之后（通知了客户端），部分任务需要做处理"""
		player.questStatusChangeSkyBox()

	def canShare(self):
		"""判断当前任务是否能共享"""
		return bool(self._canShare)

	def getTitle(self):
		"""获取任务标题"""
		return self._title
		
	def getNextQuest( self, player ):
		"""获取nextQuest"""
		if self._nextQuestID.find("|") > 0:
			questIDList = self._nextQuestID.split("|")
			profession = player.getProfession()
			if len( questIDList ) <= profession - 1:
				KBEDebug.ERROR_MSG( "Quest(id:%i) can not find nextQuest(%s),as player profession(%i)"%(self.id, self._nextQuestID, profession ))
				return 0
			return int( questIDList[profession-1] )
		if self._nextQuestID == "":
			return 0
		return int( self._nextQuestID )

	def setCanAbandon(self, flagID):
		"""设置任务能否放弃的属性"""
		self._canAbandon = flagID

	@staticmethod
	def functionsCheck(functions, player, params = {}):
		for func in functions:
			if not func.check(player, params):
				return False
		return True

	@staticmethod
	def functionsDo(functions, player, params = {}):
		for func in functions:
			func.do(player, params)