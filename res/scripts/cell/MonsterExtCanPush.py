# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import csdefine
import csstatus
import Math
import math
import random
import csarithmetic
import Monster
import CoreInterface.MonsterCombatInterface as MonsterCombatInterface




class MonsterExtCanPush(  Monster.Monster ):
	"""
	可以被玩家推动的怪
	"""

	def __init__( self ):
		Monster.Monster.__init__( self )


	def onRolePushComplete(self, srcEntityID):
		"""
		exposed method
		玩家推怪物移动
		"""
		player = KBEngine.entities.get( srcEntityID )
		# if player.actionForbidSign( csdefine.ACTION_FORBID_SPELL ):
		# 	return
		yaw = csarithmetic.getYawByVector3(self.position-player.position)
		if not self.getScript().isOtherMoving(player) and self.getScript().isCanPush(self, yaw):
			pos = self.getScript().getPushPosition(self, yaw)
			self.gotoPosition(pos, 0.0, False)
		
#---------------------------重载方法-----------------------------------------------------
	def CELL_onClientEnterInitiativeTrap( self, srcEntityID, enterID ):
		"""
		exposed method
		触发客户端主动反应陷阱
		"""
		entity = KBEngine.entities.get( enterID )
		if not entity:
			return
		if not entity.isReady() or entity.inDestroying():
			return
		buffID = self.getScript().getPushBuffID(entity)
		if buffID:
			entity.addBuff( entity, buffID )
		self.pushTimer = self.addTimerCallBack( 1.5, "onRolePushComplete",( srcEntityID, ) )
		#entity.clientEntity(self.id).CLIENT_OnRoleNearbyMonster(self.id)

	def CELL_onClientLeaveInitiativeTrap( self, srcEntityID, enterID ):
		"""
		exposed method
		离开客户端主动反应陷阱
		"""
		entity = KBEngine.entities.get( enterID )
		if not entity:
			return
		if not entity.isReady() or entity.inDestroying():
			return
		buffID = self.getScript().getPushBuffID(entity)
		if buffID:
			entity.removeBuffByID( buffID )

		if self.pushTimer:
			self.popTimer(self.pushTimer)
			self.pushTimer = 0