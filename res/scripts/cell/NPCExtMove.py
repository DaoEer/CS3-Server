# -*- coding: utf-8 -*-

import KBEngine
import NPC
import csarithmetic
from CoreInterface.NPCAmbulantInterface import NPCAmbulantInterface
import csdefine
import KBEDebug

MOVE_TIMES = 6		#欢乐鼎每一轮移动次数

class NPCExtMove( NPC.NPC, NPCAmbulantInterface ):
	"""
	可移动可对话有副本事件的NPC（欢乐鼎）
	"""
	def __init__( self ):
		NPC.NPC.__init__( self )
		NPCAmbulantInterface.__init__( self )
		self.moveCount = 0
		self._canTalk = False
		self.TimerID = 0
		self._isTrue = False
		
	def HLDReset( self ):
		self.moveCount = 0
		self.setCanTalk( False )
		self.TimerID = 0		
		self._isTrue = False
	
	def getSpeed( self ):
		return 10.0
		
	def HLDMove(self, pos ):
		""" 欢乐鼎在圆形范围内随机移动 """
		self.moveCount += 1
		if self.moveCount > MOVE_TIMES:
			spaceEntity = self.getCurrentSpace()
			for player in spaceEntity._spaceRoles:
				player.client.EndPlayBindEffect( self.id )
			self.setCanTalk( True )
			return
		moveSpeed = self.position.flatDistTo( pos ) / 1.0
		self.moveToPosition( pos, True, True, 0.1 )

	def HLDStartMove( self, pos, radius ):
		"""
		欢乐鼎开始移动
		"""
		if self.moveCount > MOVE_TIMES:
			return
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		endPosList = self.getPosList( pos, radius )
		entitylist = spaceEntity.getEntityRecord( self.scriptID )
		if len( endPosList ) != len(entitylist):
			KBEDebug.ERROR_MSG( "has no pos" )
			return
		for eid in entitylist:
			HLDEntity = KBEngine.entities.get(eid)
			if not HLDEntity:
				continue
			index = entitylist.index(eid)
			HLDEntity.HLDMove( endPosList[index] )
		self.addTimerCallBack( 1.5, "HLDStartMove",(pos,radius) )

	def getPosList( self, pos, radius ):
		"""
		获得所有欢乐鼎下个移动的坐标
		"""
		endPosList = []
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return endPosList
		entitylist = spaceEntity.getEntityRecord( self.scriptID )
		for i in range( 0, len(entitylist) ):
			endPos = None
			while endPos == None:
				srcPos = csarithmetic.getPositionByCircular( pos , radius )
				endPos = self.getEndPos(endPosList,srcPos )
				if endPos != None:
					endPosList.append(endPos)
		return endPosList

	def getEndPos( self, endPosList,srcPos ):
		"""
		获得最终位置
		"""
		for pos in endPosList:
			if pos.flatDistTo(srcPos) < 1.0:
				return None
		return srcPos

	def getMoveCount( self ):
		return self.moveCount

	def setCanTalk(self, isAble ):
		self._canTalk = isAble
		
	def queryCanTalk(self):
		return self._canTalk
		
	def setIsTrue(self, isTrue ):
		self._isTrue = isTrue
		
	def queryIsTrue(self):
		return self._isTrue
		