# -*- coding- : utf-8 -*-
import csdefine
from ConfigObject.Reward.RewardBase import RewardBase

class RewardNothing( RewardBase.RewardBase ):
	"""
	奖励空类型
	"""
	def __init__( self, configSection ):
		pass
	
	
	def addReward( self, rewarderID, reason ):
		pass