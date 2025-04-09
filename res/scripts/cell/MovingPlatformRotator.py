# -*- coding: utf-8 -*-


import KBEDebug
import csdefine
import Functions
#cell
from MovingPlatform import MovingPlatform

class MovingPlatformRotator( MovingPlatform ):
	"""
	旋转类型平台脚本
	"""
	def __init__( self ):
		MovingPlatform.__init__( self )

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		self.startRotat()
		
	def startRotat( self ):
		"""
		开始旋转
		"""
		object = self.getScript()
		self.startLoopRotator(object.moveSpeed)