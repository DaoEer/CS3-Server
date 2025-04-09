# -*- coding: utf-8 -*-
import random, Math, time

import KBEngine
from KBEDebug import *

import csdefine
import Extra.Extend as Extend
from PlayerAI.State.CStateInterface import CStateBase

TONGNUM = 0
class CTongAI(CStateBase):
	"""
	"""
	def __init__(self, ai):
		CStateBase.__init__(self, ai)
		self.callbackID = 0
		
	def reset(self):
		"""
		"""
		if self.callbackID:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
	
	def enter(self):
		"""
		"""
		#注册事件
		self.ai.owner.eventObj.registerEvent("Event_CTongAISys_onReceTongInfos", self)
		self.ai.owner.eventObj.registerEvent("Event_CTongAISys_onTongJoin", self)
		self.ai.owner.eventObj.registerEvent("Event_CTongAISys_onReqJoinTong", self)
		self.ai.owner.eventObj.registerEvent("Event_CTongAISys_onLeaveTong", self)
		
		#各个机器人随机一个时间开始进入AI，不然一开始都涌进去，可能还没有一个帮会创建
		callbackTime = random.randint(1, 10)
		self.callbackID = KBEngine.callback(callbackTime, self.onEnter)
		
	def leave(self):
		"""
		"""
		self.reset()
		
		#反注册
		self.ai.owner.eventObj.unregisterEvent("Event_CTongAISys_onReceTongInfos", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CTongAISys_onTongJoin", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CTongAISys_onReqJoinTong", self)
		self.ai.owner.eventObj.unregisterEvent("Event_CTongAISys_onLeaveTong", self)
		
	def onEvent(self, name, *argv):
		"""
		"""
		if name == "Event_CTongAISys_onTongJoin":
			self.inviteJoinTong()
		elif name == "Event_CTongAISys_onReqJoinTong":
			#有人申请加入帮会，直接同意好了
			self.ai.owner.base.replyJoinTong(str(*argv), True)
		elif name == "Event_CTongAISys_onReceTongInfos":
			if len(self.ai.owner.tongs):
				self.joinTong()
			else:
				self.createTong()
		elif name == "Event_CTongAISys_onLeaveTong":	#如果帮会解散了，那么重新获取帮会列表进行加入
			self.onEnter()
		
	def onEnter(self):
		"""
		"""
		self.callbackID = 0
		self.ai.owner.base.RequireTongInfo() #请求帮会列表
		
	def onJoinTong(self):
		"""
		"""
		self.callbackID = 0
		if self.ai.owner.tongDBID: return
		self.onEnter()
	
	def joinTong(self):
		"""
		"""
		if self.ai.owner.tongDBID:
			self.ai.think()
			return
		
		#随机出5个，申请加入
		tongDBIDList = list(self.ai.owner.tongs.keys())
		amount = 5 if len(tongDBIDList) >= 5 else len(tongDBIDList)
		temp = random.sample(tongDBIDList, amount)
		for id in temp: self.ai.owner.base.tongReqJoin(str(id))
		
		#加入延时器，如果一定时间后，还没加入帮会，则再申请加一次
		self.callbackID = KBEngine.callback(5, self.onJoinTong)
		
	def inviteJoinTong(self):
		"""
		"""
		if not self.ai.owner.tongDBID:
			self.onEnter()
			return
		
		#从玩家中随机挑出6个发送邀请
		entities = self.ai.owner.entitiesInRange( 50, cnd = lambda entity : True if entity.entityFlag==csdefine.ENTITY_FLAG_ROLE and not self.ai.owner.isInSelfTong(entity.id) else False )
		entities = random.sample(entities, 6 if len(entities) >= 6 else len(entities))
		for entity in entities: 
			self.ai.owner.cell.tongInviteJoin(entity.id)
			self.ai.owner.outputMsg("tongInviteJoin {}".format(entity.id))
		
		self.callbackID = KBEngine.callback(5, self.onCallBack)
		
	def createTong(self):
		"""
		"""
		#如果已经加入了帮会
		if self.ai.owner.tongDBID:
			self.ai.think()
			return
		
		global TONGNUM	#这里加global，是因为后面对它进行了重新复制，如果没有这步操作，这里可以不加global
		name = str(int(time.time()) * 100 + TONGNUM)
		TONGNUM += 1
		self.ai.owner.cell.tongCreate(name)	#创建帮会
		self.ai.owner.outputMsg("tongCreate")
		
	def onCallBack(self):
		"""
		"""
		self.callbackID = 0
		self.ai.think()
