# -*- coding: utf-8 -*-
#
import KBEngine
from KBEDebug import *
from ConfigObject.Talk.TalkBase import TalkFunction
from ConfigObject.Talk import TalkVisible

class TalkFuncMgr:
	"""
	功能执行管理器
	"""
	def __init__(self):
		"""
		@param	param: pyDataSection
		@type	param: pyDataSection
		"""
		self._visibles = []		# 可见性
		self._functions= []

	def init(self, configData):
		"""
		数据初始化
		@param configData: py data section
		@type  configData: py data section 字典
		"""
		if len(configData["visibles"]):
			for visibleData in configData["visibles"]:
				#添加TalkVisible实例
				self._visibles.append(getattr(TalkVisible, visibleData["key"])(visibleData))

		if len(configData["functions"]):
			for funcData in configData["functions"]:
				#添加TalkFunction实例
				self._functions.append(TalkFunction.TalkFunction(funcData))

	def isVisible(self, player, talkEntity, args):
		"""
		检查npc的可见性
		"""
		for v in self._visibles:
			if not v.isVisible(player, talkEntity, args):
				return False

		return True

	def do(self, dlgKey, player, talkEntity, args):
		"""
		执行一个功能，必须重载
		@param	player: 玩家
		@type	player: Entity
		@param	talkEntity: 一个扩展的参数
		@type	talkEntity: entity
		@return: None
		"""
		for action in self._functions:
			action.do(dlgKey, player, talkEntity, args)
