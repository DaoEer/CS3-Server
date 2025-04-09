
from KBEDebug import *
import ItemFactory
import ConfigObject.Item.ItemBase as ItemBase
import pickle

class ItemTypeImpl:
	"""
	"""
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
	
		if obj is None:
			return { "ownerID" : 0, "uid" : 0, "id" : 0, "amount" : 0, "order" : -1, "bindType":0 ,"itemEndTime":"", "dynamicData" : {}, "tempData" : {} }
	
		return obj.getDictFromObj()

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		itemID = dict.get("id", 0)
		if itemID == 0: return None
		amount = dict.get("amount", 1)
		item = ItemFactory.ItemFactoryInst.createDynamicItem( itemID, amount, dict )
		if item is None:
			ERROR_MSG("ItemTypeImpl createItem error! Item(%s) is None"%itemID )
		return item

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return True
		return isinstance( obj, ItemBase.ItemBase )


instance = ItemTypeImpl()


