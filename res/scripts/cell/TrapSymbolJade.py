# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from Trap import Trap
import csdefine
import time

class TrapSymbolJade( Trap ):
	"""
	陷阱 符玉
	"""
	def __init__( self ):
		Trap.__init__( self )
		self.registToSpace()

	def registToSpace( self ):
		"""注册到space"""
		space = self.getCurrentSpace()
		if space:
			space.registTrapToSpace( self.id )
		
	def unRegistToSpace( self ):
		"""取消注册"""
		space = self.getCurrentSpace()
		if space:
			space.unRegistTrapToSpace( self.id )

	def delayOnEnterDead( self ):
		"""
		延迟进入死亡状态
		"""
		lifeTime = self.lifeTime - time.time()
		if lifeTime > 0:
			self.addTimerCallBack(lifeTime,"changeState",(csdefine.ENTITY_STATE_DEAD,))
	

	def onEnterDead( self ):
		"""
		virtual method
		进入死亡状态
		"""
		self.unRegistToSpace()
		Trap.onEnterDead( self )