# -*- coding: utf-8 -*-
import random
import Math

import KBEngine
import KBEDebug

import KST_Config
import Extra.Extend as Extend
from PlayerAI.State.CStateInterface import CStateBase
from Extra.SpaceConfigMgr import g_spaceConfigMgr

class CRunBase( CStateBase ):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.nodeIndex = -1
		
	def getNode(self):
		currentSpace = self.ai.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		spawnCfg = g_spaceConfigMgr.getSpaceSpawnCfgByScriptID(currentSpace)
		if spawnCfg is None:
			KBEDebug.ERROR_MSG("not found space[%s] spawn" %(currentSpace))
			return Extend.calRandomWalkPos(self.ai.owner.position, 10)
		
		if len(spawnCfg) <= 0:
			KBEDebug.ERROR_MSG("spawnCfg[%d] is None" %(currentSpace))
			return Extend.calRandomWalkPos(self.ai.owner.position, 10)
		
		#如果刚开始，那么随机选一个
		if self.nodeIndex < 0:
			self.nodeIndex = random.randint(0, len(spawnCfg))
		
		if self.nodeIndex >= len(spawnCfg):
			self.nodeIndex = 0
		
		cfg = spawnCfg.get(self.nodeIndex, None)
		if cfg is None:
			KBEDebug.ERROR_MSG("space[%s] spawn is None" %(currentSpace))
			return Extend.calRandomWalkPos(self.ai.owner.position, 100)
		
		#从刷新点配置中获取坐标信息
		position = cfg.get("position", None)
		if position is None:
			KBEDebug.ERROR_MSG("space[%s] position is None" %(currentSpace))
			return Extend.calRandomWalkPos(self.ai.owner.position, 100)
		
		self.nodeIndex += 1
		pos = Math.Vector3(position[0], position[1], position[2])
		if (self.ai.owner.position - pos).length >= 3:
			return pos
		return Extend.calRandomWalkPos(self.ai.owner.position, 100)

class CRun( CRunBase ):
	"""
	"""
	def __init__(self, ai):
		CRunBase.__init__(self, ai)
		self.controllerID = 0
		
	def enter(self):
		self.onMove()
		
	def leave(self):
		if self.controllerID != 0:
			self.ai.owner.cancelController(self.controllerID)
			self.controllerID = 0
		
	def reEnter(self):
		self.onMove()
	
	def onMove(self):
		self.controllerID = self.ai.owner.moveToPos(self.getNode())
		
	def onMoveOver(self, controllerID, userData):
		self.controllerID = 0
		self.findTarget()
		
	def onMoveFailure(self, controllerID, userData):
		self.controllerID = 0
		self.findTarget()

	def findTarget(self):
		"""
		"""
		#开始找目标
		if self.ai.findTarget():
			self.ai.think()
			return
		
		self.onMove()

class CRunRandom( CRunBase ):
	"""
	"""
	def __init__(self, ai):
		CRunBase.__init__(self, ai)
		
		self.controllerID = 0
		self.callbackID = 0
		self.randomWalkRadius = self.ai.getWalkRadius()
		
	def enter(self):
		self.spawnPosition = Math.Vector3(self.ai.owner.position)
		self.move()
		
	def leave(self):
		if self.controllerID != 0:
			self.ai.owner.cancelController(self.controllerID)
			self.controllerID = 0
		
	def onMoveOver(self, controllerID, userData):
		self.controllerID = 0
		if self.ai.getLoop():
			if self.callbackID == 0:
				self.callbackID = KBEngine.callback(0.5, self.onCallBack)
			#self.move()
		
	def onMoveFailure(self, controllerID, userData):
		self.controllerID = 0
		if self.callbackID == 0:
			self.callbackID = KBEngine.callback(0.5, self.onCallBack)
		#self.move()

	def move(self):
		if self.controllerID != 0:
			return
			
		self.controllerID = self.ai.owner.moveToPos(self.getNode())
		
	def getNode(self):
		"""
		"""
		return Extend.calRandomWalkPos(self.spawnPosition, self.randomWalkRadius)
		
	def onCallBack(self):
		self.callbackID = 0
		self.move()
		

class CRunRandomAndUseSkill( CRunBase ):
	"""
	"""
	def __init__(self, ai):
		CRunBase.__init__(self, ai)
		
		self.controllerID = 0
		self.castTimerID = 0
		
	def enter(self):
		self.move()
		self.useSkill()
		
	def leave(self):
		if self.controllerID != 0:
			self.ai.owner.cancelController(self.controllerID)
			self.controllerID = 0
			
		if self.castTimerID!= 0:
			KBEngine.cancelCallback(self.castTimerID)
			self.castTimerID = 0
		
	def onMoveOver(self, controllerID, userData):
		self.controllerID = 0
		if KST_Config.walk_loop:
			self.move()
		
	def onMoveFailure(self, controllerID, userData):
		self.controllerID = 0
		self.move()

	def move(self):
		if self.controllerID != 0:
			return
			
		self.controllerID = self.ai.owner.moveToPos(self.getNode())
		
	def useSkill(self):
		if self.castTimerID:
			return
		
		for skillID in self.ai.owner.skillsList:
			self.ai.useSkill( skillID, self.ai.owner.id )
		self.castTimerID = KBEngine.callback(3, self.onUseSkill)
		
	def onUseSkill(self):
		self.castTimerID = 0
		self.useSkill()
	
class CRunForFindTarget( CRunBase ):
	"""
	"""
	def __init__(self, ai):
		CRunBase.__init__(self, ai)	

		self.controllerID = 0
		self.findTargetTimerID = 0

	def enter(self):
		self.move()
		
	def leave(self):
		if self.controllerID != 0:
			self.ai.owner.cancelController(self.controllerID)
			
		if self.findTargetTimerID != 0:
			KBEngine.cancelCallback(self.findTargetTimerID)
			self.findTargetTimerID = 0
		
	def onMoveOver(self, controllerID, userData):
		self.controllerID = 0
		self.move()
		
	def onMoveFailure(self, controllerID, userData):
		self.controllerID = 0
		self.move()
	
	def move(self):
		center = self.ai.spawnPosition
		radius = self.ai.walkRadius
		self.controllerID = self.ai.owner.moveToPos(Extend.calRandomWalkPos(center, radius))
		
		if self.findTargetTimerID == 0:
			self.findTargetTimerID = KBEngine.callback(3, self.findTarget)
		
	def findTarget(self):
		"""
		"""
		self.findTargetTimerID = 0

		#开始找目标
		if self.ai.findTarget():
			self.ai.think()
			return
		
		self.findTargetTimerID = KBEngine.callback(3, self.findTarget)

class CRunForSkillAI( CRunBase ):
	"""
	"""
	ROWNUM = 0
	LINENUM = 0
	
	def __init__(self, ai):
		CRunBase.__init__(self, ai)
		self.controllerID = 0

	def enter(self):
		self.move()
		
	def leave(self):
		if self.controllerID != 0:
			self.ai.owner.cancelController(self.controllerID)
			self.controllerID = 0
		
	def onMoveOver(self, controllerID, userData):
		self.controllerID = 0
		self.ai.think()
		
	def onMoveFailure(self, controllerID, userData):
		self.controllerID = 0
		self.ai.think()
	
	def move(self):
		self.controllerID = self.ai.owner.moveToPos(self.getNode())
	
	def getNode(self):
		"""
		"""
		pos = self.ai.owner.position
		x = KST_Config.skill_stand_distance * CRunForSkillAI.ROWNUM
		z = KST_Config.skill_stand_distance * CRunForSkillAI.LINENUM
		
		CRunForSkillAI.ROWNUM += 1
		if CRunForSkillAI.ROWNUM >= 5:
			CRunForSkillAI.ROWNUM = 0
			CRunForSkillAI.LINENUM += 1
		
		return Math.Vector3(pos.x + x, pos.y, pos.z + z)
	