# -*- coding: utf-8 -*-

from BotTasks.BehaviorBase import BehaviourBase

class Behaviour1( BehaviourBase.BehaviourBase ):
	def __init__( self, bid, config  ):
		BehaviourBase.BehaviourBase.__init__( self, bid, config  )

#做任务行为
class Behaviour2( BehaviourBase.BehaviourBase ):
	def __init__( self, bid, config  ):
		BehaviourBase.BehaviourBase.__init__( self, bid, config  )
		self.nextQuestID = config["nextqid"]
		
	def doAction( self, roleEntity, index ):
		if int(index) >= len( self._actions ):
			roleEntity.outputMsg("behaviour finish behOver")
			roleEntity.behOver()
		else:
			self._actions[ index ].doAction( roleEntity )
	
	def getNext(self,entity):
		if "|" in self.nextQuestID:
			return self.nextQuestID.split("|")[ entity.getProfession() ]
		return self.nextQuestID
		
#完成副本
class Behaviour3( BehaviourBase.BehaviourBase ):
	def __init__( self, bid, config  ):
		BehaviourBase.BehaviourBase.__init__( self, bid, config  )
		self.nextSpace = ""
		
	def doAction( self, roleEntity, index ):
		if int(index) >= len( self._actions ):
			roleEntity.outputMsg("behaviour finish behOver")
			roleEntity.behOver()
		else:
			self._actions[ index ].doAction( roleEntity )
	
	def getNext(self,entity):
		return None
		

BehaviourBase.BehaviourBase.setClass( "Behaviour1", Behaviour1 )
BehaviourBase.BehaviourBase.setClass( "Behaviour2", Behaviour2 )
BehaviourBase.BehaviourBase.setClass( "Behaviour3", Behaviour3 )