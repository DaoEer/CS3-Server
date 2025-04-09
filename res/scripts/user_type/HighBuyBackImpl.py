# -*- coding: utf-8 -*-

"""
cell/base部份的ItemTypeImpl实现模块.
"""
import KBEngine

class _HighBuyBackImpl:
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
	class HighBuyBackImpl( _HighBuyBackImpl ): pass
else:
	# for cellapp、client
	import json
	import Functions
	class HighBuyBackData( dict ):
		"""
		高级回购数据类
		"""
		def __init__( self ):
			"""
			创建
			"""
			self.time = 0.0
			self.item = None
			
		def init( self, time, item ):
			"""
			初始化
			"""
			self.time = time
			self.item = item

		def getDict( self ):
			"""
			打包成字典
			"""
			data = {}
			data["time"] = self.time
			data["item"] = self.item
			return data

		def getString( self ):
			"""
			打包成字符串
			"""
			data = self.getDict()
			itemInst = data["item"]
			tempdict = {"id":str(itemInst.id), "uid":str(itemInst.uid),"amount":str(itemInst.amount), "bindType":str(itemInst.bindType), "itemOrder":"" }
			data["item"] = Functions.toJsonString( [tempdict] )
			return json.dumps( data )

	class HighBuyBackImpl:
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
			obj = HighBuyBackData()
			obj.init( dict["time"], dict["item"] )
			return obj

		def isSameType( self, obj ):
			"""
			This method check whether an object is of the wrapper type.

			@param obj: The obj parameter in an arbitrary Python object.
			@return: This method should return true if obj is a wrapper instance.
			"""
			if obj is None: return False
			return isinstance( obj, HighBuyBackData )

# 自定义类型实现实例
instance = HighBuyBackImpl()