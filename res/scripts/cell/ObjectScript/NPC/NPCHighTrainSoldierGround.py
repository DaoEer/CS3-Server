# -*- coding: utf-8 -*-
from ObjectScript.NPC import NPCTrainSoldierGround

class NPCHighTrainSoldierGround( NPCTrainSoldierGround.NPCTrainSoldierGround ):
	def __init__( self ):
		NPCTrainSoldierGround.NPCTrainSoldierGround.__init__( self )
		self.requireSoldierAmount = 0 #占领移除的士兵数量
		self.requireSoldierLevel = 0	#占领士兵等级要求
		self.requireOccupyType = 0 # 占领练兵场类型
		self.requireMoney = 0	# 消耗的金钱

	def initData( self, configData ):
		NPCTrainSoldierGround.NPCTrainSoldierGround.initData( self, configData )
		if configData["Param5"]:
			requireList = [int(i) for i in configData["Param5"].split("|")]
			self.requireOccupyType = requireList[0]
			self.requireSoldierAmount = requireList[1]
			self.requireSoldierLevel = requireList[2]
			self.requireMoney = requireList[3]

	def getRequireOccupyType( self ):
		return self.requireOccupyType

	def getRequireSoldierAmount( self ):
		return self.requireSoldierAmount

	def getRequireSoldierLevel( self ):
		return self.requireSoldierLevel

	def getRequireMoney( self ):
		return self.requireMoney
