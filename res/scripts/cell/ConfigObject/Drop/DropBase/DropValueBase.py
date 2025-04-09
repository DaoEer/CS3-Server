# -*- coding- : utf-8 -*-

class DropValueBase( object ):
	"""
	掉落数值类
	"""
	_TYPES = {}
	def __init__( self, value ):
		self._value = value
	
	@classmethod
	def registerOjbect( SELF, type, classOjbect ):
		SELF._TYPES[ type ] = classOjbect

	@classmethod
	def getObject( SELF, type ):
		return SELF._TYPES.get( type, None )
		
	def addValue( self, entityList ):
		"""
		处理掉落
		"""
		pass