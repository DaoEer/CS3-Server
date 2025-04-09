# -*- coding: utf-8 -*-
#

import random
import math

import csdefine
import Const
from KBEDebug import *
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader
from SmartImport import smartImport

class QuestScriptLoopGroup():
	"""
	环任务组
	6个任务构成1环，3环构成一轮
	"""
	def __init__(self):
		self._questLevelSection = ""					# 等级段35-39
		self._quests = {  1:[], 2:[], 3:[] }		# 环任务{{ complex: [questID...] }，....}
		self._fixRewardsByLoop = { 6 : [], 12 : [], 18 : [], 24 : [], 30 : [], 36 : [],  42 : [], 48 : [], 54 : [] }
		self._fixRewardsByLun = { 18:0, 36:0, 54:0}		# 轮任务奖励（为了完成一轮回到环任务NPC处）

	def initFromConfig(self, data):
		self._questLevelSection = data["levelSection"]
		
		#加载任务ID
		for complex, questIDs in data["quests"].items():
			for id in questIDs:
				questScript = g_QuestLoader.getScript( id )
				questScript.initLoopDatas( self._questLevelSection, int( complex ) )
				if int(complex) in self._quests.keys():
					self._quests[ int(complex) ].append( id )
				
		self._fixRewardsByLun[18] = data["firstLunQuestID"]
		self._fixRewardsByLun[36] = data["secondLunQuestID"]
		self._fixRewardsByLun[54] = data["thirdLunQuestID"]
	
		#加载任务奖励
		for rewardData in data["firstLunOneLoopRewards"]:
			reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
			reward.init(rewardData)
			self._fixRewardsByLoop[6].append(reward)
			
		for rewardData in data["firstLunTwoLoopRewards"]:
			reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
			reward.init(rewardData)
			self._fixRewardsByLoop[12].append(reward)

		for rewardData in data["firstLunThreeLoopRewards"]:
			reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
			reward.init(rewardData)
			self._fixRewardsByLoop[18].append(reward)
			
		for rewardData in data["secondLunOneLoopRewards"]:
			reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
			reward.init(rewardData)
			self._fixRewardsByLoop[24].append(reward)
			
		for rewardData in data["secondLunTwoLoopRewards"]:
			reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
			reward.init(rewardData)
			self._fixRewardsByLoop[30].append(reward)

		for rewardData in data["secondLunThreeLoopRewards"]:
			reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
			reward.init(rewardData)
			self._fixRewardsByLoop[36].append(reward)
			
		for rewardData in data["thirdLunOneLoopRewards"]:
			reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
			reward.init(rewardData)
			self._fixRewardsByLoop[42].append(reward)
			
		for rewardData in data["thirdLunTwoLoopRewards"]:
			reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
			reward.init(rewardData)
			self._fixRewardsByLoop[48].append(reward)

		for rewardData in data["thirdLunThreeLoopRewards"]:
			reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % rewardData["script"])()
			reward.init(rewardData)
			self._fixRewardsByLoop[54].append(reward)
			
	def getFixRewardByLoop( self, num ):
		"""获取每环（轮）奖励"""
		return self._fixRewardsByLoop.get( num, [] )
		
	def getRandomLoopQuest( self, player ):
		"""随机获取环任务"""
		questIDs = []
		tempquests = {  1:[], 2:[], 3:[] }
		for index in range( 1, 4):
			for questID in self._quests[ index ]:
				if player.questLogger.query( questID ):continue		# 如果玩家已经完成了，则不随机该任务
				quest = g_QuestLoader.getScript( questID )
				if not quest.requirementCheck( player ):continue	# 如果不满足任务条件，则不随机该任务
				tempquests[ index ].append( questID )				# 先筛选出可以随机的

		quests = dict( tempquests )									#如果tempquests数目不够的话 后面要再从tempquests里面取
		for ringNum in range( Const.LOOP_QUEST_RING_NUM ):
			aRingIDs = []
			tempOrdinaryIDs = []
			for index in Const.MUST_LOOP_QUEST_TYPE:
				if quests[ index ]:
					tempMustID = random.choice( quests[ index ] )
					quests[index] = [i for i in quests[index] if i != tempMustID]
					aRingIDs.append( tempMustID )

				elif tempquests[ index ]:
					tempMustID = random.choice( tempquests[ index ] )		#不够的话还是要取之前的重复取
					aRingIDs.append( tempMustID )

			ordinaryNum = int( Const.QUEST_OF_NUM_LOOP/Const.LOOP_QUEST_RING_NUM - len( aRingIDs ) ) 		#要多少个普通任务

			if len( quests[ 3 ] ) >= ordinaryNum:														#以下是取普通任务
				tempOrdinaryIDs = random.sample( quests[ 3 ], ordinaryNum )
				quests[ 3 ] = [i for i in quests[ 3 ] if i not in tempOrdinaryIDs]
				aRingIDs.extend( tempOrdinaryIDs )

			elif len( tempquests[ 3 ] ) >= ordinaryNum - len( quests[ 3 ] ):
				tempOrdinaryIDs.extend( random.sample( tempquests[ 3 ] , ordinaryNum - len( quests[ 3 ] ) ) )
				tempOrdinaryIDs.extend( quests[ 3 ] )
				aRingIDs.extend( tempOrdinaryIDs )
				
			questIDs.extend( random.sample(aRingIDs , len(aRingIDs) ) )
		return 	questIDs
				
	def finishLoopQuest( self, player ):
		"""完成一轮任务"""
		num = player.loopQuest["loopQuestNum"]
		if num in self._fixRewardsByLun:
			player.acceptQuest( self._fixRewardsByLun[num] )