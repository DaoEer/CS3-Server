# -*- coding: utf-8 -*-

import SpellBox
import csstatus
import csdefine
import KBEngine
import KBEDebug
import ItemTypeEnum

class SpellBoxPlunderBox( SpellBox.SpellBox ):
	"""
	帮会掠夺战 宝箱
	"""
	def __init__(self):
		SpellBox.SpellBox.__init__(self)
	
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		SpellBox.SpellBox.CELL_onClientReady( self, srcEntityID )
		#if self.openEntityID:
		#	self.playAction( self.getScript().param4 )

	def pickUpItem( self, player, itemUIDs ):
		"""
		拾取物品
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		wangDaoItemUIDList = []
		for itemUID in itemUIDs:
			for itemInst in self.spellBoxItemList:
				if itemInst.uid != int(itemUID):
					continue
				
				if itemInst.getQuality() == ItemTypeEnum.QUALITY_GREEN_SHEN:
					wangDaoItemUIDList.append(itemUID)
					break
					
				status = player.addItemCheck(itemInst)
				if status == csstatus.ITEM_GO_ON:
					player.addItem(itemInst, csdefine.ITEM_ADD_BY_PICKUP)
					if player.getClient():
						player.client.OnPickUpSpellBoxItem(self.id, itemUID)
					self.spellBoxItemList.remove(itemInst)
					break
					
		if len(wangDaoItemUIDList) > 0: #王道神兵由帮主分配
			if player.getClient():
				tempMembers = []
				winnerBelongType = spaceEntity.getWinnerTongBelongSide()
				for entity in spaceEntity._spaceRoles:
					if entity.id == player.id:
						continue
					tempMembers.append({"id": entity.id, "name": entity.getName()})
				player.client.OnPickUpSpellBoxToMember(self.id, str(wangDaoItemUIDList[0]), tempMembers)
			
		self.checkSpellBox()
				
	def checkSpellBox(self):
		"""
		"""
		if not len(self.spellBoxItemList):
			if self.lifeTimerID > 0:
				self.popTimer( self.lifeTimerID )
				self.lifeTimerID = 0
			self.destroySelf()
			
	def pickUpSpellBoxToMember(self, player, uid, dstEntityID):
		"""
		分配物品给成员
		"""
		dstEntity = KBEngine.entities.get( dstEntityID, None )
		if not dstEntity:
			#player.statusMessage("","")	
			return
			
		for itemInst in self.spellBoxItemList:
			if itemInst.uid == int(uid):
				status = dstEntity.addItemCheck(itemInst)
				if status == csstatus.ITEM_GO_ON:
					dstEntity.addItem(itemInst, csdefine.ITEM_ADD_BY_PICKUP)
					if player.getClient():
						player.client.OnPickUpSpellBoxItem(self.id, itemUID)
					self.spellBoxItemList.remove(itemInst)
					break
				else:
					player.statusMessage(csstatus.ITEM_TARGET_SPACE_LESS, "")
					break
		self.checkSpellBox()
		
	def notifySpellBoxInteractiveOver( self, playerID  ):
		"""
		交互结束
		"""
		self.playAction( self.getScript().param5 )  #播放关箱动作

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
		通知其他客户端禁止交互
		"""
		entity = KBEngine.entities.get(playerID)
		if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			self.belongEntityDBID = entity.playerDBID
			entity.otherClients.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_IS_INTERACT)

	def notify_OtherClientCanInteractive( self,playerID ):
		"""
		通知其他客户端可以交互
		"""
		entity = KBEngine.entities.get(playerID)
		if entity and entity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			entity.otherClients.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_ROLE_IS_INTERACT)