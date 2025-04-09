# -*- coding: utf-8 -*-
import copy

from BotTasks.Behaviours import BehaviourBase

class TaskBase( object ):
	_TASK_CLASS = {}
	def __init__( self, taskID, config ):
		self.taskID = taskID
		self._behaviours = {}	#当前任务的行为列表
		self._orderList = []
		self.initData( config )
		
	@classmethod
	def setClass( SELF, className, classObj ):
		SELF._TASK_CLASS[ className ] = classObj
	
	@classmethod
	def getClassObj( SELF, className, taskID, config ):
		return SELF._TASK_CLASS[ className ]( taskID, config )

	def getOrderList( self ):
		return copy.copy( self._orderList )

	def initData( self, config ):
		"""
		初始化数据
		"""
		self._orderList = sorted( config.keys() )
		for bid, section in config.items():
			self._behaviours[ bid ] = BehaviourBase.BehaviourBase.getClassObj( bid, section )

	def initBehMgr( self, roleEntity ):
		"""
		开始
		"""
		for bid, bobj in self._behaviours.items():
			roleEntity.behaviours.addBehaviour(  bid, bobj )  
