# -*- coding: utf-8 -*-
import Math
import random
from SpaceCopyTong import SpaceCopyTong
import KBEDebug
import KBEngine

class SpaceCopySLZD( SpaceCopyTong ):
	"""
	试炼之地
	"""
	def __init__( self ):
		SpaceCopyTong.__init__( self )

	def randomFlagstonePlayEffect(self, effectID, amount, intervalTime):
		"""
		随机顺序石板播放光效
		"""
		self.SLZDrandomList.clear()
		self.SLZDrandomIndex = 0
		self.SLZDrandomList.extend(self.getScript().getSLZDSrciptIDs(amount))
		self.intervalTimer = self.addTimerRepeat( intervalTime, "flagstonePlayEffect",( effectID, ) )


	def flagstonePlayEffect(self, effectID):
		if len(self.SLZDrandomList) <= self.SLZDrandomIndex:
			if self.intervalTimer:
				self.popTimer(self.intervalTimer)
				self.intervalTimer = 0
			return
		for id in self.getEntityRecord( self.SLZDrandomList[self.SLZDrandomIndex] ):
			entity = KBEngine.entities.get( id )
			if not entity:
				continue
			entity.allClients.CLIENT_OnPlayParticles( entity.id, effectID, "", 1.0, Math.Vector3(0,0,0) )	
		self.SLZDrandomIndex += 1


	def onPlayerTreadFlagstone(self, scriptID):
		"""
		玩家踩上石板后
		"""
		if len(self.SLZDrandomList) <= 0:
			return
		_scriptID = self.SLZDrandomList.pop(0)
		if scriptID != _scriptID:
			self.getScript().onConditionChange(self, "", self.id, "SLZDFailure", "")
			return

		if len(self.SLZDrandomList) == 0:
			self.getScript().onConditionChange(self, "", self.id, "SLZDSuccess", "")
