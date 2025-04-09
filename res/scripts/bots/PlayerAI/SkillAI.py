# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug

import csdefine
import KST_Config
import Extra.Extend as Extend
from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.AI_Run import CRunForSkillAI
from PlayerAI.State.AI_System import CNull
from PlayerAI.State.AI_Dead import CDeadToRevive
from PlayerAI.State.AI_Attack import CRoleAttack_1
from PlayerAI.State.CStateInterface import eAIState

class SkillAI( AIBase ):
	"""
	"""
	def __init__(self):
		AIBase.__init__(self)
		
		self.moveToDefaultPos = False
		self.actionStatus[eAIState.NULL] = CNull(self)
		self.actionStatus[eAIState.Run] = CRunForSkillAI(self)
		self.actionStatus[eAIState.Attack] = CRoleAttack_1(self)
		self.actionStatus[eAIState.Dead] = CDeadToRevive(self)
		
	def onEnterSpace(self):
		AIBase.onEnterSpace(self)
		self.owner.eventObj.registerEvent("Event_OnMonsterDead", self)
		
	def onLeaveSpace(self):
		AIBase.onLeaveSpace(self)
		self.owner.eventObj.unregisterEvent("Event_OnMonsterDead", self)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		if not self.enterDefaultMap:
			self.enterDefaultSpace()
			return
		
		self.think()
		
	def think(self):
		"""
		"""
		if not self.moveToDefaultPos:
			self.changeAIState(eAIState.Run)
			self.moveToDefaultPos = True
			return
		
		self.cloneMonster()
		#self.changeAIState(eAIState.Attack)
	
	def startAction(self, key, param):
		"""
		"""
		if key == "Attack":
			KBEngine.callback(3, self.startAttack)
	
	def startAttack(self):
		"""
		"""
		self.changeAIState(eAIState.Attack)
		
	def cloneMonster(self):
		"""
		"""
		#克隆木桩怪
		pos = self.owner.position
		self.owner.GMCommand(self.owner, "clone", "29900101")
		
	def onMonsterDead(self, scriptID, id):
		"""
		"""
		self.owner.GMCommand(self.owner, "clone", scriptID)
		
	def findTarget(self):
		"""
		获取范围内离自己最近的一个怪物
		"""
		result = None
		minDist = -1

		for e in self.owner.entitiesInRange( 5, cnd = lambda entity : True if entity.entityFlag==csdefine.ENTITY_FLAG_MONSTER and Extend.checkCanAttack( entity ) else False ):
			dstToEntity = self.owner.position.distTo( e.position )
			if minDist == -1:
				minDist = dstToEntity
				result = e
				if minDist == 0:
					break

			if dstToEntity < minDist:
				dstToEntity = minDist
				result = e
	
		return result
	

AIBase.setClass("SkillAI", SkillAI)