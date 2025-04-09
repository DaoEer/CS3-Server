# encoding=utf8
"""
	desc	任务奖励给与顺序类
	file	QuestRewardSequence.py
	author  bqq6290
	ref	 http://172.16.2.227/browse/CST-3969
"""

import KBEDebug
import csdefine
import csstatus
import ItemFactory
import  ConfigObject.Quest.QuestRewards as QuestRewards
from Reward import RewardSequenceData

class QuestRewardSequence(object):
	"""
		奖励配置格式 = {
			奖励类别名称:优先级
		}
		奖励类别名称是一个字符串
		优先级是一个数字，数值越大的奖励越在后面给与
	"""
	instance = None
	def __new__(clazz):
		"""单例类Singleton太难用了"""
		if not clazz.instance:
			clazz.instance = object.__new__(clazz)
			clazz.instance.init(RewardSequenceData.datas)
		return clazz.instance

	def init(self,prioritiesConfig):
		self.priority_map = {}
		self.loadRewardConfig(
			prioritiesConfig
		)

	def loadRewardConfig(self,config):
		"""加载奖励的优先级设置"""
		for rewardClassName,priority in config.items():
			rewardClass = getattr(QuestRewards,rewardClassName,None)
			if rewardClass:
				self.setRewardPriority(rewardClass,priority)
			else:
				KBEDebug.ERROR_MSG("reward class %s not found!!!"%rewardClassName)
				assert False

	def setRewardPriority(self,rewardClass,priority):
		"""给某一个奖励类设置一个优先级"""
		self.priority_map[id(rewardClass)] = int(priority)
	
	def getRewardPriority(self,rewardClass):
		"""获得某个奖励类的优先级"""
		try:
			return self.priority_map[id(rewardClass)]
		except KeyError:
			return 1

	def rewardPriorityGetter(self,rewardInstance):
		"""奖励实体的优先级计算函数"""
		return self.getRewardPriority(type(rewardInstance))

	def doGiveReward(self,player,rewards,questScript,params):
		"""
			按照自定义奖励顺序给与玩家奖励
			参数:
			@player	 玩家
			@rewards	多个奖励实例
			@params	 奖励上下文
			@exposed	供外部使用
		"""
		rewardList = sorted(rewards,key = self.rewardPriorityGetter)
		ItemRewardList=[]
		ItemList=[]
		for reward in rewardList:
			if reward.getRewardType() != csdefine.QUEST_REWARD_TYPE_ITEM:
				reward.do(player, params)
			else:
				ItemRewardList.append(reward)
				itemId, amount = reward.getItemIdAndAmount(player)
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemId, amount)
				ItemList.append(itemInst)

		if player.addItemListCheck(ItemList) == csstatus.ITEM_GO_ON:
			for reward in ItemRewardList:
				reward.do(player, params)
		else:
			player.sendRemainItemWithMail(ItemList, csdefine.REMAIN_ITEM_QUEST, csdefine.ITEM_ADD_BY_QUEST,questScript.getTitle())
