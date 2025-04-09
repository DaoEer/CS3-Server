# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEDebug
import json

class BuyShopMallItemListImpl( object ):
	"""
	"""
	def __init__( self ):
		"""
		"""
		self.shopMallType = ""
		self.slot = ""
		self.itemType = 0
		self.itemID = 0
		self.amount = 0
		self.moneyType = 0

	def getString( self ):
		"""
		给予字符串
		"""
		data = {"shopMallType":self.shopMallType,"slot":self.slot,"itemID":self.itemID, "amount":self.amount, "moneyType":self.moneyType,"itemType":self.itemType }
		return json.dumps( data )

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		itemDict = {"shopMallType":obj.shopMallType,"slot":obj.slot,"itemID":obj.itemID, "amount":obj.amount, "moneyType":obj.moneyType, "itemType":obj.itemType }
		return itemDict

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = BuyShopMallItemListImpl()
		obj.shopMallType = dict["shopMallType"]
		obj.slot = dict["slot"]
		obj.itemID = dict["itemID"]
		obj.amount = dict["amount"]
		obj.moneyType = dict["moneyType"]
		obj.itemType = dict["itemType"]
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, BuyShopMallItemListImpl )

# 自定义类型实现实例
instance = BuyShopMallItemListImpl()