# -*- coding: utf-8 -*-
import random, time

import KBEngine
import KBEDebug

import KST
import csdefine
import Extra.Extend as Extend

import KST_Config
from PlayerAI.State.AI_Run import CRun
from PlayerAI.State.AI_Attack import CAttack
from PlayerAI.State.AI_Dead import CDeadToRevive
from PlayerAI.State.CStateInterface import eAIState
from PlayerAI.State.AI_System import CNull
from PlayerAI.Base.AIBase import AIBase
import PlayerAI.State.AI_Space as AI_Space 

class SpaceCampAI( AIBase ):
	"""
	"""
	def __init__(self):
		AIBase.__init__(self)
		
		self.actionStatus[eAIState.NULL] = CNull(self)
		self.actionStatus[eAIState.Run] = CRun(self)
		self.actionStatus[eAIState.Dead] = CDeadToRevive(self)
		self.actionStatus[eAIState.Attack] = CAttack(self)
		
		self.space_test = None
		self.attackTarget = None
		self.hasSetLevel = False
		self.callbackID = 0
		
		spaceinfos = []
		for k,v in KST_Config.spaceCamp_maps.items():
			if v[1]: spaceinfos.append((k, v[0]))
		
		if len(spaceinfos) <= 0:
			KBEDebug.ERROR_MSG("space error")
			return
		
		self.space_test = random.choice(spaceinfos)
		
	def onEnterSpace(self):
		"""
		"""
		self.owner.eventObj.registerEvent("Event_OnHPChanged", self)
		self.owner.eventObj.registerEvent("Event_OnMPChanged", self)

	def onLeaveSpace(self):
		"""
		"""
		self.attackTarget = None
		self.changeAIState(eAIState.NULL)
		self.owner.eventObj.unregisterEvent("Event_OnHPChanged", self)
		self.owner.eventObj.unregisterEvent("Event_OnMPChanged", self)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		if not self.hasSetLevel:
			self.hasSetLevel = True
			self.owner.GMCommand(self.owner, "setLevel", "35")
		
		self.think()
		
	def think(self):
		"""
		"""
		if self.space_test is None:
			return
		
		currentSpace = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if currentSpace == self.space_test[0]:	#进入了选定的阵营战场地图
			if self.attackTarget:
				self.changeAIState(eAIState.Attack)
				return
				
			self.changeAIState(eAIState.Run)
			return

		t = KST.tempData.get("NEXT_CAMP_TIME", 0)
		if t + 30 <= time.time():
			if not hasattr(AI_Space, self.space_test[1]):
				KBEDebug.ERROR_MSG("not found spaceAI[%s]" %(self.space_test[1]))
				return
				
			spaceAI = getattr(AI_Space, self.space_test[1])
			self.actionStatus[eAIState.Space] = spaceAI(self)
			self.changeAIState(eAIState.Space)
			return
		
		#第一个进入到这里来的，定时先关闭下space。
		if KST.tempData.get("camp_space_need_close", False):
			KST.tempData["camp_space_need_close"] = False
			KBEngine.callback(int(t - time.time()), self.onCloseSpace)
		
		#进入移动状态
		self.attackTarget = None
		self.changeAIState(eAIState.Run)
		KBEngine.cancelCallback(self.callbackID)
		self.callbackID = KBEngine.callback(int(t - time.time()) + 60, self.onCallBack)
		
	def findTarget(self):
		"""
		获取范围内离自己最近的一个怪物
		"""	
		result = None
		minDist = -1

		for e in self.owner.entitiesInRange( 20, cnd = lambda entity : True if entity.entityFlag in [csdefine.ENTITY_FLAG_MONSTER, csdefine.ENTITY_FLAG_ROLE] and Extend.checkCanAttack( entity, self.owner ) else False ):
			dstToEntity = self.owner.position.distTo( e.position )
			if minDist == -1:
				minDist = dstToEntity
				result = e
				if minDist == 0:
					break
			
			if dstToEntity < minDist:
				dstToEntity = minDist
				result = e
		
		self.attackTarget = result
		return result
		
	def onCallBack(self):
		self.callbackID = 0
		self.think()
		
	def onCloseSpace(self):
		"""
		"""
		self.owner.GMCommand(self.owner, "activity_control", "晶石狩猎场开始 0")
		self.owner.GMCommand(self.owner, "activity_control", "灵脉战场 0") 
		self.owner.GMCommand(self.owner, "activity_control", "英雄王座 0") 
		
		
		
AIBase.setClass("SpaceCampAI", SpaceCampAI)