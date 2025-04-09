# -*- coding: utf-8 -*-
import KBEngine
import time
import csdefine
import cschannel_msgs
from KBEDebug import *
from ObjectScript.NPC import NPC

from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader

DIALOG_TALK_KEY = ""
EXTRA_TALK_PARAM = ""


class TongNPC( NPC.NPC ):
	def __init__( self ):
		NPC.NPC.__init__( self )

	def gossipWith(self, selfEntity, srcEntityID):
		"""
		处理玩家请求与NPC对话的信息
		"""
		playerEntity = KBEngine.entities.get(srcEntityID)
		if playerEntity is None:
			ERROR_MSG( "TongNPC::gossipWith:Can't found gossip with player entity %i!" % srcEntityID )
			return
		selfEntity.talkWith( srcEntityID, DIALOG_TALK_KEY, EXTRA_TALK_PARAM )
		finishQuests = g_QuestLoader.getFinishNPCQuests( self )
		for fquest in finishQuests:
			status = playerEntity.queryQuestStatus( fquest.id )
			if status == csdefine.QUEST_DONE:
				playerEntity.addGossipOption( str( fquest.id ), cschannel_msgs.TONG_DAILY_QUEST_TITLE, csdefine.GOSSIP_TYPE_COMPLETE_TONG_DAILY_QUEST )
				break
				
		qList = playerEntity.dailyQuest.getAcceptQuestList()
		startQuests = g_QuestLoader.getStartNPCQuests( self )
		for quest in startQuests:
			if quest.id in qList:
				playerEntity.addGossipOption( str( quest.id ), cschannel_msgs.TONG_DAILY_QUEST_TITLE, csdefine.GOSSIP_TYPE_CAN_ACCEPT_TONG_DAILY_QUEST )
				break