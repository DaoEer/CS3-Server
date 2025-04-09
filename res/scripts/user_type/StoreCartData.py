# -*- coding: utf-8 -*-

import KBEDebug
class StoreCartData( dict ):

	def getList( self):
		"""
		获得列表
		"""
		data = []
		for k,v in self.items():			
			for n,m in v.items():
				i = {}
				i["goodsType"] = k
				i["goodsID"] = n
				i["amount"] = m
				data.append( i )
		return data

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		"""
		data = {}
		data["items"] = []
		for k,v in obj.items():
			for n,m in v.items():
				i = {}
				i["goodsType"] = k
				i["goodsID"] = n
				i["amount"] = m
				data["items"].append( i )
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		"""
		obj = StoreCartData()
		for i in dict["items"]:
			if i["goodsType"] not in obj:
				obj[i["goodsType"]] = {}
			obj[i["goodsType"]][i["goodsID"]] = i["amount"]
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		"""
		if obj is None: return True
		return isinstance( obj, StoreCartData )

instance = StoreCartData()