# -*- coding: utf-8 -*-
import Const
import Math
import KBEMath
import KBEngine
from KBEDebug import *
import time
import csstatus
import csconst
import json
import random
import Functions
from ObjectScript import Space
from ObjectScript.Space.SpaceCopyMagicMazeChild import SpaceCopyMagicMazeChild
from AnswerConfig.MagicMazeAnswer import Datas as answerDatas


class SpaceCopyMagicMazeChildAnswer( SpaceCopyMagicMazeChild ):
	"""
	幻阵迷宫 问答玩法
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChild.__init__( self )
		self.startAnswerTimeSec = 0
		self.totalAnswerTimeSec = 0
		self.countDownTimeSec = 0
		self.closeTimeSec = 0
		self.extraPersonRate = 0.0
		self.extraTeamRate = 0.0
		self.questionCount = 0
		self.rewardCountList = []
		self.perfectTeamReward = {"messageID":0,"spellboxID":"","position":Math.Vector3(0.0, 0.0, 0.0),"direction":Math.Vector3(0.0, 0.0, 0.0)}
		self.goodTeamReward = {"messageID":0,"spellboxID":"","position":Math.Vector3(0.0, 0.0, 0.0),"direction":Math.Vector3(0.0, 0.0, 0.0)}
		
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyMagicMazeChild.initData( self, configData )
		self.startAnswerTimeSec = configData["SpaceData"].get("startAnswerTimeSec", 0)
		self.totalAnswerTimeSec = configData["SpaceData"].get("totalAnswerTimeSec", 0)
		self.countDownTimeSec = configData["SpaceData"].get("countDownTimeSec", 0)
		self.closeTimeSec = configData["SpaceData"].get("closeTimeSec", 0)
		self.extraPersonRate = configData["SpaceData"].get("extraPersonRate", 0.0)
		self.questionCount = configData["SpaceData"].get("questionCount", 0)
		perfectTeamReward = configData["SpaceData"].get("perfectTeamReward",{})
		if perfectTeamReward:
			self.perfectTeamReward["messageID"] = perfectTeamReward.get("messageID", 0)
			self.perfectTeamReward["spellboxID"] = perfectTeamReward.get("spellboxID", "")
			self.perfectTeamReward["position"] = Math.Vector3(0.0, 0.0, 0.0)
			self.perfectTeamReward["direction"] = Math.Vector3(0.0, 0.0, 0.0)
			posStr = perfectTeamReward.get( "position", "" )
			pos = Functions.vector3TypeConvert( posStr )
			if pos:
				self.perfectTeamReward["position"] = KBEMath.Unreal2KBEnginePosition( pos )

			dirStr = perfectTeamReward.get( "direction", "" )
			dir = Functions.vector3TypeConvert( dirStr )
			if dir:
				self.perfectTeamReward["direction"] = KBEMath.Unreal2KBEngineDirection( dir )
				
		goodTeamReward = configData["SpaceData"].get("goodTeamReward",{})
		if goodTeamReward:
			self.goodTeamReward["messageID"] = goodTeamReward.get("messageID", 0)
			self.goodTeamReward["spellboxID"] = goodTeamReward.get("spellboxID", "")
			self.goodTeamReward["position"] = Math.Vector3(0.0, 0.0, 0.0)
			self.goodTeamReward["direction"] = Math.Vector3(0.0, 0.0, 0.0)
			posStr = goodTeamReward.get( "position", "" )
			pos = Functions.vector3TypeConvert( posStr )
			if pos:
				self.goodTeamReward["position"] = KBEMath.Unreal2KBEnginePosition( pos )

			dirStr = goodTeamReward.get( "direction", "" )
			dir = Functions.vector3TypeConvert( dirStr )
			if dir:
				self.goodTeamReward["direction"] = KBEMath.Unreal2KBEngineDirection( dir )
				
		rewardPotential = configData["SpaceData"].get("rewardPotential", "")
		if rewardPotential:
			self.rewardCountList = [ int(i) for i in rewardPotential.split("|")]
		
		
	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		SpaceCopyMagicMazeChild.startSpaceLife( self, selfEntity )
		selfEntity.startCountDownTimer = selfEntity.addTimerCallBackForScript( self.startAnswerTimeSec - self.countDownTimeSec, "initAnswerCountDown", () )
		selfEntity.startAnswerTimer = selfEntity.addTimerCallBackForScript( self.startAnswerTimeSec, "initAnswerQuestion", () )
		selfEntity.endAnswerTimer = selfEntity.addTimerCallBackForScript( self.startAnswerTimeSec + self.totalAnswerTimeSec, "endAnswerQuestion", () )
		
	def getAnswerData( self ):
		return answerDatas
	
	def getAnswer( self, questionID):
		return answerDatas.get(questionID).get("answer",Const.MAGIC_MAZE_ANSWER_OPTION_LIST[0])
		
	def getDescription( self, questionID):
		return answerDatas.get(questionID).get("questionDes","")
		
	def getOption(self, questionID):
		options = []
		answerData = answerDatas.get(questionID)
		for key in Const.MAGIC_MAZE_ANSWER_OPTION_LIST:
			option = answerData.get(key, "")
			if option == "":
				break
			options.append(option)
		return options
		
	def initAnswerCountDown( self, selfEntity):
		answerData = self.getAnswerData()
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				player.client.CLIENT_StartMagicMazeQuest(self.totalAnswerTimeSec, self.questionCount)
		
	def initAnswerQuestion(self, selfEntity):
		answerData = self.getAnswerData()
		selfEntity.startAnswerTime = time.time()
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				questionList = random.sample(answerData.keys(),self.questionCount)
				selfEntity.playerQuestionInfo[player.playerDBID] = {}
				selfEntity.playerQuestionInfo[player.playerDBID]["playerName"] = player.playerName
				selfEntity.playerQuestionInfo[player.playerDBID]["profession"] = player.getProfession()
				selfEntity.playerQuestionInfo[player.playerDBID]["questionList"] = questionList
				selfEntity.playerQuestionInfo[player.playerDBID]["playerMB"] = player.base
				selfEntity.playerQuestionInfo[player.playerDBID]["rightAnswerCount"] = 0
				selfEntity.playerQuestionInfo[player.playerDBID]["endTime"] = selfEntity.startAnswerTime + self.totalAnswerTimeSec
				DEBUG_MSG("playerDBID is %s, endTime is %s, startAnswerTime is %s"%(player.playerDBID,selfEntity.playerQuestionInfo[player.playerDBID]["endTime"],selfEntity.startAnswerTime))
				self.sendRandomQuestionToClient( selfEntity, player, player.playerDBID)
		
	def endAnswerQuestion(self, selfEntity):
		selfEntity.popTimer( selfEntity.startCountDownTimer )
		selfEntity.popTimer( selfEntity.startAnswerTimer )
		selfEntity.popTimer( selfEntity.endAnswerTimer )
		allRightPlayerCount = 0
		goodPlayerID = 0
		results = self.calculateResults(selfEntity, True)
		goodPlayerInfo = results[0]
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				player.client.CLIENT_MagicMazeAnswerQuestionEnd(json.dumps(results))
				rightAnswerCount = selfEntity.playerQuestionInfo[player.playerDBID]["rightAnswerCount"]
				endTime = selfEntity.playerQuestionInfo[player.playerDBID]["endTime"]
				allRightPlayerCount += rightAnswerCount
				if selfEntity.playerQuestionInfo[player.playerDBID]["playerName"] == goodPlayerInfo["playerName"] and rightAnswerCount == goodPlayerInfo["right"]:
					goodPlayerID = playerCell.id
					
					
		totalRewardCount = 0
		for rewardCount in self.rewardCountList:
			totalRewardCount += rewardCount
		
		teamRate = allRightPlayerCount / (self.questionCount * max(len(selfEntity._spaceRoles), 1))
		if teamRate == 1.0:
			self.rewardTeam(selfEntity,self.perfectTeamReward)
		elif teamRate >= Const.MAGIC_MAZE_ANSWER_GOOD_RATE:
			self.rewardTeam(selfEntity,self.goodTeamReward)
		
		if allRightPlayerCount != 0:
			self.rewardPerson(selfEntity, goodPlayerID, totalRewardCount)
			
		#副本10s后关闭
		selfEntity.popTimer( selfEntity.lifeTimer )
		selfEntity.lifeTimer = 0
		selfEntity.popTimer( selfEntity.lifeNotifyTimer )
		selfEntity.lifeNotifyTimer = 0
			
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( self.closeTimeSec, "closeSpace", () )
		if self.closeTimeSec - Const.SPACE_LIFE_NOTIFY_TIME >= 0:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( self.closeTimeSec - Const.SPACE_LIFE_NOTIFY_TIME, \
																			"showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for playerCell in selfEntity._spaceRoles:
			playerCell.client.ShowSpaceLife( str(self.closeTimeSec * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ) )
			
		selfEntity.playerQuestionInfo = {}
		
	def rewardTeam(self, selfEntity, teamReward):
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				player.client.statusMessage(teamReward["messageID"], "")
		selfEntity.createSpellBox( teamReward["spellboxID"], tuple(Math.Vector3(teamReward["position"])), teamReward["direction"], {} )
		
	def rewardPerson(self, selfEntity, goodPlayerID, totalRewardCount):
		if goodPlayerID != 0:
			goodPlayer = KBEngine.entities.get( goodPlayerID, None )
			if goodPlayer:
				#获取额外奖励，弹出提示信息
				for playerCell in selfEntity._spaceRoles:
					player = KBEngine.entities.get( playerCell.id, None )
					if player:
						player.client.statusMessage(csstatus.HUAN_ZHEN_MI_GONG_ANSWER_QUESTION_GOOD_PLAYER_MSG, goodPlayer.playerName)
				goodPlayer.addPotential(int(totalRewardCount * self.extraPersonRate))
		
	def sendRandomQuestionToClient( self, selfEntity, player, playerDBID):
		questionList = selfEntity.playerQuestionInfo[playerDBID]["questionList"]
		if len(questionList) == 0:
			self.sendQuestionResults(selfEntity)
		currentQuestionID = random.choice(questionList)  #实现随机取题
		questionList.remove(currentQuestionID)
				
		currentAnswer = self.getAnswer( currentQuestionID ) # 当前考题答案
		currentDescription = self.getDescription( currentQuestionID ) # 当前问题的描述
		currentOption = list( self.getOption( currentQuestionID ) )
		
		answer_str = currentOption[Const.MAGIC_MAZE_ANSWER_OPTION_LIST.index(currentAnswer)]
		random.shuffle(currentOption)#实现答案选项的随机
		currentAnswer0 = Const.MAGIC_MAZE_ANSWER_OPTION_LIST[currentOption.index(answer_str)]

		selfEntity.playerQuestionInfo[playerDBID]["currentQuestionID"] = currentQuestionID #保存到答题玩家信息字典中
		selfEntity.playerQuestionInfo[playerDBID]["currentDescription"] = currentDescription
		selfEntity.playerQuestionInfo[playerDBID]["currentOption"] = currentOption
		selfEntity.playerQuestionInfo[playerDBID]["questionList"] = questionList
		selfEntity.playerQuestionInfo[playerDBID]["currentAnswer"] = currentAnswer0 #实现答案调整后的映射
		
		player.client.CLIENT_ReceiveQuestion(currentQuestionID, currentDescription, json.dumps(currentOption))
		
	def playerAnswer( self, selfEntity, player, playerDBID, questionID, answer):
		if playerDBID not in selfEntity.playerQuestionInfo:
			return
			
		if questionID != selfEntity.playerQuestionInfo[playerDBID]["currentQuestionID"]:
			return
		
		questionList = selfEntity.playerQuestionInfo[playerDBID]["questionList"]
		
		if int(answer) != Const.MAGIC_MAZE_ANSWER_OPTION_LIST.index( selfEntity.playerQuestionInfo[playerDBID]["currentAnswer"] ):
			player.client.CLIENT_ReceiveQuestionState(questionID, 0)
		else:
			player.client.CLIENT_ReceiveQuestionState(questionID, 1)
			selfEntity.playerQuestionInfo[playerDBID]["rightAnswerCount"] += 1
			rightAnswerCount = selfEntity.playerQuestionInfo[playerDBID]["rightAnswerCount"]
			player.addPotential(int(self.rewardCountList[rightAnswerCount - 1]))
		
		if len(questionList) == 0:
			selfEntity.playerQuestionInfo[playerDBID]["endTime"] = time.time()
			DEBUG_MSG("playerDBID is %s, endTime is %s"%(playerDBID,selfEntity.playerQuestionInfo[playerDBID]["endTime"]))
		
		finishedPlayerCount = 0
		for playerCell in selfEntity._spaceRoles:
			playerEntity = KBEngine.entities.get( playerCell.id, None )
			if playerEntity:
				playerQuestionList = selfEntity.playerQuestionInfo[playerEntity.playerDBID]["questionList"]
				if len(playerQuestionList) == 0:
					finishedPlayerCount += 1
		if finishedPlayerCount == len(selfEntity._spaceRoles):
			self.endAnswerQuestion(selfEntity)
		else:
			if len(questionList) == 0:
				self.sendQuestionResults(selfEntity)
			else:
				self.selectNextQuestion( selfEntity, player, playerDBID)
		
		
	def selectNextQuestion(self, selfEntity, player, playerDBID):
		self.sendRandomQuestionToClient(selfEntity, player, playerDBID)
		
		
	def calculateResults(self, selfEntity, isEnd):
		results = []
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				questionInfo = selfEntity.playerQuestionInfo[player.playerDBID]
				questionList = questionInfo["questionList"]
				if isEnd or len(questionList) == 0:
					result = {}
					result["playerName"] = questionInfo["playerName"]
					result["profession"] = questionInfo["profession"]
					result["right"] = questionInfo["rightAnswerCount"]
					result["error"] = self.questionCount - questionInfo["rightAnswerCount"]
					result["time"] = int( questionInfo["endTime"] - selfEntity.startAnswerTime )
					DEBUG_MSG("playerDBID is %s, time is %s"%(player.playerDBID,result["time"]))
					results.append(result)
					
		results.sort(key = lambda result:result["time"])
		results.sort(key = lambda result:result["right"],reverse=True)
		return results

	def sendQuestionResults(self, selfEntity):
		results = self.calculateResults(selfEntity, False)
		for playerCell in selfEntity._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				playerQuestionList = selfEntity.playerQuestionInfo[player.playerDBID]["questionList"]
				if len(playerQuestionList) == 0:
					player.client.CLIENT_MagicMazeAnswerQuestionEnd(json.dumps(results))
