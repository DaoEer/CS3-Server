# -*- coding: utf-8 -*-

import Math
#cell
from MovingPlatform import MovingPlatform
import KBEDebug

class MovingPlatformLotus( MovingPlatform ):
	"""
	莲叶移动平台
	"""
	def __init__( self ):
		MovingPlatform.__init__( self )
		self.upAndDownDis = 0.0
		self._standTimes = 1
		self._spawnPos = Math.Vector3(self.position.x, self.position.y, self.position.z)

	def onsTandLotus(self):
		object = self.getScript()
		if not object.isStandMove:
			return
		if self._standTimes > 1:
			return
		self.lotusMoveStart()
		self._standTimes += 1

	def resetPosition(self):
		"""
		Define method
		重置位置
		"""
		if self._standTimes > 1:
			self._standTimes = 1
			self.moveToPosition( self._spawnPos,False,True )

	def lotusMoveStart(self):
		"""
		Define method
		开始移动
		"""
		if self._standTimes > 1:
			return
		object = self.getScript()
		if object.moveDirect == 1:
			dstPos = Math.Vector3(self.position.x, self.position.y+object.moveDistance, self.position.z)
			self.moveToPosition( dstPos,False,True )
		elif object.moveDirect == 2:
			dstPos = Math.Vector3(self.position.x, self.position.y + object.moveDistance, self.position.z)
			self.moveToPosition( dstPos,False,True )
			self.upAndDownDis = -(object.moveDistance * 2)
		self._standTimes += 1

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		MovingPlatform.onMoveOver( self, controllerID, userData )
		object = self.getScript()
		if object.moveDirect == 2:
			dstPos = Math.Vector3(self.position.x,self.position.y + self.upAndDownDis,self.position.z)
			self.moveToPosition( dstPos,False,True )
			self.upAndDownDis = -self.upAndDownDis




