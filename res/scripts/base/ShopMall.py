import KBEngine
import KBEDebug
import time
import csdefine
from ConfigObject.ShopMall.ShopMallMgr import g_shopMallMgr

class ShopMall(
		KBEngine.Entity
	):

	def __init__( self ):
		"""
		"""
		KBEngine.Entity.__init__(self)
		self.config = None

	def init( self, shopMallTypeId, config):
		"""
		初始化
		"""
		self.shopMallTypeId = shopMallTypeId
		self.config = config
		self.reload()

	def reload( self ):
		"""
		重新加载一遍物品，纠正配置表的修改
		"""
		if self.config == None:
			return
		slotList = list( self.amountLimititems.keys() )
		for slot in self.config.keys():
			if slot in slotList:
				if self.config[slot]["itemID"] == self.amountLimititems[slot]["itemID"]:
					if self.config[slot]["openRule"].get("amountLimit",None) == None: 
						return
					if self.config[slot]["openRule"]["amountLimit"] < self.amountLimititems[slot]["amount"]:
						self.amountLimititems[slot]["amount"] = self.config[slot]["openRule"]["amountLimit"]
				else:
					self.amountLimititems[slot]["itemID"] = self.config[slot]["itemID"]
					self.amountLimititems[slot]["amount"] = self.config[slot]["openRule"]["amountLimit"]

				slotList.remove( slot )
			elif len(self.config[slot]["openRule"]) > 0:
				if self.config[slot]["openRule"].get("amountLimit",None) != None:
					self.amountLimititems[slot] = {"id":slot, "itemID":self.config[slot]["itemID"], "amount":self.config[slot]["openRule"]["amountLimit"] }

		for slot in slotList:
			del self.amountLimititems[slot]

	def getAmountLimitItemData(self):
		"""
		返回商城限量的物品数据
		"""
		return self.amountLimititems

	def getItemData( self, slot ):
		"""
		通过位置得到限量物品数据
		"""
		if slot in self.amountLimititems.keys():
			return self.amountLimititems[slot]
		return None

	def getItemConfig( self, slot ):
		"""
		通过位置得到物品配置
		"""
		if self.config == None:
			return None
		return self.config.get( slot, None)

	def getShopMallData( self ):
		"""
		获得该商场的所有数据
		"""
		slotList = list( self.items.keys() )
		for slot in slotList:
			del self.items[slot]
		for key,value in self.config.items():
			self.items[key] = {"id":key, "itemID":value["itemID"], "amount":value["amount"]}
		#获得限量的物品数据
		amountLimitItemData = self.getAmountLimitItemData()
		if len(amountLimitItemData) > 0:
			for key,value in amountLimitItemData.items():
				if self.items.get(key,None) == None:
					continue
				self.items[key] = value
		return self.items

	def reduceShopMallItem( self, slot, itemID, amount ):
		"""
		通过物品位置，id和数量减去商城有限制物品数量
		"""
		if self.reduceShopMallItemCheck(slot, itemID, amount):
			item = self.getItemData(slot)
			item["amount"] -= amount
			self.writeToDB()
			return True
		else:
			KBEDebug.ERROR_MSG("item amount %s error"%amount)
		return False
	
	def addShopMallItem( self,slot, itemID, amount ):
		"""
		通过物品位置，id和数量增加商城有限制物品数量
		"""
		item = self.getItemData( slot )
		if item["itemID"] == itemID:
			if item["amount"] >= 0:
				item["amount"] += amount
				self.writeToDB()
			return True
		return False

	def reduceShopMallItemCheck( self,slot,itemID,amount ):
		"""
		检查有限制数量的商品是否足够
		""" 
		item = self.getItemData(slot)
		if item != None:
			if item["itemID"] == itemID:
				if item["amount"] >= amount:
					return True
		return False

	def requestBuyShopMallItemPrice( self,shopMallTypeId, slot,itemID, amount, moneyType,couponUID,role ):
		"""
		请求物品的价格
		"""
		item = self.getItemConfig( slot )
		if item != None:
			if item["itemID"] == itemID:
				price = amount * g_shopMallMgr.getItemPrice( shopMallTypeId,slot,itemID,moneyType )
				#是有开放规则的物品
				if len(item["openRule"]) > 0:
					#判断该物品是否开放
					if g_shopMallMgr.IsOpen(self,item["openRule"],slot,itemID,amount):
						if item["openRule"].get("discount",None) != None:
							price = price * item["openRule"]["discount"] * amount
					else:
						KBEDebug.ERROR_MSG(" This item is not open ")
						return -1
				return price
		return -1

	def onDestroy( self ):
		"""
		销毁时
		"""
		self.destroyTime = time.time()
		#销毁之前会自动保存，这里不需要手动调用一次
		#不然安全关服会有相应的错误log
		#like:ShopMall::writeToDB(): is destroyed! entityid=21, dbid=3
		#self.writeToDB()
