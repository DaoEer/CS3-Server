# -*- coding: utf-8 -*-


type_to_class_map = {}

def MAP_TASK_TYPE_TO_TASK_CLASS( taskType, classObj ):
	type_to_class_map[ taskType ] = classObj


class SpaceStageTaskDataType:
	"""
	副本阶段任务数据类
	"""
	def __init__( self ):
		self.taskIndex = 0
		self.title = ""
		self.reqVal = 0 	#需要完成的数量
		self.val = 0		#已经完成的数量
		self.param1 = ""
		self.param2 = ""
		self.param3 = ""
		self.navigateData = ""
		self.isShowByProgressbar = 0
		self.priority = 0

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		if isinstance( obj, dict ):
			return obj

		_dict = { "implType" : obj.getType(), "taskIndex": obj.taskIndex, "title": obj.title, "reqVal":  obj.reqVal, "val": obj.val, "param1": obj.param1, "param2": obj.param2, "param3": obj.param3, "navigateData": obj.navigateData, "isShowByProgressbar":obj.isShowByProgressbar }
		return _dict

	def createObjFromDict( self, _dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		objClass = type_to_class_map.get( _dict["implType"], None )
		if objClass:	# 在dbmgr里，这个值应该会为None，因此在那里面并没有任何东西可以初始化它
			obj = objClass()
			obj.init( _dict["taskIndex"], _dict )
			return obj
		return None

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		# 在dbmgr中，这个obj应该是一个dict
		return isinstance( obj, ( SpaceStageTaskDataType, dict ) )

instance = SpaceStageTaskDataType()