# -*- coding: utf-8 -*-
from MovingPlatform import MovingPlatform
class MovingPlatformTrigger( MovingPlatform ):
	"""
	移动平台
	"""
	def __init__( self ):
		MovingPlatform.__init__( self )
	def OnReadyToMoveBack(self):
		pass
		
	def OnReadyToMove(self):
		pass
