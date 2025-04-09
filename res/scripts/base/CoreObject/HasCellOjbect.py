# -*- coding: utf-8 -*-

"""
用于有cell对象类型的基本类型
"""

import KBEDebug
from CoreObject.GameObject import GameObject

class HasCellOjbect( GameObject ):
	def __init__( self ):
		GameObject.__init__( self )
		self._cellIsCreated = False

	def isCellCreate( self ):
		return self._cellIsCreated
	
	def doDestroyClean( self ):
		"""
		vitural method
		做销毁前的清理
		"""
		pass
	
	def destroySelf( self, hasDestroy = False ):
		if self.cell is not None:
			self.cell.destroyCellByBase()
		else:
			try:
				self.doDestroyClean()
			except AttributeError as errstr:
				KBEDebug.ERROR_MSG( "entity ( %s, %d), doDestroyClean Error : %s!!!" % ( self.__class__.__name__, self.id, errstr ) )
			
			GameObject.destroySelf( self, hasDestroy )
		
#-----------------引擎回调------------------------------------------
	def onLoseCell( self ):
		"""
		CELL丢失
		"""
		if self.cell is not None:
			self.cell.destroyCellByBase()
		else:
			self._cellIsCreated = False
			self.destroySelf()
	
	def onGetCell( self ):
		"""
		CELL创建完成
		"""
		self._cellIsCreated = True