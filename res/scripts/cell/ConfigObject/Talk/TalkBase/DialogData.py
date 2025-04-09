# -*- coding: utf-8 -*-
#
import KBEngine
from KBEDebug import *
from ConfigObject.Talk.TalkBase import DialogMsg
from ConfigObject.Talk.TalkBase import TalkFuncMgr


class DialogData:
	"""
	对话抽象层:对话数据处理
	"""
	def __init__(self, section = None):
		self._dlgMsg = None		#instance of DialogMsg
		self._dlgDepands = {}	#key is menuKey, value is instance of class DialogData
		self._func = None		#instance of TalkFuncMgr
		if section:
			self.init(section)

	def init(self, section):
		"""
		@param section: py data section
		@type  section: py data section 字典
		"""
		# init dialog message
		self.initDialogMsg(section)

		# init functions
		self._func = TalkFuncMgr.TalkFuncMgr()
		self._func.init(section)

	def initDialogMsg(self, section):
		"""
		@param section: py data section
		@type  section: py data section 字典
		"""
		dlg = DialogMsg.DialogMsg()
		self._dlgMsg = dlg
		dlg.setMsg(section["msg"])

		if "keys" in section:
			if len(section["keys"]):
				for m in section["keys"]:
					key = m["key"]
					title = m["title"]
					type = m["type"]
					dlg.addMenu(key, title, type)

		return

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
		self._func.do(dlgKey, player, talkEntity, args)
		if self._dlgMsg is None:
			# 没有对话,直接返回
			return

		# send dialog
		if self._dlgMsg.getMsg() != "" or len( self._dlgMsg.getMenus() ) >0:
			player.setGossipText(talkEntity.id, self._dlgMsg.getMsg())

		for m in self._dlgMsg.getMenus():
			if self._dlgDepands[m[0]].canVisible(player, talkEntity, args):
				player.addGossipOption(*m)

	def canVisible(self, player, talkEntity, args):
		"""
		检查对话动作是否允许
		@param player: 玩家
		@type  player: Entity
		@param talkEntity: 一个扩展的参数
		@type  talkEntity: entity
		@return: None
		"""
		return self._func.isVisible(player, talkEntity, args)

	def buildDepend(self, manager):
		"""
		@param manager: 类的管理者
		@type  manager: DialogManager
		"""
		if self._dlgMsg is None:
			return

		menus = self._dlgMsg.getMenuKeys()

		for m in menus:
			dlgData = manager.getDialog(m)
			if dlgData is None:
				continue
			self._dlgDepands[m] = dlgData
