
# -*- coding: utf-8 -*-
"""
技能持有效果和buff持有效果数据.
"""

import Functions

class HoldEffectDataType:
	"""
	一个持有效果的数据
	"""
	def __init__( self ):
		self.index = 0
		self.sourceType = 0
		self.sourceID = 0
		self.configIndex = 0
		self.buffIndex = 0
		self.casterID = 0
		self.param = {}
	
	def setTempData( self, key, value ):
		self.param[ key ] = value
	
	def getTempData( self, key, default = None ):
		if key in self.param:
			return self.param[key]
		return default
	
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		buffData = []
		d = { 	"index"			: obj.index,
				"sourceType"	: obj.sourceType,
				"sourceID"		: obj.sourceID,
				"configIndex"	: obj.configIndex,
				"buffIndex"		: obj.buffIndex,
				"casterID"		: obj.casterID,
				"param"			: obj.param,
			}
		return d
		
	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = HoldEffectDataType()
		obj.index = dict["index"]
		obj.sourceType = dict["sourceType"]
		obj.sourceID = dict["sourceID"]
		obj.configIndex = dict["configIndex"]
		obj.buffIndex = dict["buffIndex"]
		obj.casterID = dict["casterID"]
		obj.param = dict["param"]
		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		
		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isinstance( obj, HoldEffectDataType )


instance = HoldEffectDataType()