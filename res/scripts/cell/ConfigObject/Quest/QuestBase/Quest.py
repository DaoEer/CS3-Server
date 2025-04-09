# -*- coding: utf-8 -*-
#
from KBEDebug import *
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
from MsgLogger import g_logger
import csstatus


class Quest:
	def __init__(self):
		self._id = 0
		self._tasks = {}
		self._script = None

	def initFromConfig(self, id, tasks, data):
		self._id = id
		for task in tasks:
			self._tasks[task.id] = task

	def initFromStream(self, data):
		self._id = data["id"]
		for task in data["tasks"]:
			if task["id"] not in self._tasks:
				return
			self._tasks[task["id"]].initFromStream(task)

	def packStreamData(self):
		tasks = [t.packStreamData() for t in self._tasks.values()]
		return {"id": self._id, "tasks": tasks}

	@property
	def id(self):
		return self._id

	@property
	def type(self):
		return self.getScript().type

	def getScript(self):
		if not self._script:
			self._script =  g_QuestLoader.getScript(self._id)
		
		return self._script
		
	def getTask( self, index ):
		if index in self._tasks:
			return self._tasks[index]
		return None

	def checkQuestIsTimeOut( self ):
		"""
		"""
		return False
		
	def getCurPriority( self ):
		"""获取当前的任务目标优先级"""
		tasks = sorted( self._tasks.values(), key = lambda x :x.priority )
		for task in tasks:
			if task.isDone():continue
			return task.priority
		return 0
		
	def onPlayerAddQuest( self, player ):
		"""玩家添加任务"""
		curPriority = self.getCurPriority()
		for task in self._tasks.values():											# 根据任务目标优先级先刷新任务目标\注册
			if curPriority >= task.priority:
				if task.refreshProgress( player ):
					player.client.onUpdateQuestTask(self._id, task.id, task.progress)
					if task.isDone():
						questScript = self.getScript()
						questScript.taskCompleteBy( player, task.id, {} )
						self.onTaskCompleted( task.id, player )
						return
			task.registerEvent( self, player )
		
	def onPlayerRemoveQuest( self, player ):
		"""玩家移除任务"""
		for task in self._tasks.values():
			task.deregisterEvent( self, player )
			
	def onPlayerLogin( self, player ):
		"""玩家登陆"""
		curPriority = self.getCurPriority()
		for task in self._tasks.values():
			if task.isDone():continue
			if curPriority >= task.priority:
				task.registerEvent( self, player )
				
	def onTaskCompleted( self, taskID, player ):
		"""某个任务目标完成"""
		task = self.getTask( taskID )
		if task:
			curPriority = self.getCurPriority()
			if curPriority == 0 or curPriority == task.priority:
				return														# 如果当前优先级，还没有完成！则下一个优先级任务目标不注册
			for otask in self._tasks.values():
				if otask.priority == curPriority:
					if otask.refreshProgress( player ):
						player.client.onUpdateQuestTask(self._id, otask.id, otask.progress)
						if otask.isDone():
							questScript = self.getScript()
							questScript.taskCompleteBy( player, otask.id, {} )
							self.onTaskCompleted( otask.id, player )
							return
				otask.registerEvent( self, player )

	def updateTask(self, player, eventID, taskID, params):
		"""更新任务目标进度"""
		if not self.canUpdateTaskProgress( taskID ):				#
			return
		if taskID in self._tasks:
			presentTaskState = self._tasks[taskID].isDone()
			if(self._tasks[taskID].updateProgress(player, eventID, params)):
				if player.client is not None:
					player.client.onUpdateQuestTask(self._id, taskID, self._tasks[taskID].progress)
				if self._tasks[taskID].isDone() and presentTaskState == False:
					questScript = g_QuestLoader.getScript( self._id )
					questScript.taskCompleteBy( player, taskID, params )
					self.onTaskCompleted( taskID, player )
				
				# 任务完成通知
				if self.isDone():
					# 通知客户端任务为完成状态 需更新任务列表界面该任务的状态标识
					player.client.onQuestComplete(self._id)
					#添加日志
					g_logger.completeQuestLog( player.playerDBID, player.getName(), self.id, self.getScript().getTitle(), player.getLevel(), player.grade )
					
		else:
			ERROR_MSG("Task %i is not in quest %i" % (taskID, self._id))
			
	def completeTask(self, player, taskID, params):
		"""使指定任务目标为完成状态"""
		if not self.canUpdateTaskProgress( taskID ):
			return
		if taskID in self._tasks:
			#将指定任务目标设置为完成
			self._tasks[taskID].setDone()
			
			if player.client is not None:
				player.client.onUpdateQuestTask(self._id, taskID, self._tasks[taskID].progress)
			if self._tasks[taskID].isDone():
				questScript = g_QuestLoader.getScript( self._id )
				questScript.taskCompleteBy( player, taskID, params )
				self.onTaskCompleted( taskID, player )
				
			# 任务完成通知
			if self.isDone():
				# 通知客户端任务为完成状态 需更新任务列表界面该任务的状态标识
				player.client.onQuestComplete(self._id)
				#添加日志
				g_logger.completeQuestLog( player.playerDBID, player.getName(), self.id, self.getScript().getTitle(), player.getLevel(), player.grade )
		else:
			ERROR_MSG("Task %i is not in quest %i" % (taskID, self._id))
		
	def canUpdateTaskProgress( self, taskID ):
		"""是否能更新任务目标"""
		# 需要按优先级顺序完成任务目标
		priority = self._tasks[taskID].priority
		for task in self._tasks.values():
			if task.priority < priority and not task.isDone():
				return False										# 数字越低，优先级越高
		return True

	def resetTask(self, player ):
		"""
		重置任务目标
		"""
		if taskID in self._tasks:
			if(self._tasks[taskID].resetProgress(player)):
				if player.client is not None:
					player.client.onUpdateQuestTask(self._id, taskID, self._tasks[taskID].progress)

	def resetOneTask(self, player, taskID):
		"""
		重置某个任务目标
		"""
		self._tasks[taskID].resetProgress( player )
		player.client.onUpdateQuestTask(self._id, taskID, self._tasks[taskID].progress)

	def onDone(self, player):
		"""任务完成"""
		#默认任务完成自动提交
		player.commitQuest(self._id)

	def isDone(self):
		"""任务是否完成"""
		for task in self._tasks.values():
			if not task.isDone():
				return False
		return True

	def setDone(self, player):
		"""让任务自动完成，可用于测试"""
		for task in self._tasks.values():
			if not task.isDone():
				task.setDone()
				if player.client is not None:
					player.client.onUpdateQuestTask(self._id, task.id, self._tasks[task.id].progress)
					player.client.onQuestComplete(self._id)

	def taskProgress(self, taskID):
		"""查询某个任务目标的进度"""
		if taskID in self._tasks:
			return self._tasks[taskID].progress
		else:
			return None

	def taskIsDone(self, taskID):
		"""查询某个任务目标是否完成"""
		if taskID in self._tasks:
			return self._tasks[taskID].isDone()
		else:
			return False

	def gmSetTaskDone( self, player, qusetID, taskID, progress):
		"""
		GM命令改变任务目标状态
		"""
		priority = self._tasks[taskID].priority
		for task in self._tasks.values():
			if task.priority < priority and not task.isDone():
				player.statusMessage( csstatus.GM_QUEST_TASK_USE_FAILURE )
				return
		self._tasks[taskID]._progress += int(progress)
		if self._tasks[taskID].goal < self._tasks[taskID]._progress:
			self._tasks[taskID]._progress = self._tasks[taskID].goal
		
		if player.client is not None:
				player.client.onUpdateQuestTask(self._id, taskID, self._tasks[taskID].progress)

		if self._tasks[taskID]._progress >= self._tasks[taskID].goal:
			self._tasks[taskID].setDone()

		if self._tasks[taskID].isDone():
			questScript = g_QuestLoader.getScript( self._id )
			questScript.taskCompleteBy( player, taskID, {} )
			self.onTaskCompleted( taskID, player )
				
			# 任务完成通知
		if self.isDone():
			# 通知客户端任务为完成状态 需更新任务列表界面该任务的状态标识
			player.client.onQuestComplete(self._id)
		return True
