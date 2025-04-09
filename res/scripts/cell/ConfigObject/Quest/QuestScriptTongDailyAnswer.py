# -*- coding: utf-8 -*-
import json
import time
import random
import KBEDebug
import KBEngine
import Const
import QuestEventDefine

from ConfigObject.Quest.QuestScriptTongDaily import QuestScriptTongDaily
from AnswerConfig.TongAnswer import Datas as answerDatas

from MsgLogger import g_logger
import LogDefine

class QuestScriptTongDailyAnswer( QuestScriptTongDaily ):
	"""
	帮会 日常任务 答题任务
	"""
	def __init__(self):
		QuestScriptTongDaily.__init__(self)
		self.totalAnswerTimeSec = 10.0    #每道题的答题时间
		self.totalAnswer  = 5 			 # 需要答对题数

	def afterClientAccepted(self, player, params = {}):
		"""
		接了任务之后（通知了客户端），部分任务需要做处理
		"""
		self.sendRandomQuestionToClient(player)

	def getAnswerData( self ):
		return answerDatas

	def getQuestionIdList( self ):
		idList = []
		for key,velue in answerDatas.items():
			if "questionID" in velue:
				idList.append(velue["questionID"])
		return idList

	def getAnswer( self, questionID):
		"""
		获取答题答案
		"""
		return answerDatas.get(questionID).get("answer",Const.TONG_ANSWER_OPTION_LIST[0])

	def getDescription( self, questionID):
		"""
		获取答题描述
		"""
		return answerDatas.get(questionID).get("questionDes","")

	def getOption(self, questionID):
		"""
		获取答题答案选项
		"""
		options = []
		answerData = answerDatas.get(questionID)
		for key in Const.TONG_ANSWER_OPTION_LIST:
			option = answerData.get(key, "")
			if option == "":
				break
			options.append(option)
		return options

	def sendRandomQuestionToClient( self, player):
		"""
		发送随机题目到客户端
		"""
		questionList = player.queryTemp("replyTongQuestion", [])
		answerData = self.getAnswerData()
		questionIDList = self.getQuestionIdList()
		random.shuffle(questionIDList)
		currentQuestionID = 0
		for questionID in questionIDList:
			if questionID not in questionList:
				currentQuestionID = questionID
				break
		currentDescription = self.getDescription( currentQuestionID ) # 当前问题的描述
		currentOption =self.getOption( currentQuestionID )	
		player.client.OnReceiveTongKnowledge(self._id, currentQuestionID, currentDescription, json.dumps(currentOption))
		
		timer = player.addTimerCallBack( self.totalAnswerTimeSec, "playerAnswerTongQuestion", ( player.id, str(self._id), str(currentQuestionID), "timeup") )
		player.setTemp("tongQuestionAnswerTimer", timer) #当答题时间超过后，需要重新答题

	def onPlayerAnswer( self, player, questionID, answer):
		"""
		玩家回答
		"""
		timer = player.queryTemp("tongQuestionAnswerTimer", 0)
		if timer:
			player.popTimer(timer)
			player.removeTemp("tongQuestionAnswerTimer")
	
		if answer == "timeup":
			return

		if answer != self.getAnswer(questionID):
			player.client.OnKnowledgeAnswerResult(questionID, 0)
		else:
			questionList = player.queryTemp("replyTongQuestion", [])
			questionList.append(questionID)
			player.setTemp("replyTongQuestion", questionList)
			player.client.OnKnowledgeAnswerResult(questionID, 1)
			player.triggerQuestEvent( QuestEventDefine.EVENT_ANSWER_QUESTION, None )
			questionCount = player.queryTemp("tongQuestionCount",0) + 1
			if questionCount < self.totalAnswer:	  # 回答正确5个就结束
				player.setTemp("tongQuestionCount", questionCount)
			else:
				player.removeTemp("tongQuestionCount")
				player.client.CLIENT_CloseTongKnowledge()
				#添加活动参与记录
				g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_JWSJ, player.accountDBID, player.playerDBID, player.getLevel(), "", "", int(time.time()), 0, LogDefine.ACTIVE_STATE_TYPE_SUCCESS)
				return
		self.sendRandomQuestionToClient(player)

	def onStopTongQuestion( self, player):
		"""
		暂停答题
		"""
		timer = player.queryTemp("tongQuestionAnswerTimer", 0)
		if timer:
			player.popTimer(timer)
			player.removeTemp("tongQuestionAnswerTimer")
