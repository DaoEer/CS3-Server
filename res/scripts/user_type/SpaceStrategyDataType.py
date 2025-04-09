# -*- coding: utf-8 -*-

import Define

type_to_strategy_map = {}

def MAP_STRATEGY_TYPE_TO_STRATEGY_CLASS( strategyType, classObj ):
	type_to_strategy_map[ strategyType ] = classObj


class SpaceStrategyDataType( object ):
	"""
	副本策略点数据类
	"""
	def __init__( self ):
		self.index = 0
		self.value = 0			
		self.pointBelongType = 0	#策略点归属类型
		self.describe = ""
		self.param1 = ""
		self.param2 = ""
		self.param3 = ""
		self.conditions = []
		self.rewardGrade = ""

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.
		
		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		_dict = { "implType" : obj.getType(), "index": obj.index, "value":obj.value, "pointBelongType":obj.pointBelongType,"describe": obj.describe, "param1": obj.param1, "param2": obj.param2, "param3": obj.param3,"rewardGrade":obj.rewardGrade }
		return _dict
		
	def createObjFromDict( self, _dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.
		
		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		objClass = type_to_strategy_map.get( _dict["implType"], None )
		if objClass:	# 在dbmgr里，这个值应该会为None，因此在那里面并没有任何东西可以初始化它
			obj = objClass()
			obj.init( _dict["index"], _dict )
			return obj
		return None
		
	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		
		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return obj is None or isinstance( obj, SpaceStrategyDataType )

instance = SpaceStrategyDataType()

