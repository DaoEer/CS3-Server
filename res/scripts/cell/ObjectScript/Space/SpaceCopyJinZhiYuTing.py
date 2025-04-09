# -*- coding: utf-8 -*-

import time
import KBEMath
import KBEDebug
import csdefine
import Const
import Define
import csconst
import Functions
import csstatus
from ObjectScript.Space.SpaceCopyJiYuan import SpaceCopyJiYuan

class SpaceCopyJinZhiYuTing( SpaceCopyJiYuan ):
	"""
	副本金枝玉庭
	"""
	def __init__( self ):
		SpaceCopyJiYuan.__init__( self )
		self.rewards = {}
		self.goldNumAboutGrade = [] #达到每一档奖励所需的金币数量
		self.soundsAboutEachGrade = [] #达到每一档奖励的语音提示
	def initData( self, configData ):
		"""
		"""
		SpaceCopyJiYuan.initData( self, configData )
		
		rewards = configData["SpaceData"].get("rewards", "") #档次:档次对应收集金币最低数量:奖励金精数量|...
		if rewards:
			for reward in rewards.split("|"):
				level, amount, rewardValue, sound = reward.split(":")
				self.rewards[int(amount)] = (int(level), int(rewardValue))
				self.goldNumAboutGrade.append(int(amount))
				self.soundsAboutEachGrade.append(sound)
	def onLeave( self, selfEntity, playerRole, packArgs ):
		JiyuanSpaceData = playerRole.queryTemp("JiyuanSpaceData", None)
		leaveReason = packArgs.get("leaveReason", -1)
		if not JiyuanSpaceData or leaveReason == Define.LEAVE_SPACE_REASON_LOGOUT: #如果没有获取到机缘副本数据，则表示晶石狩猎场已经关闭
			playerRole.addSparHunTingTotalIntegral(playerRole.sparHunTingIntegral)
			exchMoneyScale = playerRole.queryTemp("copy_exchMoneyScale", 0)
			playerRole.playerExchangeToMoney(exchMoneyScale, playerRole.sparHunTingTotalIntegral)
			playerRole.setSparHunTingIntegral(0)
			playerRole.setSparHunTingTotalIntegral(0)
			playerRole.removeTemp("copy_exchMoneyScale")
			
		SpaceCopyJiYuan.onLeave( self, selfEntity, playerRole, packArgs )
