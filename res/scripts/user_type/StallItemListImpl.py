# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEDebug

class StallItemListImpl( object ):
	"""
	"""
	def __init__( self ):
		"""
		"""
		self.itemID = 0
		self.amount = 0
		self.price = 0
		self.id = ""

	def getDict( self ):
		"""
		获取字典
		"""
		return {"id":self.id,"itemID":self.itemID, "amount":self.amount, "price":self.price }

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
 
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		itemDict = {"id":obj.id,"itemID":obj.itemID, "amount":obj.amount, "price":obj.price }
		return itemDict

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = StallItemListImpl()
		obj.id = dict["id"]
		obj.itemID = dict["itemID"]
		obj.amount = dict["amount"]
		obj.price = dict["price"]
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, StallItemListImpl )


class StalLempItemList(dict):
	def __init__( self ):
		dict.__init__(self)
		

	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		datas = []
		dict={"datas": datas}
		for d in obj["datas"]:
			dict["datas"].append(d)
		return dict
	

	def createObjFromDict( self, dict ):
		"""
		解包
		"""
		obj = self.__class__()
		obj["datas"] = []
		for dct in dict["datas"]:
			o = StallItemListImpl().createObjFromDict(dct)
			obj["datas"].append(o)
		return obj
	

	def isSameType( self, obj ):
		"""
		比较
		"""
		if obj is None: return False
		return isinstance( obj, StalLempItemList )

class TempItemDataDict(dict):
	def __init__(self):
		dict.__init__(self)

	def getDictFromObj(self, obj):
		itemDict = {"id": obj["id"], "itemID": obj["itemID"], "amount": obj["amount"], "price": obj["price"]}
		return itemDict

	def createObjFromDict(self, dict):
		obj = TempItemDataDict()
		obj["id"] = dict["id"]
		obj["itemID"] = dict["itemID"]
		obj["amount"] = dict["amount"]
		obj["price"] = dict["price"]
		return obj

	def isSameType(self, obj):
		if obj is None: return False
		return isinstance( obj, TempItemDataDict )

class SellItemDataDict( dict ):
	"""
	"""
	def __init__( self ):
		"""
		"""
		dict.__init__(self)


	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
 
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		itemDict = {"itemID": obj["itemID"], "id": obj["id"], "amount": obj["amount"], "price": obj["price"],\
					"combatPower": obj["combatPower"],\
					"attackPropertiesStr": obj["attackPropertiesStr"],\
					"attachPropertiesStr": obj["attachPropertiesStr"], "intensifyDataStr": obj["intensifyDataStr"],\
					"hardiness": obj["hardiness"]}
		return itemDict

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = SellItemDataDict()
		obj["itemID"] = dict["itemID"]
		obj["id"] = dict["id"]
		obj["amount"] = dict["amount"]
		obj["price"] = dict["price"]
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
		return isinstance( obj, SellItemDataDict )

class BuyAndSellList(dict):
	def __init__( self ):
		dict.__init__(self)
		

	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		stallCollectionItemList = []
		stallSellItemList = []
		dict={"stallCollectionItemList": stallCollectionItemList,"stallSellItemList":stallSellItemList}
		for d in obj["stallCollectionItemList"]:
			dict["stallCollectionItemList"].append(d)

		for j in obj["stallSellItemList"]:
			dict["stallSellItemList"].append(j)
		return dict
	

	def createObjFromDict( self, dict ):
		"""
		解包
		"""
		obj = self.__class__()
		obj["stallSellItemList"] = []
		obj["stallCollectionItemList"] = []
		for dct in dict["stallSellItemList"]:
			o = SellItemDataDict().createObjFromDict(dct)
			obj["stallSellItemList"].append(o)

		for d in dict["stallCollectionItemList"]:
			i = TempItemDataDict().createObjFromDict(d)
			obj["stallCollectionItemList"].append(i)
		return obj
	

	def isSameType( self, obj ):
		"""
		比较
		"""
		if obj is None: return False
		return isinstance( obj, BuyAndSellList )

class OnRequestStallItemList(dict):
	def __init__( self ):
		dict.__init__(self)
		

	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		stallCollectionItemList = []
		stallSellItemList = []
		dict={"stallCollectionItemList": stallCollectionItemList,"stallSellItemList":stallSellItemList}
		for d in obj["stallCollectionItemList"]:
			dict["stallCollectionItemList"].append(d)

		for j in obj["stallSellItemList"]:
			dict["stallSellItemList"].append(j)
		return dict
	

	def createObjFromDict( self, dict ):
		"""
		解包
		"""
		obj = self.__class__()
		obj["stallSellItemList"] = []

		for dct in dict["stallSellItemList"]:
			o = TempItemDataDict().createObjFromDict(dct)
			obj["stallSellItemList"].append(o)

		obj["stallCollectionItemList"] = []	

		for d in dict["stallCollectionItemList"]:
			i = TempItemDataDict().createObjFromDict(d)
			obj["stallCollectionItemList"].append(i)
		return obj
	

	def isSameType( self, obj ):
		"""
		比较
		"""
		if obj is None: return False
		return isinstance( obj, OnRequestStallItemList )

# 自定义类型实现实例
instance = StallItemListImpl()

LempItemData = StalLempItemList()

tempItemData = TempItemDataDict()

buyandselldict = SellItemDataDict()
	
buyandselllist = BuyAndSellList()

onRequestStallItemList = OnRequestStallItemList()