# -*- coding: utf-8 -*-

import KBEDebug

class RoleOccupyTrainInfo( object ):
	"""
	玩家占领练兵场数据
	"""
	def __init__( self ):
		"""
		"""
		self.occupyTrainLineNumber = 0
		self.occupyTrainIndex = -1

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		tempDict = {}
		tempDict["occupyTrainLineNumber"] = obj.occupyTrainLineNumber
		tempDict["occupyTrainIndex"] = obj.occupyTrainIndex
		return tempDict

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = RoleOccupyTrainInfo()
		obj.occupyTrainLineNumber = dict["occupyTrainLineNumber"]
		obj.occupyTrainIndex = dict["occupyTrainIndex"]
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, RoleOccupyTrainInfo )


# 自定义类型实现实例
instance = RoleOccupyTrainInfo()