# -*- coding: utf-8 -*-
import Math

import csdefine
from NPCMoveScript import MoveBase

import KBEDebug
import KBEngine

class MoveFightDisperse( MoveBase.MoveBase ):
	#小怪物追击及散开表现
	def start( self, entity, selectMovePos, selectStyle ):
		"""
		vitural  method
		开始移动
		"""
		if entity.hasFlag(csdefine.FLAG_CAN_FLY):
			moveControlID = entity.moveToPointExt( selectMovePos,  entity.moveSpeed,  0.1, True )
		else:
			moveControlID = entity.navigatePointExt( selectMovePos,  entity.moveSpeed, 0.1, True )
		
		return moveControlID

	def getMovePosition( self, entity, selectMovePos, selectStyle ):
		"""
		vitural  method
		获得目标位置
		"""
		return selectMovePos