# -*- coding: utf-8 -*-

from BotTasks import Tasks
from BotTasks import config

class TaskManager( dict ):
	def __init__( self ):
		dict.__init__( self )
	
	def getTask( self, taskName ):
		"""
		开始行为
		"""
		if not taskName in self:
			configSec = config.getSourceConfig( taskName )
			self[ taskName ] = Tasks.TaskBase.TaskBase.getClassObj( "TaskCommond", taskName, configSec.Datas )

		return self[ taskName ]

g_taskMgr = TaskManager()