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
from AnswerConfig.MagicMazeAcidSeries import Datas as answerDatas

class SpaceCopyMagicMazeChildAcidSeries( SpaceCopyMagicMazeChild ):
	"""
	幻阵迷宫 迷幻丛书
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChild.__init__( self )
		self.count = 0  #计数
		self.currentQuestionID = 0
		self.currentAnswer = []
		self.questionList = []
		self.currentDescription = ""
		self.voiceIDList = []

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyMagicMazeChild.initData( self, configData )
		self.groups = configData["SpaceData"].get( "spawnGroup", "" )
		self.spellBoxScriptID = configData["SpaceData"].get( "spellBoxScriptID", 0 )
		self.npcScriptID = configData["SpaceData"].get( "drawNPCScriptID",0 )
		self.questionCount = configData["SpaceData"].get( "questionCount", 0 )
		self.threeAnswerPools = configData["SpaceData"].get( "threeAnswerPools", "" )
		self.threeBlankBuff = configData["SpaceData"].get( "threeBlankBuff", "" )
		self.fourAnswerPools = configData["SpaceData"].get( "fourAnswerPools", "" )
		self.fourBlankBuff = configData["SpaceData"].get( "fourBlankBuff", "" )
		self.randomBuffID = configData["SpaceData"].get( "randomBuffID", "" )
		self.punishmentBuff = configData["SpaceData"].get( "punishmentBuff", 0 )
		self.sleepyBuff = configData["SpaceData"].get( "sleepyBuff", 0 )
		voiceIDList = configData["SpaceData"].get( "voiceID", "" )
		if voiceIDList:
			self.voiceIDList = voiceIDList.split("|")

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyMagicMazeChild.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.groups, self.spellBoxScriptID, self.npcScriptID, self.questionCount, self.threeAnswerPools, self.threeBlankBuff,\
			self.fourAnswerPools, self.fourBlankBuff, self.randomBuffID, self.punishmentBuff, self.sleepyBuff, self.voiceIDList)
