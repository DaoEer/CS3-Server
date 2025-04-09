# -*- coding: utf-8 -*-

import time
import KBEMath
import KBEDebug
import KBEngine
import csdefine
import Const
import csconst
import Functions
import csstatus
import Define
from ObjectScript.Space.SpaceCopy import SpaceCopy

class SpaceCopyTrainingGroundSave( SpaceCopy ):
	"""
	练兵场 布防图
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.itemDatas = {}				# { itemID : num }
		self.itemInfos =  {}			# { scriptID : itemID }
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		itemDatas = configData["SpaceData"].get( "ItemDatas", "" )
		if itemDatas:
			itemStrList = itemDatas.split("|") 
			for itemStr in itemStrList:
				iStr = itemStr.split(":")
				if len(iStr) >= 2:
					self.itemDatas.update({ int(iStr[0]) : int(iStr[1])})
					
		itemInfos = configData["SpaceData"].get( "ItemInfos", "" )
		if itemInfos:
			itemStrList = itemInfos.split("|") 
			for itemStr in itemStrList:
				iStr = itemStr.split(":")
				if len(iStr) >= 2:
					self.itemInfos.update({ iStr[0] : int(iStr[1])})
		
	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		KBEngine.globalData["TrainSoldierGroundManager"].requestSpaceNPCInfo( selfEntity, selfEntity.belongDBID, selfEntity.scriptID )
		
	def onRequestSpaceNPCInfo( self, selfEntity, spaceData ):
		"""
		请求保存的数据回调
		"""
		for playerRole in selfEntity._spaceRoles:
			self.addPlayerItem(selfEntity, playerRole)
		
	def onEnter( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家进入副本
		"""
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		if selfEntity.isInitNPC:				# 如果初始化了 副本保存数据！就添加物品
			self.addPlayerItem(selfEntity, playerRole)

	def addPlayerItem( self, selfEntity, playerRole):
		"""给玩家布防的物品"""
		itemDatas = dict( self.itemDatas )
		for scriptID, num in selfEntity.hasSaveNPC.items():				# 去除已经布防的物品
			if scriptID in self.itemInfos:
				itemID = self.itemInfos[scriptID]
				if itemID in itemDatas:
					itemDatas[itemID] -= num
					if itemDatas[itemID] <= 0:
						itemDatas.pop(itemID)
		for itemID, num in itemDatas.items():
			playerRole.addItemByID( itemID, num )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		spaceNPCInfo = {}
		spaceNPCInfo["spaceDatas"] = []
		saveScriptIDs = list(self.itemInfos.keys())
		for scriptID, mBoxs in selfEntity.getAllEntityMailBoxRecord().items():
			if scriptID in saveScriptIDs:
				for mBox in mBoxs:
					temp = {}
					temp["scriptID"] = scriptID
					temp["position"] = mBox.position
					temp["direction"] = mBox.direction
					temp["createArgs"] = {}
					spaceNPCInfo["spaceDatas"].append( temp )
			
		if spaceNPCInfo["spaceDatas"]:
			spaceNPCInfo["belongDBID"] = selfEntity.belongDBID
			spaceNPCInfo["spaceScriptID"] = selfEntity.scriptID
			KBEngine.globalData["TrainSoldierGroundManager"].saveSpaceNPCInfo( spaceNPCInfo )
			
		SpaceCopy.onLeave(self, selfEntity, playerRole, packArgs )
		
	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		if selfEntity.isInitNPC:				# 如果初始化了 副本保存数据！就添加物品
			self.addPlayerItem(selfEntity, playerRole)
			
