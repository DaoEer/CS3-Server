# -*- coding: utf-8 -*-

from SpaceCopyMagicMaze import SpaceCopyMagicMaze
import KBEDebug
import Math
import KBEngine
import random
import KBEMath
import Const
import Functions
import csdefine
import copy
from AnswerConfig.MagicMazeAcidSeries import Datas as answerDatas

class SpaceCopyMagicMazeChildAcidSeries( SpaceCopyMagicMaze ):
	"""
	幻阵迷宫 迷幻丛书
	"""
	def __init__( self ):
		SpaceCopyMagicMaze.__init__( self )
		self.direction = Math.Vector3(0, 0, 0)
		self.count = 0
		self.questionNum = 1
		self.initChooseTopic()

	def initSpaceData( self, groups, spellBoxScriptID, npcScriptID, questionCount, threeAnswerPools, threeBlankBuff, fourAnswerPools, fourBlankBuff, randomBuffID, punishmentBuff, sleepyBuff, voiceIDList ):
		"""
		初始化数据
		"""
		self.groups = groups
		self.spellBoxScriptID = spellBoxScriptID
		self.npcScriptID = npcScriptID
		self.questionCount = questionCount
		self.threeAnswerPools = threeAnswerPools
		self.threeBlankBuff = threeBlankBuff
		self.fourAnswerPools = fourAnswerPools
		self.fourBlankBuff = fourBlankBuff
		self.randomBuffID = randomBuffID
		self.punishmentBuff = punishmentBuff
		self.sleepyBuff = sleepyBuff
		self.voiceIDList = voiceIDList

	def getAnswerDatas( self, questionID ):
		"""
		获取答案字典
		"""
		answerDict = {}
		if answerDatas.get(questionID).get( "answer" ):
			answerData = answerDatas.get(questionID).get("answer").split("|")
			for data in answerData:
				answer = data.split(":")
				answerDict[answer[0]] = answer[1]

		return answerDict

	def getAnswerCfg( self, questionID ):
		"""
		获取答案
		"""
		answerList = []
		if answerDatas.get(questionID).get( "answer" ):
			answerBuff = answerDatas.get(questionID).get("answer").split("|")
			for data in answerBuff:
				answer = data.split(":")
				answerList.append(answer[1])
		return answerList

	def getDescriptionCfg( self, questionID ):
		"""
		获取问题描述的语音ID
		"""
		return answerDatas.get( questionID ).get( "questionDes", "" )

	def initChooseTopic( self ):
		"""
		随机选择一组题目
		"""
		self.questionList = random.sample( answerDatas.keys(), self.questionCount )
		self.currentQuestionID = random.choice(self.questionList)
		self.questionList.remove(self.currentQuestionID)
		
	def refreshAssignEntity( self, questionID ):
		"""
		刷新空白书卷上的entity
		"""
		tempSubscript = 0
		answerList = self.getAnswerCfg( questionID )
		if len(answerList) == Const.MAGIC_MAZE_THREE:
			entityScriptInfo = self.threeAnswerPools.split("|")
			threeBlankBuff = self.threeBlankBuff.split("|")
			for onePosInfo in entityScriptInfo:
				tempInfo = onePosInfo.split(":")
				posStr = Functions.vector3TypeConvert( tempInfo[1] )
				entity = self.createSpellBox( str(tempInfo[0]), KBEMath.Unreal2KBEnginePosition( posStr ), self.direction, {} )
				if tempSubscript < len(answerList):
					entity.addBuff( entity, int(threeBlankBuff[tempSubscript]) )
					tempSubscript +=1
		else:
			entityScriptInfo = self.fourAnswerPools.split("|")
			fourBlankBuff = self.fourBlankBuff.split("|")
			for onePosInfo in entityScriptInfo:
				tempInfo = onePosInfo.split(":")
				posStr = Functions.vector3TypeConvert( tempInfo[1] )
				entity = self.createSpellBox( str(tempInfo[0]), KBEMath.Unreal2KBEnginePosition( posStr ), self.direction, {} )
				if tempSubscript < len(answerList):
					entity.addBuff( entity, int(fourBlankBuff[tempSubscript]) )
					tempSubscript +=1
		self.refreshBatchEntity(questionID)

	def refreshBatchEntity( self, questionID ):
		"""
		刷新刷某些批次的entity
		"""
		groups = self.groups.split("|")
		for group in groups:
			self.spawnGroupEntity( int(group), "", 0 )
		subscript = 0
		idList = self.getEntityRecord( str(self.spellBoxScriptID) )
		answerList = self.getAnswerCfg( questionID )
		templist = list(idList)
		specifiedIDs = random.sample( idList, len(answerList) )
		for specifiedID in specifiedIDs:
			entity = KBEngine.entities.get( specifiedID )
			if not entity:
				continue
			if subscript < len(answerList):
				entity.addBuff( entity, int(answerList[subscript]) )
				subscript +=1
				templist.remove( specifiedID )
		otherSub = 0
		randomBuffIDList = self.randomBuffID.split("|")
		randomBuffID = random.sample( randomBuffIDList, len(templist) )
		for randomID in templist:
			otherEntity = KBEngine.entities.get( randomID )
			if not otherEntity:
				continue
			if otherSub < len(randomBuffID):
				otherEntity.addBuff( otherEntity, int(randomBuffID[otherSub]) )
				otherSub += 1

	def destroyBatchEntity( self ):
		"""
		销毁存活的某批次某scriptID的entity
		"""
		record = copy.deepcopy(self.getAllEntityMailBoxRecord())
		for scriptID, entityList in record.items():
			for entity in entityList:
				if entity.getEntityFlag() != csdefine.ENTITY_FLAG_SPELL:
					continue
				entity.destroySelf()

	def sendRandomQuestion( self ):
		"""
		从一组题目随机选择一题开始答题
		"""
		if len(self.questionList) == 0:
			return
		self.currentAnswer = self.getAnswerCfg(self.currentQuestionID)	#当前考题答案
		self.currentDescription = self.getDescriptionCfg(self.currentQuestionID)	#当前考题描述
		self.onPlayVoice( self.currentDescription )
		for playerCell in self._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				player.client.CLIENT_onProblemDescription(self.currentDescription, self.questionNum )
		
	def onStartFreshEntity( self ):
		"""
		开始刷新全场的题目
		"""
		self.refreshAssignEntity( self.currentQuestionID )
		
	def calculateResults( self ):
		"""
		较对结果
		"""
		self.count += 1
		if self.count == len(self.getAnswerCfg( self.currentQuestionID )):
			self.addTimerCallBack( 1.0, "destroyBatchEntity", () )
			if self.playerQuestionAnswer == self.getAnswerDatas( self.currentQuestionID ):
				self.onPlayVoice( self.voiceIDList[0] )
				self.getScript().onConditionChange( self, "", self.id, "ANSWER", "" )
				for playerCell in self._spaceRoles:
					player = KBEngine.entities.get( playerCell.id, None )
					if player:
						player.removeAllBuff()
						player.client.CLIENT_onCalculateResults(1)
			else:
				self.onPlayVoice( self.voiceIDList[1] )
				for playerCell in self._spaceRoles:
					player = KBEngine.entities.get( playerCell.id, None )
					if player:
						player.removeAllBuff()
						player.addBuff( player, int(self.punishmentBuff) )
						player.client.CLIENT_onCalculateResults(0)
			self.getScript().onConditionChange( self, "", self.id, "PLAYACTION", "" )
			self.addTimerCallBack( 5.0, "selectNextTopic", () )
			self.count = 0

	def selectNextTopic( self ):
		"""
		开始下一题
		"""
		self.questionNum += 1
		self.currentQuestionID = random.choice(self.questionList)
		self.questionList.remove(self.currentQuestionID)
		self.sendRandomQuestion()
		self.onStartFreshEntity()
		self.playerQuestionAnswer = {}

	def sandmanCollisionPunishment( self, playerCell ):
		"""
		瞌睡虫碰撞惩罚
		"""
		positionIndex = 0
		for position, buffID in self.playerMetSandmanDict.items():
			if len(playerCell.findBuffsByBuffID(int(buffID))):
				playerCell.removeBuffByID(int(buffID))
				entity = self.createSpellBox( str(self.spellBoxScriptID), position, self.direction, {} )
				entity.addBuff(entity, int(buffID))
				positionIndex = position
				break
		if positionIndex in self.playerMetSandmanDict:
			self.playerMetSandmanDict.pop(positionIndex)
		playerCell.addBuff( playerCell, int(self.sleepyBuff) )

	def onPlayVoice( self, voiceID ):
		"""
		播放语音提示
		"""
		idList = self.getEntityRecord(str(self.npcScriptID))
		npcEntity = KBEngine.entities.get( idList[0] )
		if not npcEntity:
			return
		npcEntity.allClients.CLIENT_BubbleDialogue( voiceID )

