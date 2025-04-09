# -*- coding- : utf-8 -*-

import KBEngine
import Define
import csdefine
from ConfigObject.Reward.RewardBase import RewardBase

class RewardSkillBase( RewardBase.RewardBase ):
	"""
	技能类
	"""
	def __init__( self, configSection ):
		self._skillID = configSection[ "goodsid" ]

class RewardBuff( RewardSkillBase ):
	"""
	buff
	"""
	def __init__( self, configSection ):
		RewardSkillBase.__init__( self, configSection )
			
	def addReward( self, rewarderID, reason ):
		
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addBuff(rewarder, int(self._skillID))
		