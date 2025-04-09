# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopyJiYuan import SpaceCopyJiYuan
import csdefine
import KBEngine
import time

from MsgLogger import g_logger
import LogDefine

class SpaceCopyJinZhiYuTing( SpaceCopyJiYuan ):
	"""
	副本金枝玉庭
	"""
	def __init__( self ) :
		SpaceCopyJiYuan.__init__( self )

	def MonsterPickUpLostTreasures( self ):
		"""
		守卫收取场景中的财宝
		"""
		for e in self._spaceRoles:
			for scriptID in self.allFuDaiScriptIDList:
				idList = self.getEntityRecord(scriptID)
				for id in idList:
					entity = KBEngine.entities.get(id,None)
					if entity == None:
						return
					entity.onFuDaiCollisionMonster( entity, e )
					
	def onPlayerExchangeToMoney(self, roleMB, playerIntegral, money):
		pass
		
	def getJieSuanData(self):
		"""
		"""
		costTime = int(self.lifeStopTime - self.lifeStartTime ) + self.dynamicTime
		levelValue = 0
		rewardValue = 0
		
		amountList = list(self.getScript().rewards.keys())
		amountList.sort(reverse=True)
		for amount in amountList:
			level, value = self.getScript().rewards[amount]
			if self.integralToolAmount >= amount:
				levelValue = level
				rewardValue = value
				break
		
		return (int(costTime), levelValue, rewardValue, self.recordPlayerDieNumber)
		
	def JSSLC_JiYuanSpaceCopyJieSuan(self):
		"""
		晶石狩猎场机缘副本结算
		"""
		costTime, levelValue, rewardValue, dieNumber = self.getJieSuanData()
		for roleCell in self._spaceRoles:
			if roleCell.getClient(): roleCell.client.CLIENT_ShowJSSLCJiYuanJieSuanWnd(costTime, levelValue, rewardValue, dieNumber)
			g_logger.roleActiveRecord(LogDefine.ACTIVE_SPACE_TYPE_DEFAULT, roleCell.accountDBID, roleCell.playerDBID, roleCell.getLevel(), "", "", self.lifeStartTime, costTime, LogDefine.ACTIVE_STATE_TYPE_SUCCESS, self.scriptID)
		
	def JSSLC_JiYuanSpaceGetIntegral(self, player):
		"""
		晶石狩猎场机缘 获得金精奖励
		"""
		costTime, levelValue, rewardValue, dieNumber = self.getJieSuanData()
		player.addSparHunTingIntegral(rewardValue)
		player.client.ShowSpellBoxResultMessage(csdefine.SPELL_BOX_RESULT_ADD_INTEGRAL, rewardValue)