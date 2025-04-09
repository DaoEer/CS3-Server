# -*- coding: utf-8 -*-


import KBEngine
import KBEDebug
#script
import Monster
import time
import csarithmetic
import csdefine
import Const
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface
import CoreInterface.NPCAmbulantInterface as NPCAmbulantInterface

class MonsterExtRotat( Monster.Monster ):
	"""
	旋转怪物
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		self.startRotator()

	def startRotator( self ):
		"""
		开始旋转
		"""
		self.startLoopRotator( self.getScript().getRotatorSpeed() )

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.NPCAmbulantInterface.doMoveOver( self, controllerID, userData )