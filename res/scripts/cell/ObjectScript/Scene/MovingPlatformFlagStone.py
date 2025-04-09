# -*- coding: utf-8 -*-


#cell
import ObjectScript.Scene.MovingPlatformLotus as MovingPlatformLotus

class MovingPlatformFlagStone( MovingPlatformLotus.MovingPlatformLotus ):
	"""
	石板移动平台脚本
	"""
	def __init__( self ):
		MovingPlatformLotus.MovingPlatformLotus.__init__( self )
		self.isStandMove = 0