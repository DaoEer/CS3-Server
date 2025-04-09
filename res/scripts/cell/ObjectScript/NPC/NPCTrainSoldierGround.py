# -*- coding: utf-8 -*-
from ObjectScript.NPC import NPC

class NPCTrainSoldierGround( NPC.NPC ):
	def __init__( self ):
		NPC.NPC.__init__( self )
		self.startHour = 0 #宣战和争夺开始时间
		self.endHour = 0	#宣战和争夺结束时间
		self.enterPVESpace = "" #进入PVE的space
		self.enterPVPSpace = "" #进入PVP的space
		self.trainGroundType = 0

	def initData( self, configData ):
		NPC.NPC.initData( self, configData )
		if configData["Param1"]:
			self.startHour = int(configData["Param1"].split("-")[0])
			self.endHour = int(configData["Param1"].split("-")[1])

		self.enterPVESpace = configData["Param2"]
		self.enterPVPSpace = configData["Param3"]

		if configData["Param4"]:
			self.trainGroundType = int(configData["Param4"])

	def getStartHour( self ):
		"""
		获得开始时间小时
		"""
		return self.startHour

	def getEndHour( self ):
		"""
		获得结束时间
		"""
		return self.endHour

	def getEnterPVESpace( self ):
		return self.enterPVESpace

	def getEnterPVPSpace( self ):
		return self.enterPVPSpace

	def getTrainGroundType( self ):
		return self.trainGroundType
