# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyRingTaskChild import SpaceCopyRingTaskChild
import KBEngine
import KBEDebug
import Const
import Math
import Functions
import KBEMath

class SpaceCopyJSZZ( SpaceCopyRingTaskChild ):
	"""
	CST-7896 金树种子
	"""
	def __init__( self ):
		SpaceCopyRingTaskChild.__init__( self )
		self.plantCenterPos = None
		self.plantRadius = 0.0
		self.plantSkillID = 0
		self.searchSkillID = 0
		self.treeScriptID = ""
		self.rewardItemIDs = []
		self.roleReviveTime = 5.0
		self.rewardMoney = 0
		self.useItemIDs = []
		self.costItemIDs = []
		self.allCostItemIDs = []

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyRingTaskChild.initData( self, configData )
		plantCenterPosStr = configData["SpaceData"].get("plantCenterPos","")
		pos = Functions.vector3TypeConvert( plantCenterPosStr )
		if pos:
			self.plantCenterPos = pos#KBEMath.Unreal2KBEnginePosition( pos )
		else:
			KBEDebug.ERROR_MSG("space %s plantCenterPos is error"%self.scriptID)
		self.plantRadius = configData["SpaceData"].get("plantRadius",0.0)
		self.plantSkillID = configData["SpaceData"].get("plantSkillID",0)
		self.searchSkillID = configData["SpaceData"].get("searchSkillID",0)
		self.treeScriptID = configData["SpaceData"].get("treeScriptID","")
		rewardItemIDStr = configData["SpaceData"].get("rewardItemIDs","")
		if rewardItemIDStr:
			self.rewardItemIDs = [int(i) for i in rewardItemIDStr.split("|")]

		self.rewardMoney = configData["SpaceData"].get("rewardMoney",0)
		useItemIDStr = configData["SpaceData"].get("useItemIDs","")
		costItemIDData = configData["SpaceData"].get("costItemIDs","")
		if useItemIDStr:
			self.useItemIDs = [int(i) for i in useItemIDStr.split("|") ]

		if costItemIDData:
			costItemIDStrs = [i for i in costItemIDData.split("|")]
			for costItemIDStr in costItemIDStrs:
				self.costItemIDs.append([int(i) for i in costItemIDStr.split(":") ])
				self.allCostItemIDs.extend([int(i) for i in costItemIDStr.split(":") ])

	def onEnter( self, selfEntity, playerRole, packArgs ):
		treeEntitys = selfEntity.getEntityMailBoxRecord( self.treeScriptID )
		if playerRole.getClient() and not len(treeEntitys):
			playerRole.client.ShowJSZZPlantWin( self.plantCenterPos )
		if playerRole.getClient() and len(treeEntitys):
			playerRole.client.ShowJSZZProtectWin(self.rewardItemIDs)
		SpaceCopyRingTaskChild.onEnter( self, selfEntity, playerRole, packArgs )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		treeEntitys = selfEntity.getEntityMailBoxRecord( self.treeScriptID )
		if playerRole.getClient() and not len(treeEntitys):
			playerRole.client.ShowJSZZPlantWin( self.plantCenterPos )
		if playerRole.getClient() and len(treeEntitys):
			playerRole.client.ShowJSZZProtectWin(self.rewardItemIDs)
		SpaceCopyRingTaskChild.onLogin( self, selfEntity, playerRole )

	def getPlantCenterPos( self ):
		"""
		"""
		return self.plantCenterPos

	def getPlantRadius( self ):
		"""
		"""
		return float(self.plantRadius)

	def getPlantSkillID( self ):
		"""
		"""
		return self.plantSkillID

	def getSearchSkillID( self ):
		"""
		"""
		return self.searchSkillID

	def setReviveType( self ):
		"""
		设置复活类型  CST-2208
		"""
		pass

	def onPlayerGetItem( self, selfEntity, playerRole, itemInstID, amount ):
		"""
		玩家获得物品
		"""
		SpaceCopyRingTaskChild.onPlayerGetItem( self, selfEntity, playerRole, itemInstID, amount )
		if itemInstID in self.useItemIDs:  #可以使用的物品
			index = self.useItemIDs.index(itemInstID)
			costItemIDs = self.costItemIDs[index]
			itemLengths = []
			for i in range(0,len(costItemIDs)):
				itemInsts = playerRole.getItemInstsByID( costItemIDs[i] )
				itemLengths.append(len(itemInsts))
			useAmount = min(itemLengths)
			if useAmount > 0:
				itemInsts = playerRole.getItemInstsByID(itemInstID)
				itemInsts[0].addUseNumber( useAmount, playerRole )
		else:
			for i in range(0,len(self.costItemIDs)):
				if itemInstID in self.costItemIDs[i]:
					itemInsts = playerRole.getItemInstsByID(itemInstID)
					costItemIDs = self.costItemIDs[i]
					isAddUseNumber = True
					for costItemID in costItemIDs:
						costItems = playerRole.getItemInstsByID(costItemID)
						if len(costItems) < len(itemInsts):
							isAddUseNumber = False
							break
					if isAddUseNumber:
						useItemID = self.useItemIDs[i]
						useItems = playerRole.getItemInstsByID(useItemID)
						if len(useItems):
							useItems[0].addUseNumber(1,playerRole)

	def onPlayerRemoveItem( self, selfEntity, playerRole, itemInstID, amount ):
		"""
		玩家移除物品
		"""
		SpaceCopyRingTaskChild.onPlayerRemoveItem( self, selfEntity, playerRole, itemInstID, amount )
		if itemInstID not in self.allCostItemIDs:
			return
		for i in range(0,len(self.costItemIDs)):
			if itemInstID in self.costItemIDs[i]:
				itemLengths = []
				for costItemID in self.costItemIDs[i]:
					itemInsts = playerRole.getItemInstsByID( costItemID )
					itemLengths.append(len(itemInsts))
				useAmount = min(itemLengths)
				useItemID = self.useItemIDs[i]
				useItems = playerRole.getItemInstsByID(useItemID)
				if len(useItems):
					if useAmount == useItems[0].amount:
						continue
					else:
						addAmount = useAmount - useItems[0].amount
						useItems[0].addUseNumber(addAmount,playerRole)
	
	def getReviveToExitInfo( self, playerRole ):
		luckySpaceData = playerRole.queryTemp("LuckySpaceData", None)
		exitInfo = SpaceCopyRingTaskChild.getReviveToExitInfo( self, playerRole )
		if luckySpaceData is not None: exitInfo = ( luckySpaceData[1], luckySpaceData[2], luckySpaceData[3] )
		#KBEDebug.DEBUG_MSG("role %s getReviveToExitInfo %s" %(playerRole.id, exitInfo))
		return exitInfo