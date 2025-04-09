# -*- coding: utf-8 -*-

class DataTypeDictBase( dict ):
	def __init__( self ):
		pass
	
	@classmethod
	def getDictFromObj( self, obj ):
		"""
		"""
		return obj
	
	@classmethod
	def createObjFromDict( self, proDict ):
		"""
		"""
		return proDict
	
	@classmethod
	def isSameType( self, obj ):
		"""
		"""
		return isinstance( obj, self.__class__ )
