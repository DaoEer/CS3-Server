# -*- coding: utf-8 -*-


import ObjectScript.Scene.MovingPlatform as MovingPlatform

class MovingPlatformTrigger( MovingPlatform.MovingPlatform ):

	def __init__( self ):
		MovingPlatform.MovingPlatform.__init__( self )
		self.playAction = ""
		self.delayTime = 0.0
		self.triggerBuffs = []
		self.startBuffs = []

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		MovingPlatform.MovingPlatform.initData( self, configData )
		strList = configData["Param2"].split("|")
		self.playAction = strList[0]
		if len(strList)> 1:
			self.triggerBuffs = [int(i) for i in strList[1].split(":")]
		if len(strList)> 2:
			self.startBuffs = [int(i) for i in strList[2].split(":")]
		if configData["Param3"]:
			self.delayTime = float(configData["Param3"])

