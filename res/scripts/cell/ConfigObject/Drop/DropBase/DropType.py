# -*- coding- : utf-8 -*-

import KBEngine
import KBEDebug
import Math
import csdefine
import random, json, copy
import Define, Const
import ItemTypeEnum
import KBEMath

from ConfigObject.Drop import DropItem
from ConfigObject.Drop import DropValue
from ConfigObject.Drop.DropBase.DropBoxConfigLoader import g_dropBoxConfigLoader


DROP_TYPE_DIRECT	=	1	#直接获得
DROP_TYPE_DROPBOX	=	2	#能过掉落箱子去拾取

class DTypeBase( object ):
	_TYPES = {}
	_USE_TYPES = {}
	def __init__( self, dtConfig, args ):
		self._dropItems = []
		self.initData( dtConfig, args )

	@classmethod
	def registerOjbect( SELF, type, classObject ):
		SELF._TYPES[ type ] = classObject

	@classmethod
	def getObject( SELF, type ):
		return SELF._TYPES.get( type, None )


	def initData( self, dtConfig, args ):
		pass

	def doDrop( self, allocationDatas, dieEntity, killer, args ):
		"""
		执行掉落
		"""
		pass

class DTypeDirect( DTypeBase ):
	"""
	直接掉落类型
	"""
	def __init__( self, dtConfig, args ):
		DTypeBase.__init__( self, dtConfig, args )
		#self._dropItems = []

	def initData( self, dtConfig, args ):
		DTypeBase.initData( self, dtConfig, args )
		for type, value in dtConfig.items():
			self._dropItems.append( DropValue.DropValueBase.getObject( type )( value ) )
			
	def doDrop( self, allocationDatas, dieEntity, killer, args ):
		"""
		执行掉落功能
		"""
		ownershipIDs = dieEntity.calculateBootyOwner()
		for ditem in self._dropItems:
			for id, dbid in ownershipIDs.items():
				extra = 0
				if dbid in allocationDatas:
					extra = allocationDatas[dbid].get( ditem.getType(), 0 )
				ditem.addValue( id, extra )
	
class DTypePickBox( DTypeBase ):
	"""
	掉落箱子类型
	"""
	def __init__( self, dtConfig, args ):
		DTypeBase.__init__( self, dtConfig, args )
		#self._dropItems = []

	def initData( self, dtConfig, args ):
		DTypeBase.initData( self, dtConfig, args )
		self.dropBoxID = args["dropBoxID"]
		
		for data in dtConfig:
			#data = {"goodsid": itemid, "amount": amount}
			self._dropItems.append( DropItem.DropItemBase.getObject( "item" )( data ) )
			
	def doDrop( self, allocationDatas, dieEntity, killer, args ):
		"""
		执行掉落功能
		"""
		#已经分配完毕的直接丢宝箱中。
		for dbid, datas in allocationDatas.items():
			for data in datas:
				itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( dieEntity, killer, args )
				self.createDropBox(dieEntity, itemInst, dbid, [dbid], csdefine.TEAM_PICKUP_TYPE_FREEDOM, dbid, 0)
				
		if not dieEntity.hasBootOwner():
			return
		
		type = dieEntity.bootyOwnerTypeObj.getType()
		allocation, allocationQuality = dieEntity.bootyOwnerTypeObj.getAllocation()
		if type == csdefine.DROP_OWNER_TYPE_PERSON:	#个人
			ownerDBID = dieEntity.bootyOwnerTypeObj.ownnerDBID
			
			for ditem in self._dropItems:
				itemInst = ditem.getItem( dieEntity, killer, args )
				self.createDropBox(dieEntity, itemInst, ownerDBID, [ownerDBID], allocation, ownerDBID, 0)
			return
		
		if type == csdefine.DROP_OWNER_TYPE_TEAM:	#队伍
			ascriptionID = dieEntity.bootyOwnerTypeObj.ownnerID
			teamCaptainDBID = dieEntity.bootyOwnerTypeObj.teamCaptainDBID
			ownershipIDs = list(dieEntity.bootyOwnerTypeObj.getOwnerIDs(dieEntity).values())
			
			#队伍只有一个人的话改为自由拾取。
			if len(ownershipIDs) <= 1: 
				allocation = csdefine.TEAM_PICKUP_TYPE_FREEDOM
			
			for ditem in self._dropItems:
				itemInst = ditem.getItem( dieEntity, killer, args )
				if allocation == csdefine.TEAM_PICKUP_TYPE_FREEDOM or itemInst.getQuality() < ItemTypeEnum.QUALITY_GREEN:
					self.createDropBox(dieEntity, itemInst, 0, ownershipIDs, csdefine.TEAM_PICKUP_TYPE_FREEDOM, ascriptionID, teamCaptainDBID)
					continue
				
				self.createTeamDropBox(dieEntity, itemInst, ownershipIDs, allocation, ascriptionID, teamCaptainDBID)
		
	def createDropBox(self, dieEntity, itemInst, ownID, ownershipIDs, allocation, ascriptionID, teamCaptainDBID ):
		"""
		创建掉落宝箱实体
		"""
		config = g_dropBoxConfigLoader.getDropBoxConfig(self.dropBoxID)
		if config is None:
			KBEDebug.ERROR_MSG( "DTypePickBox:doDrop error, not found config(%s)" %(self.dropBoxID) )
			return
		
		#策划要求绿色品质以上的物品宝箱的模型不一样
		modelNumber = config["Model"]
		if itemInst.getQuality() >= ItemTypeEnum.QUALITY_GREEN:
			modelNumber = "SK_ZW0245_2_NPC" 
		
		dropRemainTime = 120
		if int(config["RemainTime"]) > 0:
			dropRemainTime = int(config["RemainTime"])
		
		params = {
			"scriptID" 	: dieEntity.scriptID,
			"name" 		: dieEntity.getName(), 
			"isGreen"	: itemInst.getQuality() >= ItemTypeEnum.QUALITY_GREEN,
			"dropRewardOrSpaceReward" : 0,				#区分掉落:0 / 副本奖励:1
		}
		
		#策划要求同ID的物品掉落后也要分开在不同的宝箱中
		amount = itemInst.getAmount()
		for i in range(amount):
			_itemInst = copy.deepcopy(itemInst)
			_itemInst.amount = 1
			
			args = {
				"modelNumber"		: modelNumber,
				"allocation"		: allocation, 
				"ownershipIDs"		: ownershipIDs,
				"ascriptionID"		: ascriptionID,
				"teamCaptainDBID"	: teamCaptainDBID,
				"displayOnClient"	: config["IsDisplay"],
				"notAllocationItems": [] if ownID else [_itemInst],
				"allocationItems"	: {ownID:[_itemInst]} if ownID else {},
				"modelScale"		: Const.DROPBOX_START_SCALE, 
				"dropRemainTime"	: dropRemainTime,
				"params"			: params,
			}
			
			dropBox = dieEntity.createEntityNear( "DropBox", tuple(Math.Vector3(dieEntity.position)), dieEntity.direction, args )
			if dropBox is None:
				KBEDebug.ERROR_MSG("createDropBox error")
				return
		
	def createTeamDropBox(self, dieEntity, itemInst, ownerDBIDs, allocation, teamID, teamCaptainDBID):
		"""
		"""
		config = g_dropBoxConfigLoader.getDropBoxConfig(self.dropBoxID)
		if config is None:
			KBEDebug.ERROR_MSG( "DTypePickBox:doDrop error, not found config(%s)" %(self.dropBoxID) )
			return
		
		modelScale = Const.DROPBOX_START_SCALE
		#策划要求绿色品质以上的物品宝箱的模型不一样
		modelNumber = config["Model"]
		if itemInst.getQuality() >= ItemTypeEnum.QUALITY_GREEN:
			modelNumber = "SK_ZW0245_2_NPC" 
			modelScale = Const.GREEN_DROPBOX_START_SCALE
		
		args = {
			"freeAllocationItems"	: {},
			"notAllocationItems"	: {itemInst.uid:itemInst},
			"teamID"				: teamID,
			"allocation"			: allocation,
			"ownerDBIDs"			: ownerDBIDs,
			"modelScale"			: modelScale,
			"modelNumber"			: modelNumber,
			"teamCaptainDBID"		: teamCaptainDBID,
		}
		dropbox = dieEntity.createEntityNear("TeamDropBox", tuple(Math.Vector3(dieEntity.position)), dieEntity.direction, args)
		if dropbox is None:
			KBEDebug.ERROR_MSG("Create Team DropBox Fail %s, %s, %s" %(teamID, ownerDBIDs))
			return
		

DTypeBase.registerOjbect( DROP_TYPE_DIRECT, DTypeDirect )
DTypeBase.registerOjbect( DROP_TYPE_DROPBOX, DTypePickBox )