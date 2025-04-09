# -*- coding- : utf-8 -*-

from ConfigObject.Drop.DropBase import DropType


DROP_TYPE_DIRECT	=	1	#直接获得
DROP_TYPE_DROPBOX	=	2	#能过掉落箱子去拾取

class DropObject( object ):
	def __init__( self, objConfig ):
		self._dropTypesInfos = {}
		self.initData( objConfig )

	def initData( self, objConfig ):
		self._dropTypesInfos[ DROP_TYPE_DIRECT ] = DropType.DTypeBase.getObject( DROP_TYPE_DIRECT )( dtSec )
		self._dropTypesInfos[ DROP_TYPE_DROPBOX ] = DropType.DTypeBase.getObject( DROP_TYPE_DROPBOX )( dtSec )

	
	def doDrop( self, dieEntity, killer, args ):
		"""
		执行掉落处理
		"""
		for t, tobj in self._dropTypesInfos.items():
			tobj.doDrop( dieEntity, killer, args )
