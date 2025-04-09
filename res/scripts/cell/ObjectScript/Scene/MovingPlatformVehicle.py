# -*- coding: utf-8 -*-


#cell
import ObjectScript.Scene.MovingPlatform as MovingPlatform
import Math
import math

class MovingPlatformVehicle( MovingPlatform.MovingPlatform ):
	"""
	可移动载具
	"""
	def __init__( self ):
		MovingPlatform.MovingPlatform.__init__( self )
		self.childrenCanMove = 0	#移动平台上的Entity能不能自动控制移动
		self.socketList = []			#插槽列表
		self.maxNum = 2			#最大乘坐数量
		self.riderModelId = ""
		self.triggerBuffs = []

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		MovingPlatform.MovingPlatform.initData( self, configData )
		if configData["Param2"]:
			strList = configData["Param2"].split(":")
			if len(strList) >= 2:
				self.riderModelId  = strList[0]
				self.triggerBuffs = strList[1].split("|")
			elif len(strList) == 1:
				self.riderModelId = strList[0]
		if configData["Param3"]:
			splitStr = configData["Param3"].split(":")
			if len(splitStr) >= 2:
				self.maxNum = int(splitStr[0])
				self.socketList = splitStr[1].split("|")
			elif len(splitStr) == 1:
				self.socketList = splitStr[0].split("|")
				self.maxNum = len(self.socketList)
		"""
		预留
		if configData["Param4"]:
			self.childrenCanMove = float(configData["Param4"])
		"""