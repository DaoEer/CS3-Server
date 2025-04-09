# -*- coding: utf-8 -*-

from BotTasks.Targets import TargetBase
from BotTasks.Actions import ActionBase


class BehaviourBase( object ):
	_BEHAVIOUR_CLASS = {}
	def __init__( self, bid, config ):
		self._id = bid
		self._actions = {}
		#self._targets = []
		self.initData( config )
		
	@classmethod
	def setClass( SELF, className, classObj ):
		SELF._BEHAVIOUR_CLASS[ className ] = classObj
	
	@classmethod
	def getClassObj( SELF, bid, config ):
		scriptName = config[ "Script" ]
		return SELF._BEHAVIOUR_CLASS[ scriptName ]( bid, config )
	
	def initData( self, config ):
		for id,actSec in config[ "actions" ].items():
			self._actions[int(id)] = ActionBase.ActionBase.getClassObj( actSec )

		#for tarSec in config[ "targets" ]:
			#self._targets.append( TargetBase.TargetBase.getClassObj( tarSec ) )
			
	def getID(self):
		return self._id

	def doOver( self, roleEntity, index ):
		"""
		检查Action是否完成目标
		"""
		return self._actions[ index ].checkIsCompleted( roleEntity )
	
	def isArrived(self, roleEntity, index):
		"""
		检查机器人是否到达目标位置
		"""
		return self._actions[ index ].isArrived(roleEntity)
		
	def arrive(self, roleEntity, index):
		"""
		机器人向目标位置移动
		"""
		return self._actions[ index ].arrive(roleEntity)
	
	def doAction( self, roleEntity, index ):
		if index >= len( self._actions ):
			return False
		else:
			self._actions[ index ].doAction( roleEntity )
			return True
		
	def getNext(self,entity):
		return None
		
	def actionKeys( self ):
		return sorted(self._actions.keys())
	