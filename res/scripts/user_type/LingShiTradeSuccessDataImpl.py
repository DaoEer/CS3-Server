# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEDebug
import json

class LingShiTradeSuccessDataImpl( object ):
	"""
	"""
	def __init__( self ):
		"""
		"""
		self.uid = ""
		self.amount = 0
		self.price = 0
		self.isSend = 0
		self.tradeType = -1

	def getString( self ):
		"""
		给予字符串
		"""
		data = {"uid":self.uid,"amount":self.amount, "price":self.price,"isSend":self.isSend,"tradeType":self.tradeType }
		return json.dumps( data )

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		itemDict = {"uid":obj.uid,"amount":obj.amount, "price":obj.price,"isSend":obj.isSend, "tradeType":obj.tradeType }
		return itemDict

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = LingShiTradeSuccessDataImpl()
		obj.uid = dict["uid"]
		obj.amount = dict["amount"]
		obj.price = dict["price"]
		obj.isSend = dict["isSend"]
		obj.tradeType = dict["tradeType"]
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, LingShiTradeSuccessDataImpl )

# 自定义类型实现实例
instance = LingShiTradeSuccessDataImpl()