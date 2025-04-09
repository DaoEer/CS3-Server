# -*- coding: utf-8 -*-
import KBEDebug
import json
import ItemFactory
import Functions
import Math
import csdefine

class FastTeamData( object ):
	"""
	快速组队 数据类
	"""
	def __init__( self ):
		self.camp = csdefine.CMAP_NONE
		self.profession = csdefine.CLASS_UNKNOWN
		self.minLevel = 1
		self.maxLevel = 100
		self.chatType = csdefine.CHAT_TYPE_WORLD

	def getString( self ):
		"""
		打包成字符串发给客户端
		"""
		pass

	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		data = {"camp":obj.camp,"profession": obj.profession,"minLevel":obj.minLevel,"chatType":obj.chatType,"maxLevel":obj.maxLevel}
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = self.__class__()
		obj.camp = dict["camp"]
		obj.profession = dict["profession"]
		obj.minLevel = dict["minLevel"]
		obj.maxLevel = dict["maxLevel"]
		obj.chatType = dict["chatType"]
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, FastTeamData )

# 自定义类型实现实例
g_fastTeamDataInfo = FastTeamData()