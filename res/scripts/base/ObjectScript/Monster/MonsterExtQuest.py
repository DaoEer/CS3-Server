# -*- coding: utf-8 -*-

import KBEngine
import Math
import csdefine
import ObjectScript.Monster.Monster as Monster


class MonsterExtQuest( Monster.Monster ):
	"""
	任务怪（处理特定任务目标状态下的表现，比如屏蔽主动攻击，语音喊话等）
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.questStatusDict = {}

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		if configData is not None:
			Monster.Monster.initData( self, configData )
			if 'questStatus' in configData:
				questStatus = configData["questStatus"].strip()
				self.initQuestStatuesDict( questStatus )

	def initQuestStatuesDict(self, questStatus):
		"""
		初始化 self.questStatusDict    格式："20001:2|20002:3;1:2"  转化为 {20001:{"questStatus":2,"taskStatus":{}},20002:{"questStatus":3,"taskStatus":{1:2,}}}
		"""
		if not len(questStatus):
			return

		_questStatus = questStatus.split("|")
		for status in _questStatus:
			strList = status.split(";")
			#第一个为quest状态，后面的为task状态
			qs = strList[0].split(":")
			self.questStatusDict[qs[0]] = {"questStatus":int(qs[1]),"taskStatus":{}}
			if len(strList)<2:	continue
			for taskStatus in strList[1:]:
				ts = taskStatus.split(":")
				self.questStatusDict[qs[0]]["taskStatus"].update({int(ts[0]):int(ts[1])})

	def checkQuestStatues(self, playerEntity):
		"""
		检查目标玩家身上的任务状态是否满足条件 多个条件满足一个就返回True
		"""
		if not playerEntity or playerEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False

		for questID, statusValue in self.questStatusDict:
			if not playerEntity.hasQuest(questID):
				continue
			if playerEntity.queryQuestStatus(questID) != statusValue["questStatus"]:
				continue
			if  not len(statusValue["taskStatus"]):
				return True
			for taskID, taskStatus in statusValue["taskStatus"]:
				if playerEntity.queryTaskStatus(questID, taskID) != taskStatus:
					break
				return True

		return False

	


	


