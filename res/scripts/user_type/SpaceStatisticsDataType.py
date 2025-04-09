# -*- coding: utf-8 -*-

import SpaceStatisticsEntryDataType

class SpaceStatisticsDataType:
	"""
	副本统计数据类
	"""
	def __init__( self ):
		self.title = ""
		self.questID = 0
		self.comment = ""
		self.statisticsList = []

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		if obj is None:
			return { "title":"", "questID" : 0, "comment":"", "statisticsList":[] }
		
		if isinstance( obj, dict ):
			return obj

		_dict = {}
		_dict["title"] = obj.title
		_dict["questID"] = obj.questID
		_dict["comment"] = obj.comment
		tempList =[]
		for entry in obj.statisticsList:
			entryDict = SpaceStatisticsEntryDataType.instance.getDictFromObj( entry )
			tempList.append( entryDict )
		_dict["statisticsList"] = tempList
		return _dict
		
	def createObjFromDict( self, _dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = SpaceStatisticsDataType()
		obj.title = _dict["title"]
		obj.questID = _dict["questID"]
		obj.comment = _dict["comment"]
		for entryDict in _dict["statisticsList"]:
			entryObj = SpaceStatisticsEntryDataType.instance.createObjFromDict( entryDict )
			obj.statisticsList.append( entryObj )
		return obj
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		
		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return obj is None or isinstance( obj, ( SpaceStatisticsDataType, dict ) )

instance = SpaceStatisticsDataType()

