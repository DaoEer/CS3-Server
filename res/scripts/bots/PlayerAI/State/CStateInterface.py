# -*- coding: utf-8 -*-

import weakref

class eAIState(object):
	"""
	"""
	NULL = 0
	Idle = 1
	Attack = 2
	RunAction = 3
	Run = 4
	HoldState = 5
	Team = 6
	Dead = 7
	Pet = 8
	Teleport = 9
	Tong = 10
	Space = 11
	CleanSys = 12
	CItem = 13
	CChat = 14
	
	
class CStateBase(object):
	"""
	"""
	def __init__(self, ai):
		"""
		"""
		self.ai = weakref.proxy(ai)
		
	def enter(self):
		pass
		
	def leave(self):
		pass
		
	def reEnter(self):
		pass
		
		
	def onEnterWorld(self):
		pass
		
	def onLeaveWorld(self):
		pass
		
	def onEnterSpace(self):
		pass
		
	def onLeaveSpace(self):
		pass
		
	def onMoveOver(self, controllerID, userData):
		pass
		
	def onMoveFailure(self, controllerID, userData):
		pass
		
	def onTickCallBack(self, tick):
		pass