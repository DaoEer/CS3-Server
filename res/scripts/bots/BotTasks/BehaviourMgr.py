# -*- coding: utf-8 -*-
#
import KBEngine
import KBEDebug
import csdefine
import Define

from BotTasks import config
from BotTasks.BehaviorBase import TaskManager

class BehaviourControl( object ):
	"""
	BOT行为管理器，用于BOT行为排队功能
	"""
	def __init__( self, behObj ):
		object.__init__( self )
		self.behObj = behObj
		self.actList = self.behObj.actionKeys()
		self.actionIndex = self.actList.pop(0)
		
	def reset( self, entity ):
		"""
		重置
		"""
		self.behObj = None
		self.actList = self.behObj.actionKeys()		
		self.actionIndex = self.actList.pop(0)
	
	def isCanAddBehavior( self, entity, args, priorityLevel = csdefine.BEHAVIOUR_COMMON ):
		if priorityLevel not in self or len( self[ priorityLevel ] ) == 0:
			return True
		return False

	def do( self, entity ):
		if not self.behObj.isArrived(entity, self.actionIndex):
			self.behObj.arrive(entity, self.actionIndex)
		else:
			self.behObj.doAction( entity, self.actionIndex )
		
	def doOver( self, entity ):
		if self.behObj.doOver( entity, self.actionIndex ):
			self.doNext(entity)
		else:
			self.do(entity)
		
	def doNext(self,entity):
		entity.resetMonsterCounter()
		if not self.actList:
			entity.behDoNext()
			return
		self.actionIndex = self.actList.pop(0)
		self.do(entity)
		
	def getNext(self,entity):
		return self.behObj.getNext(entity)


class BehaviourMgr( dict ):
	def __init__( self ):
		self.currentID = 0
		self.doList = [] #执行顺序
		self.taskObj = None

	def doOver( self, entity ):
		if self.currentID ==0:
			return
		self[ self.currentID ].doOver( entity )
	
	def doNext( self, entity ):
		self.currentID = self[ self.currentID ].getNext(entity)
		if self.currentID is None:
			if len(self.doList)==0:
				entity.outputMsg("behaviour %s is finished"%self.currentID)
				return			
			self.currentID = self.doList.pop( 0 )
			self[ self.currentID ].do( entity )			
		elif self.currentID in self:
			self[ self.currentID ].do( entity )
		else:
			entity.outputMsg("behaviour %s is not found!"%self.currentID )

	def addBehaviour( self, bid, behObj ):
		self[ bid ] = BehaviourControl( behObj )

	def startTask( self, entity, taskName, startKey ):
		entity.GMCommand( entity, "full", "" )
		self.taskObj = TaskManager.g_taskMgr.getTask( taskName )
		if taskName == "quest":
			startKey = "20101010"
		if self.taskObj:
			self.doList = self.taskObj.getOrderList()
			self.currentID = startKey
			self.taskObj.initBehMgr( entity )
			self[ self.currentID ].do( entity )
