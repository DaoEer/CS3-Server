# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import KBEngine
import random
import KBEMath
import Const
import Functions
import csdefine
import copy
from AnswerConfig.CangGongDianAnswer import Datas as answerDatas

class SpaceCopyCangGongDian( SpaceCopy ):
	"""
	藏功殿
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.direction = Math.Vector3(0, 0, 0)
		self.currentQuestionID = 1		# 当前题编号
		self.count = 0

	def initSpaceData( self, scrollScriptID, wordScriptID, spawnGroup, randomBuffIDList, promptBuff, voiceID, delayTime, nextTime, wordNum, monsterIDList, totalQuestionsNum ):
		"""
		初始化数据
		"""
		self.scrollScriptID = scrollScriptID		# 书卷的SpellBox的ScriptID以及对应的位置
		self.wordScriptID = wordScriptID			# 字的SpellBox的SCriptID
		self.spawnGroup = spawnGroup				# 批次
		self.randomBuffIDList = randomBuffIDList	# 随机Buff池
		self.promptBuff = promptBuff				# 提示Buff
		self.voiceID = voiceID						# 回答错误的语音提示
		self.delayTime = delayTime					# 延时销毁场上的entity
		self.nextTime = nextTime					# 延时开始下一道答题
		self.wordNum = wordNum						# 字数
		self.monsterIDList = monsterIDList			# 怪物的ScriptID列表
		self.totalQuestionsNum = totalQuestionsNum	#总题数

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

	def refreshAnswerBook( self, questionID ):
		"""
		刷新答题书卷Entity
		"""
		tempSubscript = 0
		entityScriptInfo = self.scrollScriptID.split("|")
		promptBuff = self.promptBuff.split("|")
		answerList = self.getAnswerCfg( questionID )
		for onePosInfo in entityScriptInfo:
			tempInfo = onePosInfo.split(":")
			posStr = Functions.vector3TypeConvert( tempInfo[1] )
			entity = self.createSpellBox( str(tempInfo[0]), KBEMath.Unreal2KBEnginePosition( posStr ), self.direction, {} )
			if tempSubscript < len(answerList):
				entity.addBuff( entity, int(promptBuff[tempSubscript]) )
				tempSubscript +=1
		self.createspawnGroupEntity( questionID )

	def createspawnGroupEntity( self, questionID ):
		"""
		生成某些批次的entity
		"""
		spawnGroups = self.spawnGroup.split("|")
		groups = random.sample( spawnGroups, self.wordNum )
		for group in groups:
			self.spawnGroupEntity( int(group), "", 0 )

		subscript = 0
		groupIdList = self.getEntityRecord( str(self.wordScriptID) )
		answerList = self.getAnswerCfg( questionID )
		specifiedIDs = random.sample( groupIdList, len(answerList) )
		for specifiedID in specifiedIDs:
			entity = KBEngine.entities.get( specifiedID )
			if not entity:
				continue
			if subscript < len(answerList):
				entity.addBuff( entity, int(answerList[subscript]) )
				subscript +=1
				groupIdList.remove( specifiedID )

		otherSub = 0
		randomBuffIDList = self.randomBuffIDList.split("|")
		randomBuffID = random.sample( randomBuffIDList, len(groupIdList) )
		for randomID in groupIdList:
			otherEntity = KBEngine.entities.get( randomID )
			if not otherEntity:
				continue
			if otherSub < len(randomBuffID):
				otherEntity.addBuff( otherEntity, int(randomBuffID[otherSub]) )
				otherSub += 1

		if self.currentQuestionID == 2:
			entityList = random.sample( specifiedIDs, 1 )
			self.creatMonsterEntity( entityList, 0 )
		elif self.currentQuestionID == 3:
			entityList = random.sample( specifiedIDs, 1 )
			self.creatMonsterEntity( specifiedIDs, 1 )
		elif self.currentQuestionID == 4:
			entityList = random.sample( specifiedIDs, 1 )
			self.creatMonsterEntity( entityList, 2 )

	def creatMonsterEntity( self, entityList, index ):
		"""
		创建怪物
		"""
		for entityID in entityList:
			entity = KBEngine.entities.get( entityID )
			if not entity:
				continue
			self.createEntityByScriptID( self.monsterIDList[index], entity.position, self.direction, {} )

	def destroyBatchEntity( self ):
		"""
		销毁场上所有的SpellBox
		"""
		record = copy.deepcopy(self.getAllEntityMailBoxRecord())
		for scriptID, entityList in record.items():
			for entity in entityList:
				if entity.getEntityFlag() == csdefine.ENTITY_FLAG_SPELL:
					entity.destroySelf()

	def onStartFreshEntity( self ):
		"""
		开始刷新全场的题目
		"""
		self.refreshAnswerBook( self.currentQuestionID )

	def onStartAnswerQuestions( self ):
		"""
		开始答题
		"""
		self.currentDescription = self.getDescriptionCfg(self.currentQuestionID)			# 当前考题描述
		for playerCell in self._spaceRoles:
			player = KBEngine.entities.get( playerCell.id, None )
			if player:
				player.showMessagePlaySound( self.currentDescription )						# 半身像播放问题描述语音
				player.client.CLIENT_DisplayProblemDescription( self.currentDescription )	# 通知右方界面提示问题描述
		self.onStartFreshEntity()

	def onCalculateResults( self ):
		"""
		较对结果
		"""
		self.count += 1
		if self.count == len( self.getAnswerCfg(self.currentQuestionID) ):
			self.addTimerCallBack( self.delayTime, "destroyBatchEntity", () )
			if self.questionAnswerDict == self.getAnswerDatas( self.currentQuestionID ):
				self.currentQuestionID += 1
				for playerCell in self._spaceRoles:
					self.getScript().onConditionChange( self, "", self.id, "true", "" )
			else:
				for playerCell in self._spaceRoles:
					playerCell.showMessagePlaySound( self.voiceID )	
			if self.currentQuestionID > self.totalQuestionsNum:
				self.getScript().onConditionChange( self, "", self.id, "end", "" )
				for playerCell in self._spaceRoles:
					playerCell.client.CloseProblemDescription()
				return
			self.getScript().onConditionChange( self, "", self.id, "PlayAction", "" )
			self.addTimerCallBack( self.nextTime, "selectNextTopic", () )

	def selectNextTopic( self ):
		"""
		开始下一题
		"""
		self.count = 0
		self.onStartAnswerQuestions()
		self.questionAnswerDict = {}