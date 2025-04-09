# -*- coding: utf-8 -*-
import random
import KBEDebug
import csstatus
import csdefine
import ItemTypeEnum
import ConfigObject.Item.ItemUse as ItemUse
import ItemFactory
import BaseDataStructure
import csarithmetic
from ConfigObject.Trade.TradeMgr import g_tradeMgr

from ConfigObject.Drop import DropItem
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr

class ItemMysteriousBox( ItemUse.ItemUse ):
	"""
	神秘宝盒
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		
		#神秘商人出现概率 | 神秘商人scriptID | 神秘商人没有触发时给予一个的补偿奖励ID
		temp = srcData["Param1"].split("|")
		self._mysteriousShopData = (float(temp[0]), temp[1], temp[2])
		
		#固定奖励ID
		self._rewardIDs = []
		if srcData["Param2"]:
			self._rewardIDs = srcData["Param2"].split("|")
		
		#标记是否随机到技能
		self._isShop = False	
		self._items = []
		
	def doBox( self, owner ):
		"""
		根据配置，随机得到相应的物品或者技能（召唤神秘商人）
		"""
		self._items = []
		self._isShop = False
		
		for rewardID in self._rewardIDs:
			self._items.extend(self.getItemsByRewardID(rewardID, owner))
		
		#先看看是否能随机到神秘商人
		probability = random.uniform(0, 100)
		if probability <= self._mysteriousShopData[0]:
			self._isShop = True
			return
		
		#没有随机到神秘商人，给一个补偿奖励
		if self._mysteriousShopData[2]:
			self._items.extend(self.getItemsByRewardID(self._mysteriousShopData[2], owner))
			
	def getItemsByRewardID(self, rewardID, owner):
		"""
		"""
		items = []
		rewardItemDatas = []
		def calcRewardDatas(rewardDatas):
			for data in rewardDatas:
				type = data["type"]
				amount = data["amount"]
				goodsid = data["goodsid"]
				# 物品奖励
				if type == csdefine.REWARD_TYPE_ITEM:
					rewardItemDatas.append( data )
		
		rewardDatas = RewardMgr.g_rewardMgr.getReward(rewardID, {"gift" : self, "player" : owner})
		calcRewardDatas( rewardDatas )
		for data in rewardItemDatas:
			itemInst = DropItem.DropItemBase.getObject( "item" )( data ).getItem( None, None, {} )
			items.append(itemInst)
		return items
	
	def checkUse(self, owner ):
		"""
		使用物品检测
		"""
		#判断是否正在使用其它物品
		if owner.getUsingItem():
			return csstatus.ITEM_USING_NOW
		
		self.doBox(owner)
		checkResult = ItemUse.ItemUse.checkUse( self, owner )
		if checkResult != csstatus.ITEM_USE_GO_ON_MSG:
			return checkResult
		
		return csstatus.ITEM_USE_GO_ON_MSG

	def use(self, owner, target):
		"""
		使用物品
		"""
		if len(self._items) > 0:
			status = owner.addItemListCheck(self._items)
			if status != csstatus.ITEM_GO_ON:
				owner.statusMessage(status)
				return status
			
			for itemInst in self._items:
				owner.addItem(itemInst, csdefine.ITEM_ADD_BY_SYS)
		
		if self._isShop:
			#半径2米范围内随机出一个坐标
			position = csarithmetic.getPositionByByLinks(owner.position, 0.5, 2)
			shopEntity = owner.createNPC(self._mysteriousShopData[1], position, owner.direction, {"ownerDBID" : owner.playerDBID})
			spaceEntity = owner.getCurrentSpace()
			if shopEntity and spaceEntity:
				spaceEntity.globalWorld(csstatus.MYSTERIOUS_SHOP_ZHAOHUAN_NPC, owner.playerName)
			
		owner.removeItemByAmount( self, 1, csdefine.ITEM_REMOVE_BY_USE )
		return csstatus.ITEM_USE_GO_ON_MSG
