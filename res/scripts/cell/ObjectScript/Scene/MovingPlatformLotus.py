# -*- coding: utf-8 -*-


#cell
import ObjectScript.Scene.MovingPlatform as MovingPlatform

class MovingPlatformLotus( MovingPlatform.MovingPlatform ):
	"""
	莲叶移动平台脚本
	"""
	def __init__( self ):
		MovingPlatform.MovingPlatform.__init__( self )
		self.moveDirect = 0
		self.moveDistance = 0
		self.isStandMove = 1

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		MovingPlatform.MovingPlatform.initData( self, configData )
		if configData["Param2"]:
			self.moveDirect = int(configData["Param2"])
		if configData["Param3"]:
			self.moveDistance = float(configData["Param3"])
