# -*- coding: utf-8 -*-

import Math
import time
import csdefine
import KBEngine
from CoreObject import SpellObject

class MultiAreaSpellBox( SpellObject.SpellObject ):
	def __init__( self ):
		SpellObject.SpellObject.__init__( self )

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		SpellObject.SpellObject.CELL_onClientReady( self, srcEntityID )
		self.getScript().onClientActorReady(self)
		self.isExecuted[self.currentArea] = False
		self.allClients.CLIENT_OnSwitchArea( self.currentArea )
		if self.currentArea in self.getScript().holdAction:
			self.playAction( self.getScript().holdAction[self.currentArea] )
		if self.currentArea in self.getScript().holdEffectID:
			self.playParticles( self.getScript().holdEffectID[self.currentArea] )
		player = KBEngine.entities.get( srcEntityID )
		self.getScript().refreshGossipCondition( self, player )
		self.position = self.position

	def requestRefreshCondition( self, selfEntity, playerEntity ):
		"""
		可交互光效动态更新
		"""
		selfEntity.getScript().refreshGossipCondition( selfEntity, playerEntity )
		selfEntity.getScript().RefreshAreaStatus( selfEntity, playerEntity )

	def onDelayTimeSwitchArea( self, areaIndex ):
		"""
		切换到指定的检测区域
		"""
		self.currentArea = areaIndex
		self.allClients.CLIENT_OnSwitchArea( areaIndex )
		if self.currentArea in self.getScript().holdAction:
			self.playAction( self.getScript().holdAction[self.currentArea] )
		if self.currentArea in self.getScript().holdEffectID:
			self.playParticles( self.getScript().holdEffectID[self.currentArea] )

	def stopHoldActionAndEffect( self ):
		"""
		停止持有动作和持有光效
		"""
		if self.currentArea in self.getScript().holdAction:
			self.stopParticles()
		if self.currentArea in self.getScript().holdEffectID:
			self.stopAction()

	def playParticles(self, effectID):
		"""
		播放光效
		"""
		self.allClients.CLIENT_OnPlayParticles( self.id, effectID, "", 1.0, Math.Vector3(0,0,0) )

	def stopParticles( self ):
		"""
		停止光效
		"""
		self.allClients.CLIENT_OnStopParticles()
		
	def playAction(self, actionID):
		"""
		播放动作
		"""
		self.allClients.CLIENT_OnPlayAction( actionID, -1.0 )

	def stopAction( self ):
		"""
		停止动作
		"""
		self.allClients.CLIENT_StopAction()
