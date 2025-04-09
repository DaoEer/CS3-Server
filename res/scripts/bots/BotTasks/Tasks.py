# -*- coding: utf-8 -*-

from BotTasks.BehaviorBase import TaskBase

#quest
class TaskCommond( TaskBase.TaskBase ):
	def __init__( self, taskID, config ):
		TaskBase.TaskBase.__init__( self, taskID, config )
		

	def checkIsCompleted( self, roleEntity ):
		return True

TaskBase.TaskBase.setClass( "TaskCommond", TaskCommond )