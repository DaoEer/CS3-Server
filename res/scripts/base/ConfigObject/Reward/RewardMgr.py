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
from ConfigObject.Reward.RewardBase import RewardSetScript

EQUIP_SCRIPT = [ "RewardEquipForRLAndRPToWeight", "RewardEquipForDieLevelToWeight" ]
QUEST_SCRIPT = [ "RewardForQuestIDAndMonsterIDToRate" ]

class RewardMgr( Singleton ):
	"""
	奖励数据管理器
	"""
	def __init__( self ):
		Singleton.__init__( self )
		self._rewardDatas = {}
		self.init()

	def init( self ):
		self._rewardDatas.clear()
		configSection = RewardData.datas
		for rewardID, data in configSection.items():
			rewardData = self.getRewardData( data["script"], rewardID )
			if rewardData != None:
				self._rewardDatas[ rewardID ] = RewardSetScript.RewardSetScript.getObject( data["script"] )( rewardData, data )
	
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
		return RewardSetScript.RewardSetScript.getObject( script )
		
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
		if rewardID in self._rewardDatas:
			return self._rewardDatas[ rewardID ].fetch( rewardID, args )
		else:
			return None
		

	def doReward( self, rewardData, rewarderID, reason ):
		"""
		#发奖
		rewardData: 奖励的数据
		rewarderID: 获奖者
		reason: 获奖原因
		"""
		RewardObject.RewardObject( rewardData ).doReward( rewarderID, reason )
		

g_rewardMgr = RewardMgr()