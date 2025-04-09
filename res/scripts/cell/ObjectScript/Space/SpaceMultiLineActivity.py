# -*- coding: utf-8 -*-

import Const
import KBEngine
import csdefine
import random
import ItemFactory
import csstatus
from ObjectScript.Space.SpaceMultiLine import SpaceMultiLine

class SpaceMultiLineActivity( SpaceMultiLine ):
	"""
	大地图活动
	"""
	def __init__( self ):
		SpaceMultiLine.__init__( self )

	def initData( self, configData ):
		SpaceMultiLine.initData( self, configData )

		self.goldTreeAreaIndex = []   #金树种子圆形区域标识 
		areaIndex = configData["SpaceData"].get("CircleAreaIndex","")  #活动名:index index...|活动名:index index...
		if areaIndex:
			self.setAreaIndex(areaIndex)
		
		LLBZ = configData["SpaceData"].get("LLBZArea","")
		self.LLBZgreyBuffID = int(configData["SpaceData"].get("LLBZgreyBuff", 0))
		if LLBZ:
			self.setLLBZData(LLBZ)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

	def setCircleAreaIndex(self, areaIndexStr):
		"""
		设置活动圆形区域标识
		"""
		List = areaIndexStr.split("|")
		for string in List:		
			if string.split(":")[0] == "GoldTree":  #金树种子圆形区域标识
				self.goldTreeAreaIndex = [int(i) for i in string.split(":")[0].split()]

	#---------------------------福袋活动--------------------------------------------
	def onEnterActivityCircleArea(self, playerRole, areaIndex):
		if areaIndex in self.goldTreeAreaIndex:		# 显示金树种子罗盘
			playerRole.client.CLIENT_ShowGoldTreeCompass(areaIndex)

	def onLeaveActivityCircleArea(self, playerRole, areaIndex):
		if areaIndex == self.goldTreeAreaIndex[-1]:		# 关闭金树种子罗盘
			playerRole.client.CLIENT_ShowGoldTreeCompass(0)