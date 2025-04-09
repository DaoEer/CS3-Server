# -*- coding: utf-8 -*-

import time
import KBEMath
import KBEDebug
import csdefine
import Const
import csconst
import Functions
import csstatus
import Define
from ObjectScript.Space.SpaceCopyJiYuan import SpaceCopyJiYuan


SPACE_PASS_LEVEL_RD = 1 #入道
SPACE_PASS_LEVEL_CC = 2 #出尘
SPACE_PASS_LEVEL_WD = 3 #问鼎
SPACE_PASS_LEVEL_CF = 4	#超凡

class SpaceCopyXKTB( SpaceCopyJiYuan ):
	"""
	副本虚空探宝
	"""
	def __init__( self ):
		SpaceCopyJiYuan.__init__( self )
		
	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		#通知客户端清空探宝次数
		if playerRole.getClient(): 
			playerRole.getClient().CLIENT_notifyProbeTimes(0)
			
		JiyuanSpaceData = playerRole.queryTemp("JiyuanSpaceData", None)
		leaveReason = packArgs.get("leaveReason", -1)
		if not JiyuanSpaceData or leaveReason == Define.LEAVE_SPACE_REASON_LOGOUT: #如果没有获取到机缘副本数据，则表示晶石狩猎场已经关闭
			playerRole.addSparHunTingTotalIntegral(playerRole.sparHunTingIntegral)
			exchMoneyScale = playerRole.queryTemp("copy_exchMoneyScale", 0)
			playerRole.playerExchangeToMoney(exchMoneyScale, playerRole.sparHunTingTotalIntegral)
			playerRole.setSparHunTingIntegral(0)
			playerRole.setSparHunTingTotalIntegral(0)
			playerRole.removeTemp("copy_exchMoneyScale")
			
		SpaceCopyJiYuan.onLeave(self, selfEntity, playerRole, packArgs)
		
	def spaceSettlement_onSpaceSuccess6369(self, selfEntity):
		"""
		副本通关 显示结算界面
		"""
		if selfEntity.getScript().getSpaceType() not in [csdefine.SPACE_TYPE_JSSLC_CHANCE_COPY]:
			return
		costTime = int( selfEntity.lifeStopTime - selfEntity.lifeStartTime ) + selfEntity.dynamicTime
		probeTimes = selfEntity.queryTemp("PROBETIMES", -1)
		level = 0
		if probeTimes >= 9:
			level = SPACE_PASS_LEVEL_CF
		elif probeTimes >= 6 and probeTimes <= 8:
			level = SPACE_PASS_LEVEL_WD
		elif probeTimes >=3  and probeTimes <= 5:
			level = SPACE_PASS_LEVEL_CC
		else:
			level = SPACE_PASS_LEVEL_RD
		
		for role in selfEntity._spaceRoles:
			if role.getClient():
				role.client.CLIENT_ShowSpaceSettlementWin(csdefine.SPACE_TYPE_JSSLC_CHANCE_COPY, role.sparHunTingIntegral, int(costTime), selfEntity.recordPlayerDieNumber, level )
			