# -*- coding: utf-8 -*-

import Const
import KBEDebug
import csstatus
import csdefine
import ItemTypeEnum
import ConfigObject.Item.ItemUse as ItemUse
import ConfigObject.Reward.RewardBase.RewardMgr as RewardMgr
import ItemFactory
import BaseDataStructure



VALUE_TYPE_REASON = {
	csdefine.REWARD_TYPE_MONEY: csdefine.MONEY_ADD_REASON_USE_GIFT_ITEM,		# 金币奖励
	csdefine.REWARD_TYPE_EXP: csdefine.EXP_ADD_REASON_USE_GIFT_ITEM,			# 经验奖励
	csdefine.REWARD_TYPE_XIUWEI: csdefine.XIUWEI_ADD_REASON_USE_GIFT_ITEM,		# 修为奖励
	csdefine.REWARD_TYPE_POTENTIAL: csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,# 潜能奖励
	csdefine.REWARD_TYPE_BANGGONG:csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,	# 帮贡奖励
	csdefine.REWARD_TYPE_TONG_MONEY:csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,# 帮会资金奖励
	csdefine.REWARD_TYPE_FEATS:csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,		# 功勋奖励
	csdefine.REWARD_TYPE_MORALE:csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,	# 气运奖励
	csdefine.REWARD_TYPE_PSIONIC : csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM, # 灵能奖励
	csdefine.REWARD_TYPE_BINDMONEY: csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM,# 绑金奖励
	csdefine.REWARD_TYPE_LINGSHI : csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM, # 灵石奖励
	csdefine.REWARD_TYPE_XUANSHI : csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM, # 玄石奖励
	csdefine.REWARD_TYPE_XIANSHI : csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM, # 仙石奖励
	csdefine.REWARD_TYPE_EXPLOIT: csdefine.POTENTIAL_ADD_REASON_USE_GIFT_ITEM, 	# 军功奖励
}

class ItemGift( ItemUse.ItemUse ):
	"""
	礼包
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self.giftID = srcData.get("Param1")	#奖励ID
		self._values = []	#根据奖励ID生成的经验等数值奖励
		self._items = []	#根据奖励ID生成的物品奖励奖励
		self._titles = []	#根据奖励ID生成的称号奖励

	def getGiftData( self, giftID, owner ):
		"""
		获取礼包数据
		"""
		args = { "gift": self, "player": owner }
		giftData = RewardMgr.g_rewardMgr.getReward( giftID, args )
		return giftData
	
	def onAddValue( self, owner ):
		"""
		玩家添加数值
		"""
		for data in self._values:
			RewardMgr.g_rewardMgr.doReward( data, owner.id, VALUE_TYPE_REASON[ data["type"] ] )

	def onAddTitle(self, owner):
		"""
		添加称号
		"""
		for data in self._titles:
			RewardMgr.g_rewardMgr.doReward(data, owner.id, "title")

	def onAddItem( self, owner ):
		"""
		往背包添加物品
		"""
		if owner.addItemListCheck(self._items) == csstatus.ITEM_GO_ON:
			for itemInst in self._items:
				if self.bindType == ItemTypeEnum.BINDED_STATE:
					itemInst.bindType = ItemTypeEnum.BINDED_STATE
				owner.addItem( itemInst, csdefine.ITEM_ADD_BY_USE_GIFT_ITEM )
				#if itemInst.__class__.__name__ == "ItemLevelGift":
					#giftData = itemInst.getGiftData(itemInst.giftID, owner)
					#itemInst.doGift(giftData, owner)
					#reqLevel = itemInst.getItemDir("ReqLevel", 1)
					#ids, amounts = itemInst.getIDAndAmount()
					#owner.showNextLevelGiftItem(reqLevel, ids, amounts)
			dct = {}
			List = []
			for i in self._items[:5]:
				itemList = owner.itemsBag.getItemByID(i.id)
				if len(itemList):
					r = {}
					r.update({"key":str(itemList[0].uid)})
					r.update({"value":i.amount})
					List.append(r)
			if List:
				dct.update({"dictData":List})
				obj = BaseDataStructure.g_dictStrInt.createObjFromDict(dct)
				owner.client.CLIENT_ShowItemListIcon(obj)
		else:
			for index, itemInst in enumerate(self._items):
				if self.bindType == ItemTypeEnum.BINDED_STATE:
					self._items[index].bindType = ItemTypeEnum.BINDED_STATE
			owner.sendRemainItemWithMail(self._items, csdefine.REMAIN_ITEM_GIFT, csdefine.ITEM_ADD_BY_USE_GIFT_ITEM)
		#self.specialItemNotify(owner)
	
	def doGift( self, giftList, owner ):
		"""
		根据得到的数据生成具体的奖励（物品或数值）
		"""
		if not giftList:
			return
		for data in giftList:
			type = data["type"]
			if type == csdefine.REWARD_TYPE_NOTHING:
				continue
			elif type == csdefine.REWARD_TYPE_CREWARD:
				for i in range( data["amount"] ):
					giftData = self.getGiftData( data["goodsid"], owner )
					self.doGift( giftData, owner )
			elif type == csdefine.REWARD_TYPE_ITEM:
				itemInst = ItemFactory.ItemFactoryInst.createDynamicItem( data["goodsid"], data["amount"] )
				self._items.append( itemInst )
			elif type == csdefine.REWARD_TYPE_TITLE:	#增加称号选项
				self._titles.append( data )
			else:
				self._values.append( data )
	
	def checkUse(self, owner ):
		"""
		使用物品检测
		"""
		self._values.clear()
		self._items.clear()
		giftData = self.getGiftData( self.giftID, owner )
		self.doGift( giftData, owner )
		#判断是否正在使用其它物品
		if owner.getUsingItem():
			return csstatus.ITEM_USING_NOW
			
		checkResult = ItemUse.ItemUse.checkUse( self, owner )
		if checkResult != csstatus.ITEM_USE_GO_ON_MSG:
			return checkResult
		return csstatus.ITEM_USE_GO_ON_MSG

	def use(self, owner, target):
		"""
		使用物品
		"""
		result = owner.addItemListCheck(self._items)
		if result != csstatus.ITEM_GO_ON:
			return result
		
		owner.removeItemByAmount( self, 1, csdefine.ITEM_REMOVE_BY_USE )
		
		self.onAddItem( owner )	
		self.onAddValue( owner )
		self.onAddTitle( owner )
		return csstatus.ITEM_USE_GO_ON_MSG
		
	def specialItemNotify(self, owner):
		"""
		"""
		if self.getItemDir("HighValue"):
			for itemInst in self._items:
				if itemInst.getQuality() >= ItemTypeEnum.QUALITY_GREEN_SHENG:
					spaceEntity = owner.getCurrentSpace()
					if spaceEntity:
						messageArg = "{}|{}|{}".format(owner.getName(), self.getItemDir("Describe"), itemInst.getItemDir("ItemName"))
						spaceEntity.globalWorld(csstatus.ITEM_ADD_IN_SPACE_OPEN_BOX, messageArg)
					if owner.getClient():
						owner.client.CLIENT_PlaySound(Const.SHENGJIE_ITEM_GET_SOUND)
						owner.client.CLIENT_PlayEffect(Const.SHENGJIE_ITEM_GET_EFFECTID)
				