# -*- coding: utf-8 -*-


#cell
import ObjectScript.Scene.MovingPlatform as MovingPlatform
import Math
import math

class MovingPlatformRotator( MovingPlatform.MovingPlatform ):
	"""
	旋转类型平台脚本
	"""
	def __init__( self ):
		MovingPlatform.MovingPlatform.__init__( self )
		self.moveSpeed = 0.0


	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		MovingPlatform.MovingPlatform.initData( self, configData )
		if configData["Param2"]:
			self.moveSpeed = float(configData["Param2"])