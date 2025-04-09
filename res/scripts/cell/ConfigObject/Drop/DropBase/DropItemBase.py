# -*- coding- : utf-8 -*-
class DropItemBase( object ):
	"""
	掉落物品类
	"""
	_TYPES = {}
	def __init__( self, configSection ):
		self._itemID = configSection[ "goodsid" ]
		self._amount = configSection[ "amount" ]

	@classmethod
	def registerOjbect( SELF, type, classOjbect ):
		SELF._TYPES[ type ] = classOjbect

	@classmethod
	def getObject( SELF, type ):
		return SELF._TYPES.get( type, None )

	def getItem( self, dieEntity, killer, args ):
		"""
		获取掉落实例 用于箱子
		"""
		pass