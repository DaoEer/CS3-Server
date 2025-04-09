# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from LoadModule import *
import Functions
import csdefine
import Const
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader


class NPCQuestInterface:

	def __init__( self ):
		pass

	def questWith( self, playerEntity, questID ):
		"""
		对话任务选项相关
		"""
		#获取该npc上的所有可交任务脚本
		questScipt = g_QuestLoader.getScript( questID )
		questState = playerEntity.queryQuestStatus( questID )
		
		if questScipt.type == csdefine.QUEST_TYPE_MAILLINE:					#主线任务直接弹出半身像
			playerEntity.sendApplyQuestDataByClick( questID, self.id )
			if questState == csdefine.QUEST_DONE:
				playerEntity.showMessagePlaySound(questScipt._data["finishTaskDes"])
				return
			else:
				playerEntity.showMessagePlaySound(questScipt._data["description"])
				return
				
		elif questScipt.type == csdefine.QUEST_TYPE_LOOP:						# 环任务
			playerEntity.sendApplyQuestDataByClick( questID, self.id )
			
		else:
			if questState == csdefine.QUEST_DONE:
				playerEntity.addGossipOption( str( questID ), questScipt.title, csdefine.GOSSIP_TYPE_COMPLETE_QUEST )
			else:
				playerEntity.addGossipOption( str( questID ), questScipt.title, csdefine.GOSSIP_TYPE_CAN_ACCEPT_QUEST )
	
	def questDataApplyByClick(self, srcEntityID, questID, questStatus):
		"""
		<Exposed method>
		客户端点击任务选项申请任务界面数据
		@param questID: 任务ID (string)
		@param questStatus: 任务的状态 (string)
		"""
		# playerEntity:说话的玩家 type:Entity
		playerEntity = KBEngine.entities.get(srcEntityID)
		questID = int( questID )

		if playerEntity is None:
			ERROR_MSG("NPCQuestInterface::questDataApplyByClick: Can't find entity %i" % srcEntityID)
			return

		questScipt = g_QuestLoader.getScript( questID )
		questData = questScipt._data
		questStatus = playerEntity.queryQuestStatus( questID )

		# 判断该任务是否在进行对话的npc上
		if int(questStatus) == csdefine.GOSSIP_TYPE_CAN_ACCEPT_QUEST:
			# 该npc上所有可接的任务
			canAcceptQuests = g_QuestLoader.getStartNPCQuests(self)

			canAcceptQuestsIdList = []

			for aquest in canAcceptQuests:
				canAcceptQuestsIdList.append(aquest.id)

			if questID not in canAcceptQuestsIdList:
				ERROR_MSG("NPCQuestInterface::questDataApplyByClick: questID %i not in npc %i" % (questID, int(self.scriptID)))
				return


		if int(questStatus) in [csdefine.GOSSIP_TYPE_COMPLETE_QUEST, csdefine.GOSSIP_TYPE_NOT_COMPLETE_QUEST]:
			# 该npc上所有可交的任务
			canCommitQuests = g_QuestLoader.getFinishNPCQuests(self)

			canCommitQuestsIdList = []

			for cquest in canCommitQuests:
				canCommitQuestsIdList.append(cquest.id)

			if questID not in canCommitQuestsIdList:
				ERROR_MSG("NPCQuestInterface::questDataApplyByClick: questID %i not in npc %i" % ( questID, int(self.scriptID)))
				return
				
			if questStatus == csdefine.GOSSIP_TYPE_NOT_COMPLETE_QUEST and questScipt.type == csdefine.QUEST_TYPE_MAILLINE:		#主线任务直接弹出半身像
				if questScipt._data["unFinishTaskDes"]:
					description = questScipt._data["unFinishTaskDes"]
				else:
					description = Const.UNFINISH_QUEST_DESCRIPT
				playerEntity.showMessagePlaySound( description )
				return
			
		playerEntity.sendApplyQuestDataByClick( questID, self.id )
		playerEntity.sendGossipComplete( self.id )

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
			WARNING_MSG("NPCQuestInterface::questStatusApply: entity %i out of AIO" % self.id)
			return

		# 对发送申请的npc进行遍历 如果玩家在npc处有可提交的任务则优先显示
		if self.hasDoneQuestByType( playerEntity, csdefine.QUEST_TYPE_MAILLINE ):
			playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_QUEST_SIGN_IS_DONE )
			return
		if self.hasNotDoneQuestByType( playerEntity, csdefine.QUEST_TYPE_MAILLINE ):
			playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_QUEST_SIGN_NOT_DONE )
			return

		if self.hasAcceptQuestByType( playerEntity, csdefine.QUEST_TYPE_MAILLINE ):
			playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_QUEST_SIGN_NOT_ACCEPT )
			return
		# 环任务
		if self.hasDoneQuestByType( playerEntity, csdefine.QUEST_TYPE_LOOP ):
			playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_LOOPQUEST_SIGN_IS_DONE )
			return
		if self.hasNotDoneQuestByType( playerEntity, csdefine.QUEST_TYPE_LOOP ):
			playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_LOOPQUEST_SIGN_NOT_DONE )
			return
		if self.hasAcceptQuestByType( playerEntity, csdefine.QUEST_TYPE_LOOP ):
			playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_LOOPQUEST_SIGN_NOT_ACCEPT )
			return
		playerEntity.clientEntity( self.id ).CLIENT_SetQuestSign( csdefine.NPC_QUEST_SIGN_NO_ACCEPT )
		
	def hasDoneQuestByType( self, playerEntity, questType ):
		"""是否有 可交任务 """
		finishQuests = g_QuestLoader.getFinishNPCQuests( self )
		for fquest in finishQuests:
			if fquest.type == questType and playerEntity.queryQuestStatus( fquest.id ) == csdefine.QUEST_DONE:
				return True
		if playerEntity.loopQuest["loopQuestList"]:
			loopQuestID = playerEntity.loopQuest["loopQuestList"][0]
			for fquest in finishQuests:
				questState = playerEntity.queryQuestStatus( fquest.id )
				if fquest.type == questType and fquest.id == loopQuestID:
					if questState == csdefine.QUEST_DONE:
						return True
		return False
		
	def hasNotDoneQuestByType( self, playerEntity, questType ):
		"""是否 有未完成任务 """
		finishQuests = g_QuestLoader.getFinishNPCQuests( self )
		for fquest in finishQuests:
			if fquest.type == questType and playerEntity.queryQuestStatus( fquest.id ) == csdefine.QUEST_NOT_DONE:
				return True
		if playerEntity.loopQuest["loopQuestList"]:
			loopQuestID = playerEntity.loopQuest["loopQuestList"][0]
			for fquest in finishQuests:
				questState = playerEntity.queryQuestStatus( fquest.id )
				if fquest.type == questType and fquest.id == loopQuestID:
					if questState == csdefine.QUEST_NOT_DONE:
						return True
		return False
		
	def hasAcceptQuestByType( self, playerEntity, questType ):
		"""是否有 可接任务"""
		if questType == csdefine.QUEST_TYPE_LOOP:
			if playerEntity.loopQuest["loopQuestNum"] >= Const.LOOP_QUEST_CAN_ACCEPT_NUM:		# 环任务一天只能做 3轮
				return False
		
		startQuests = g_QuestLoader.getStartNPCQuests( self )
		for squest in startQuests:
			if squest.type == questType:
				if playerEntity.queryQuestStatus( squest.id ) == csdefine.QUEST_NOT_ACCEPT:
				#需求:加上等级限制 自身等级-可接任务的所需等级＞10，将不显示绿色感叹号
					if playerEntity.level - squest.level > csdefine.QUEST_ACCEPT_FLAG_LIMIT:
						continue
					if squest.requirementCheck( playerEntity ):
						return True
#		if playerEntity.loopQuest["loopQuestList"]:
#			loopQuestID = playerEntity.loopQuest["loopQuestList"][0]
#			startQuests = g_QuestLoader.getStartNPCQuests( self )
#			for squest in startQuests:
#				if squest.type == questType and squest.id == loopQuestID:
#					questState = playerEntity.queryQuestStatus( squest.id )
#					if questState == csdefine.QUEST_NOT_ACCEPT:
#						if squest.requirementCheck( playerEntity ):
#							return True
		return False
	
	def getQuestGossipWith( self, playerEntity ):
		"""
		获取可对话的任务ID
		"""
		finishQuests = g_QuestLoader.getFinishNPCQuests( self )
		for fquest in finishQuests:
			# 该npc可交任务的状态
			questID = fquest.id
			fquestStatus = playerEntity.queryQuestStatus( questID )
			if fquestStatus == csdefine.QUEST_DONE:
				return questID
		startQuests = g_QuestLoader.getStartNPCQuests( self )
		for squest in startQuests:
			# 该npc可接任务的状态
			questID = squest.id
			squestStatus = playerEntity.queryQuestStatus( questID )
			if squestStatus == csdefine.QUEST_NOT_ACCEPT and squest.requirementCheck( playerEntity ):
				if squest.type == csdefine.QUEST_TYPE_MAILLINE:
					return questID
# 		其他任务判断
# 		if playerEntity.loopQuest["loopQuestList"]:
# 			loopQuestID = playerEntity.loopQuest["loopQuestList"][0]
# #			for fquest in finishQuests:
# #				if fquest.id == loopQuestID:
# #					if playerEntity.queryQuestStatus( loopQuestID ) == csdefine.QUEST_DONE:
# #						return loopQuestID
# 			for squest in startQuests:
# 				if squest.id == loopQuestID:
# 					if playerEntity.queryQuestStatus( loopQuestID ) == csdefine.QUEST_NOT_ACCEPT:
# 						return loopQuestID
		return 0
	