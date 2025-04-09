# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEngine

class _HighBuyBackListImpl:
	"""
	基本的聊天数据类
	"""
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


# 不同的component使用不同的实例类
if KBEngine.component == "baseapp":
	# for dbmgr、baseapp
	class HighBuyBackListImpl( _HighBuyBackListImpl ): pass
else:
	# for cellapp、client
	import json
	import time
	from HighBuyBackImpl import HighBuyBackData
	class HighBuyBackList( dict ):
		"""
		高级回购列表数据类
		"""
		def __init__( self ):
			"""
			创建
			"""
			pass
			
		def init( self, items ):
			"""
			初始化
			"""
			for data in items:
				self[data.item.uid] = data

		def add( self, itemInst ):
			"""
			增加数据
			"""
			data = HighBuyBackData()
			data.init( time.time(), itemInst )
			self[itemInst.uid] = data

		def getDict( self ):
			"""
			打包成字典
			"""
			data = {}
			data["items"] = []
			for x in self.values():
				data["items"].append( x )
			return data

		def getString( self ):
			"""
			打包成字符串
			"""
			data = {}
			for key, value in self.items():
				data[key] = json.loads( value.getString() )
			return json.dumps( data )

	class HighBuyBackListImpl:
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
			obj = HighBuyBackList()
			obj.init( dict["items"] )
			return obj

		def isSameType( self, obj ):
			"""
			This method check whether an object is of the wrapper type.

			@param obj: The obj parameter in an arbitrary Python object.
			@return: This method should return true if obj is a wrapper instance.
			"""
			if obj is None: return False
			return isinstance( obj, HighBuyBackList )

# 自定义类型实现实例
instance = HighBuyBackListImpl()