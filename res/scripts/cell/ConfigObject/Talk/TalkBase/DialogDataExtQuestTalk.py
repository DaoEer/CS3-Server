# -*- coding: utf-8 -*-
#
import KBEngine
import KBEDebug
from KBEDebug import *
from ConfigObject.Talk.TalkBase import DialogMsg
from ConfigObject.Talk.TalkBase import TalkFuncMgr
import QuestEventDefine

class DialogDataExtQuestTalk:
	"""
	对话抽象层:对话数据处理
	"""
	def __init__(self, section = None):
		if section:
			self.init(section)

	def init(self, section):
		"""
		@param section: py data section
		@type  section: py data section 字典
		"""
		# init dialog message
		self._questTalks = section




	def doTalk(self, dlgKey, player, talkEntity, args):
		"""
		执行对话动作
		@param player: 玩家
		@type  player: Entity
		@param talkEntity: 对话的原始目标Entity
		@type  talkEntity: Entity
		@param args: 对话参数
		@return: None
		"""
		for questTalk in self._questTalks:
			if self.isCanDo(player, questTalk["questID"], questTalk["taskID"]):
				if player.isMountOnPet():
					player.transformPet( player.id )
				player.dialogWithNPCTaskScriptID(talkEntity.scriptID)
				player.showMessagePlaySound(questTalk["voiceID"])
#				player.triggerQuestEvent(QuestEventDefine.EVENT_TALK_WITH_NPC, talkEntity.scriptID)
				return True
		return False

	def isCanDo(self, player, questID, taskID):
		"""
		检测是否能执行任务对话
		"""
		#格式：1:2;2:3   2:完成，3:未完成 这个配置的意思是目标1完成，目标2未完成
		taskIDStrList = taskID.split(";")
		for taskIDStr in taskIDStrList:
			splitList = taskIDStr.split(":")
			tID = int(splitList[0])
			tState = int(splitList[1])
			if tState == csdefine.TASK_DONE:
				if not csdefine.TASK_DONE == player.queryTaskStatus(questID, tID):
					return False
			else:
				if not csdefine.TASK_NOT_DONE == player.queryTaskStatus(questID, tID):
					return False
		return True

		


