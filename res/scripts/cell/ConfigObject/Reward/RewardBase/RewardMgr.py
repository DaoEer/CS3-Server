# -*- coding- : utf-8 -*-

import HotUpdate
import KBEDebug
import KBEngine
import csdefine
import LoadModule
from Reward import RewardNormalData
from Reward import RewardData
from Singleton import Singleton
from ConfigObject.Reward.RewardBase import RewardObject
from ConfigObject.Reward.RewardBase import RewardRule

EQUIP_SCRIPT = [ "RewardEquipForRLAndRPToWeight", "RewardEquipForRLToWeight", "RewardEquipForDieLevelToWeight", "RewardEquipForDieLevelAndRPToWeight" ]
QUEST_SCRIPT = [ "RewardForQuestIDAndMonsterIDToRate" ]

ITEM_DATA_PATH = "Item/ItemData.json"
#奖励类型
REWARD_TYPE_LIST = [
	csdefine.REWARD_TYPE_NOTHING,
	csdefine.REWARD_TYPE_MONEY,
	csdefine.REWARD_TYPE_EXP,
	csdefine.REWARD_TYPE_ITEM,
	csdefine.REWARD_TYPE_XIUWEI,
	csdefine.REWARD_TYPE_POTENTIAL,
	csdefine.REWARD_TYPE_BANGGONG,
	csdefine.REWARD_TYPE_TONG_MONEY,
	csdefine.REWARD_TYPE_FEATS,
	csdefine.REWARD_TYPE_MORALE,
	csdefine.REWARD_TYPE_CREWARD,
	csdefine.REWARD_TYPE_EXP_BL,
	csdefine.REWARD_TYPE_POTENTIAL_BL,
	csdefine.REWARD_TYPE_XIUWEI_BL,
	csdefine.REWARD_TYPE_MONEY_BL,
	csdefine.REWARD_TYPE_BINDMONEY_BL,
	csdefine.REWARD_TYPE_BUFF,
	csdefine.REWARD_TYPE_BARRACKSEXP,
	csdefine.REWARD_TYPE_INTEGRAL,
	csdefine.REWARD_TYPE_PSIONIC,
	csdefine.REWARD_TYPE_EXPLOIT,
	csdefine.REWARD_TYPE_TITLE,
	csdefine.REWARD_TYPE_BINDMONEY,
	csdefine.REWARD_TYPE_XIANSHI,
	csdefine.REWARD_TYPE_LINGSHI,
	csdefine.REWARD_TYPE_XUANSHI
]
REWARD_TYPE_BL = [csdefine.REWARD_TYPE_EXP_BL, csdefine.REWARD_TYPE_POTENTIAL_BL, csdefine.REWARD_TYPE_XIUWEI_BL, csdefine.REWARD_TYPE_MONEY_BL, csdefine.REWARD_TYPE_BINDMONEY_BL]

class RewardMgr( Singleton ):
	"""
	奖励数据管理器
	"""
	def __init__( self ):
		Singleton.__init__( self )
		self._rewardDatas = {}
		self.init()
		
		self._itemDatas = LoadModule.openJsonCfg(ITEM_DATA_PATH)
		self.checkRewardNoramlData()

	def init( self ):
		self._rewardDatas.clear()
		configSection = RewardData.datas
		for rewardID, data in configSection.items():
			rewardData = self.getRewardData( data["script"], rewardID )
			if rewardData != None:
				func_ = getattr( RewardRule, data["script"], None )
				if func_:
					self._rewardDatas[ rewardID ] = func_( rewardData, data )
				else:
					KBEDebug.ERROR_MSG("Can not find rewrd by script(%S)"% data["script"])
	
	def checkRewardNoramlData(self):
		"""
		RewardNormalData数据有效性检测
		"""
		configSection = RewardNormalData.datas
		for rewardID, rewardList in configSection.items():
			for reward in rewardList:
				if reward["type"] not in REWARD_TYPE_LIST:
					KBEDebug.ERROR_MSG("(RewardNormalID:%s) type:%s is config error!"%(rewardID, reward["type"]))
				else:
					if reward["type"] == csdefine.REWARD_TYPE_ITEM:
						if reward["goodsid"] not in self._itemDatas:
							KBEDebug.ERROR_MSG("(RewardNormalID:%s) goodsid:%s is config error!"%(rewardID, reward["goodsid"]))
				if reward["amount"]:
					if reward["type"] not in REWARD_TYPE_BL and type(eval(reward["amount"])) != int:
						KBEDebug.ERROR_MSG("(RewardNormalID:%s) amount:%s is config error!"%(rewardID, reward["amount"]))

	def reloadConfig( self ):
		"""
		配置支持热更新
		"""
		HotUpdate.reloadByModule( RewardNormalData )
		HotUpdate.reloadByModule( RewardData )
		
		self.init()
		
	def getRewardScript( self, script ):
		"""
		根据脚本类型获取生成奖励的脚本
		"""
		return getattr( RewardRule, script, None )
		
	def getRewardData( self, script, rewardID ):
		"""
		获取奖励需要的数据，nuomalData, questData, equipData
		"""
		data = []
		if script in EQUIP_SCRIPT or script in QUEST_SCRIPT:
			#RewardEquipData.datas	由于每个装备奖励的数据都是一样，所以该数据在生成装备奖励处处理
			#RewardQuestData.datas	由于每个任务奖励的数据都是一样，所以该数据在生成任务奖励处处理
			data = {}
		else:
			data = RewardNormalData.datas[ rewardID ]
		return data
		
	def getReward( self, rewardID, args ):
		"""
		#获取奖励
		rewardID: 奖励编号
		args: 触发奖励条件
		"""
		rewardDatas = []
		if rewardID in self._rewardDatas:
			rewardDatas = self._rewardDatas[ rewardID ].fetch( rewardID, args )
			if KBEngine.cellAppData.get("DEBUG_REWARD_FLG", None):
				KBEDebug.DEBUG_MSG_FOR_REWARD("Reward(ParentRewardID: {}) set is )：".format(rewardID))
				for data in rewardDatas:
					KBEDebug.DEBUG_MSG_FOR_REWARD(str(data))

			for index, data in enumerate( rewardDatas ):
				if index >= 100:											# 因为下面的extend，策划配置错误的话，有可能出现死循环。
					KBEDebug.ERROR_MSG("Reward id(%s) is err!"%rewardID)
					break
				if data["type"] == csdefine.REWARD_TYPE_CREWARD:			# 因为有一些外部的功能，需要获取奖励的内容。所以在这里child需要展开
					rewardDatas.extend( self.getReward( data["goodsid"], args) )
		else:
			KBEDebug.ERROR_MSG("Can not find Reward(id:%s)"%rewardID)
		delNum = 0
		for index, data in enumerate( list(rewardDatas) ):
			if data["type"] == csdefine.REWARD_TYPE_CREWARD:
				rewardDatas.pop( index - delNum )
				delNum += 1

		return rewardDatas

	def doReward( self, rewardData, rewarderID, reason ):
		"""
		#发奖
		rewardDatas: 奖励的数据
		rewarderID: 获奖者
		reason: 获奖原因
		"""
		return RewardObject.RewardObject( rewardData ).doReward( rewarderID, reason )

	def doRewards( self, rewardDatas, rewarderID, reason ):
		"""
		#发奖
		rewardDatas: 奖励的数据
		rewarderID: 获奖者
		reason: 获奖原因
		"""
		failAdd = []				# 添加失败的物品？
		for rewardData in rewardDatas:
			result = self.doReward( rewardData, rewarderID, reason )
			if result:
				failAdd.append( result )
		return failAdd

g_rewardMgr = RewardMgr()