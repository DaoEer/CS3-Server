# -*- coding: utf-8 -*-
#
# data
import npctalk
# path
from ConfigObject.Talk.TalkBase import DialogManager
# common
import KBEngine
from KBEDebug import *

import HotUpdate

import NPCQuestTalk


class NPCTalkLoader:
	"""
	NPC对话内容加载器
	"""
	_instance = None

	def __init__(self):
		# 不允许有2个或2个以上实例
		assert NPCTalkLoader._instance is None
		# key == npcID
		# value == DialogManager()
		self._datas = {}
		NPCTalkLoader._instance = self
	
	def initTalkConfig( self, scriptID ):
		"""
		初始化一个对话
		"""
		talkData = npctalk.getSourceConfig( scriptID )
		npcQuestTalkdatas = NPCQuestTalk.Datas
		for key in talkData.Datas:
			self._datas[key] = DialogManager.DialogManager(talkData.Datas[key]["talks"])			
			if key in self._datas and npcQuestTalkdatas.get(key):
				self._datas[key].initQuestTalk(npcQuestTalkdatas[key])
			
	def reloadTalkConfig( self, scriptID ):
		"""
		配置支持热加载
		"""
		configData = npctalk.reloadSourceConfig( scriptID )
		if configData:
			for key in configData.Datas.keys():
				try:
					self._datas[key] = DialogManager.DialogManager(configData.Datas[key]["talks"])
				except Exception as e:
					CRITICAL_MSG( "Talk config error!! scriptID:%s \n\n config section:\n%s \n\n Error Infos:\n%s\n\n\n"%( key, str( configData.Datas[key]["talks"] ), e) )
				return True
		return False

	def get(self, scriptID):
		"""
		根据npcID取得对话脚本
		@return: instance of DialogManager
		"""
		if scriptID not in self._datas:
			self.initTalkConfig( scriptID )
			
		return self._datas.get( scriptID )

	@staticmethod
	def instance():
		"""
		"""
		if NPCTalkLoader._instance is None:
			NPCTalkLoader._instance = NPCTalkLoader()

		return NPCTalkLoader._instance