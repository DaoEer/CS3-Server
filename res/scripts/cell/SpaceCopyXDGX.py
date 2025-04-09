# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopyRingTask import SpaceCopyRingTask
import csdefine
import Math
import random
import math
import csarithmetic

class SpaceCopyXDGX( SpaceCopyRingTask ):
	"""
	环任务【仙岛归墟】
	X列 Y行
	"""
	def __init__( self ) :
		SpaceCopyRingTask.__init__( self )
		self.floorIDList = []
		self.totalFloorIDList = []
		self.destroyFloorIDList = []
		self.stopTime = 0.0
		self.alreadyStopTime = 0.0 #已停止销毁的时间
		self.alreadyStopTimer = 0

	def onTeleportCompleted( self, playerRole ):
		SpaceCopyRingTask.onTeleportCompleted( self, playerRole )
		if playerRole.getClient():
			playerRole.client.Client_CreateFloor(self.getScript().getGridLenNumber(), self.getScript().getGridWidNumber())

	def firstFloorPosition( self, firstFloorPos, gridLenth, gridWidth ):
		"""
		第一个格子的的坐标和长度和宽度
		"""
		self.firstFloorPos = firstFloorPos
		self.gridWidth = gridWidth
		self.gridLength = gridLenth
		for x in range(0,self.getScript().getGridWidNumber() * self.getScript().getGridLenNumber() ):
			self.floorIDList.append(x)
			self.totalFloorIDList.append(x)

		self.startRandomDestroyFloor(self.getScript().getDelyTime(),self.getScript().getDestroyGrideNum()  )

	def startRandomDestroyFloor( self, time , destroyGrideNum ):
		"""
		开始随机销毁格子
		"""
		self.randomDestroyFloorTimerID = self.addTimerRepeat( time,"randomDestroyFloor",(destroyGrideNum,) )

	def randomDestroyFloor( self, destroyGrideNum ):
		"""
		随机销毁格子
		"""
		if len(self.floorIDList) < destroyGrideNum:
			if self.randomDestroyFloorTimerID:
				self.popTimer(self.randomDestroyFloorTimerID)
				self.randomDestroyFloorTimerID = 0
			for floorID in self.floorIDList:
				self.removeFloorByFloorID( floorID )
			return
		random.shuffle(self.floorIDList)
		floorIDList = random.sample( self.floorIDList,destroyGrideNum )
		for floorID in floorIDList:
			self.removeFloorByFloorID( floorID )

	def stopRandomDestroyFloor( self, stopTime ):
		"""
		停止销毁格子
		"""
		if self.randomDestroyFloorTimerID:
			self.popTimer(self.randomDestroyFloorTimerID)
			self.randomDestroyFloorTimerID = 0
		if self.alreadyStopTimer:
			self.popTimer( self.alreadyStopTimer )
			self.alreadyStopTimer = 0
			self.alreadyStopTime = 0.0
		self.stopTime = stopTime
		self.alreadyStopTimer = self.addTimerRepeat(1.0,"addAlreadyStopTime",())
		for role in self._spaceRoles:
			if role.getClient():
				role.client.CLIENT_ShowStopDestroyFloorTime( stopTime )

	def addAlreadyStopTime( self ):
		"""
		"""
		self.alreadyStopTime += 1.0
		if self.alreadyStopTime == self.stopTime:
			self.stopTime = 0.0
			self.alreadyStopTime = 0.0
			self.popTimer( self.alreadyStopTimer )
			self.alreadyStopTimer = 0

	def removeFloorByFloorID( self, floorID ):
		"""
		移除格子
		"""
		if floorID in self.floorIDList:
			self.floorIDList.remove(floorID)
			for role in self._spaceRoles:
				if role.getClient():
					role.client.Client_RemoveFloor( floorID )
		if floorID not in self.destroyFloorIDList:
			self.destroyFloorIDList.append(floorID)

		self.destroyAllFloorEntity( floorID )

	def addFloorID( self, floorID ):
		"""
		增加格子
		"""
		if floorID in self.floorIDList:
			return
		self.floorIDList.append(floorID)
		for role in self._spaceRoles:
			if role.getClient():
				role.client.Client_AddFloor( floorID )
		if floorID in self.destroyFloorIDList:
			self.destroyFloorIDList.remove(floorID)

	def getFloorPositionByFloorID( self, floorID ):
		"""
		通过floorID 获得 格子的位置
		"""
		x = floorID // self.getScript().getGridWidNumber()
		y = floorID - self.getScript().getGridWidNumber() * x
		position = Math.Vector3( self.firstFloorPos.x + self.gridWidth * x + 2.0,self.firstFloorPos.y + 5.54, self.firstFloorPos.z + self.gridLength * y +0.02 )
		return position

	def getFloorIDListByRange( self, range, srcPos ):
		"""
		获得销毁的格子列表  通过某个范围
		"""
		tempFloorIDList = []
		for floorID in self.floorIDList:
			dstPos = self.getFloorPositionByFloorID(floorID)
			if srcPos.flatDistTo(dstPos) < range:
				tempFloorIDList.append(floorID)
		return tempFloorIDList

	def getFillFloorID( self, position ):
		"""
		填充格子
		"""
		floorID = -1
		vectorPos = position - self.firstFloorPos
		x = round(vectorPos.x/self.gridLength)
		y = round(vectorPos.z/self.gridWidth)
		floorID = x *self.getScript().getGridWidNumber() + y
		if floorID not in self.totalFloorIDList:
			return -1
		return floorID

	def isInFloorIDList( self, floorID ):
		"""
		"""
		if floorID in self.floorIDList or floorID not in self.totalFloorIDList:
			return True
		return False

	def destroyAllFloorEntity( self, floorID ):
		"""
		销毁格子上的所有DropBox
		"""
		floorPos = self.getFloorPositionByFloorID(floorID)
		dropBoxs = self.getEntityMailBoxRecord("") #掉落的箱子
		tempDropList = []
		for dropBox in dropBoxs:
			if csarithmetic.isInRectangleExt( dropBox.position, floorPos, 0.0, self.gridWidth+ 0.7, self.gridLength +0.02):
				tempDropList.append(dropBox)

		for tempDrop in tempDropList:
			tempDrop.destroySelf()

	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加entityMailBox 记录
		"""
		SpaceCopyRingTask.addEntityMailBoxRecord( self, scriptID, entityMailBox )
		if scriptID == "":#掉落的箱子
			floorID = self.getFillFloorID(entityMailBox.position)
			if floorID in self.destroyFloorIDList:
				entityMailBox.delayDestroy(1.0)