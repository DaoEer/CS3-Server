# -*- coding: utf-8 -*-


import KBEngine
import KBEDebug
#script
import MonsterOptimize
import time
import csarithmetic
import csdefine
import Const
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface

class MonsterCommander( MonsterOptimize.MonsterOptimize ):
	"""
	指挥官类型小怪
	"""
	def __init__( self ):
		MonsterOptimize.MonsterOptimize.__init__( self )
		self.memberDict = {}
		self.soldierScriptID = ""
		self.tempTargetList = []

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_COMMANDER)
		
	def createSoldiers(self, scriptID, amount):
		"""
		"""
		self.soldierScriptID = scriptID
		for index in range(int(amount)):
			self.createEntityByScriptID(scriptID, self.position, self.direction, {"cmderID":self.id,"memberIndex":index+1, "spawnPos":self.position, "belongSide":self.getBelongSide()})
	def onSoldierCreate(self, soldierID):
		"""
		"""
		self.addMember(soldierID)

	def addMember(self, memberID):
		"""
		"""
		if memberID not in self.memberDict:
			memberEntity = KBEngine.entities.get(memberID)
			if memberEntity:
				data = {memberID:memberEntity}
				self.memberDict.update(data)

	def removeMember(self, memberID):
		"""
		"""
		if memberID in self.memberDict:
			self.memberDict.pop(memberID)
			triggerEntity = KBEngine.entities.get(memberID)
			self.triggerEvent(csdefine.ENTITY_EVENT_MEMBER_SOLDIER_CHANGE,[], triggerEntity)

	def getAllMember( self ):
		"""
		获得所有士兵
		"""
		return self.memberDict

	def destorySoldiers( self ):
		"""
		销毁所有士兵
		"""
		for member in self.memberDict.values():
			if member:
				member.destroySelf()
		self.memberDict.clear()

	def sendCmdFollow(self, startDist, spacing, columnMax, moveSpeed):
		"""
		"""
		for member in self.memberDict.values():
			if member:
				member.doCmdFollow(self.position, self.direction, startDist, spacing, columnMax, moveSpeed)
			
	def sendCmdRectFormation(self, startDist, spacing, columnMax, moveSpeed):
		"""
		"""
		for member in self.memberDict.values():
			if member:
				member.doCmdRectFormation(self.position, self.direction, startDist, spacing, columnMax, moveSpeed)

	def sendCmdCircleFormation(self, startDist, spacing, columnMax, moveSpeed):
		"""
		"""
		for member in self.memberDict.values():
			if member:
				member.doCmdCircleFormation(self.position, self.direction, startDist, spacing, columnMax, moveSpeed)

	def sendCmdAttack(self):
		"""
		"""
		for member in self.memberDict.values():
			if member:
				member.doCmdAttack()

	def sendCmdUseSkill(self):
		"""
		"""
		for member in self.memberDict.values():
			if member:
				member.doCmdUseSkill()

	#--------------------------test----------------------
	def follow(self):
		"""
		"""
		for member in self.memberDict.values():
			if member:
				member.moveToFollowTargetPos(3.0, 2.0, 5)

	def rect(self):
		for member in self.memberDict.values():
			if member:
				member.moveToRectFormationTargetPos(3.0, 2.0, 5)


	def circle(self):
		for member in self.memberDict.values():
			if member:
				member.moveToCircleFormationTargetPos(3.0, 2.0, 10)



	#-------------------------------teamEnemyList--------------
	
