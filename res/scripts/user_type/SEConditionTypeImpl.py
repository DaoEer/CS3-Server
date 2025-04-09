# -*- coding: utf-8 -*-

import KBEngine

if KBEngine.component == "cellapp":
	
	def getDictFromObj( obj ):
		"""
		"""
		if obj is None:
			return {"id" : 0, "param1" : "", "param2" : "", "param3" : "", "param4" : ""}
		return { "id" : obj.id, "param1" : str(obj.param1), "param2" : str(obj.param2), "param3" : str(obj.param3), "param4" : str(obj.param4) }
	
	def createObjFromDict( dictData ):
		""""""
		from ConfigObject.SpaceEvent.SpaceEventConditionsLoader import g_SEConditionsLoader
		obj = g_SEConditionsLoader.createConditionObj( dictData["id"], dictData )
		return obj

	def isSameType( obj ):
		""""""
		if obj is None: return True
		from ConfigObject.SpaceEvent.SpaceEventBase.SEConditions.SEConditionBase import SEConditionBase
		return isinstance( obj, SEConditionBase )

else:
	def getDictFromObj( obj ):
		"""
		"""
		return obj
	
	def createObjFromDict( dictData ):
		""""""
		return dictData

	def isSameType( obj ):
		""""""
		return True

class SEConditionTypeImpl:
	"""
	实现cell部份的副本事件条件数据的创建、还原
	"""
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		return getDictFromObj( obj )

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		return createObjFromDict( dict )

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.
		
		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		return isSameType( obj )

instance = SEConditionTypeImpl()
	