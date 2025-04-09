# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import ItemTypeEnum
import random
import KBEDebug
import ItemFactory
import csdefine
import Math

class SpaceCopyBraveDestinyLand( SpaceCopy ):
	"""
	CST-9020 勇闯夺命岛
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

	def onRoleBeKill( self, killEntity, dieEntity, amount ):
		"""
		玩家被击杀 掉落箱子
		"""
		roleItemList = dieEntity.getItemListByKBType( ItemTypeEnum.BAG_SPACE_COPY )
		if not len( roleItemList ):
			return
		resultItems = []
		for roleItem in roleItemList:
			if roleItem.id != spaceEntity.membersMgr[dieEntity.playerDBID].equipWeaponItemID:
				resultItems.append( roleItem )
		for item in resultItems:
			if item.id == spaceEntity.getScript().defaultWeapon:
				resultItems.remove(item)
				break
		
		if len( resultItems ) < amount:
			amount = len(resultItems)
		dropItems = random.sample( resultItems, amount )
		tempItemDict = {}
		for dropItem in dropItems:
			tempItemDict[dropItem.id] = 1
		if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_YCJMD:
			for itemID, amount in tempItemDict.items():
				itemInsts = dieEntity.getItemInstsByID(itemID)
				dieEntity.removeItemByAmount( itemInsts[0], amount, csdefine.ITEM_REMOVE_BY_SPACE_EVENT )
			killEntity.addBossItemDictData( tempItemDict )
			return
		itemList = []
		for itemID, amount in tempItemDict.items():
			item = ItemFactory.ItemFactoryInst.createDynamicItem( itemID,amount,{} )
			itemList.append(item)
		for item in itemList:
			items = dieEntity.getItemInstsByID( item.id )
			if not len(items):
				continue
			dieEntity.removeItemByAmount( items[0], item.amount, csdefine.ITEM_REMOVE_BY_SPACE_EVENT )

		DBIDs = []
		dropBoxEntity = self.createEntityNear( "DropBox",dieEntity.position,Math.Vector3(0,0,0),{"modelNumber":"SM_DropBox", "modelScale":1.0,"allocationItems":{},"notAllocationItems":itemList,"ownershipIDs":DBIDs,"allocation": 1})

	def setBirthInfos( self, birthInfos ):
		
		self.birthInfos.extend(birthInfos)
	
	def getBirthInfos( self ):
		"""
		获得出生点坐标
		"""
		infos = random.choice(self.birthInfos)
		self.birthInfos.remove( infos )
		return infos

	def memberEquipWeapon( self, player,skillID, equipWeaponItemID ):
		"""
		玩家装备武器
		"""
		self.membersMgr.memberEquipWeapon( player,skillID, equipWeaponItemID )

	def addYCJMDSkillBarData( self, player, index, type, id ):
		"""
		增加快捷栏数据
		"""
		self.membersMgr.addSkillBarData( player, index, type, id )

	def removeYCJMDSkillBarData( self, player, index ):
		"""
		移除快捷栏数据
		"""
		self.membersMgr.removeSkillBarData( player, index )

	def exchangeYCJMDSkillBarData( self, player, srcIndex, dstIndex ):
		"""
		交换快捷栏数据
		"""
		self.membersMgr.exchangeSkillBarData( player, srcIndex, dstIndex )
