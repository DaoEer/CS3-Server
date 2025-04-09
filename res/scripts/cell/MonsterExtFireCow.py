# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import Math
import csdefine
import KBEDebug

class MonsterExtFireCow( Monster.Monster ):
	"""
	火焰牛魔
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def receiveDamage( self, casterID, skillID, damageType, damage, isCritical, isParry, deadEffect, actForbid ):
		Monster.Monster.receiveDamage( self, casterID, skillID, damageType, damage, isCritical, isParry, deadEffect, actForbid )
		if self.recoverTimer:
			self.popTimer(self.recoverTimer)
			self.recoverTimer = 0
		self.recoverTimer = self.addTimerRepeat( 3.0, "recoverFireCowAnger",() )
		self.angerValue += 1
		self.showFireCowAngerUI()
		if self.angerValue == 100:
			if self.getScript().getAICmd():
				self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (self.id, self.scriptID, self.getScript().getAICmd()))
			self.angerValue = 0
			self.showFireCowAngerUI()

	def recoverFireCowAnger( self ):
		"""
		降低暴怒值
		"""
		self.angerValue -= self.getScript().getRecoverValue()
		if self.angerValue < 0:
			self.angerValue = 0
		self.showFireCowAngerUI()

	def showFireCowAngerUI(self):
		"""
		显示暴怒值界面
		"""
		if not self.isInSpaceCopy() and not self.isInSpacePlane():
			return
		spaceEntity = self.getCurrentSpace()
		for player in spaceEntity._spaceRoles:
			player.client.ShowFireCowAngerUI(self.angerValue)


	def onEnterFight( self ):
		"""
		virtual method
		进入战斗
		"""
		Monster.Monster.onEnterFight( self )
		self.showFireCowAngerUI()

	def onEnterDead( self ):
		"""
		virtual method
		进入死亡
		"""
		spaceEntity = self.getCurrentSpace()
		for player in spaceEntity._spaceRoles:
			player.client.ShowFireCowAngerUI(-1)
		Monster.Monster.onEnterDead( self )
