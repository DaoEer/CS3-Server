# -*- coding: utf-8 -*-
"""
 ĿǰKBEngine��֧��cell���ݶ�̬Ǩ�ƣ������ⲿ�ֿ�����
"""
import KBEngine


if KBEngine.component in set( ["db", "baseapp"] ):
	class SpawnPointDataType:
		def getDictFromObj( self, obj ):
			"""
			The method converts a wrapper instance to a FIXED_DICT instance.
			
			@param obj: The obj parameter is a wrapper instance.
			@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
			"""
			return obj
			
		def createObjFromDict( self, dict ):
			"""
			This method converts a FIXED_DICT instance to a wrapper instance.
			
			@param dict: The dict parameter is a FIXED_DICT instance.
			@return: The method should return the wrapper instance constructed from the information in dict.
			"""
			return dict
			
		def isSameType( self, obj ):
			"""
			This method check whether an object is of the wrapper type.
			@param obj: The obj parameter in an arbitrary Python object.
			@return: This method should return true if obj is a wrapper instance.
			"""
			return True
else:
	class SpawnPointDataType:
		def getDictFromObj( self, obj ):
			"""
			The method converts a wrapper instance to a FIXED_DICT instance.
			
			@param obj: The obj parameter is a wrapper instance.
			@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
			"""
			dict = {}
			dict["_entityType"] = obj._entityType
			dict["scriptID"] = obj.scriptID
			dict["spawnDict"] = obj.spawnDict
			dict["entityID"] = obj.entityID
			return dict
			
		def createObjFromDict( self, dict ):
			"""
			This method converts a FIXED_DICT instance to a wrapper instance.
			
			@param dict: The dict parameter is a FIXED_DICT instance.
			@return: The method should return the wrapper instance constructed from the information in dict.
			"""
			from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory
			obj = g_spawnPointFactory.getSpawnPointFunc( dict["_entityType"] )()
			obj.initData( dict[ "spawnDict" ] )
			obj.entityID = dict[ "entityID" ]
			return obj
			
		def isSameType( self, obj ):
			"""
			This method check whether an object is of the wrapper type.
			
			@param obj: The obj parameter in an arbitrary Python object.
			@return: This method should return true if obj is a wrapper instance.
			"""
			from ObjectScript.SpawnPoint.SpawnBase import SpawnBase
			return isinstance( obj, SpawnBase )
		
instance = SpawnPointDataType()