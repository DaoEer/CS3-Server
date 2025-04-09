# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import Math
import ECBProximityDefine
from ObjectScript.Trap.TrapBase import TrapBase

class ServerTriggerTrap( TrapBase ):
	"""
	由服务器判定触发的陷阱
	"""
	def __init__( self ):
		TrapBase.__init__( self )
	
	def addTrigger( self, selfEntity ):
		"""
		entity的心跳
		"""
		selfEntity.addProximityExt( int( selfEntity.triggerRadius ), 0, ECBProximityDefine.PROXIMITY_COMMON )

	def initEntity( self, selfEntity ):
		"""
		virtual method.
		陷阱初始化
		"""
		selfEntity.addTimerCallBackForScript( self.delayStartTime, "addTrigger", () )
		TrapBase.initEntity( self, selfEntity )

	def onEnterTrap( self, selfEntity, enterID ):
		"""
		virtual method.
		进入陷阱
		"""
		TrapBase.onEnterTrap( self, selfEntity, enterID )

	def onLeaveTrap( self, selfEntity, enterID ):
		"""
		virtual method.
		离开陷阱
		"""
		TrapBase.onLeaveTrap( self, selfEntity, enterID )

