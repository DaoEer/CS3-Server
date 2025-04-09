import KBEDebug
import Functions

class PickUpItemData( dict ):
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
				"quality": obj["quality"] }

		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = PickUpItemData()
		obj["id"] = dict["id"]
		obj["uid"] = dict["uid"]
		obj["amount"] = dict["amount"]
		obj["bindType"] = dict["bindType"]
		obj["quality"] = dict["quality"]

		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, PickUpItemData )

class PickUpItemDatas(dict):
	
	def __init__( self ):
		dict.__init__( self )

	def getDictFromObj( self, obj ):
		
		dict={ "pickUpItemList": [] }

		for d in obj["pickUpItemList"]:
			dict["pickUpItemList"].append(d)

		return dict

	def createObjFromDict( self, dict ):
		obj = PickUpItemDatas()

		obj["pickUpItemList"] = []

		for dct in dict["pickUpItemList"]:
			o = PickUpItemData().createObjFromDict(dct)
			obj["pickUpItemList"].append(o)

	def isSameType( self, obj ):
		if obj is None: return False
		return isinstance( obj, PickUpItemDatas )

# 自定义类型实现实例
pickUpItemDict = PickUpItemData()

pickUpItemList = PickUpItemDatas()