# -*- coding: utf-8 -*-
#

import csdefine
import csstatus
import ItemFactory
import random
import Const
from KBEDebug import *
import KBEngine
from SmartImport import smartImport
from ConfigObject.Quest.QuestBase.QuestScript import QuestScript

from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader

import Quest.QuestConfigs.LoopQuestGrade as LoopQuestGrade
import Quest.QuestConfigs.LoopQuestRatio as LoopQuestRatio
import Reward.RewardBasicValueData as RewardBase

class QuestScriptLoop( QuestScript ):
	"""
	环任务
	"""

	def __init__(self):
		QuestScript.__init__(self)
		self._type = csdefine.QUEST_TYPE_LOOP
		self._complex = 1							# 任务复杂度
		self._group = ""							# 任务组
		
	def initLoopDatas( self, group, complex ):
		self._group = group
		self._complex = complex

	@property
	def group(self):
		return self._group

	@property
	def complex(self):
		return self._complex
		
	def getQuestDataByTalk( self, player ):
		"""
		点击任务选项后将任务数据发送到客户端以显示任务界面内容
		"""
		talkQuestData = QuestScript.packQuestStream( self, player )		# 环任务需要任务目标
		
		talkQuestData["loopQuestNum"] = player.loopQuest["loopQuestNum"]
		talkQuestData["rewards"] = self.getRewardByTalk( player )
		
		return talkQuestData
		
	def packQuestStream( self, player ):
		"""
		打包任务数据
		"""
		questInfo = QuestScript.packQuestStream( self, player )
		
		questInfo["loopQuestNum"] = player.loopQuest["loopQuestNum"]
		questInfo["rewards"] = self.getRewardByTalk( player )
		return questInfo
		
	def taskCompleteBy( self, player, taskID, params ):
		"""完成任务目标行为"""
		QuestScript.taskCompleteBy( self, player, taskID, params )
		if player.queryQuestStatus( self._id ) == csdefine.QUEST_DONE:
			if self.query("isAutoCommit"):	
				player.commitQuest( self._id )
		
	def tryToReward(self, player, params = {}):
		"""
		必须保证所有奖励都可以成功发放，才发放奖励
		"""
		#1、任务奖励配置可配置在两个地方，a：任务配置中 b:环任务奖励配置表.xlsx中
		#2、任务奖励一般只会配置在上述两个地方中的一个，这是由策划去保证
		if not QuestScript.tryToReward(self, player, params):
			return False
			
		rewards = self.getRewardByAward( player )
		for reward in rewards:
			if not reward.check(player, params):
				return False

		ItemRewardList = []
		ItemList = []
		for reward in rewards:
			if reward.getRewardType() != csdefine.QUEST_REWARD_TYPE_ITEM:
				reward.do(player, params)
			else:
				ItemRewardList.append(reward)
				itemId, amount = reward.getItemIdAndAmount( player )
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemId, amount)
				ItemList.append(itemInst)

		if ItemList:
			if player.addItemListCheck(ItemList) == csstatus.ITEM_GO_ON:
				for reward in ItemRewardList:
					reward.do(player, params)
			else:
				player.sendRemainItemWithMail(ItemList, csdefine.REMAIN_ITEM_QUEST, csdefine.ITEM_ADD_BY_QUEST, self.getTitle())
		return True

	def generalOneReward( self, script, rewardValue ):
		"""
		生成单个任务奖励
		"""
		data = { "param1": str(rewardValue), "param2": "", "param3": "" }
		reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % script)()
		reward.init(data)
		return reward
				
	def getRewardByTalk( self, player ):
		"""
		任务对话获取奖励提示
		"""
		rewards = {}
		num = player.loopQuest["loopQuestNum"] + 1
		loop = int( num / 7 ) + 1								# 任务环数
		index = num % 6 or 6									# 任务序列
		
		#if isFirstTime and not isAbandonQuest:									# 第一次生成需要roll,确不是放弃任务
		player.loopQuest["isRewardMoney"] = True								# 策划需求 奖励都要钱
				
		# 环任务配置了多个阶梯，接任务时任务奖励只能显示 "？？？"。配置相同的数值，就显示 具体的数值
		if  self._id in LoopQuestGrade.Datas and len(LoopQuestGrade.Datas[self._id]) >= 1:
			gradeExpRatio = LoopQuestGrade.Datas[self._id][0]["expRatio"]
			gradeMoneyRatio = LoopQuestGrade.Datas[self._id][0]["moneyRatio"]
			for data in LoopQuestGrade.Datas[self._id]:
				if gradeExpRatio != data["expRatio"]:
					gradeExpRatio = "？？？"
				if gradeMoneyRatio != data["moneyRatio"]:
					gradeMoneyRatio = "？？？"
			
			expRatio, moneyRatio = self.getLoopRewardRadio( player )
			if gradeExpRatio == "？？？":
				exp = gradeExpRatio
			else:
				level = player.getLevel()
				expBase = RewardBase.datas[level]["exp"]
				exp = int(gradeExpRatio *expRatio * expBase)
			rewards.update( { str( csdefine.QUEST_REWARD_TYPE_EXP): str( exp ) } )
				
			if player.loopQuest["isRewardMoney"]:
				if gradeMoneyRatio == "？？？":
					money = gradeMoneyRatio
				else:
					level = player.getLevel()
					moneyBase = RewardBase.datas[level]["money"]
					money = int(gradeMoneyRatio *moneyRatio * moneyBase)
				rewards.update( { str( csdefine.QUEST_REWARD_TYPE_MONEY): str( money ) } )
		return rewards
		
	def getRewardByAward( self, player ):
		"""完成任务，给奖励"""
		rewards = []
		num = player.loopQuest["loopQuestNum"] + 1
		loop = int( num / 7 ) + 1								# 任务环数
		index = num % 6 or 6									# 任务序列
		
		gradeExpRatio, gradeMoneyRatio = self.getGradeReward( player )
		expRatio, moneyRatio = self.getLoopRewardRadio( player )
		
		level = player.getLevel()
		expBase = RewardBase.datas[level]["exp"]
		reward = self.generalOneReward( "QuestRewardExp", int(gradeExpRatio *expRatio * expBase) )
		rewards.append( reward )
		if player.loopQuest["isRewardMoney"]:
			moneyBase = RewardBase.datas[level]["money"]
			reward = self.generalOneReward( "QuestRewardMoney", int( gradeMoneyRatio *moneyRatio * moneyBase) )
			rewards.append( reward )
			
		groupScript = g_QuestLoader.getLoopQuestScript( self._group )
		if groupScript:
			fixReward = groupScript.getFixRewardByLoop( num )
			rewards.extend( fixReward )
		return rewards

	def requirementCheck(self, player):
		"""判断玩家的条件是否满足可接取任务的显示要求"""
		return QuestScript.requirementCheck(self, player) and \
		not player.hasQuestType( csdefine.QUEST_TYPE_LOOP )
				
	
	def getLoopRewardRadio( self, player ):
		"""获得环数相关倍率"""
		num = player.loopQuest["loopQuestNum"] + 1
		loop = int( num / 7 ) + 1								# 任务环数
		index = num % 6 or 6									# 任务序列
		expRatio = 1.0
		moneyRatio = 1.0
		try:
			expRatio = LoopQuestRatio.Datas[loop][index]["QuestRewardExp"][self.complex]		# 奖励经验系数
			moneyRatio = LoopQuestRatio.Datas[loop][index]["QuestRewardMoney"][self.complex]	# 奖励金钱系数
		except:
			ERROR_MSG("LoopQuestRatio find loop(%d), index(%d), quest complex(%d) is error"%(loop,index,self.complex))
		return expRatio, moneyRatio
	
	def getGradeReward( self, player ):
		"""获得对应的档次倍率"""
		if self._id in LoopQuestGrade.Datas:
			grades = LoopQuestGrade.Datas[self._id]
			if len(grades) == 1:						# 只有一个档次阶梯
				return grades[0]["expRatio"], grades[0]["moneyRatio"]
			else:
				qNum = player.loopQuest["taskCompleteNum"]
				for gad in grades:
					if gad["lower"] <= qNum and qNum <= gad["upper"]:
						return gad["expRatio"], gad["moneyRatio"]
		return 1.0, 1.0

	def getGradeScore( self, player ):
		"""获得对应的档次评分"""
		if self._id in LoopQuestGrade.Datas:
			grades = LoopQuestGrade.Datas[self._id]
			if len(grades) == 1:						# 只有一个档次阶梯
				return int(grades[0]["score"])
			else:
				qNum = player.loopQuest["taskCompleteNum"]
				for gad in grades:
					if gad["lower"] <= qNum and qNum <= gad["upper"]:
						return int(gad["score"])
		return 1
		
	def getGradeRewardIDAndBuff( self, player ):
		"""获取对应的buff和奖励ID"""
		if self._id in LoopQuestGrade.Datas:
			grades = LoopQuestGrade.Datas[self._id]
			if len(grades) == 1:
				return grades[0]["rewardID"], grades[0]["buff"]
			else:
				qNum = player.loopQuest["taskCompleteNum"]
				for gad in grades:
					if gad["lower"] <= qNum and qNum <= gad["upper"]:
						return gad["rewardID"], gad["buff"]
		return "", ""
		
	def getAllGradeReward( self ):
		"""获取所有的档次倍率"""
		if self._id in LoopQuestGrade.Datas:
			return LoopQuestGrade.Datas[self._id]
		return None
	
	def afterClientAccepted(self, player, params = {}):
		"""接了任务之后（通知了客户端），部分任务需要做处理"""
		player.loopQuest["isAbandonQuest"] = False
		player.loopQuest["taskCompleteNum"] = 0
		
		if player.queryQuestStatus( self._id ) == csdefine.QUEST_DONE:
			if self.query("isAutoCommit"):	
				player.commitQuest( self._id )
		
	def afterClientAbandon(self, player, params = {}):
		"""放弃任务之后（通知了客户端），部分任务需要做处理"""
		player.loopQuest["isAbandonQuest"] = True
		
	def afterClientCommitted(self, player, params = {}):
		"""提交任务之后（通知了客户端），部分任务需要做处理"""
		if player.loopQuest["loopQuestList"]:						# 移除已完成任务
			popQuestID = player.loopQuest["loopQuestList"].pop(0)
			player.loopQuest["loopQuestNum"] += 1
			player.loopQuestProgress += 1
			KBEngine.globalData["RingTaskSpaceMgr"].setCurrentProgress( str(player.playerDBID), player.loopQuestProgress )
			spaceEntity = player.getCurrentSpace()
			if spaceEntity:
				spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "CommitLoopQuest", "")
			
		if player.loopQuest["loopQuestList"]:						# 如果有下一个任务 且 自动接任务，直接接受任务
			questID = player.loopQuest["loopQuestList"][0]
			questScript = g_QuestLoader.getScript(questID)
			if questScript.query("isAutoAccept"):					
				player.acceptQuest( questID )
		else:														# 完成了所有的环任务
			questScriptGroup = g_QuestLoader.getLoopQuestScript(self.group)
			questScriptGroup.finishLoopQuest( player )
			player.loopQuestProgress = 0
			KBEngine.globalData["RingTaskSpaceMgr"].setCurrentProgress( str(player.playerDBID), player.loopQuestProgress )