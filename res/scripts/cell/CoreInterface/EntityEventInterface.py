# -*- coding: utf-8 -*-


import KBEngine
import KBEDebug


class EntityEventInterface():
	#entity事件接口
	#订阅感兴趣的entity的eventType类型的事件消息 自身也能被别人订阅 当有消息发生的时候通知给订阅者

	def __init__(self):
		self.entityEventSubscriptions = {}			#订阅内容 {eventType:{subscriberID:{callbackStr1, callbackStr2}}
		self.entityEventNotices	   = {}			#通知内容 {eventType:{targetID:{callbackStr1, callbackStr2}}

#-----------------------------subscriber----------------------------------------------

	def entityEventSubscribe(self, eventType, targetID, callbackStr):
		"""
		订阅感兴趣的entity事件
		"""
		target = KBEngine.entities.get(targetID, None)
		if not target:
			return
		if not eventType in self.entityEventSubscriptions:
			self.entityEventSubscriptions[eventType] = {}
		if targetID not in self.entityEventSubscriptions.keys():
			self.entityEventSubscriptions[eventType] = {targetID:{callbackStr}}
		else:
			self.entityEventSubscriptions[eventType][targetID].add(callbackStr)

		target.entityEventAttach(self.id, eventType, callbackStr)

	def entityEventUnsubscribe(self, eventType, targetID):
		"""
		取消订阅
		"""
		if  eventType in self.entityEventSubscriptions and targetID in self.entityEventSubscriptions:
			self.entityEventSubscriptions[eventType].pop(targetID)
			if not len(self.entityEventSubscriptions[eventType]):
				self.entityEventSubscriptions.pop(eventType)

		target = KBEngine.entities.get(targetID, None)
		if not target:
			return

		target.entityEventDetach(self.id, eventType)

	def entityEventUnsubscribeAllEvents(self):
		"""
		取消所有订阅
		"""
		while len(self.entityEventSubscriptions):
			eventType, data = self.entityEventSubscriptions.popitem()
			targetIDList = list(data.keys())
			while len(targetIDList):
				targetID = targetIDList.pop()
				target = KBEngine.entities.get(targetID, None)
				if  target:
					target.entityEventDetach(self.id, eventType)

	def entityEventRecieveNotify(self, eventType, notifierID, callbackStr, args=[]):
		"""
		override method
		接收订阅事件消息
		"""
		if not eventType in self.entityEventSubscriptions or not notifierID in self.entityEventSubscriptions[eventType].keys():
			return
		if not hasattr(self, callbackStr):
			return
		callback = getattr(self, callbackStr)
		callback(eventType, notifierID, args)

			

#-----------------------------notifier------------------------------------------------

	def entityEventAttach(self, subscriberID, eventType, callbackStr):
		"""
		关联订阅者
		"""
		if not eventType in self.entityEventNotices:
			self.entityEventNotices[eventType] = {}		
		if not subscriberID in self.entityEventNotices[eventType]:
			self.entityEventNotices[eventType] = {subscriberID:{callbackStr}}
		self.entityEventNotices[eventType][subscriberID].add(callbackStr)

	def entityEventDetach(self, subscriberID, eventType):
		"""
		移除订阅者
		"""
		if not eventType  in self.entityEventNotices:
			return
		if subscriberID in self.entityEventNotices[eventType]:
			self.entityEventNotices[eventType].pop(subscriberID)
			if not len(self.entityEventNotices[eventType]):
				self.entityEventNotices.pop(eventType)

	def entityEventNotify(self, eventType, args):
		"""
		通知订阅者
		"""

		for targetID, callbackStrs in self.entityEventNotices[eventType].items():
			target = KBEngine.entities.get(targetID, None)
			if not target:
				KBEDebug.ERROR_MSG("targetID= %d callbackStr=%s"%(targetID, callbackStrs))
				continue

			for callbackStr in callbackStrs:
				target.entityEventRecieveNotify(eventType, self.id, callbackStr, args)
			
			
	def triggerEntityEvent(self, eventType, args):
		"""
		"""
		if not eventType in self.entityEventNotices:
			return
		self.entityEventNotify(eventType, args)



	def callbackTestFunc(self, eventType, notifierID, args):
		"""
		"""
		KBEDebug.ERROR_MSG("self.id=%d eventType=%d notifierID=%d args=%s"%(self.id, eventType, notifierID, args))