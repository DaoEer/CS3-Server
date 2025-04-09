# -*- coding: utf-8 -*-
import time
from KBEDebug import *
from configObject import Quest
import csdefine
class RoleQuestInterface:
	
	def __init__(self):
		self.questTable={}
		self.questLog = []
		self.hasInitQuest = False
		
	def resetQuest(self):
		for q in self.questTable:
			self.abandonQuest( q )
			
		self.questTable = {}
		self.questLog = []
		self.GMCommand( self, "remove_completed_quest" , "0" )
		
	def getUnaccomplishedQuest(self):
		"""
		"""
		if len(self.questTable) <= 0:
			return None
		
		quest = None
		for q in self.questTable.values():
			if q.isDone(): continue
			if quest is None: 
				quest = q
				continue
			
			if quest.acceptTime < q.acceptTime:
				quest = q
				
		return quest
		
	def OnQuestInitNotity(self):
		"""
		"""
		self.hasInitQuest = True
		
	def acceptQuest( self, questID ):
		"""接任务"""
		self.cell.rquestToAcceptQuest( str(questID ))
		self.outputMsg("rquestToAcceptQuest {}".format(questID))
		
	def commitQuest( self, questID ):
		"""交任务"""
		self.chooseReward( str(questID) )			#如果有需要选择的奖励，先选择奖励。
		self.cell.requestToCommitQuest( str(questID ))
		self.outputMsg("requestToCommitQuest {}".format(questID))
	
	def abandonQuest( self, questID ):
		"""放弃任务"""
		self.cell.requestToAbandonQuest( str(questID ))
		self.outputMsg("requestToAbandonQuest {}".format(questID))
	
	def chooseReward( self, questID ):
		"""选择奖励"""
		quest = self.questTable[questID]
		if str(csdefine.QUEST_REWARD_TYPE_ITEM_CHOOSE) in quest.rewards.keys():
			rewards = quest.rewards[ str(csdefine.QUEST_REWARD_TYPE_ITEM_CHOOSE) ]
			for reward in rewards:
				index = reward["index"]
				itemInfo = reward["datas"].split("|")[0].replace( ":", "|" )
				self.cell.questChooseReward( questID, str(index), itemInfo)
				self.outputMsg("questChooseReward {}".format(questID))
		
	def onAcceptQuest(self, dataStream):
		"""
		接任务
		"""
		questData = eval( dataStream )["ROOT"]
		quest=Quest.Quest()
		quest.init(self, questData)
		self.questTable[ quest.id ] =  quest
		self.outputMsg("QUEST_AcceptQuest [%s]" %(quest.getQuestInfo()))
		if len(self.questTable) > 1:
			self.outputMsg("AcceptQuest error [%s]" %(list(self.questTable.keys())))
		
		if quest.isDone():
			self.onQuestComplete(quest.id)
		else:
			self.eventObj.fireEvent("Event_OnAcceptQuest", quest.id)
		
	def onAddQuest(self, dataStream):
		"""
		新增任务
		"""
		self.onAcceptQuest(dataStream)
		
	def onCommitQuest(self, questID):
		"""
		交任务
		"""
		self.questLog.append(questID)
		if questID in self.questTable:
			self.questTable.pop( questID )
		self.eventObj.fireEvent("Event_onQuestCommit", questID)
		self.outputMsg("QUEST_COMMIT questID: %s" %(questID))
		
	def onAbandonQuest(self, questID):
		"""
		放弃任务
		"""
		qstID = str(questID)
		if qstID in self.questTable:
			self.questTable.pop( qstID )
	
	def onQuestComplete(self, questID):
		"""
		任务完成
		"""
		#交任务
		self.eventObj.fireEvent("Event_onQuestComplete", questID)
		self.cell.requestToCommitQuest(str(questID))
		self.questTable.pop(questID, None)
		#任务完成即从任务列表删除，如果读不到，说明完成了
		self.outputMsg("requestToCommitQuest %s" % questID)
		
	def resetQuestAction( self ):
		self.GMCommand( self, "remove_completed_quest")
		self.questTable={}
		self.questLog = []
	
#------no use------	
	def onUpdateQuestTask(self, questID, taskID, progress):
		"""
		更新任务目标
		"""
		#self.outputMsg("botsMSG: QUEST_UPDATE_TASK questID: %s, task:%s, progress:%s, BEGIN" % (questID, taskID, str(progress)))
		if questID not in self.questTable:
			#ERROR_MSG("not found quest[%d:%d:%d]" %(questID, taskID, progress))
			return
		
		self.questTable[questID].updateTaskProgress(self, taskID, progress)
		self.eventObj.fireEvent("Event_onUpdateQuestTask", questID, taskID)
		#self.outputMsg("botsMSG: QUEST_UPDATE_TASK questID: %s, task:%s, progress:%s, END" % (questID, taskID, str(progress)))
	
	def onRecvQuestLog(self, dataStream):
		pass
		
	def onSetQuestContent(self, dataStream):
		#ERROR_MSG(dataStream)
		data = eval( dataStream )["ROOT"]
		questID = int(data["id"])
		self.cell.rquestToAcceptQuest(str(questID))
		self.outputMsg("rquestToAcceptQuest {}".format(questID))
	
	def OnQuestStatusChange(self):
		pass
		
	def onRemoveQuestLog(self, questID):
		pass
		
	def onClearQuestLog(self):
		pass
		
	def ShowLoopRewardTip( self, msgInfo, exp, money ):
		pass
	def OnRequestTongDailyQuest( self, p1, p2 ):
		pass
	def OnReceiveTongKnowledge( self, p1, p2, p3, p4 ):
		pass
	def OnKnowledgeAnswerResult( self, p1, p2 ):
		pass
	def CLIENT_CloseTongKnowledge( self ):
		pass
	def ShowDynamicRewards( self, p1, p2 ):
		pass
	def ShowLoopQuestSpaceWin( self, p1, p2, p3, p4, p5 ):
		pass
	def SetQuestTaskDone( self, p1, p2 ):
		pass
	def StartTimeQuest( self, p1, p2 ):
		pass
	def StartWhisperQuest( self, p1, p2, p3, p4, p5 ):
		pass
	def OnCompleteWhisperQuest( self, p1, p2, p3 ):
		pass
	def ShowTongDailyQuestSpaceWin( self, p1, p2, p3, p4, p5 ):
		pass
	def ShowLoopQuestWin(self):
		pass
	

	def onRemoveQuestLogByType( self, p1 ):
		pass