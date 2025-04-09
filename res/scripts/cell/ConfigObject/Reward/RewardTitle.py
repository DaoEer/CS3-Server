# -*- coding- : utf-8 -*-

import KBEngine
import Define
import csdefine
from ConfigObject.Reward.RewardBase import RewardBase


class RewardTitle(RewardBase.RewardBase):
	"""
	称号奖励类
	"""
	def __init__(self, configSection):
		self._titleID = configSection["goodsid"]

	def addReward(self, rewarderID, reason):
		"""
		增加称号
		"""
		rewarder = KBEngine.entities.get(rewarderID, None)
		if rewarder:
			rewarder.addTitle(int(self._titleID))  #需要做一个 str 到 int 的转换 两个配置的 数据类型不一致