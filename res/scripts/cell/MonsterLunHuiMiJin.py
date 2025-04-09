# -*- coding: utf-8 -*-
import KBEngine
import Monster
import csdefine
import Const
import KBEDebug
import Math
import math
import random
import csarithmetic
import CoreInterface.NPCAmbulantInterface as NPCAmbulantInterface


class MonsterLunHuiMiJin( Monster.Monster ):
	"""
	轮回秘境 -- 有远程攻击属性怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_ORIGIN_PET)

	def startMoveBehindPos( self, targetEntity, disPos, distance = 0.0, faceMovement = True, layer = 0 ):
		"""
		向背后移动
		"""
		diffPos = self.position - targetEntity.position
		diffPos.normalise()
		# 为表现，加入随机角度
		randomY = random.uniform( math.pi/6, -math.pi/6 )
		yaw = csarithmetic.getYawByVector3( diffPos ) + randomY
		position = Math.Vector3( self.position.x + disPos * math.sin(yaw), self.position.y, self.position.z + disPos * math.cos(yaw) )
		self.moveStart( csdefine.MOVE_TYPE_MOVE_POINT, self.getSpeed(), True, ( position, distance, faceMovement, layer) )

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.NPCAmbulantInterface.doMoveOver( self, controllerID, userData )
		self.destroySelf()