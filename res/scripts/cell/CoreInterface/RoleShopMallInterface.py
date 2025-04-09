# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
from ItemFactory import ItemFactoryInst
import json
import ItemTypeEnum
import Functions
from MsgLogger import g_logger


class RoleShopMallInterface:
	"""
	玩家商城接口类
	"""
	def __init__( self ):
		pass

	def receiveShopMallGoods( self,totalxianShiPrice,totallingShiPrice,totalxuanShiPrice,isAmountLimitItem, buyDataListStr,couponUID,targetDBID):
		"""
		<Define method>
		玩家接收商城物品验证
		@param couponUID ：优惠劵的UID
		@type couponUID：STRING

		@param totalxianShiPrice ：仙石总价格
		@type totalxianShiPrice：INT32
		@param totallingShiPrice ：灵石总价格
		@type totallingShiPrice：INT32
		@param totalxuanShiPrice ：玄石总价格
		@type totalxuanShiPrice：INT32

		@param isAmountLimitItem ：是否为限量商品
		@type isAmountLimitItem：BOOL
		"""
		try:
			buyDataList = json.loads( buyDataListStr )
		except:
			KBEDebug.ERROR_MSG("data is error")
			return
			
		if targetDBID > 0:
			itemListData = []
			for buyData in buyDataList:
				temp = {"id":buyData[2],"amount":buyData[3]}
				itemListData.append(temp)
			self.base.createGivingGoodsData( targetDBID,json.dumps(itemListData)) #通知Base 创建一条物品数据
		else:
			itemInstListMap = {}
			index = 0
			for buyData in buyDataList:
				itemInst = ItemFactoryInst.createDynamicItem( buyData[2],buyData[3] )
				if itemInst == None:
					KBEngine.globalData["ShopMallManager"].returnBuyShopMallItem( isAmountLimitItem, buyDataListStr )
					return
				#判断物品的类型
				if buyData[5] in [ItemTypeEnum.ITEM_CHENGYI,ItemTypeEnum.ITEM_WAIZHUANG,ItemTypeEnum.ITEM_FACE,ItemTypeEnum.ITEM_PENDANT,ItemTypeEnum.ITEM_DECORATION]:
					if self.isInFacadeBag(itemInst):
						KBEngine.globalData["ShopMallManager"].returnBuyShopMallItem( isAmountLimitItem, buyDataListStr )
						return
					if not self.addItemToFacadeBagCheck( itemInst ):
						KBEngine.globalData["ShopMallManager"].returnBuyShopMallItem( isAmountLimitItem, buyDataListStr )
						return
				else:
					if not self.addItemCheck(itemInst)== csstatus.ITEM_GO_ON:
						KBEngine.globalData["ShopMallManager"].returnBuyShopMallItem( isAmountLimitItem, buyDataListStr )
						return
				itemInstListMap[index] = { "itemInst":itemInst,"itemState":buyData[6],"itemType":buyData[5] }
				index += 1
			self.receiveItemToBag(itemInstListMap)	
		#else:
		#	self.base.createGivingGoodsData( targetDBID, itemInstList ) #通知Base 创建一条物品数据
		
		#g_logger.tradeShopBuyLog( self.playerDBID, self.getName(), itemIDs, itemUIDs, itemNames, itemAmounts, totalxianShiPrice, totallingShiPrice, totalxuanShiPrice, self.grade )
		
		#接收商城物品的回调，通知Base扣除金币
		self.base.receiveShopMallGoodsCB( couponUID,totalxianShiPrice,totallingShiPrice,totalxuanShiPrice)

	def receiveGoodsDataItems( self, goodsData ):
		"""
		<Define method>
		接收赠送的物品数据
		"""
		itemListData = json.loads(goodsData)
		itemInstList = []
		for itemData in itemListData:
			itemInst = ItemFactoryInst.createDynamicItem( itemData["id"],itemData["amount"] )
			if itemInst == None:
				return
			itemInstList.append( itemInst )
		#self.receiveItemToBag(itemInstList,csdefine.SHOP_GOODS_PERMANENT)

	def receiveItemToBag( self,itemInstListMap ):
		"""
		<Define method>
		添加到背包中
		@param itemInstListMap ：物品字典   { "itemInst":itemInst,"itemState":buyData[6],"itemType":buyData[5] }
				itemInst ：物品
				itemState ：物品的状态标识
		csdefine.SHOP_GOODS_PERMANENT		= 	1#表示永久购买
		csdefine.SHOP_GOODS_TEMPORARY		=	2#表示临时购买
				itemType : 物品类型  成衣、装饰等
		"""
		facadeItemList = []
		bagItemList = []
		success = False
		for itemData in itemInstListMap.values():
			#判断物品的类型
			if itemData["itemType"] in [ItemTypeEnum.ITEM_CHENGYI,ItemTypeEnum.ITEM_WAIZHUANG,ItemTypeEnum.ITEM_FACE,ItemTypeEnum.ITEM_PENDANT,ItemTypeEnum.ITEM_DECORATION] \
				and not self.isInFacadeBag(facadeItem):
				facadeItemList.append(itemData["itemInst"])
			else:
				bagItemList.append(itemData["itemInst"])
		if self.addToFacadeBagCheck(facadeItemList) and self.addToCommonBagCheck(bagItemList):
			for facadeItem in facadeItemList:
				for itemData in itemInstListMap.values():
					if facadeItem.uid == itemData["itemInst"].uid:
						self.addItemToFacadeBag(facadeItem,itemData["itemState"],itemData["itemType"])
			for bagItem in bagItemList:
				self.addItem(bagItem,csdefine.ITEM_ADD_BY_SHOPMALLTRADE)
			success = True
		return success


	def addToFacadeBagCheck( self,facadeItemList ):
		"""
		添加到外观背包检查
		"""
		if len(facadeItemList) < 0:
			return False
		for facadeItem in facadeItemList:
			if self.isInFacadeBag(facadeItem):
					return False
			if not self.addItemToFacadeBagCheck( facadeItem ):
					return False
		return True

	def addToCommonBagCheck( self,bagItemList ):
		"""
		添加到普通背包检查
		"""
		if len(bagItemList) < 0:
			return False
		for bagItem in bagItemList:
			if not self.addItemCheck(bagItem)== csstatus.ITEM_GO_ON:
				return False
		return True

	def updateShiTou( self, xianshi, lingshi, xuanshi ):
		"""
		define method
		更新属性
		"""
		self.xianshiForCell = xianshi
		self.lingshiForCell = lingshi
		self.xuanshiForCell = xuanshi
		
	def hasEnoughXianShi( self, value ):
		"""
		"""
		return self.xianshiForCell >= value
		
	def payXianShi( self, value, reason, order ):
		"""
		支付仙石
		"""
		if self.hasEnoughXianShi(value):
			self.base.payXianShiFromCell(value, reason, order)
			return True
		return False
		
	def hasEnoughLingShi( self, value ):
		"""
		"""
		return self.lingshiForCell >= value
		
	def payLingShi( self, value, reason, order ):
		"""
		支付灵石
		"""
		if self.hasEnoughLingShi(value):
			self.base.payLingShiFromCell(value, reason, order)
			return True
		return False
		
	def hasEnoughXuanShi( self, value ):
		"""
		"""
		return self.xuanshiForCell >= value
		
	def payXuanShi( self, value, reason, order ):
		"""
		支付玄石
		"""
		if self.hasEnoughXuanShi(value):
			self.base.payXuanShiFromCell(value, reason, order)
			return True
		return False
		
	def hasEnoughShiTou( self, value ):
		"""
		"""
		return self.xianshiForCell + self.lingshiForCell >= value
		
	def payShiTou( self, value, reason, order ):
		"""
		"""
		self.base.payShiTouFromCell(value, reason, order)