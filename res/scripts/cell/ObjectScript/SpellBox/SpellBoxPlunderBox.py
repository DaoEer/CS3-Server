# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
from ObjectScript.SpellBox import SpellBox
import random
import ItemFactory
import csstatus
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr

class SpellBoxPlunderBox( SpellBox.SpellBox ):
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化entity
		"""
		SpellBox.SpellBox.initEntity( self, selfEntity )
		
		if self.param1 and self.param2:
			for rewardInfo in self.param1.split("|"):	#帮主配置 打赢帮会等级:奖励ID|...
				level, rewardID = rewardInfo.split(":")
				selfEntity.tongLeaderRewardData[int(level)] = rewardID
			for rewardInfo in self.param2.split("|"):	#帮会成员 打赢帮会等级:奖励ID|...
				level, rewardID = rewardInfo.split(":")
				selfEntity.tongMemberRewardData[int(level)] = rewardID
			
	def gossipWith( self, selfEntity, srcEntityID ):
		"""
		玩家点击交互
		"""
		if selfEntity.id == srcEntityID:
			return
		
		playerCell = KBEngine.entities.get( srcEntityID, None )
		if playerCell is None:
			KBEDebug.ERROR_MSG( "SpellBox::gossipWith:Can't found gossip with player entity %i!" % srcEntityID )
			return
			
		spaceEntity = playerCell.getCurrentSpace()
		if not spaceEntity:
			return
		
		#只有胜利者才能打开箱子
		winnerTongDBID = spaceEntity.getWinnerTongDBID()
		if playerCell.tongDBID != winnerTongDBID:
			playerCell.statusMessage(csstatus.TONG_PLUNDER_CAN_NOT_OPEN_BOX)
			return

		#一个玩家只能打开一个宝箱
		openBoxEntityID = spaceEntity.getOpenBoxEntityID(playerCell.playerDBID)
		if openBoxEntityID != -1 and openBoxEntityID != selfEntity.id: #已经打开过宝箱，并且不是同个宝箱
			playerCell.statusMessage(csstatus.TONG_PLUNDER_HAS_OPENED_BOX)
			return
			
		if selfEntity.belongEntityDBID != 0:
			if playerCell.playerDBID != selfEntity.belongEntityDBID:
				return
			#selfEntity.pickUpAllItems(playerCell)
			#return
			
		SpellBox.SpellBox.gossipWith( self, selfEntity, srcEntityID )

	def onPlayerIntonateOver( self, selfEntity, playerCell ):
		"""
		virtual method
		玩家吟唱结束
		"""
		selfEntity.playAction( self.param4 ) #播放开箱动作
		selfEntity.belongEntityDBID = playerCell.playerDBID
		
		spaceEntity = selfEntity.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onTriggerBox( selfEntity.id, selfEntity.scriptID )
			spaceEntity.addOpenBoxRecord(playerCell.playerDBID, selfEntity.id)

		if playerCell.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_YCJMD:
			selfEntity.YCJMDBossPickUpItem( playerCell )
			return
		
		if playerCell.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			playerCell.spaceStrategy_onTriggerBox( selfEntity.scriptID )
			
			if selfEntity.firstOpen: #第一次打开宝箱时生成物品
				extraItemList = [] #赢得对方帮会商店上的物品的一半
				if spaceEntity.getScript().getSpaceChildType() == csdefine.SPACE_TYPE_CHILD_TONG_PLUNDER:
					extraItemList = spaceEntity.getRewardItems()
				level = spaceEntity.getLoserTongLevel()
				itemList = self.getRandomReward(selfEntity, playerCell, level)
				selfEntity.spellBoxItemList.extend(extraItemList)
				selfEntity.spellBoxItemList.extend(itemList)
				selfEntity.firstOpen = False
			
			tempItemArray = []
			for itemInst in selfEntity.spellBoxItemList:
				tempDict = { "id": itemInst.id,"uid": itemInst.uid,"amount": itemInst.amount,"bindType": itemInst.bindType, "dynamicData": itemInst.getDynamicDataForClient(self) }
				tempItemArray.append( tempDict )

			if playerCell.getClient():
				playerCell.client.SendSpellBoxPickItems(selfEntity.id, tempItemArray)
				
			playerCell.setInteractiveSpellBox( selfEntity )
		
	def getRandomReward(self, selfEntity, playerCell, level):
		"""
		获取奖励
		"""
		#帮主和其他帮会成员的奖励ID不一样
		itemList = []
		rewardID = ""
		if playerCell.isTongLeader():
			rewardID = selfEntity.tongLeaderRewardData.get(level, "")
		else:
			rewardID = selfEntity.tongMemberRewardData.get(level, "")
		if rewardID:
			self.getRewardData(playerCell, rewardID, itemList)
		return itemList
			
	def getRewardData(self, playerCell, rewardID, itemList):
		"""
		"""
		rewardData = RewardMgr.g_rewardMgr.getReward( str(rewardID), {"player": playerCell} )
		if rewardData:
			for data in rewardData:
				if data["type"] == csdefine.REWARD_TYPE_CREWARD:
					self.getRewardData(player, data["goodsid"], itemList)
					continue
				if data["type"] == csdefine.REWARD_TYPE_ITEM:
					itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(data["goodsid"], data["amount"])
					itemList.append(itemInst)
