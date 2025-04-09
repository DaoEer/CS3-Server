# -*- coding: utf-8 -*-


import KBEDebug
import csdefine
import Functions
#cell
from MovingPlatform import MovingPlatform

class MovingPlatformShade( MovingPlatform ):
	"""
	移动平台 逐渐透明至消失
	"""
	def __init__( self ):
		MovingPlatform.__init__( self )
		
		if self.hasFlag( csdefine.FLAG_AI_TICK ):
			self.isShadeing = 1
			self.addTimerCallBack( 2.0, "startShaderMove", ())
		
	def startMove( self ):
		"""
		开始移动(屏蔽MovingPlatform的移动方式)
		"""
		pass
		
	def startShaderMove( self ):
		"""
		开始移动
		"""
		MovingPlatform.startMove( self )
		self.delayShade()
		
	def delayShade( self ):
		if self.isShadeing:
			object = self.getScript()
			if object.shadeTime > 0:
				self.addTimerCallBack( object.shadeTime, "beginShade", () )
			
	def beginShade( self ):
		"""开始渐变过程"""
		object = self.getScript()
		warnParticle = ""
		if object.warnParticle:
			warnParticle = "|" + object.warnParticle
		if object.shadeDurationTime > 0:
			self.shadeTime = "1|" + str( Functions.getTime( object.shadeDurationTime ) ) + warnParticle
			self.addTimerCallBack( object.shadeDurationTime + object.endShadeTime, "showAgain", () )
		else:
			self.shadeTime = "1|0" + warnParticle
			self.showAgain()
			
	def showAgain( self ):
		"""
		再次显示
		"""
		object = self.getScript()
		if object.endShadeDurationTime > 0:
			self.shadeTime = "2|" + str( Functions.getTime( object.endShadeDurationTime ) )
			self.addTimerCallBack( object.endShadeDurationTime + object.endShadeTime, "delayShade", () )
		else:
			self.shadeTime = "2|0"
			self.delayShade()
		
	def onWitnessed( self, isWitnessed ):
		"""
		玩家视野范围内才开始执行
		"""
		if not self.hasFlag( csdefine.FLAG_AI_TICK ):
			if isWitnessed:
				self.isShadeing = 1
				self.startShaderMove()
			else:
				self.isShadeing = 0
