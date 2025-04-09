# -*- coding: utf-8 -*-
#############
# 火海怪物entity
#############

import ObjectScript.Monster.Monster as Monster


class MonsterExtCircleEffect( Monster.Monster ):
	"""
	火海怪物entity
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.startRadius = 0.0
		self.height = 0.0
		self.totalTime = 0.0
		self.holdTime = 0.0
		self.intervalTime = 0.0
		
	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		Param1 =configData["Param1"].split("|")
		self.startRadius = float(Param1[0])
		if len(Param1) > 1:
			self.height = float(Param1[1])
		Param2 = configData["Param2"].split("|")
		self.totalTime = float(Param2[0])
		self.intervalTime = float(Param2[1])
		self.holdTime = float(Param2[2])
		self.buffID = int(configData["Param3"])
		
	def getRadius(self):
		"""
		外圈半径
		"""
		return self.startRadius

	def getHeight(self):
		return self.height

	def getTotalTime(self):
		"""
		缩放总时间
		"""
		return self.totalTime

	def getIntervalTime(self):
		"""
		移动间隔时间
		"""
		return self.intervalTime

	def getHoldTime(self):
		"""
		移动间隔时间
		"""
		return self.holdTime

	def getBuffID(self):
		return self.buffID