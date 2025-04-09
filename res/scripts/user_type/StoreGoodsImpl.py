# -*- coding: utf-8 -*-
import Functions




class StoreGoodsImpl(dict):
	"""
	商城商品
	"""
	def __init__(self):
		self.ID 				= 0
		self.GoodsType  		= 0
		self.GoodsState 		= 0
		self.ItemType  			= 0
		self.ItemID	 			= 0
		self.Price 				= 0
		self.LimitTime 			= ""
		self.LimitAmount 		= -1
		self.ServeLimitAmount 	= -1
		self.DiscountTime 		= ""
		self.DiscountPrice 		= 0
		self.RefreshType 		= 0
		self.Description 		= ""
		self.ThirdLable 		= 0
		self.RebateRate 		= 0.0


	def initData( self, data ):
		self.ID = data["ID"]
		self.GoodsType = data["GoodsType"]
		self.GoodsState = data["GoodsState"]
		self.ItemType = data["ItemType"]
		self.ItemID = data["ItemID"]
		self.Price = data["Price"]
		self.LimitTime = data["LimitTime"]
		self.LimitAmount = data["LimitAmount"]
		self.ServeLimitAmount = data["ServeLimitAmount"]
		self.DiscountTime = data["DiscountTime"]
		self.DiscountPrice = data["DiscountPrice"] if data["DiscountPrice"] > 0 else data["Price"]
		self.RefreshType = data["RefreshType"]
		self.Description = data["Description"]
		self.ThirdLable = data["ThirdLable"]
		self.RebateRate = data["RebateRate"]


	def pickDataForClient( self ):
		data = {}
		data["ID"] = self.ID
		data["GoodsType"] = self.GoodsType
		data["GoodsState"] = self.GoodsState
		data["ItemType"] = self.ItemType
		data["ItemID"] = self.ItemID
		data["Price"] = self.Price
		data["LimitTime"]	= self.LimitTime
		data["LimitAmount"] = self.LimitAmount
		data["ServeLimitAmount"] = self.ServeLimitAmount
		data["DiscountTime"] = self.DiscountTime
		data["DiscountPrice"] = self.DiscountPrice
		data["RefreshType"] = self.RefreshType
		data["Description"] = self.Description
		data["ThirdLable"] = self.ThirdLable
		data["RebateRate"] = self.RebateRate

		return data

	@classmethod
	def getDictFromObj( self, obj ):
		return obj.pickDataForClient()

	@classmethod
	def createObjFromDict( self, data ):
		obj = StoreGoodsImpl()
		obj.initData( data )
		return obj


	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		"""
		if obj is None: return True
		return isinstance( obj, StoreGoodsImpl )

instance = StoreGoodsImpl()