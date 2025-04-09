# -*- coding: utf-8 -*-

import csdefine
import csstatus
import KBEDebug
import KBEngine
from ObjectScript.SpellBox import SpellBox
import random
import ItemFactory

class SpellBoxPickItem( SpellBox.SpellBox ):
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化entity
		"""
		SpellBox.SpellBox.initEntity( self, selfEntity )
		if self.param1 and self.param2 and self.param3:
			itemIDs = [int(i) for i in self.param1.split("|")] 			#物品ID
			amounts = [int(i) for i in self.param2.split("|")]			#物品数量
			probabilitys = [float(i) for i in self.param3.split("|") ]  #物品概率
			for itemID in itemIDs:
				index = itemIDs.index(itemID)
				temp = random.uniform(0,1)
				if temp < probabilitys[index]:
					itemInst = ItemFactory.ItemFactoryInst.createDynamicItem( itemID, amounts[index])
					selfEntity.spellBoxItemList.append(itemInst )

			if not len( selfEntity.spellBoxItemList ):
				itemID = random.choice( itemIDs )
				index = itemIDs.index( itemID )
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem( itemID, amounts[index])
				selfEntity.spellBoxItemList.append(itemInst )


	def gossipWith( self, selfEntity, srcEntityID ):
		"""
		玩家点击交互
		"""
		if selfEntity.openEntityID:
			playerCell = KBEngine.entities.get( srcEntityID, None )
			if not playerCell:
				return
			selfEntity.pickUpAllItems(playerCell)
			return
		SpellBox.SpellBox.gossipWith( self, selfEntity, srcEntityID )

	def onPlayerIntonateOver( self, selfEntity, playerCell ):
		"""
		virtual method
		玩家吟唱结束
		"""
		selfEntity.playAction( self.param4 ) #播放开箱动作
		selfEntity.openEntityID = playerCell.id
		spaceEntity = selfEntity.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onTriggerBox( selfEntity.id, selfEntity.scriptID )

		if playerCell.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_YCJMD:
			selfEntity.YCJMDBossPickUpItem( playerCell )
			return

		if playerCell.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			playerCell.spaceStrategy_onTriggerBox( selfEntity.scriptID )

			tempItemArray = []
			for itemInst in selfEntity.spellBoxItemList:
				tempDict = { "id":itemInst.id,"uid":itemInst.uid,"amount":itemInst.amount,"bindType":itemInst.bindType, "dynamicData":itemInst.getDynamicDataForClient( self ) }
				tempItemArray.append( tempDict )

			if playerCell.getClient():
				playerCell.client.SendSpellBoxPickItems( selfEntity.id,tempItemArray )

			playerCell.setInteractiveSpellBox( selfEntity )

	def onLifeTimeCB( self, selfEntity ):
		"""
		virtual method
		生存时间到达
		"""
		selfEntity.lifeTimerID = 0
		if selfEntity.cooldownTime < 0:
			selfEntity.destroySelf()
			return
		spaceEntity = selfEntity.getCurrentSpace()
		if not spaceEntity:
			return
		cooldownTime = selfEntity.cooldownTime
		position = selfEntity.position
		direction = selfEntity.direction
		spaceEntity.addTimerCallBack( cooldownTime,"createSpellBox",( selfEntity.scriptID,position,direction,{} ) )
		selfEntity.destroySelf()


	def pickUpItem( self, selfEntity, player, itemUIDs ):
		"""
		拾取物品
		"""
		for itemUID in itemUIDs:
			for itemInst in selfEntity.spellBoxItemList:
				if itemInst.uid != int(itemUID):
					continue
				status = player.addItemCheck( itemInst )
				if status == csstatus.ITEM_GO_ON:
					player.addItem( itemInst, csdefine.ITEM_ADD_BY_PICKUP )
					if player.getClient():
						player.client.OnPickUpSpellBoxItem( selfEntity.id,itemUID )
					selfEntity.spellBoxItemList.remove(itemInst)
					break

		if not len(selfEntity.spellBoxItemList):
			spaceEntity = selfEntity.getCurrentSpace()
			if selfEntity.cooldownTime < 0:
				player.clearInteractiveSpellBox()
				selfEntity.destroySelf()
				return
			if not spaceEntity:
				return
			cooldownTime = selfEntity.cooldownTime
			position = selfEntity.position
			direction = selfEntity.direction
			if selfEntity.lifeTimerID > 0:
				selfEntity.popTimer( selfEntity.lifeTimerID )
				selfEntity.lifeTimerID = 0
			spaceEntity.addTimerCallBack( cooldownTime,"createSpellBox",( selfEntity.scriptID,position,direction,{} ) )
			player.clearInteractiveSpellBox()
			selfEntity.destroySelf()