# -*- coding: utf-8 -*-
#
import Math
import time

import KBEngine
import KBEDebug

import csdefine
import SpellBox
from ImpInterface.InteractiveStateInterface import InteractiveStateInterface


class SpellBoxAdvanced(
	SpellBox.SpellBox,
	InteractiveStateInterface,
	):
	"""
	CST-4161 程序功能需求（0级）——"法阵"交互功能研究
	"""
	def __init__(self):
		SpellBox.SpellBox.__init__(self)
		InteractiveStateInterface.__init__(self)
		
		self.interactiveStateTimerID = 0
		self.interactiveStateHoldEffectList = []
		
		self.interactiveTargets = set() 		#正在交互的目标ID列表
		self.interactiveTargetNum = 1 			#交互人数限制 0表示无限制
		self.followerIDs = set() 				#随从ID
		self.onInit()


	def onInit(self):
		"""
		"""
		self.getScript().onInit(self)

	def setMasterID(self, masterID):
		"""
		"""
		self.masterID = masterID

	def getMaster(self):
		"""
		"""
		master = KBEngine.entities.get(self.masterID, None)
		return master

	def addFollower(self, fid):
		"""
		"""
		self.followerIDs.add(fid)
		
	def removeFollower(self, fid):
		"""
		"""
		if fid in self.followerIDs:
			self.followerIDs.remove(fid)

	def getFollowers(self):
		"""
		"""
		followers = []
		for fID in self.followerIDs:
			f = KBEngine.entities.get(fID, None)
			if not f:
				KBEDebug.ERROR_MSG("followerID = %d is not exist!")
				continue
			followers.append(f)
		return followers
		
	def getFollowerByID(self, fid):
		"""
		"""
		if fid not in self.followerIDs:
			return None
			
		return KBEngine.entities.get(fid, None)
		
	def setComplete(self, value):
		"""
		设置完成度达标阈值百分比（默认为100）
		"""
		if value <= 0:
			return
		
		self.complete = value
		
	def getComplete(self):
		"""
		"""
		return self.complete
	
	def addInteractiveTarget(self, targetID):
		"""
		"""
		self.interactiveTargets.add(targetID)
		self.entityEventSubscribe(csdefine.ENTITY_EVENT_ENTITY_STATE_CHANGE, targetID, "entityEventCB_EntityStateChange")
		#开启状态 >> 处理状态
		if self.isInteractiveState(csdefine.INTERACTIVE_STATE_OPEN):
			self.changeInteractiveState(csdefine.INTERACTIVE_STATE_INPROGRESS)

	def interruptAllInteractive(self):
		"""
		中断所有的交互
		"""
		for targetID in list(self.interactiveTargets):
			self.getScript().interruptInteractive(self, targetID)

	def removeInteractiveTarget(self, targetID):
		"""
		"""
		if targetID not in self.interactiveTargets:
			return
			
		self.interactiveTargets.remove(targetID)
		self.entityEventUnsubscribe(csdefine.ENTITY_EVENT_ENTITY_STATE_CHANGE, targetID)
		if not len(self.interactiveTargets):
			self.interruptProgress()

	def updateProgress(self):
		"""
		更新进度
		"""
		self.getScript().updateProgress(self)


	def completeProgress(self):
		"""
		与目标交互完成
		"""
		# >> 解决状态
		self.changeInteractiveState(csdefine.INTERACTIVE_STATE_RESOLVED)


	def interruptProgress(self):
		"""
		中断交互
		"""
		if self.isInteractiveState(csdefine.INTERACTIVE_STATE_ACCEPT) or self.isInteractiveState(csdefine.INTERACTIVE_STATE_CLOSED):
			return
			
		self.getScript().interruptProgress(self)
		
	def reTrigger(self):
		"""
		"""
		#看看当前有哪些能进行交互
		entities = self.entitiesInRangeExt(self.maxGossipDis, "Role")
		for e in entities:
			self.CELL_reqStartInteractive(e.id)
		
	def tick(self):
		"""
		心跳(需要配置心跳时间)
		"""
		self.getScript().tick(self)
		
	def stateTick(self):
		"""
		状态内定时器
		"""
		self.getScript().stateTick(self)
		
	def trigger(self, eventType, args = [], triggerEntity = None):
		"""
		触发事件
		"""
		self.getScript().trigger(self, eventType, args, triggerEntity)
		
	def destroySelfForTimeOut(self):
		"""
		"""	
		self.getScript().destroyForTimeOut(self)


#-------------------------------客户端的请求-----------------------------------------

	def CELL_reqStartInteractive(self, srcEntity):
		"""
		exposed method
		请求开始交互的接口
		"""

		self.getScript().startInteractive(self, srcEntity)
		
	def CELL_reqInterruptInteractive(self, srcEntity):
		"""
		exposed method
		请求中断交互的接口
		"""

		if self.isInteractiveState(csdefine.INTERACTIVE_STATE_ACCEPT) or self.isInteractiveState(csdefine.INTERACTIVE_STATE_CLOSED):
			return
		
		self.getScript().interruptInteractive(self, srcEntity)

	def entityEventCB_EntityStateChange(self, eventType, notifierID, args):
		"""
		状态改变事件回调
		"""
		notifier = KBEngine.entities.get(notifierID, None)
		if notifier:
			#如果交互者死亡 中断其交互
			newState = args["newState"]
			if newState == csdefine.ENTITY_STATE_DEAD:
				self.getScript().interruptInteractive(self, notifierID)