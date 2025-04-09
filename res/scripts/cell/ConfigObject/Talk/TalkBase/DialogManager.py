# -*- coding: utf-8 -*-
#
import KBEngine
import KBEDebug
from ConfigObject.Talk.TalkBase import DialogData
from ConfigObject.Talk.TalkBase import DialogDataExtQuestTalk



class DialogManager:
	"""
	对话抽象层:npc对话管理
	"""
	def __init__(self, section = None):
		"""
		"""
		self._dialogs = {}		# key is dlgKey with string type, value is instance of class DialogData
		if section:
			self.init(section)

	def init(self, section):
		"""
		@param section: py data section
		@type  section: py data section 列表
		"""
		#load all dialogs
		for sec in section:
			dlg = DialogData.DialogData(sec)
			self._dialogs[sec["key"]] = dlg

		#build dialog depend
		for v in self._dialogs.values():
			v.buildDepend(self)

	def initQuestTalk(self, section):
		"""
		@param section: py data section
		@type  section: py data section 列表
		"""
		#load all dialogs
	
		dlg = DialogDataExtQuestTalk.DialogDataExtQuestTalk(section)
		self._dialogs["questTalk"] = dlg


	def doTalk(self, dlgKey, player, talkEntity, args):
		"""
		执行对话动作
		@param dlgKey: 对话关键字
		@type  dlgKey: string
		@param player: 玩家
		@type  player: Entity
		@param talkEntity: 一个扩展的参数
		@type  talkEntity: Entity
		@param args: 对话参数
		@return: None
		"""
		if dlgKey == "":
			if not self.doQuestTalk(dlgKey, player, talkEntity, args):
				self.doCommonTalk(dlgKey, player, talkEntity, args)
		else:
			try:
				dlg = self._dialogs[dlgKey]
			except KeyError:
				return
			dlg.doTalk(dlgKey, player, talkEntity, args)


	def doCommonTalk(self, dlgKey, player, talkEntity, args):
		"""
		执行普通对话动作
		@param dlgKey: 对话关键字
		@type  dlgKey: string
		@param player: 玩家
		@type  player: Entity
		@param talkEntity: 一个扩展的参数
		@type  talkEntity: Entity
		@param args: 对话参数
		@return: None
		"""
		dlg = self._dialogs["Talk"]		#第一次请求对话时 dlgKey = "" 发送对话配置的第一层内容
		dlg.doTalk(dlgKey, player, talkEntity, args)


	def doQuestTalk(self, dlgKey, player, talkEntity, args):
		"""
		执行任务对话动作
		@param dlgKey: 对话关键字
		@type  dlgKey: string
		@param player: 玩家
		@type  player: Entity
		@param talkEntity: 一个扩展的参数
		@type  talkEntity: Entity
		@param args: 对话参数
		@return: None
		"""
		dlg = self._dialogs.get("questTalk")   #第一次请求对话时 dlgKey = "" 有任务对话先执行任务对话，没有再执行普通对话
		if not dlg:
			return False
		return dlg.doTalk(dlgKey, player, talkEntity, args)

		


	def getDialog(self, dlgKey):
		"""
		以指定关键字取得一个对话，不存在则返回None

		@param dlgKey: 对话关键字
		@type  dlgKey: string
		@return: instance of DialogData/None
		"""
		try:
			return self._dialogs[dlgKey]
		except KeyError:
			return None

