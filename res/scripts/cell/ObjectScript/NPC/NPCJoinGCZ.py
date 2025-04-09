# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
from ObjectScript.NPC import NPC
DIALOG_TALK_KEY = ""
EXTRA_TALK_PARAM = ""

class NPCJoinGCZ( NPC.NPC ):
	def __init__( self ):
		NPC.NPC.__init__( self )
		self.numGCZs = []			# 攻城战场次
		self.gczStartTimes = []		# 攻城战开始时间
		self.gczMaxJoinNums = []	# 攻城战最大参加人数
		self.needLevel = 0			# 报名要求等级
		self.needSoldierNum = 0 	# 报名要求士兵数

	def initData( self, configData ):
		if configData is not None:
			NPC.NPC.initData( self, configData )
			self.numGCZs = [int(i) for i in configData["Param1"].split("|")]
			self.gczStartTimes = configData["Param2"].split("|")
			self.gczMaxJoinNums = [int(i) for i in configData["Param3"].split("|")]
			self.needLevel = int( configData["Param4"] )
			self.needSoldierNum = int( configData["Param5"] )

	def getReqLevel( self ):
		return self.needLevel

	def getReqSoldierNum( self ):
		return self.needSoldierNum

	def getMaxJoinNumByNum( self, num ):
		"""
		获得参加攻城战最大人数
		"""
		if num in self.numGCZs:
			index = self.numGCZs.index(num)
			return self.gczMaxJoinNums[index]
		return 0

	def getGCZStartTimeByNum( self, num ):
		"""
		获得攻城战的时间
		"""
		if num in self.numGCZs:
			index = self.numGCZs.index(num)
			return self.gczStartTimes[index]
		return ""

	def getNumberGCZs( self ):
		return self.numGCZs

	def getGCZStartTimes( self ):
		return self.gczStartTimes

	def getGCZMaxJoinNums( self ):
		return self.gczMaxJoinNums
		
		
		