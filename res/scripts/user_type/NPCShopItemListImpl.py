# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEDebug
import Functions

class NPCShopItemListImpl( dict ):
	"""
	"""
	def getString( self ):
		"""
		给予字符串
		"""
		data = {}
		for key, value in self.items():
			data[key] = {"id":value["id"], "amount":value["amount"], "startTime":value["startTime"] }
		return Functions.toJsonString( data )

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		data = {}
		data["items"] = []
		if obj:
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
			obj[data["id"]] = data
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return True
		return isinstance( obj, NPCShopItemListImpl )


class TempDict(dict):
	def __init__(self):
		dict.__init__(self)
	
	def getDictFromObj(self, obj):
		data = {"id": obj["id"], "uid": obj["uid"], "amount": obj["amount"], "bindType": obj["bindType"]}

		return data

	def createObjFromDict(self, dict):
		obj = TempDict()
		obj["id"] = dict["id"]
		obj["uid"] = dict["uid"]
		obj["amount"] = dict["amount"]
		obj["bindType"] = dict["bindType"]

		return obj

	def isSameType( self, obj ):
		if obj is None: return False
		return isinstance( obj, TempDict )


class BuyBackItemDict( dict ):
	"""
	"""
	def __init__(self):
		dict.__init__(self)

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		data = {"id": obj["id"], "uid": obj["uid"], "amount": obj["amount"], "bindType": obj["bindType"],\
					"combatPower": obj["combatPower"],\
					"attackPropertiesStr": obj["attackPropertiesStr"],\
					"attachPropertiesStr": obj["attachPropertiesStr"], "intensifyDataStr": obj["intensifyDataStr"],\
					"hardiness": obj["hardiness"]}
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = BuyBackItemDict()
		obj["id"] = dict["id"]
		obj["uid"] = dict["uid"]
		obj["amount"] = dict["amount"]
		obj["bindType"] = dict["bindType"]
		obj["combatPower"] = (dict["combatPower"] if "combatPower" in dict else 0)
		obj["attackPropertiesStr"] = (dict["attackPropertiesStr"] if "attackPropertiesStr" in dict else "")
		obj["attachPropertiesStr"] = (dict["attachPropertiesStr"] if "attachPropertiesStr" in dict else "")
		obj["intensifyDataStr"] = (dict["intensifyDataStr"] if "intensifyDataStr" in dict else "")
		obj["hardiness"] = (dict["hardiness"] if "hardiness" in dict else 0)
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, BuyBackItemDict )

class BuyBackItemList(dict):
	
	def __init__( self ):
		dict.__init__( self )

	def getDictFromObj( self, obj ):
		dict={ "buyBackItemDataList": [] }
		for d in obj["buyBackItemDataList"]:
			dict["buyBackItemDataList"].append(d)

		return dict

	def createObjFromDict( self, dict ):
		obj = BuyBackItemList()

		obj["buyBackItemDataList"] = []

		for dct in dict["buyBackItemDataList"]:
			o = BuyBackItemDict().createObjFromDict(dct)
			obj["buyBackItemDataList"].append(o)

	def isSameType( self, obj ):
		if obj is None: return False
		return isinstance( obj, BuyBackItemList )




# 自定义类型实现实例
instance = NPCShopItemListImpl()

tempDict = TempDict()

buyBackItemDict = BuyBackItemDict()

buyBackItemList = BuyBackItemList()


