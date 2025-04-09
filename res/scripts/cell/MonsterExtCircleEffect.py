# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import Math
import csdefine
import KBEDebug

class MonsterExtCircleEffect( Monster.Monster ):
	"""
	火海怪物entity
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.isFirst = False
		
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		if self.isFirst:
			return
		self.isFirst = True
		times = self.getScript().getTotalTime()/self.getScript().getIntervalTime()
		self.reduceRadius = self.getScript().getRadius()/times
		self.startRadius = self.getScript().getRadius()
		self.originRadius = self.getScript().getRadius()
		self.intervaTimer = self.addTimerRepeat( self.getScript().getIntervalTime(), "tickHitEntity",() )
		self.addTimerCallBack( self.getScript().getHoldTime(), "endkHitEntity",() )
		self.checkIsInSaveArea()

	def tickHitEntity(self):
		self.originRadius -= self.reduceRadius
		if self.originRadius <= 0.0 and self.intervaTimer:
			self.popTimer(self.intervaTimer)

	def endkHitEntity(self):
		if self.checkAreaTimer:
			self.popTimer(self.checkAreaTimer)
		buffID = self.getScript().getBuffID()
		spaceEntity = self.getCurrentSpace()
		for player in spaceEntity._spaceRoles:
			if len(player.findBuffsByBuffID(buffID)):
				player.removeBuffByID(buffID)

	def checkIsInSaveArea( self ):
		"""
		检查玩家是否在安全区域里
		"""
		if self.checkAreaTimer:
			self.popTimer(self.checkAreaTimer)
		self.checkAreaTimer = self.addTimerRepeat(0.1, "tickCheckIsInSaveArea",() )

	def tickCheckIsInSaveArea( self ):
		"""
		"""
		buffID = self.getScript().getBuffID()
		spaceEntity = self.getCurrentSpace()
		for player in spaceEntity._spaceRoles:
			if player.position.flatDistTo( self.position ) >= self.originRadius \
			and player.position.flatDistTo( self.position ) <= self.startRadius \
			and abs(player.position.y - self.position.y) <= self.getScript().getHeight():
				if len(player.findBuffsByBuffID(buffID)):
					continue
				player.addBuff(player, buffID)
			else:
				player.removeBuffByID(buffID)
