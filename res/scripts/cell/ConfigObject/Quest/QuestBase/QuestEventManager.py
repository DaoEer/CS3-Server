# -*- coding: utf-8 -*-
#
import QuestEventDefine


class QuestEventManager:

	def __init__(self):
		self._events = {}

	def initFromStream(self, data):
		"""从打包数据恢复"""
		for event in data["events"]:

			observers = set()
			for observer in event["observers"]:
				observers.add((observer["questID"], observer["taskID"]))

			self._events[event["eventID"]] = observers

	def packStreamData(self):
		"""打包传输数据"""
		events = []
		for eventID, observers in self._events.items():
			events.append({
				"eventID": eventID,
				"observers": [{"questID": q, "taskID": t} for q, t in observers]
				})

		return {"events": events}

	def registerEvent(self, eventID, observer):
		"""注册任务事件"""
		assert eventID in QuestEventDefine.events
		if self._events.get( eventID, [] ):
			if observer in self._events[eventID]:return

		if eventID not in self._events:
			self._events[eventID] = set()

		self._events[eventID].add(observer)

	def deregisterEvent(self, eventID, observer):
		"""注销任务事件"""
		if eventID in self._events and observer in self._events[eventID]:
			self._events[eventID].remove(observer)
			if len(self._events[eventID]) == 0:
				del self._events[eventID]

	def hasEvent(self, eventID):
		"""是否存在指定事件"""
		return eventID in self._events

	def queryObservers(self, eventID):
		"""查询事件"""
		if eventID in self._events:
			return tuple(self._events[eventID])
		else:
			return ()

	def clear(self):
		"""清空事件数据，通常重新注册事件时调用"""
		self._events.clear()