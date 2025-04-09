# -*- coding: utf-8 -*-

import KBEngine

class PublicActRecordDataType:
	"""
	玩家cell_public游戏记录数据类型
	"""
	def __init__( self ):
		self.recordKey = 0
		self.param1 = ""
		self.param2 = ""
		self.param3 = ""
	
	def init( self, recordKey, param1, param2, param3 ):
		self.recordKey = recordKey
		self.param1 = param1
		self.param2 = param2
		self.param3 = param3
	
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		_dict = { "recordKey" : obj.recordKey, "param1": obj.param1, "param2":  obj.param2, "param3": obj.param3 }
		return _dict

	def createObjFromDict( self, _dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = PublicActRecordDataType()
		obj.init( _dict["recordKey"], _dict["param1"], _dict["param2"], _dict["param3"] )
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isinstance( obj, PublicActRecordDataType )

instance = PublicActRecordDataType()
