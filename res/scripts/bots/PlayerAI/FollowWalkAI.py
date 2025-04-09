# -*- coding: utf-8 -*-
import Math
import KBEngine
import KBEDebug

import KST_Config
from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.AI_Run import CRunRandom
from PlayerAI.State.CStateInterface import eAIState

class FollowWalkAI( AIBase ):
	"""
	测试跟随移动
	"""
	def __init__(self):
		AIBase.__init__(self)
		self.actionStatus[eAIState.Run] = CRunRandom(self)
		self.callbackID = 0
		self.callbackIDForSync = 0
		self.controlEntity = []
		self.lastPos = {}
		self.lastDir = {}
		
	def reset(self):
		if self.callbackID:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
		if self.callbackIDForSync:
			KBEngine.cancelCallback(self.callbackIDForSync)
			self.callbackIDForSync = 0
		self.controlEntity.clear()
		
	def onEnterSpace( self ):
		"""
		"""
		AIBase.onEnterSpace(self)
		self.owner.eventObj.registerEvent("Event_OnControlMonster", self)
		
	def onLeaveSpace( self ):
		"""
		"""
		self.reset()
		AIBase.onLeaveSpace(self)
		self.owner.eventObj.unregisterEvent("Event_OnControlMonster", self)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		spaceScriptID = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if KST_Config.follow_enter_default_map:
			if spaceScriptID != KST_Config.default_map[0]:
				self.enterDefaultSpace()
				return
			
			self.owner.GMCommand(self.owner, "watch")
			self.owner.GMCommand(self.owner, "testMonsterFight", "20 20")
			self.owner.GMCommand(self.owner, "follow", "10")
		else:
			if spaceScriptID != KST_Config.follow_map:
				self.owner.GMCommand(self.owner, "follow")
				return
			
			self.owner.GMCommand(self.owner, "follow", "20 0")
		
		#自己控制的entity由自己手动进行位置同步
		if not KST_Config.follow_auto_sync_server:
			self.callbackIDForSync = KBEngine.callback(KST_Config.follow_sync_frequency, self.onCallBackForSync)
		self.callbackID = KBEngine.callback(5, self.onCallBack)
		
	def think(self):
		"""
		"""
		self.changeAIState(eAIState.Run)
		
	def getLoop(self):
		return True
	
	def getWalkRadius(self):
		return KST_Config.follow_radius
		
	def onCallBack(self):
		self.callbackID = 0
		self.think()
		
	def onControlMonster(self, entityID):
		"""
		"""
		self.controlEntity.append(entityID)
		
	def onCallBackForSync(self):
		"""
		"""
		self.callbackIDForSync = 0
		self.callbackIDForSync = KBEngine.callback(KST_Config.follow_sync_frequency, self.onCallBackForSync)
		
		positions = []
		directions = []
		#同步位置、朝向
		for id in self.controlEntity:
			entity = self.owner.clientapp.entities.get(id, None)
			if not entity: continue
			
			pos = Math.Vector3(entity.position.x, entity.position.y, entity.position.z)
			self.lastPos.setdefault(id, pos)
			if (entity.position - self.lastPos[id]).length > 0.1:
				positions.append({"id" : id, "pos" : pos})
				self.lastPos[id] = pos
			
			dire = Math.Vector3(entity.direction.x, entity.direction.y, entity.direction.z)
			self.lastDir.setdefault(id, dire)
			if (entity.direction - self.lastDir[id]).length > 0.1:
				directions.append({"id" : id, "pos" : dire})
				self.lastDir[id] = dire
		
		if len(positions) or len(directions):
			self.owner.cell.syncEntityPos(positions, directions)
		
AIBase.setClass("FollowWalkAI", FollowWalkAI)