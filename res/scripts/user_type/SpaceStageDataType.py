# -*- coding: utf-8 -*-

import SpaceStageTaskDataType

class SpaceStageDataType:
	"""
	副本阶段数据类
	"""
	def __init__( self ):
		self.stageIndex = 0
		self.title = ""
		self.comment = ""
		self.tasks = []

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		if obj is None:
			return { "stageIndex":0, "title":"", "comment":"", "tasks":[] }
		
		if isinstance( obj, dict ):
			return obj

		_dict = {}
		_dict["stageIndex"] = obj.stageIndex
		_dict["title"] = obj.title
		_dict["comment"] = obj.comment
		tempList =[]
		for task in obj.tasks:
			taskDict = SpaceStageTaskDataType.instance.getDictFromObj( task )
			tempList.append( taskDict )
		_dict["tasks"] = tempList
		return _dict
		
	def createObjFromDict( self, _dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = SpaceStageDataType()
		obj.stageIndex = _dict["stageIndex"]
		obj.title = _dict["title"]
		obj.comment = _dict["comment"]
		for taskDict in _dict["tasks"]:
			taskObj = SpaceStageTaskDataType.instance.createObjFromDict( taskDict )
			obj.tasks.append( taskObj )
		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		
		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return obj is None or isinstance( obj, ( SpaceStageDataType, dict ) )

instance = SpaceStageDataType()

