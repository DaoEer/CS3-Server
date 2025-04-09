# -*- coding: utf-8 -*-
#

import csdefine
import random
import Const
from KBEDebug import *
from SmartImport import smartImport
from ConfigObject.Quest.QuestBase.QuestScript import QuestScript
from ConfigObject.Quest.QuestBase.QuestLoader import g_QuestLoader

from Quest.QuestConfigs.TongDailyQuestReward import Datas as dailyQuestReward
import Reward.RewardBasicValueData as RewardBase

class QuestScriptTongDaily( QuestScript ):
	"""
	帮会 日常任务
	"""

	def __init__(self):
		QuestScript.__init__(self)
		self._type = csdefine.QUEST_TYPE_DAILY
		
	def getQuestDataByTalk( self, player ):
		"""
		点击任务选项后将任务数据发送到客户端以显示任务界面内容
		"""
		talkQuestData = QuestScript.packQuestStream( self, player )		# 环任务需要任务目标
		talkQuestData["rewards"] = self.getRewardByTalk( player )
		return talkQuestData
		
	def packQuestStream( self, player ):
		"""
		打包任务数据
		"""
		questInfo = QuestScript.packQuestStream( self, player )
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
		#1、任务奖励配置可配置在两个地方，a：任务配置中 b:帮会任务奖励配置（TongDailyQuestRewards）.xlsx
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
				itemId = reward.getItemId()
				amount = reward.getAmount()
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemId, amount)
				ItemList.append(itemInst)

		if ItemList:
			if player.addItemListCheck(ItemList) == csstatus.ITEM_GO_ON:
				for reward in ItemRewardList:
					reward.do(player, params)
			else:
				player.sendRemainItemWithMail(ItemList, csdefine.REMAIN_ITEM_QUEST, csdefine.ITEM_ADD_BY_QUEST, self.getTitle())
		return True

	def getRewardByTalk( self, player ):
		"""
		任务对话获取奖励提示
		"""
		rewards = {}
		if self._rewards:					# 如果策划配置了普通任务的奖励，就给普通任务的
			for reward in self._rewards:
				rewards.update( reward.sendClientData( player ) )
			return rewards
		
		if self._id in dailyQuestReward:
			contribute = dailyQuestReward[self._id][0]["contribute"]
			moneyRatio = dailyQuestReward[self._id][0]["moneyRatio"]
			barracksExp = dailyQuestReward[self._id][0]["barracksExp"]
			xiuwei = dailyQuestReward[self._id][0]["xiuwei"]
			for qData in dailyQuestReward[self._id]:								# 如果给的配置数值都一样，就用配置的数值；否则用？？？显示
				if contribute != qData["contribute"] and contribute:				
					contribute = "？？？"
				if moneyRatio != qData["moneyRatio"] and moneyRatio:
					moneyRatio = "？？？"
				if barracksExp != qData["barracksExp"] and barracksExp:
					barracksExp = "？？？"
				if xiuwei != qData["xiuwei"] and xiuwei:
					xiuwei = "？？？"
				
			if contribute:
				rewards.update( { str( csdefine.QUEST_REWARD_TYPE_CONTRIBUTE): str( contribute ) } )
			if moneyRatio:
				rewards.update( { str( csdefine.QUEST_REWARD_TYPE_TONG_MONEY): str( moneyRatio ) } )
			if barracksExp:
				rewards.update( { str( csdefine.QUEST_REWARD_TYPE_BARRACKS_EXP): str( barracksExp ) })
			if xiuwei:
				rewards.update( { str( csdefine.QUEST_REWARD_TYPE_XIUWEI): str( xiuwei ) })
			
		return rewards
		
	def getRewardByAward( self, player ):
		"""完成任务，给奖励"""
		rewards = []
		contribute, money, barracksExp, xiuweiRatio, rewardID, buff = self.getGradeReward( player )
		
		if contribute:
			reward = self.generalOneReward( "QuestRewardTongContribute", int(contribute) )
			rewards.append( reward )
		
		if money:
			level = player.getLevel()
			reward = self.generalOneReward( "QuestRewardTongMoney", money )
			rewards.append( reward )
		
		#养兵经验
		if int(barracksExp) > 0:
			reward = self.generalOneReward( "QuestRewardBarracksExp", int(barracksExp) )
			rewards.append(reward)
		
		#修为
		if float(xiuweiRatio) > 0:
			reward = self.generalOneReward( "QuestRewardXiuwei", "0", str( xiuweiRatio ) )
			rewards.append( reward )
		
		return rewards
				
	def generalOneReward( self, script, *args ):
		"""
		生成单个任务奖励
		"""
		data = {}
		if len(args) > 0:
			for index, arg in enumerate(args): data["param{}".format(index+1)] = arg
		reward = smartImport("ConfigObject.Quest.QuestRewards:%s" % script)()
		reward.init(data)
		return reward
		
	def getGradeReward( self, player ):
		"""获得对应的奖励"""
		if self._id in dailyQuestReward:
			grade = player.dailyQuest.taskCompleteNum
			for qData in dailyQuestReward[self._id]:
				if qData["lower"] <= grade and qData["upper"] >= grade:
					return qData["contribute"], qData["moneyRatio"], qData.get("barracksExp", 0), qData.get("xiuwei", 0), qData.get("rewardID", ""), qData.get("buff", "")
		return 0, 0, 0, 0, "", ""
		
	def getGradeScore( self, player ):
		"""获得对应的档次评分"""
		if self._id in dailyQuestReward:
			grade = player.dailyQuest.taskCompleteNum
			for qData in dailyQuestReward[self._id]:
				if qData["lower"] <= grade and qData["upper"] >= grade:
					return int(qData.get("score", 0))
		return 0
		
	def afterClientAccepted(self, player, params = {}):
		"""接了任务之后（通知了客户端），部分任务需要做处理"""
		pass
		
	def afterClientCommitted(self, player, params = {}):
		"""有几率获得第二帮会任务"""
		if player.tongMB:
			player.tongMB.onDailyTongQuestFinish( player.playerDBID )
	
	def committedBy(self, player, params = {}):
		QuestScript.committedBy(self, player, params)
		player.dailyQuest.onFinishQuest(self.id)
		
	def abandonBy(self, player, params = {}):
		QuestScript.abandonBy(self, player, params)
		player.dailyQuest.onAbandonQuest(self.id)
