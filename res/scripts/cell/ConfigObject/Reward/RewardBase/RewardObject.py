# -*- coding- : utf-8 -*-

import KBEDebug
import csdefine

from ConfigObject.Reward import RewardValue
from ConfigObject.Reward import RewardItem
from ConfigObject.Reward import RewardSkill
from ConfigObject.Reward import RewardNothing
from ConfigObject.Reward import RewardTitle

class RewardObject( object ):
	_TYPES = {}
	def __init__( self, configSection ):
		self._rewardObj = None
		self.initData( configSection )

	def initData( self, configSection ):
		obj = RewardObject.getObject( configSection["type"] )
		if obj:
			self._rewardObj = obj( configSection )
		else:
			KBEDebug.ERROR_MSG("Can not find Reward type ",configSection)

	@classmethod
	def registerOjbect( SELF, type, classOjbect ):
		SELF._TYPES[ type ] = classOjbect

	@classmethod
	def getObject( SELF, type ):
		return SELF._TYPES.get( type, None )
	
	
	def doReward( self, rewarderID, reason ):
		"""
		执行奖励处理
		"""
		return self._rewardObj.addReward( rewarderID, reason )

RewardObject.registerOjbect( csdefine.REWARD_TYPE_MONEY, RewardValue.RewardMoney )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_EXP, RewardValue.RewardExp )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_ITEM, RewardItem.RewardItem )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_XIUWEI, RewardValue.RewardXiuWei )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_POTENTIAL, RewardValue.RewardPotential )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_BANGGONG, RewardValue.RewardBangGong )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_TONG_MONEY, RewardValue.RewardTongMoney )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_FEATS, RewardValue.RewardFeats )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_MORALE, RewardValue.RewardMorale )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_BUFF, RewardSkill.RewardBuff )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_BARRACKSEXP, RewardValue.RewardBarracksExp )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_INTEGRAL, RewardValue.RewardSparHunTingIntegral )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_NOTHING, RewardNothing.RewardNothing )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_PSIONIC, RewardValue.RewardPsionic )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_EXPLOIT, RewardValue.RewardExploit )
RewardObject.registerOjbect( csdefine.REWARD_TYPE_TITLE, RewardTitle.RewardTitle)
RewardObject.registerOjbect( csdefine.REWARD_TYPE_BINDMONEY, RewardValue.RewardBindMoney)
RewardObject.registerOjbect( csdefine.REWARD_TYPE_XIANSHI, RewardValue.RewardXianShi)
RewardObject.registerOjbect( csdefine.REWARD_TYPE_LINGSHI, RewardValue.RewardLingShi)
RewardObject.registerOjbect( csdefine.REWARD_TYPE_XUANSHI, RewardValue.RewardXuanShi)
