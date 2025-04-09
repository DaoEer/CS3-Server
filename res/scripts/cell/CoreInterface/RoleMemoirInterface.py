# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from ConfigObject.Memoir.MemoirMgr import g_memoirMgr
import Math

class RoleMemoirInterface:
	"""
	玩家仙魔录
	"""
	def __init__( self ):
		"""
		"""
		self.memoirID = ""
		self.spaceName = ""
		self.positionStr = ""
		self.directionStr = ""

	def initMemoirList( self ):
		"""
		初始化玩家仙魔录
		"""
		if self.memoirIDList:
			self.client.CLIENT_ReceiveMemoirIDList( self.memoirIDList )
		else:
			camp = self.getCamp()
			memoirID = "%i-1"%camp
			self.addMemoirStory(memoirID)
			#self.startPlayMemoirCG("1",memoirID,"","","")

	def addMemoirStory( self, memoirID ):
		"""
		<Define method>
		增加一条记录
		"""
		if memoirID in self.memoirIDList:
			return
		self.memoirIDList.append(memoirID)
		nextMemoirID = self.getNextMemoirID()
		if nextMemoirID == None:
			nextMemoirID = ""
		#self.client.CLIENT_AddMemoirStory( memoirID, nextMemoirID )

	def startPlayMemoirCG( self, memoirCGID,memoirID,spaceName,position,direction ):
		"""
		播放仙魔录动画
		"""
		self.memoirID = memoirID
		self.spaceName = spaceName
		self.positionStr = position
		self.directionStr = direction
		#self.client.CLIENT_PlayMemoirCG( memoirCGID,memoirID )

	def CELL_endPlayMemoirCG( self, playerID ):
		"""
		<exposed method>
		播放仙魔录动画完毕后
		"""
		if not self.validateClientCall( playerID ):
			return
		if len(self.memoirID) == 0:
			return
		if len(self.spaceName) != 0:
			position = self.positionStr.split(" ")
			direction = self.directionStr.split(" ")

			dstPosition = Math.Vector3( eval(position[0]), eval(position[1]), eval(position[2]) )
			dstDirection = Math.Vector3( eval(direction[0]), eval(direction[1]), eval(direction[2]) )
			self.gotoSpaceUE4(self.spaceName, Math.Vector3(dstPosition), dstDirection)
		self.addMemoirStory(self.memoirID)

	def getMemoirIDList( self ):
		"""
		获得所有记录
		"""
		return self.memoirIDList

	def getNextMemoirID( self ):
		"""
		获得下一个仙魔录ID
		"""
		return g_memoirMgr.getNextMemoirID( self )
		 