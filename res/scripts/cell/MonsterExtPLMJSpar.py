# -*- coding: utf-8 -*-


import KBEngine
import KBEDebug
#script
import Monster
import csarithmetic
import csdefine

class MonsterExtPLMJSpar( Monster.Monster ):
	"""
	CST-6262 蟠龙秘境 奇晶
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		self.moveCount = 0 # 当前移动次数
		self.centerPos = None #中心点
		self.radius = 0.0 # 半径
		self.maxMoveCount = 0 #最大移动次数
		self.dstPos = None # 移动的目标位置
		self.isTrue = False # 是否为真的奇晶

	def sparMove( self, pos, moveCount , centerPos, radius ):
		"""
		奇晶移动
		"""
		self.maxMoveCount = moveCount
		self.centerPos = centerPos
		self.radius = radius
		self.moveCount += 1
		self.dstPos = pos
		self.moveToPosition( pos, True, True, 0.1 )

	def getSpeed( self ):
		"""
		"""
		if self.dstPos == None:
			return Monster.Monster.getSpeed( self )
		return self.position.flatDistTo( self.dstPos ) / 2.0

	def sparStartMove( self, maxMoveCount, centerPos, radius ):
		"""
		奇晶开始移动
		"""
		if self.moveCount >= maxMoveCount:
			self.moveCount = 0
			spaceEntity = self.getCurrentSpace()
			if spaceEntity:
				spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "MoveEnd", "")
			return
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		endPosList = self.getPosList(centerPos, radius)
		entityList = spaceEntity.getEntityMailBoxRecord( self.scriptID )
		if len( endPosList ) != len(entityList):
			KBEDebug.ERROR_MSG( "has no pos" )
			return
		for entity in entityList:
			index = entityList.index( entity )
			entity.sparMove( endPosList[index], maxMoveCount ,centerPos, radius )

	def getPosList( self, centerPos, radius ):
		"""
		获得所有奇晶下个移动的坐标
		"""
		endPosList = []
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return endPosList
		entitylist = spaceEntity.getEntityRecord( self.scriptID )
		for i in range( 0, len(entitylist) ):
			endPos = None
			while endPos == None:
				srcPos = csarithmetic.getPositionByCircular( centerPos, radius )
				endPos = self.getEndPos(endPosList,srcPos )
				if endPos != None:
					endPosList.append(endPos)
		return endPosList

	def getEndPos( self, endPosList,srcPos ):
		"""
		获得最终位置
		"""
		for pos in endPosList:
			if pos.flatDistTo(srcPos) < 1.5:
				return None
		return srcPos
	
	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		Monster.Monster.onMoveOver( self, controllerID, userData )
		if userData != csdefine.MOVE_TYPE_MOVE_POINT:
			return
		self.moveControlID = 0
		spaceEntity = self.getCurrentSpace()
		if not spaceEntity:
			return
		#self.sparStartMove( self.maxMoveCount, self.centerPos, self.radius )
		isAllEntityStopMove = True
		entitylist = spaceEntity.getEntityMailBoxRecord( self.scriptID )
		for entity in entitylist:
			if entity.isMoving():
				isAllEntityStopMove = False
				break
		if isAllEntityStopMove:
			self.sparStartMove( self.maxMoveCount, self.centerPos, self.radius )

	def setIsTrue( self , isTrue ):
		"""
		设置是否为真奇晶
		"""
		self.isTrue = isTrue

	def getIsTrue( self ):
		"""
		获得是否为真的
		"""
		return self.isTrue
