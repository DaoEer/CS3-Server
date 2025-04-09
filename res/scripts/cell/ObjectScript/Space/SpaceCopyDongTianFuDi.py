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

SPACE_PASS_LEVEL_RD = 1 #入道
SPACE_PASS_LEVEL_CC = 2 #出尘
SPACE_PASS_LEVEL_WD = 3 #问鼎
SPACE_PASS_LEVEL_CF = 4	#超凡

class SpaceCopyDongTianFuDi( SpaceCopyJiYuan ):
	"""
	洞天福地副本
	"""
	def __init__( self ):
		SpaceCopyJiYuan.__init__( self )
		self.rewards = {}
		self.soundsAboutEachGrade = []  # 达到每一档奖励的语音提示

	def initData( self, configData ):
		"""
		"""
		SpaceCopyJiYuan.initData( self, configData )
		
		rewards = configData["SpaceData"].get("rewards", "")#档次:档次对应完成任务的要求时间:奖励金精数量|...
		if rewards:
			for reward in rewards.split("|"):
				level, levelTime, rewardValue, sound = reward.split(":")
				self.rewards[int(levelTime)] = (int(level), int(rewardValue))
				self.soundsAboutEachGrade.append(sound)

		self.soundsAboutEachGrade.sort()
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
		