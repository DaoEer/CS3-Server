# -*- coding: utf-8 -*-
#
import Math
import time
import KBEngine
import KBEDebug
import csdefine
import SpellBox
from CoreInterface.NPCAmbulantInterface import NPCAmbulantInterface

class MoveSpellBox( SpellBox.SpellBox, NPCAmbulantInterface ):
	"""
	可移动场景物件
	"""
	def __init__(self):
		SpellBox.SpellBox.__init__(self)
		NPCAmbulantInterface.__init__( self )

	def getSpeed( self ):
		"""
		获取移动速度
		"""
		return 3.0

	def moveStart( self, position, distance = 0.0, faceMovement = True, layer = 0):
		"""
		移动
		"""
		if not self.hasFlag( csdefine.FLAG_CAN_FLY ):
			moveScriptID = csdefine.MOVE_TYPE_NAVIGATE_POINT
		else:
			moveScriptID = csdefine.MOVE_TYPE_MOVE_POINT
		NPCAmbulantInterface.moveStart( self, moveScriptID, self.getSpeed(), True, ( position, distance, faceMovement, layer) )

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.doMoveOver( self, controllerID, userData )