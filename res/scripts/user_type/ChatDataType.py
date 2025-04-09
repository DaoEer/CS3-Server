# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEDebug
import json
class ChatData:
	"""
	聊天数据类
	"""
	def __init__( self ):
		"""
		创建
		"""
		self.playerDBID = 0
		self.name = ''
		self.type = -1
		self.message = ''
		self.richText = []
		self.entityType = -1
		self.parms = {}
		
	def init( self, playerDBID, name, type, entityType, message, richText, parms ):
		"""
		初始化
		"""
		self.playerDBID = playerDBID
		self.name = name
		self.type = type
		self.entityType = entityType
		self.message = message
		self.richText = richText
		self.parms = {}
		for data in parms:
			self.parms[data["key"]] = data["value"]

	def getDict( self ):
		"""
		打包成字典
		"""
		data = {}
		data["playerDBID"] = self.playerDBID
		data["name"] = self.name
		data["type"] = self.type
		data["entityType"] = self.entityType
		data["message"] = self.message
		data["richText"] = []
		for text in self.richText:
			data["richText"].append( text )
		data["parms"] = []
		for key, value in self.parms.items():
			data["parms"].append( {"key":key, "value":value} )
		return data

	def getString( self ):
		"""
		打包成字符串
		"""
		return json.dumps( self.getDict() )

class ChatDataType:
	"""
	"""
	def getDictFromObj( self, obj ):
		"""
		The method converts a wrapper instance to a FIXED_DICT instance.

		@param obj: The obj parameter is a wrapper instance.
		@return: This method should return a dictionary(or dictionary-like object) that contains the same set of keys as a FIXED_DICT instance.
		"""
		data = obj.getDict()
		return data

	def createObjFromDict( self, dict ):
		"""
		This method converts a FIXED_DICT instance to a wrapper instance.

		@param dict: The dict parameter is a FIXED_DICT instance.
		@return: The method should return the wrapper instance constructed from the information in dict.
		"""
		obj = ChatData()
		obj.init( dict["playerDBID"], dict["name"], dict["type"], dict["entityType"], dict["message"], dict["richText"], dict["parms"] )
		return obj

	def isSameType( self, obj ):
		"""
		This method check whether an object is of the wrapper type.

		@param obj: The obj parameter in an arbitrary Python object.
		@return: This method should return true if obj is a wrapper instance.
		"""
		if obj is None: return False
		return isinstance( obj, ChatData )

# 自定义类型实现实例
instance = ChatDataType()