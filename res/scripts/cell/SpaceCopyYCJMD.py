# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import ItemTypeEnum
import random
import KBEDebug
import ItemFactory
import csdefine
import Math

class SpaceCopyYCJMD( SpaceCopy ):
	"""
	CST-8726 勇闯夺命岛
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
		if len( roleItemList ) < amount:
			amount = len(roleItemList)
		dropItems = random.sample( roleItemList, amount )
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

	def getRecordFindBossScriptIDs( self ):
		"""
		获得已寻找的Boss的ScriptID
		"""
		return self.recordFindBossScriptIDs

	def addRecordFindBossScriptIDs( self, scriptID ):
		"""
		增加已寻找的Boss的scriptID
		"""
		if scriptID not in self.recordFindBossScriptIDs:
			self.recordFindBossScriptIDs.append( scriptID )