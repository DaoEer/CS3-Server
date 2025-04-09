# -*- coding: utf-8 -*-

import SpellBox
import csstatus
import csdefine
import KBEngine
import KBEDebug

class SpellBoxPickItem( SpellBox.SpellBox ):
	"""
	场景物件玩家自主选择物品
	"""
	def __init__(self):
		SpellBox.SpellBox.__init__(self)

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		SpellBox.SpellBox.CELL_onClientReady( self, srcEntityID )
		if self.openEntityID:
			self.playAction( self.getScript().param4 )

	def pickUpItem( self, player, itemUIDs ):
		"""
		拾取物品
		"""
		self.getScript().pickUpItem(self, player, itemUIDs)


	def YCJMDBossPickUpItem( self, bossEntity ):
		"""
		勇闯绝命岛Boss拾取物品 （特殊）
		"""
		itemDict = {}
		for itemInst in self.spellBoxItemList:
			itemDict[itemInst.id] = itemInst.amount
		bossEntity.addBossItemDictData( itemDict )
		self.spellBoxItemList.clear()
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		cooldownTime = self.cooldownTime
		position = self.position
		direction = self.direction
		if self.lifeTimerID > 0:
			self.popTimer( self.lifeTimerID )
			self.lifeTimerID = 0
		spaceEntity.addTimerCallBack( cooldownTime,"createSpellBox",( self.scriptID,position,direction,{} ) )
		self.destroySelf()

	def notifySpellBoxInteractiveOver( self, playerID  ):
		"""
		交互结束
		"""
		self.playAction( self.getScript().param5 )  #播放关箱动作
		self.openEntityID = 0

	def pickUpAllItems( self, player ):
		"""
		拾取所有物品
		"""
		itemUIDs = []
		for itemInst in self.spellBoxItemList:
			itemUIDs.append( str(itemInst.uid) )

		self.pickUpItem( player, itemUIDs )

	def notify_OtherClientForbidInteractive( self, playerID ):
		"""
		如果策划配置不允许多人交互,通知其他客户端禁止交互
		"""
		self.openEntityID = playerID
		entity = KBEngine.entities.get(playerID)
		if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			entity.otherClients.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_ROLE_IS_INTERACT)
		#self.allClients.CLIENT_RefreshBoxStatus()

	def notify_OtherClientCanInteractive( self,playerID ):
		"""
		通知其他客户端可以交互
		"""
		self.openEntityID = 0
		#self.allClients.CLIENT_RefreshBoxStatus()
		entity = KBEngine.entities.get(playerID)
		if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			entity.otherClients.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_ROLE_IS_INTERACT)