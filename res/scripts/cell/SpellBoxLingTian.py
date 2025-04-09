# -*- coding: utf-8 -*-

import Math
import time
import csdefine
import KBEngine
import SpellBox
import csstatus
import ItemFactory
import Functions
import KBEDebug
import csconst
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
from LunHuiMiJin.LingTianPlantCfg import Datas as LingTianPlantDatas

class SpellBoxLingTian( SpellBox.SpellBox ):
	"""
	灵田
	"""
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )
		spaceEntity = self.getCurrentSpace()
		self.belongDBID = spaceEntity.belongDBID

	def initLTData( self, data ):
		"""初始化灵田"""
		seedNum = data.seedNum
		growthStage = data.growthStage
		growTime = data.growTime
		
		if growthStage > len( LingTianPlantDatas[str( seedNum )]["growth"] ):	#已经成熟了
			self.seedNum = seedNum
			self.growthStage = growthStage
			return
			
		growStageTime = LingTianPlantDatas[ str(seedNum )]["growth"][str( growthStage )] * 60
		while int( time.time() ) - growTime>= growStageTime:
			growthStage += 1
			growTime += growStageTime
			if growthStage > len( LingTianPlantDatas[str( seedNum )]["growth"] ):	#已经成熟了
				self.seedNum = seedNum
				self.growthStage = growthStage
				return
			growStageTime = LingTianPlantDatas[ str(seedNum )]["growth"][str( growthStage )] * 60
		self.seedNum = seedNum
		self.growthStage = growthStage
		leftTime = LingTianPlantDatas[ str(seedNum )]["growth"][str( growthStage )] * 60 - ( growTime - int( time.time() ) )
		self.endTimeStr = str( (leftTime + self.getRestTime()) * 60 * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime() )
		self.addTimerCallBack( leftTime, "onGrowUpStage", () )
				
	def getPlantState( self ):
		"""获取种子状态"""
		if self.seedNum == 0:
			return csdefine.LHMJ_PLANT_STATE_NONE
		elif self.growthStage > len(LingTianPlantDatas[str(self.seedNum)]["growth"]):
			return csdefine.LHMJ_PLANT_STATE_MATURE
		return csdefine.LHMJ_PLANT_STATE_PLANT
	
	def lingTianPlant( self, player ):
		"""
		灵田种植
		"""
		#灵田尚未开发
		if self.hasFlag( csdefine.FLAG_UNVISIBLE ):return
		
		if self.getPlantState() == csdefine.LHMJ_PLANT_STATE_PLANT :
			self.allClients.ShowGrowUpMsgUI( self.id, self.endTimeStr )
			
		elif self.getPlantState() == csdefine.LHMJ_PLANT_STATE_MATURE:		# 收获
			player.statusMessage( csstatus.LING_TIAN_COLLECTION_SUCCESS, "" )
			rewardID = LingTianPlantDatas[str( self.seedNum )]["rewardID"]
			if rewardID:
				datas = RewardMgr.g_rewardMgr.getReward( str(rewardID), {"player":player} )
				RewardMgr.g_rewardMgr.doRewards( datas, player.id, csdefine.ITEM_ADD_BY_TALKING )
			self.growthStage = 0
			self.seedNum = 0
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].removeLingTianInfo( self.belongDBID, self.scriptID )
		else:									#打开开始种植UI
			player.clientEntity(self.id).ShowLingTianPlantUI( self.id )

	def onClickPlant( self, srcEntityID, itemID ):
		"""
		exposed method
		开始种植
		"""
		player = KBEngine.entities.get( srcEntityID )
		if not player.removeItemsByItemID(itemID, 1, csdefine.ITEM_REMOVE_BY_PLANT):
			KBEDebug.ERROR_MSG("player(%d) cannot find item(%d)"%(player.id, itemID))
			return
		
		item = ItemFactory.ItemFactoryInst.createDynamicItem( itemID )
		if item is None: return
		self.seedNum, totalDuration = item.getSeedIDAndTotalDuration()
		self.growthStage = 1
		self.endTimeStr = str( totalDuration * 60 * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime() )
		
		player.statusMessage( csstatus.LING_TIAN_PLANT_SUCCESS, "" )
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].saveLingTianInfo( self.belongDBID, self.scriptID, self.seedNum, self.growthStage, int(time.time() ) )
		self.addTimerCallBack( LingTianPlantDatas[ str(self.seedNum )]["growth"][str( self.growthStage )] * 60, "onGrowUpStage", () )

	def onGrowUpStage( self ):
		"""
		生长中
		"""
		self.growthStage += 1
		if self.growthStage <= len( LingTianPlantDatas[str( self.seedNum )]["growth"] ):
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].saveLingTianInfo( self.belongDBID, self.scriptID, self.seedNum, self.growthStage, int(time.time() ) )
			self.addTimerCallBack( LingTianPlantDatas[ str(self.seedNum )]["growth"][str( self.growthStage )] * 60, "onGrowUpStage", () )
		else:
			KBEngine.globalData["SpaceLunHuiMiJinMgr"].saveLingTianInfo( self.belongDBID, self.scriptID, self.seedNum, self.growthStage, 0 )

	def getRestTime( self ):
		"""
		获取剩下的总时间
		"""
		tempTime = 0
		if self.growthStage < len( LingTianPlantDatas[str( self.seedNum )]["growth"] ):
			for temp in range( self.growthStage + 1, len( LingTianPlantDatas[str( self.seedNum )]["growth"] ) ):
				tempTime += LingTianPlantDatas[ str(self.seedNum )]["growth"][str( temp )]
		return tempTime

