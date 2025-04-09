# -*- coding: utf-8 -*-
import KBEDebug
import json
import ItemFactory
import Functions
import Math

class YeZhanFengQiDataInfo5490( dict ):
	"""
	血斗凤栖镇数据 CST-5490
	"""
	def __init__( self ):
		self.roleID = 0
		self.roleMB = None
		self.roleDBID = 0
		self.kill = 0
		self.killNum = 0
		self.integral = 0
		self.roleName = ""
		self.isLogoOut = True
		self.logoOutPos = Math.Vector3(0,0,0)
		self.logoOutItemList = []
		self.isDead = True

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
		data = {"roleID":obj.roleID,"roleMB": obj.roleMB,"roleDBID":obj.roleDBID,"kill":obj.kill,"integral":obj.integral,"killNum":obj.killNum,"roleName":obj.roleName,"isDead":obj.isDead,"isLogoOut":obj.isLogoOut,"logoOutPos":obj.logoOutPos,"logoOutItemList":obj.logoOutItemList}
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = self.__class__()
		obj.roleID = dict["roleID"]
		obj.roleMB = dict["roleMB"]
		obj.roleName = dict["roleName"]
		obj.kill = dict["kill"]
		obj.killNum = dict["killNum"]
		obj.integral = dict["integral"]
		obj.roleDBID = dict["roleDBID"]
		obj.isLogoOut = dict["isLogoOut"]
		obj.logoOutPos = dict["logoOutPos"]
		obj.logoOutItemList = dict["logoOutItemList"]
		obj.isDead = dict["isDead"]
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, YeZhanFengQiDataInfo5490 )

# 自定义类型实现实例
g_yeZhanFengQiDataInfo = YeZhanFengQiDataInfo5490()