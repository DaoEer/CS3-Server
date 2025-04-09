# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEDebug
import json

class LingShiTradeDataImpl( dict ):
	"""
	"""
	def getString( self ):
		"""
		给予字符串
		"""
		data = {}
		for key, value in self.items():
			data[key] = {"uid":value["uid"], "playerDbid":value["playerDbid"], "tradeType":value["tradeType"],"amount":value["amount"],"price":value["price"],"endTime":value["endTime"],"remainTime":value["remainTime"],"earnMoney":value["earnMoney"], "sellerName":value["sellerName"]}
		return json.dumps( data )
	
	
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		data = {}
		data["items"] = []
		for o in obj.values():
			data["items"].append( o )
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = self.__class__()
		for data in dict["items"]:
			obj[data["uid"]] = data
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, LingShiTradeDataImpl )

# 自定义类型实现实例
instance = LingShiTradeDataImpl()