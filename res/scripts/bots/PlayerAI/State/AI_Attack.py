# -*- coding: utf-8 -*-
import random

import KBEngine
import KBEDebug

import csdefine
import KST_Config
import Extra.Extend as Extend
import Extra.Vector as Vector
from PlayerAI.State.CStateInterface import CStateBase

ATTACK_TIME = 2 * 60
class CAttack(CStateBase):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.controllerID = 0
		self.callbackID = 0
		self.castTimerID = 0
		self.castTime = 0
		
	def enter(self):
		self.reset()
		self.onEnter()
		
	def leave(self):
		self.reset()
		self.ai.attackTarget = None
	
	def reset(self):
		if self.ai.attackTarget:
			self.ai.attackTarget.eventObj.unregisterEvent("Event_OnMonsterLeaveWorld", self)
			
		if self.controllerID > 0:
			self.ai.owner.cancelController(self.controllerID)
			self.controllerID = 0
			
		if self.castTimerID != 0:
			KBEngine.cancelCallback( self.castTimerID )
			self.castTimerID = 0
			
		self.castTime = 0
		
	def reEnter(self):
		self.reset()
		self.onEnter()
		
	def onEnter(self):
		if self.ai.attackTarget is None:
			self.ai.think()
			return
		
		self.ai.attackTarget.eventObj.registerEvent("Event_OnMonsterLeaveWorld", self)
		self.moveToTargetPosition()
		
	def moveToTargetPosition(self):
		"""
		"""
		if self.ai.attackTarget is None:
			self.ai.think()
			return
			
		if (self.ai.owner.position - self.ai.attackTarget.position).length < 5 and self.castTime < 10:
			self.castSpell()
			return
		
		pos = self.ai.attackTarget.position
		if self.castTime >= 10:
			self.castTime = 0
			pos = Extend.calRandomWalkPos(self.ai.attackTarget.position, 3)
		
		if self.controllerID <= 0:
				self.controllerID = self.ai.owner.moveToPos(pos)
	
	def castSpell(self):
		"""
		释放技能
		"""
		if self.ai.attackTarget is None:
			self.ai.think()
			return
		
		if self.ai.attackTarget.state != csdefine.ENTITY_STATE_DEAD:
			if self.castTimerID > 0:
				return
			
			#KBEDebug.ERROR_MSG("castSpell: %d[%s], %d" %(self.ai.attackTarget.id, self.ai.attackTarget.position, self.ai.attackTarget.HP))
			self.ai.owner.turnToPos(self.ai.attackTarget.position)
			#如果设置了优先使用的技能
			if self.ai.owner.firstUseSkillID in self.ai.owner.skillsList:
				self.ai.useSkill(self.ai.owner.firstUseSkillID, self.ai.attackTarget.id)
			else:
				for skillID in self.ai.owner.skillsList:
					self.ai.useSkill( skillID, self.ai.attackTarget.id )
			
			self.castTime += 1
			self.castTimerID = KBEngine.callback(5, self.endSkill)
		else:
			#KBEDebug.ERROR_MSG("target is DEAD")
			self.ai.attackTarget.eventObj.unregisterEvent("Event_OnMonsterLeaveWorld", self)
			self.ai.attackTarget = None
			self.ai.think()
			return
			
	def endSkill(self):
		"""
		结束技能
		"""
		self.castTimerID = 0
		pos = self.ai.owner.position
		dir = self.ai.owner.direction
		#目前从其他客户端表现上来看，机器人在释放完技能后，位置会出现一些异常，这里对坐标进行一次同步，只通知其他客户端
		#UE4客户端在释放技能时，是没有这一步骤的
		self.ai.owner.GMCommand(self.ai.owner, "setSyncPosToOtherClient", "{} {} {} {} {} {}".format(pos.x, pos.y, pos.z, dir.x, dir.y, dir.z))
		self.moveToTargetPosition()
			
	def onMoveOver(self, controllerID, userData):
		self.controllerID = 0
		#KBEDebug.ERROR_MSG(self.ai.owner.position)
		self.moveToTargetPosition()
		
	def onMoveFailure(self, controllerID, userData):
		self.controllerID = 0
		#KBEDebug.ERROR_MSG(self.ai.owner.position)
		self.moveToTargetPosition()
		
	def onEvent(self, name, *argv):
		if name == "Event_OnMonsterLeaveWorld":
			self.OnMonsterLeaveWorld(*argv)
		
	def OnMonsterLeaveWorld(self, scriptID, entityID):
		if self.ai.attackTarget and self.ai.attackTarget.id == entityID:
			self.ai.attackTarget.eventObj.unregisterEvent("Event_OnMonsterLeaveWorld", self)
			self.ai.attackTarget = None
			self.ai.think()

ATTACK_OUT_TIME = 20
class CRoleAttack(CStateBase):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		
		self.controllerID = 0
		self.castTimerID= 0
		self.resetCallbackID = 0
		
	def enter(self):
		self.resetCallbackID = KBEngine.callback(ATTACK_OUT_TIME, self.onCallBack)
		self.moveToTargetPosition()
	
	def leave(self):
		if self.controllerID != 0:
			self.ai.owner.cancelController(self.controllerID)
			self.controllerID = 0
			
		if self.castTimerID != 0:
			KBEngine.cancelCallback(self.castTimerID)
			self.castTimerID = 0
			
		if self.resetCallbackID != 0:
			KBEngine.cancelCallback(self.resetCallbackID)
			self.resetCallbackID = 0
			
		self.ai.attackTarget = None
		
	def moveToTargetPosition(self):
		"""
		移动到指定目标
		"""
		if self.ai.attackTarget is None:
			self.ai.think()
			return
	
		if (self.ai.owner.position - self.ai.attackTarget.position).length > 5:
			self.controllerID = self.ai.owner.moveToPos(self.ai.attackTarget.position)
		else:
			self.castSpell()
			
	def castSpell(self):
		"""
		释放技能
		"""
		if self.ai.attackTarget.state != csdefine.ENTITY_STATE_DEAD:
			#KBEDebug.ERROR_MSG("player[%d:%s(%s)] castSpell: targe[%d:%s(%s)]" %(self.ai.owner.id, self.ai.owner.playerName, self.ai.owner.position, self.ai.attackTarget.id, self.ai.attackTarget.playerName, self.ai.attackTarget.position))
			self.ai.owner.turnToPos(self.ai.attackTarget.position)
			#skillID = random.choice(self.ai.owner.skillsList)
			#如果设置了优先使用的技能
			callbackTime = 5
			if self.ai.owner.firstUseSkillID in self.ai.owner.skillsList:
				self.ai.useSkill(self.ai.owner.firstUseSkillID, self.ai.attackTarget.id)
			else:
				if self.ai.owner.firstUseSkillID == 0:
					for skillID in self.ai.owner.skillsList:
						self.ai.useSkill( skillID, self.ai.attackTarget.id )
				else:
					skillsList = list(self.ai.owner.skillsList)
					for i in range(len(self.ai.owner.skillsList)):
						skillID = random.choice(skillsList)
						skillsList.remove(skillID)
						if self.ai.owner.checkUseSkill(skillID):
							self.ai.useSkill( skillID, self.ai.attackTarget.id )
							break
				
			self.castTimerID = KBEngine.callback(callbackTime, self.endSkill)
		else:
			self.ai.attackTarget = None
			self.ai.think()
			
	def endSkill(self):
		"""
		结束技能
		"""
		self.castTimerID = 0
		pos = self.ai.owner.position
		dir = self.ai.owner.direction
		#目前从其他客户端表现上来看，机器人在释放完技能后，位置会出现一些异常，这里对坐标进行一次同步，只通知其他客户端
		#UE4客户端在释放技能时，是没有这一步骤的
		self.ai.owner.GMCommand(self.ai.owner, "setSyncPosToOtherClient", "{} {} {} {} {} {}".format(pos.x, pos.y, pos.z, dir.x, dir.y, dir.z))
		self.moveToTargetPosition()
	
	def onMoveOver(self, controllerID, userData):
		self.controllerID = 0
		self.moveToTargetPosition()
		
	def onMoveFailure(self, controllerID, userData):
		self.controllerID = 0
		self.moveToTargetPosition()
		
	def onCallBack(self):
		self.ai.attackTarget = None
		self.ai.think()
		
class CRoleAttack_1(CStateBase):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		
		self.controllerID = 0
		self.castTimerID= 0
		self.target = None
		
		self.rolePos = None
		self.targetPos = None
		
	def enter(self):
		self.findTarget()
	
	def leave(self):
		if self.controllerID != 0:
			self.ai.owner.cancelController(self.controllerID)
			self.controllerID = 0
		
		if self.castTimerID != 0:
			KBEngine.cancelCallback(self.castTimerID)
			self.castTimerID = 0
			
		self.target = None
		
	def moveToTargetPosition(self):
		"""
		移动到指定目标
		"""
		if (self.ai.owner.position - self.target.position).length > 5:
			self.controllerID = self.ai.owner.moveToPos(self.target.position)
		else:
			self.castSpell()
			
	def castSpell(self):
		"""
		释放技能
		"""
		if self.target.state != csdefine.ENTITY_STATE_DEAD:
			#KBEDebug.ERROR_MSG("player[%d:%s(%s)] castSpell: targe[%d:%s(%s)]" %(self.ai.owner.id, self.ai.owner.playerName, self.ai.owner.position, self.ai.attackTarget.id, self.ai.attackTarget.playerName, self.ai.attackTarget.position))
			self.ai.owner.turnToPos(self.target.position)
			#skillID = random.choice(self.ai.owner.skillsList)
			#如果设置了优先使用的技能
			if self.ai.owner.firstUseSkillID in self.ai.owner.skillsList:
				self.ai.useSkill(self.ai.owner.firstUseSkillID, self.target.id)
			else:
				for skillID in self.ai.owner.skillsList:
					self.ai.useSkill( skillID, self.target.id )
			self.castTimerID = KBEngine.callback(5, self.endSkill)
		else:
			self.target = None
			self.ai.think()
			
	def endSkill(self):
		"""
		结束技能
		"""
		self.castTimerID = 0
		
		#重置坐标
		if self.rolePos:
			pos = Extend.KBEngine2UnrealPosition(self.rolePos)
			self.ai.owner.GMCommand(self.ai.owner, "setPos", "{} {} {}".format(pos[0], pos[1], pos[2]))
		if self.targetPos:
			pos = Extend.KBEngine2UnrealPosition(self.targetPos)
			self.ai.owner.GMCommand(self.target, "setPos", "{} {} {}".format(pos[0], pos[1], pos[2]))
		
		KBEngine.callback(5, self.moveToTargetPosition)
		
	def findTarget(self):
		"""
		"""
		if self.target is None:
			target = self.ai.findTarget()
			if target:
				self.targetPos = target.position
				self.rolePos = self.ai.owner.position
				self.target = target
				self.moveToTargetPosition()
				return
				
			KBEngine.callback(5, self.findTarget)
	
	def onMoveOver(self, controllerID, userData):
		self.controllerID = 0
		self.moveToTargetPosition()
		
	def onMoveFailure(self, controllerID, userData):
		self.controllerID = 0
		self.moveToTargetPosition()