# -*- coding: utf-8 -*-
import KBEngine
import csdefine
import Monster
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface
import time

class MonsterExtRefreshTime(Monster.Monster):
	def __init__( self ):
		Monster.Monster.__init__( self )

	def onRevevie(self):
		"""
		怪物复活
		"""
		self.isInPending = 0
		self.monsterAIReStart()
		self.updateBornHPMP()

	def onEnterDead(self):
		MonsterCombatInterface.MonsterCombatInterface.onEnterDead( self )

		self.getScript().onEnterDead( self )
		hasbuffhitback = False
		for index, buff in self.attrBuffs.items():
			buffname = self.getBuff(buff.buffID).__class__.__name__
			if buffname == "BuffHitBack":
				hasbuffhitback = True
		if not hasbuffhitback:
			self.stopMovingForType(csdefine.SYSTEM_MOVE)

	def pretendModel(self, endReviveTime):

		self.isInPending = 1 					        #隐藏模型
		self.changeState(csdefine.ENTITY_STATE_FREE)
		self.monsterAIStop()
		self.position = self.spawnPos
		self.allClients.CLIENT_DisplayCounodwn( endReviveTime )#通知客户端显示倒计时