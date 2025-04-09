# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine

from Extra.KBEIOLoop import KBEIOLoop
from CoreObject import MgrPersistentObject

class KBEIOLoopEntity( MgrPersistentObject.MgrPersistentObject ):
	"""
	这个KBEngine.Entity的主要作用是借助timer来loop检测IO端口
	用于tornado的AsyncHTTPClient访问远程服务器。
	"""
	def  __init__( self ):
		"""
		"""
		KBEngine.Entity.__init__(self)
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.kbeIOLoop = KBEIOLoop()
		self.kbeIOLoop.install()
		
		self.kbeIOLoop.parentEntity = self
		self.kbeIOLoop.start()
		self.onCompleteInit()
		
	def onDestroy(self):
		"""
		KBEngine method
		"""
		self.kbeIOLoop.stop()
		self.kbeIOLoop = None
		
	def onTimer(self, timerHandle, userData):
		"""
		KBEngine method
		"""
		if self.isDestroyed: return
		self.kbeIOLoop.onTimer(timerHandle, userData)
		