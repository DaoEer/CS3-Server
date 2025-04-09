# -*- coding: utf-8 -*-

import KBEngine
import Monster
import csdefine
import KBEDebug
import KBEMath
import random
import Math
import CoreInterface.NPCAmbulantInterface as NPCAmbulantInterface

class MonsterExtJingShiDongKu( Monster.Monster ):
	"""
	晶石洞窟副本 特殊怪物支持
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.moveScriptID = 0
		self.detectTimeID = 0
		
	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		self.moveToSpiritCrystalPos()

	def moveToSpiritCrystalPos( self ):
		"""
		移动到掉落在地上的灵晶位置
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		if len(spaceEntity.SpiritCrystalPos) > 0:
			for posStr in spaceEntity.SpiritCrystalPos:
				pos = Math.Vector3(KBEMath.Unreal2KBEnginePosition(posStr))
				if self.position.flatDistTo( pos ) < self.getScript().getPickUpDis():
					self.startMovePos(pos)
					spaceEntity.SpiritCrystalPos.remove(posStr)
					return
		self.moveToSpiritCrystalSkyPos()

	def moveToSpiritCrystalSkyPos( self ):
		"""
		移动到天上灵晶的位置
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return

		if not self.detectTimeID:
			self.detectTimeID = self.addTimerRepeat( 0.1, "onSpecifiedState", () )
		numericalInterval = {}
		spiritCrystalPoint = list(spaceEntity.spiritCrystalPoint.keys())
		for pos in spiritCrystalPoint:
			numericalInterval[self.position.flatDistTo(pos)] = pos

		numericalList = sorted(list(numericalInterval.keys()))
		for scope in numericalList:
			if scope > self.getScript().getScopeDis():
				posStr = numericalInterval[scope]
				numericalInterval.pop(scope)
				break

		spaceEntity.spiritCrystalNum = spaceEntity.spiritCrystalPoint[posStr]
		spaceEntity.spiritCrystalPoint.pop(posStr)
		self.useSkillToPosition( 140131002, posStr )
		self.addTimerCallBack( 0.5, "startMovePos", (posStr,))

	def onSpecifiedState( self ):
		"""
		是否为某些状态
		"""
		if self.getState() == csdefine.ENTITY_STATE_FIGHT or self.getState() == csdefine.ENTITY_STATE_DEAD:
			self.stopMovingForType( self.moveScriptID )
			self.popTimer(self.detectTimeID)
			self.detectTimeID = 0

	def startMovePos( self, position, distance = 0.0, faceMovement = True, layer = 0):
		"""
		移动
		"""
		if self.touchCount < 5:
			NPCAmbulantInterface.NPCAmbulantInterface.moveStart( self, csdefine.MOVE_TYPE_MOVE_POINT, self.getSpeed(), True, ( position, distance, faceMovement, layer) )

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.NPCAmbulantInterface.doMoveOver( self, controllerID, userData )
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		if self.getState() == csdefine.ENTITY_STATE_FIGHT or self.getState() == csdefine.ENTITY_STATE_DEAD or self.touchCount >= 5:
			return
		else:
			self.moveToSpiritCrystalPos()
				