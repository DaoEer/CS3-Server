# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ObjectScript.NPC import NPCBase

DIALOG_TALK_KEY = ""
EXTRA_TALK_PARAM = ""


class NPC( NPCBase.NPCBase ):
	def __init__( self ):
		NPCBase.NPCBase.__init__( self )

	def initData( self, configData ):
		if configData is not None:
			NPCBase.NPCBase.initData( self, configData )
			if 'WalkSpeed' in configData:
				self.walkSpeed = configData["WalkSpeed"]
			if 'MinLevel' in configData:
				self.minLevel = configData["MinLevel"]
			if 'MaxLevel' in configData:
				self.maxLevel = configData["MaxLevel"]


	def gossipWith(self, selfEntity, srcEntityID):
		"""
		处理玩家请求与NPC对话的信息
		"""
		playerEntity = KBEngine.entities.get(srcEntityID)
		if playerEntity is None:
			ERROR_MSG( "NPC::gossipWith:Can't found gossip with player entity %i!" % srcEntityID )
			return
		#由于要优先列出普通对话，再列出任务对话选项，加了这个判断
		if not selfEntity.hasMainLineQuest( playerEntity ):
			#普通对话
			selfEntity.talkWith( srcEntityID, DIALOG_TALK_KEY, EXTRA_TALK_PARAM )
		else:
			# 处理任务对话
			selfEntity.questWith( playerEntity )