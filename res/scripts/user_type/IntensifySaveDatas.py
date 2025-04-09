# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug

class IntensifySaveDatas( dict ):
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		dataList = []
		for index, data in obj.items():
			dataList.append(data)
		return { "datas" : dataList }
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		解包
		"""
		item = IntensifySaveDatas()
		for data in proDict["datas"]:
			item[data["index"]] = data
		return item
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, IntensifySaveDatas )

instance = IntensifySaveDatas()

