# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopyJiYuan import SpaceCopyJiYuan
import Math
import math
import KBEngine
import csdefine
import csstatus
import Const
import time
import KBEMath
import Functions

class SpaceCopyDongTianFuDi( SpaceCopyJiYuan ):
	"""
	洞天福地副本
	"""
	def __init__( self ) :
		SpaceCopyJiYuan.__init__( self )
		
	def onPlayerExchangeToMoney(self, roleMB, playerIntegral, money):
		pass
		
	def getJieSuanData(self):
		"""
		"""
		costTime = int(self.lifeStopTime - self.lifeStartTime ) + self.dynamicTime
		
		levelValue = 0
		rewardValue = 0
		
		timeList = list(self.getScript().rewards.keys())
		timeList.sort()
		for levelTime in timeList:
			level, value = self.getScript().rewards[levelTime]
			if costTime <= levelTime:
				levelValue = level
				rewardValue = value
				break
		
		return (int(costTime), levelValue, rewardValue, self.recordPlayerDieNumber)
		
	def JSSLC_JiYuanSpaceCopyJieSuan(self):
		"""
		晶石狩猎场机缘副本结算
		"""
		spaceEntity = self.getCurrentSpace()

		costTime, levelValue, rewardValue, dieNumber = self.getJieSuanData()
		
		for role in self._spaceRoles:
			if role.getClient():
				if levelValue != 0:
					role.showMessagePlaySound(spaceEntity.getScript().soundsAboutEachGrade[levelValue-1])
				role.client.CLIENT_ShowJSSLCJiYuanJieSuanWnd(int(costTime), levelValue, rewardValue, dieNumber)
				
	def JSSLC_JiYuanSpaceGetIntegral(self, player):
		"""
		晶石狩猎场机缘 获得金精奖励
		"""
		costTime, levelValue, rewardValue, dieNumber = self.getJieSuanData()
		player.addSparHunTingIntegral(rewardValue)
		player.client.ShowSpellBoxResultMessage(csdefine.SPELL_BOX_RESULT_ADD_INTEGRAL, rewardValue)
		