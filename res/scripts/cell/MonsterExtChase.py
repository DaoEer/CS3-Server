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

class MonsterExtChase( Monster.Monster ):
	"""
	追击目标怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def setTargetID(self, newTargetID):
		"""
		设置攻击目标ID
		"""
		self.targetID  = newTargetID
		self.chaseTargetEntity( self.targetID )

	def chaseTargetEntity( self, targetID ):
		"""
		追击目标
		"""
		targetEntity = KBEngine.entities.get( targetID, None )
		if targetEntity:
			self.chaseEntity( targetEntity, 1.0 )

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		self.doMoveOver( controllerID, userData )
		MonsterCombatInterface.MonsterCombatInterface.doMoveOver( self, controllerID, userData )

	def doMoveOver( self, controllerID, moveScriptID ):
		"""
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		if moveScriptID == csdefine.MOVE_TYPE_CHASE:
			return
		self.moveControlID = 0
		if self.moveScriptID == moveScriptID: #如果当前是在循环/多次移动，则回调到移动的tick里面
			self.getMoveScript().over( self, *self.moveArgs )