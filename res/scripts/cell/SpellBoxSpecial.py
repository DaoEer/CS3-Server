# -*- coding: utf-8 -*-
#
import Math
import time
import KBEngine
import KBEDebug
import csdefine
import SpellBox


class SpellBoxSpecial( SpellBox.SpellBox ):
	"""
	大地图特殊场景物件
	"""
	def __init__(self):
		SpellBox.SpellBox.__init__(self)
		
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		SpellBox.SpellBox.CELL_onClientReady( self, srcEntityID )
		self.getScript().onClientActorReady( self )
		player = KBEngine.entities.get( srcEntityID )
		if player.playerDBID in self.allinteractive and (self.playerIsCoolList and self.playerIsCoolList[player.playerDBID]):
			self.addTimerCallBack( 1.0,"specialPlayAction",(self.getScript().endActionID, srcEntityID) )
			if self.getScript().endEffectID != "":
				self.addTimerCallBack( 1.0,"specialPlayParticles",(self.getScript().endEffectID, srcEntityID,) )
		elif self.getScript().startEffectID != "":
			self.specialPlayParticles( self.getScript().startEffectID, srcEntityID )
	
	def onPlayerIntonateOver( self, playerID ):
		"""
		<define method>
		玩家吟唱结束
		"""
		player = KBEngine.entities.get( playerID )
		if player:
			self.getScript().onPlayerIntonateOver( self, player )
			self.specialStopParticles( self.getScript().startEffectID, playerID )
			self.specialPlayAction( self.getScript().endActionID, playerID )
			if self.getScript().endEffectID != "":
				self.specialPlayParticles( self.getScript().endEffectID, playerID )
			self.addTimerCallBack( 1.0,"temporaryRecord",(player.playerDBID,) )

	def temporaryRecord( self, playerDBID ):
		"""
		记录临时数据
		"""
		if playerDBID not in self.allinteractive:
			self.allinteractive.append( playerDBID )

	def requestRefreshCondition( self, selfEntity, playerEntity ):
		"""
		可交互光效动态更新
		"""
		selfEntity.getScript().requestRefreshStatus( selfEntity, playerEntity )

	def specialPlayParticles(self, effectID, playerID):
		"""
		播放光效
		"""
		player = KBEngine.entities.get( playerID )
		if player and player.isEntityInView( self ):
			player.client.CLIENT_OnPlayParticles( self.id, effectID, "", 1.0, Math.Vector3(0,0,0) )

	def specialStopParticles(self, effectID, playerID):
		"""
		停止光效
		"""
		player = KBEngine.entities.get( playerID )
		if player and player.isEntityInView( self ):
			player.clientEntity( self.id ).CLIENT_OnStopParticles()
		
	def specialPlayAction(self, effectID, playerID):
		"""
		播放动作
		"""
		player = KBEngine.entities.get( playerID )
		if player and player.isEntityInView( self ):
			player.clientEntity( self.id ).CLIENT_OnPlayAction( effectID, -1.0 )
		