# -*- coding: utf-8 -*-
from NPCMoveScript import MoveBase
class MoveStopOptimize( MoveBase.MoveBase ):
	def start( self, entity ):
		"""
		开始移动
		"""
		entity.clientMoveReset()
		entity.cancelController( "Movement" )
		entity.moveControlID = 0
		return 0