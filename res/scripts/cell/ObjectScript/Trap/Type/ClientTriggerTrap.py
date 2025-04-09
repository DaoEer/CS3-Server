# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
import Math
from ObjectScript.Trap.TrapBase import TrapBase
from ObjectScript.Trap.Shape.TrapShape import g_trapShapeMgr

class ClientTriggerTrap( TrapBase ):
	"""
	由客户端判定触发服务器验证的陷阱
	"""
	def __init__( self ):
		TrapBase.__init__( self )

	def initEntity( self, selfEntity ):
		"""
		virtual method.
		陷阱初始化
		"""
		TrapBase.initEntity( self, selfEntity )

	def triggerValidate( self, selfEntity, enterEntity ):
		"""
		virtual method.
		陷阱是否触发验证
		"""
		return g_trapShapeMgr.validate( selfEntity, enterEntity  )
		
	def onEnterClientTrap( self, selfEntity, enterID ):
		"""
		virtual method.
		进入客户端陷阱
		"""
		if enterID == selfEntity.id:
			return
		
		enterEntity = KBEngine.entities.get( enterID , None )
		if enterEntity == None:
			return

		if not self.triggerValidate( selfEntity, enterEntity ):				# 客户端陷阱验证
			return

		self.onEnterTrap( selfEntity, enterID )
		
	def onLeaveClientTrap( self, selfEntity, enterID ):
		"""
		virtual method.
		离开客户端陷阱
		"""
		if enterID == selfEntity.id:
			return
		
		enterEntity = KBEngine.entities.get( enterID , None )
		if enterEntity == None:
			return

#		if self.triggerValidate( selfEntity, enterEntity ):					# 传送离开陷阱，无法通过验证！暂时去掉此验证
#			return
			
		self.onLeaveTrap( selfEntity, enterID )
