# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
from ObjectScript.NPC import NPC
from ConfigObject.Talk.TalkBase import NPCTalkLoader
g_npcTalk = NPCTalkLoader.NPCTalkLoader.instance()

DIALOG_TALK_KEY = ""
EXTRA_TALK_PARAM = ""

class NPCFastTeam( NPC.NPC ):
	def __init__( self ):
		NPC.NPC.__init__( self )
		self.spaceScriptIDData = {} # {talkKey: spaceScriptID}
		self.reqLevelData = {} #需要等级 {talkKey: reqLevel}
		self.teamMaxNumData = {} #快速组队副本最多人数 {talkKey: maxNum}

	def initData( self, configData ):
		if configData is not None:
			NPC.NPC.initData( self, configData )
			if configData["Param1"]:
				for info in configData["Param1"].split("|"):
					infoList = info.split(":")
					if len(infoList) == 4:
						spaceScriptID, talkKey, reqLevel, maxNum = infoList
						self.spaceScriptIDData[talkKey] = spaceScriptID
						self.reqLevelData[talkKey] = int(reqLevel)
						self.teamMaxNumData[talkKey] = int(maxNum)

	def gossipWith(self, selfEntity, srcEntityID):
		"""
		处理玩家请求与NPC对话的信息
		"""
		playerEntity = KBEngine.entities.get(srcEntityID)
		if playerEntity is None:
			ERROR_MSG( "NPC::gossipWith:Can't found gossip with player entity %i!" % srcEntityID )
			return
			
		if playerEntity.getClient() and len(self.teamMaxNumData) > 0:
			#根据对话可见性判断是否需要打卡快速组队界面
			talkObj = g_npcTalk.get(selfEntity.getScriptID())
			for talkKey, maxNum in self.teamMaxNumData.items():
				talkDialog = talkObj.getDialog(talkKey)
				if talkDialog and talkDialog.canVisible(playerEntity, selfEntity, ""):
					spaceScriptID = self.spaceScriptIDData[talkKey]
					reqLevel = self.reqLevelData[talkKey]
					maxNum = self.teamMaxNumData[talkKey]
					isMatchFastTeam = playerEntity.getIsMatchFastTeam()
					lastFastTalkNpcID = playerEntity.getFastTeamTalkNpcID()
					if lastFastTalkNpcID != selfEntity.id: #如果本次对话的NPC和之前快速组队的NPC不是同一个，相对于本次的NPC是没有进行快速组队
						isMatchFastTeam = False
					KBEngine.globalData["FastTeamMgr"].setTeamMemberMaxNum(spaceScriptID, maxNum)
					playerEntity.client.CLIENT_OpenFastTeamWin(spaceScriptID, reqLevel, int(isMatchFastTeam), selfEntity.getScriptID(), selfEntity.id, talkKey)
					break
		
		gossipWithQuestID = selfEntity.getQuestGossipWith( playerEntity )
		if gossipWithQuestID:
			# 处理任务对话
			selfEntity.questWith( playerEntity, gossipWithQuestID )
		else:
			#普通对话
			selfEntity.talkWith( srcEntityID, DIALOG_TALK_KEY, EXTRA_TALK_PARAM )