# -*- coding: utf-8 -*-

from Trade import TradeObjects


class TradeObjectData:
	"""
	"""
	@classmethod
	def getDictFromObj( self, obj ):
		return obj.pickDict()

	@classmethod
	def createObjFromDict( self, dictData ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dictData: The dictData parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		tobj = TradeObjects.TradeObjectBase.TradeObjectBase.get( dictData[ "tradeObjectType" ] )
		tobj.initDict(  dictData )
		return tobj
	
	@classmethod
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isSameType(obj)


inst = TradeObjectData()