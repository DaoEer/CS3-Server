# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from Trap import Trap

MAX_JUMP_LONG = 70
JUMP_HIGH = 2000.0

class TrapMYJX( Trap ):
	"""
	CST-6526 冥域缉凶 弹射机关
	"""
	def __init__( self ):
		Trap.__init__( self )
		self.curEnergy = 0 #当前充能的能量
		self.maxEnergy = 0 # 最大能量
		self.checkTimer = 0
		self.reduceTimer = 0
		self.addEnergyRecord = {}

	def setMaxEnergy( self, value ):
		"""
		设置最大能量
		"""
		self.maxEnergy = value

	def skill_onClientActorCreate( self, srcEntityID ):
		"""
		Exposed method
		自己在某客户端被创建出来
		"""
		Trap.skill_onClientActorCreate( self, srcEntityID )
		playerEntity = KBEngine.entities.get( srcEntityID )
		if not playerEntity or self.maxEnergy <= 0:
			return
		if playerEntity.getClient():
			playerEntity.client.CLIENT_UpdateMYJXEnergyBar( self.curEnergy, self.maxEnergy )

	def CELL_onEnter( self, exposed, enterID ):
		"""
		<Exposed Method>
		进入客户端陷阱
		"""
		Trap.CELL_onEnter( self, exposed, enterID )
		player = KBEngine.entities.get( enterID, None )
		if not player:
			return
		if player.getClient():
			player.client.CLIENT_ShowMYJXJumpBtn()

	def CELL_onLeave( self, exposed, enterID ):
		"""
		<Exposed Method>
		离开客户端陷阱
		"""
		Trap.CELL_onLeave( self, exposed, enterID )
		player = KBEngine.entities.get( enterID, None )
		if not player:
			return
		if player.getClient():
			player.client.CLIENT_HideMYJXJumpBtn()

	def addEnergy( self, entityID,value ):
		"""
		增加能量
		"""
		if entityID not in self.addEnergyRecord:
			self.addEnergyRecord[entityID] = 0
		if self.addEnergyRecord[entityID] >= int(self.maxEnergy/2):
			return
		if self.addEnergyRecord[entityID] + value > int(self.maxEnergy/2):
			value = int(self.maxEnergy/2) - self.addEnergyRecord[entityID]
		self.addEnergyRecord[entityID] += value
		if self.curEnergy >= self.maxEnergy:
			return
		if self.curEnergy + value < self.maxEnergy:
			self.curEnergy += value
		else:
			self.curEnergy = self.maxEnergy

		self.updateEnergyToClient()
		# if self.checkTimer:
		# 	self.popTimer( self.checkTimer )
		# 	self.checkTimer = 0
		# if self.reduceTimer:
		# 	self.popTimer( self.reduceTimer )
		# 	self.reduceTimer = 0
		#self.checkTimer = self.addTimerCallBack(2.0, "addTimerCheck",() )
		if self.reduceTimer == 0:
			self.reduceTimer = self.addTimerRepeat( 1.0,"reduceEnergy",(5,) )

	def addTimerCheck( self ):
		"""
		检查能能量
		"""
		self.reduceTimer = self.addTimerRepeat( 0.1,"reduceEnergy",(5,) )

	def reduceEnergy( self, value ):
		"""
		减少能量
		"""
		entityIDs = list(self.addEnergyRecord.keys())
		if len(entityIDs) == 1:
			if self.addEnergyRecord[entityIDs[0]] >= value:
				self.addEnergyRecord[entityIDs[0]] -= value
			else:
				self.addEnergyRecord[entityIDs[0]] = 0
		elif len( entityIDs ) == 2:
			if self.addEnergyRecord[entityIDs[0]] >= self.addEnergyRecord[entityIDs[1]]:
				if self.addEnergyRecord[entityIDs[0]] > value:
					self.addEnergyRecord[entityIDs[0]] -= value
				else:
					self.addEnergyRecord[entityIDs[0]] = 0
			elif self.addEnergyRecord[entityIDs[0]] < self.addEnergyRecord[entityIDs[1]]:
				if self.addEnergyRecord[entityIDs[1]] > value:
					self.addEnergyRecord[entityIDs[1]] -= value
				else:
					self.addEnergyRecord[entityIDs[1]] = 0
		if self.curEnergy >= value:
			self.curEnergy -= value
			self.updateEnergyToClient()
		else:
			self.curEnergy = 0
			self.updateEnergyToClient()
			if len(entityIDs) == 1:
				self.addEnergyRecord[entityIDs[0]] = 0
			elif len( entityIDs ) == 2:
				self.addEnergyRecord[entityIDs[0]] = 0
				self.addEnergyRecord[entityIDs[1]] = 0
			if self.reduceTimer:
				self.popTimer(self.reduceTimer)
				self.reduceTimer = 0
				
	def clearEnergy( self ):
		"""
		"""
		self.reduceEnergy( self.curEnergy)

	def updateEnergyToClient( self ):
		"""
		更新能量条到客户端
		"""
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		for role in spaceEntity._spaceRoles:
			if role.getClient():
				role.client.CLIENT_UpdateMYJXEnergyBar( self.curEnergy, self.maxEnergy )

	def calculateJumpLong( self ):
		"""
		计算跳的多远
		"""
		jumpLong = self.curEnergy * MAX_JUMP_LONG / self.maxEnergy
		jumpHigh = self.curEnergy * JUMP_HIGH / self.maxEnergy
		self.curEnergy = 0
		return jumpLong,jumpHigh

	