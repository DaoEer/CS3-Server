# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import Const
import FightRuleMgr

import NPC
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader

class TongNPC(  NPC.NPC ):
	"""
	帮会 NPC
	"""

	def __init__( self ):
		NPC.NPC.__init__( self )
		
	def questStatusApply(self, srcEntityID):
		"""
		<Exposed method>
		当玩家进入npc视野后 客户端向服务器申请该npc身上的任务状态用于显示头顶标识
		# NPC 显示头顶标识优先级
		# 1、接取了任务，并且任务完成
		# 2、接取了任务，任务没有完成
		# 3、有任务可接
		# 4、没有可接任务
		"""
		# playerEntity:进入视野的玩家 type:Entity
		playerEntity = KBEngine.entities.get(srcEntityID)

		if self.isOutOwnerAOI( playerEntity ):
			KBEDebug.WARNING_MSG("TongNPC::questStatusApply: entity %i out of AIO" % self.id)
			return
			
#		if self.ownTongDBID != playerEntity.tongDBID:
#			return
			
		finishQuests = g_QuestLoader.getFinishNPCQuests( self )
		for fquest in finishQuests:
			status = playerEntity.queryQuestStatus( fquest.id )
			if status == csdefine.QUEST_DONE:
				playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_LOOPQUEST_SIGN_IS_DONE )
				return
				
			elif status == csdefine.QUEST_NOT_DONE:
				playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_LOOPQUEST_SIGN_NOT_DONE )
				return
			
		qList = playerEntity.dailyQuest.getAcceptQuestList()
		startQuests = g_QuestLoader.getStartNPCQuests( self )
		for quest in startQuests:
			if quest.id in qList:
				playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_LOOPQUEST_SIGN_NOT_ACCEPT )
				return
		playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_QUEST_SIGN_NO_ACCEPT )
	
	