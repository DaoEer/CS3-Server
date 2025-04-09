# -*- coding- : utf-8 -*-
import KBEngine


import csdefine
import csstatus
from ConfigObject.Reward.RewardBase import RewardBase
import KBEDebug

class RewardValueBase( RewardBase.RewardBase ):
	"""
	掉落数值类
	"""
	def __init__( self, configSection ):
		self._value = configSection["amount"]

class RewardMoney( RewardValueBase ):
	"""
	金钱
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加金钱
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addMoney( self._value, reason )
		

class RewardExp( RewardValueBase ):
	"""
	经验
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加经验
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addExp( self._value, reason )
		

class RewardXiuWei( RewardValueBase ):
	"""
	修为
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加修为
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addXiuwei( self._value, reason )
		

class RewardPotential( RewardValueBase ):
	"""
	潜能
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加潜能
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addPotential( self._value, reason )
		

class RewardBangGong( RewardValueBase ):
	"""
	帮贡
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加帮贡
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder and rewarder.tongMB:
			rewarder.tongMB.GM_CommandSetAttr( rewarder.playerDBID, "contribution", self._value )
		

class RewardTongMoney( RewardValueBase ):
	"""
	帮会金钱
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		帮会金钱
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder and rewarder.tongMB:
			rewarder.tongMB.GM_CommandSetAttr( rewarder.playerDBID, "money", self._value )

class RewardFeats( RewardValueBase ):
	"""
	功勋
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加功勋
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addFeats( self._value, reason )
		
class RewardMorale( RewardValueBase ):
	"""
	士气
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加士气
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			KBEngine.globalData["CampMgr"].addMorale( rewarder.getCamp(), self._value )
			rewarder.statusMessage( csstatus.CAMP_MORALE_ADD, self._value )
		
class RewardBarracksExp( RewardValueBase ):
	"""
	养兵经验
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加经验
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addBarracksExp( self._value )
					
class RewardSparHunTingIntegral( RewardValueBase ):
	"""
	奖励晶石狩猎场积分
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加经验
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addSparHunTingIntegral( self._value )
			
class RewardPsionic( RewardValueBase ):
	"""
	奖励 灵能
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加经验
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addPsionic( self._value )
			
class RewardExploit( RewardValueBase ):
	"""
	奖励 军功
	"""
	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加经验
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addExploit( self._value )

class RewardBindMoney( RewardValueBase ):
	"""
	奖励 绑金
	"""

	def __init__( self, configSection ):
		RewardValueBase.__init__( self, configSection )

	def addReward( self, rewarderID, reason ):
		"""
		添加绑金
		"""
		rewarder = KBEngine.entities.get( rewarderID, None )
		if rewarder:
			rewarder.addBindMoney( self._value,None)

class RewardXianShi( RewardValueBase ):
	"""
	奖励 仙石
	"""
	def __init__(self, configSection):
		RewardValueBase.__init__(self, configSection)


	def addReward(self, rewardID, reason):
		"""
		添加仙石
		"""
		rewarder = KBEngine.entities.get( rewardID, None)
		if rewarder:
			rewarder.base.addXianShi( self._value,0,0)

class RewardLingShi( RewardValueBase ):
	"""
		奖励 灵石
		"""

	def __init__(self, configSection):
		RewardValueBase.__init__(self, configSection)

	def addReward(self, rewardID, reason):
		"""
		添加灵石
		"""
		rewarder = KBEngine.entities.get(rewardID, None)
		if rewarder:
			rewarder.base.addLingShi(self._value,0,0)

class RewardXuanShi( RewardValueBase ):
	"""
		奖励 灵石
		"""

	def __init__(self, configSection):
		RewardValueBase.__init__(self, configSection)

	def addReward(self, rewardID, reason):
		"""
		添加灵石
		"""
		rewarder = KBEngine.entities.get(rewardID, None)
		if rewarder:
			rewarder.base.addXuanShi(self._value,0)
