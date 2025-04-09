# -*- coding: utf-8 -*-

import KBEDebug

class DongFuLoseData( dict ):
	def addData( self, playerDBID, playerName, level ):
		""""""
		self.update( {playerDBID: {"dbid" :playerDBID, "name":playerName, "level":level}})
	
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
#		KBEDebug.ERROR_MSG("getDictFromObj---->>", obj)
		tempDict = {}
		tempDict["datas"] = list(obj.values())
		return  tempDict
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		解包
		"""
#		KBEDebug.ERROR_MSG("createObjFromDict---->>", proDict)
		obj = DongFuLoseData()
		for data in proDict["datas"]:
			obj[data["dbid"]] = data
		return obj
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, DongFuLoseData )

g_dongFuLoseData = DongFuLoseData()
