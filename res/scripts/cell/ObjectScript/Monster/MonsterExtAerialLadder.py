# -*- coding: utf-8 -*-
import ObjectScript.Monster.Monster as Monster
import KBEDebug

class MonsterExtAerialLadder( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.finishActionID = ""
		self.fallActionID = ""
		self.initActionID = ""
		self.leaveTopOffset = 0.0 # 玩家顶部离开云梯偏移量
		self.climbLadderSpeed = 0.0 # 玩家攀爬梯子速度
		self.buffID = 0 # 玩家进入云梯变身姿势Buff

	def initData( self, configData ):
		Monster.Monster.initData( self, configData )
		self.finishActionID = configData["Param1"].split("|")[0]
		self.fallActionID = configData["Param2"]
		if len(configData["Param1"].split("|")) > 1:
			self.initActionID = configData["Param1"].split("|")[1]
		if configData["Param3"]:
			self.leaveTopOffset = float(configData["Param3"])
		if configData["Param4"]:
			self.climbLadderSpeed = float(configData["Param4"])
		if configData["Param5"]:
			self.buffID = int( configData["Param5"] )
