# -*- coding: utf-8 -*-

import Math
import time
import csdefine
import KBEngine
from CoreObject import SpellObject


class SpellBox( SpellObject.SpellObject ):
	def __init__( self ):
		SpellObject.SpellObject.__init__( self )
		#self.isCoolDowning = False		#cell_public属性：是否在冷却
		#self.isDestroyHide = False		#cell_public属性：是否处于销毁隐藏状态
		self.createTime = time.time()

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		player = KBEngine.entities.get( srcEntityID )
		SpellObject.SpellObject.CELL_onClientReady( self, srcEntityID )
		self.getScript().onClientActorReady(self)
		self.position = self.position
		if player:
			self.requestRefreshCondition(self, player)
	
	def onPlayerIntonateOver( self, playerID ):
		"""
		<define method>
		玩家吟唱结束
		"""
		player = KBEngine.entities.get( playerID )
		if player:
			self.getScript().onPlayerIntonateOver( self, player )
	
	def getRemainLifeTime( self ):
		"""
		获取剩余生命时长
		"""
		if self.lifeTime <= 0 :
			return -1
		return float( self.createTime + self.lifeTime - time.time() )

	def notify_OtherClientForbidInteractive( self, playerID ):
		"""
		如果策划配置不允许多人交互,通知其他客户端禁止交互
		"""
		if self.getScript().isInteractive == csdefine.SPELL_BOX_NOT_PLAYERS_INTERACTIVE:
			self.IsCanInteract = 0
			entity = KBEngine.entities.get(playerID)
			if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				entity.otherClients.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_IS_INTERACT)

	def notify_OtherClientCanInteractive( self,playerID ):
		"""
		通知其他客户端可以交互
		"""
		if self.getScript().isInteractive == csdefine.SPELL_BOX_NOT_PLAYERS_INTERACTIVE:
			self.IsCanInteract = 1
			entity = KBEngine.entities.get(playerID)
			if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
				try:
					entity.otherClients.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_IS_INTERACT)
				except:
					pass

	def setInteract( self, state ):
		"""
		设置是否可以交互
		"""
		self.IsCanInteract = state
		self.allClients.CLIENT_RefreshBoxStatus()

	def requestRefreshCondition( self, selfEntity, playerEntity ):
		"""
		可交互光效动态更新
		"""
		selfEntity.getScript().requestRefreshStatus( selfEntity, playerEntity )
		
	def playParticles(self, effectID):
		"""
		播放光效
		"""
		self.allClients.CLIENT_OnPlayParticles( self.id, effectID, "", 1.0, Math.Vector3(0,0,0) )
		
	def playAction(self, effectID):
		"""
		播放动作
		"""
		self.allClients.CLIENT_OnPlayAction(effectID, -1.0)
