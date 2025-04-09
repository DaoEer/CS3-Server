# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug


class PassiveSkillBarDatas(dict):
	def __init__( self ):
		pass
		
	def adSkillBarData( self, dct ):
		"""
		"""
		obj = {
			"id"		: dct["id"],
			"isLock"	: dct["isLock"],
			"skillID"	: 0
		}
		self[dct["id"]] = obj
	
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		打包
		"""
		if obj is None: return {"items" : []}
		lst = []
		for id, data in obj.items():
			lst.append(data)
		return {"items" : lst}
	
	@classmethod
	def createObjFromDict( self, dct ):
		"""
		解包
		"""
		obj = PassiveSkillBarDatas()
		for data in dct["items"]:
			obj[data["id"]] = data
		return obj
	
	@classmethod
	def isSameType( self, obj ):
		"""
		比较
		"""
		return isinstance( obj, PassiveSkillBarDatas )

g_passiveSkillBarDatas = PassiveSkillBarDatas()