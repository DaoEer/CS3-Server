# -*- coding: utf-8 -*-
from ObjectScript.NPC import NPC

class NPCExtPoint( NPC.NPC ):
	def __init__( self ):
		NPC.NPC.__init__( self )
		self.enterPVESpace = "" #进入PVE的space
		self.enterPVPSpace = "" #进入PVP的space
		self.readyTime = 0.0	#准备时间
		self.maxJoinPlayerNum = 0	# 加入的最大人数
		self.restTime = 0.0		# 休整的时间

	def initData( self, configData ):
		NPC.NPC.initData( self, configData )
		self.setEntityProperty("pointType",int(configData["Param1"]))
		self.enterPVESpace = configData["Param2"]
		self.enterPVPSpace = configData["Param3"]
		self.maxJoinPlayerNum = int( configData["Param4"] )
		if configData["Param5"]:
			self.readyTime = float( configData["Param5"].split("|")[0] )
			if len(configData["Param5"].split("|")) > 1:
				self.restTime = float( configData["Param5"].split("|")[1] )

	def getReadTime( self ):
		"""
		获得准备的时间
		"""
		return self.readyTime

	def getEnterPVESpace( self ):
		"""
		获得进入PVE space
		"""
		return self.enterPVESpace

	def getEnterPVPSpace( self ):
		"""
		获得进入PVP space
		"""
		return self.enterPVPSpace

	def getMaxJoinPlayerNum( self ):
		"""
		获得加入的最大成员数
		"""
		return self.maxJoinPlayerNum

	def getRestTime( self ):
		"""
		获得休整的时间
		"""
		return self.restTime