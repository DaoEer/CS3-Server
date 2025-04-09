# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import KBEngine
import csdefine
import csstatus
import itertools


BOARD_COORD_X_RANGE = range( -9,10 )	# 棋盘横轴坐标取值范围
BOARD_COORD_Y_RANGE = range( -9,10 )	# 棋盘纵轴坐标取值范围

SAME_NUMBER_FIVE = 5	# 五子棋相连相邻且相同的最小值
MAX_CREATE_NUMBER_EACH_TIME = 20	# 每次最大创建棋子数量


HAS_PIECE_NONE	=	0	# 无子
HAS_PIECE_BLACK	=	1	# 有黑子
HAS_PIECE_WHITE	=	2	# 有白子

class SpaceCopyYinYangQiZhen( SpaceCopy ):
	"""
	阴阳棋阵
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
	
	def initSpaceData( self, originPos, unitLength, blackID, whiteID, bossID, monsterQiZiID ) :
		"""
		初始化棋盘数据
		"""	
		self.originPos		= originPos
		self.unitLength		= unitLength
		self.blackID		= blackID
		self.whiteID		= whiteID
		self.bossID 		= bossID
		self.monsterQiZiID  = monsterQiZiID

		for x in BOARD_COORD_X_RANGE :
			for y in BOARD_COORD_Y_RANGE :
				self.pointHasPiece[(x,y)] = HAS_PIECE_NONE		# 棋盘坐标（x,y） : 棋子种类
				self.pointHasEntity[(x,y)] = 0					# 棋盘坐标（x,y） : 棋子entityID



	def getBoardPosition( self, coord_x, coord_y ) :
		"""
		获取棋盘坐标为( coord_x,coord_y )的点在游戏中的位置
		"""
		originPos = self.originPos
		unitLength = self.unitLength
		position = ( originPos[0] + unitLength * coord_x, originPos[1], originPos[2] + unitLength * coord_y )
		return position
	
	def createBlackPiece( self, coord ) :
		"""
		在坐标coord上创建黑子
		"""
		from ObjectScript.ObjectScriptFactory import g_objFactory
		position = self.getBoardPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = g_objFactory.createEntity( self.blackID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_PIECE_BLACK
		self.pointHasEntity[ coord ] = entity.id
	
	def createWhitePiece( self, coord ) :
		"""
		在坐标coord上创建白子
		"""
		from ObjectScript.ObjectScriptFactory import g_objFactory
		position = self.getBoardPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position) }
		entity = g_objFactory.createEntity( self.whiteID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_PIECE_WHITE
		self.pointHasEntity[ coord ] = entity.id
	
	def __removePiece( self, coord ) :
		"""
		从棋盘上移除棋子
		"""
		self.pointHasPiece[ coord ] = HAS_PIECE_NONE
		self.pointHasEntity[ coord ] = 0
	
	def removePointHasPiece( self, entityID ) :
		"""
		去掉坐标 ( coord_x, coord_y ) 上的有棋子的标记
		"""
		for coord,hasEntity in self.pointHasEntity.items() :
			if hasEntity == entityID :
				self.__removePiece( coord )
				return
	
	def getCurrentPieceNumber( self ) :
		"""
		获取当前棋子数
		"""
		number = 0
		for hasPiece in self.pointHasPiece.values() :
			if hasPiece != HAS_PIECE_NONE :
				number += 1
		return number


	# -------------------------------------------------
	# 五子棋相关玩法
	# -------------------------------------------------
	def initGobang( self,number ) :
		"""
		初始化一个有number个棋子的五子棋棋局，要求不能有连续5个相邻且相同的棋子。
		"""
		assert 0 < number <= len( BOARD_COORD_X_RANGE ) * len( BOARD_COORD_Y_RANGE ), "init pieces number %s error, must in [0, 19*19]" % number
		for hasPiece in list(self.pointHasPiece.values()):
			if hasPiece != HAS_PIECE_NONE :
				KBEDebug.ERROR_MSG( "the chessboard is not empty." )
				return
		allPoints = list(self.pointHasPiece.keys())
		randomPoints = random.sample( allPoints, number ) #从指定序列中(allPoints)随机取出number个随机而独立的元素
		self.randomInitPoints( randomPoints )
		# 去除连续5个相邻且相同的棋子
		gobangLinks = self.checkAllGobangLink()
		while gobangLinks :
			self.randomInitPoints( gobangLinks )
			gobangLinks = self.checkGobangLink( gobangLinks )
		self.allEntityAmount = number
		self.alreadCreateAmount = 0
		self.createPieceEntities( number )
	
	def randomInitPoints( self, points ) :
		"""
		@param points : 点列，形如[(x,y)]
		随机初始化黑白棋
		"""
		count = len( points )
		random.shuffle( points )  #随机重新排列坐标点
		blackPoints = points[0:int(count/2)]
		whitePoints = points[int(count/2):count]
		for point in blackPoints :
			self.pointHasPiece[point] = HAS_PIECE_BLACK
		for point in whitePoints :
			self.pointHasPiece[point] = HAS_PIECE_WHITE
	
	def createPieceEntities( self, number ) :
		"""
		@param number : 数量
		创建棋盘中一定数量的黑白棋子entity
		"""
		if number > MAX_CREATE_NUMBER_EACH_TIME:
			self.addTimerCallBack( 0.2,"createPieceEntities",(MAX_CREATE_NUMBER_EACH_TIME,) )
		elif number > 0:
			self.alreadCreateAmount += number
			self.createPartEntities( number )
		else:
			return

	def createPartEntities( self, number ):
		for point,entityID in self.pointHasEntity.items() :
			if entityID != 0 or self.pointHasPiece[point] == HAS_PIECE_NONE :
				continue
			number -= 1
			if number < 0 :
				self.addTimerCallBack( 0.2,"createPieceEntities",((self.allEntityAmount - self.alreadCreateAmount),) )
				break
			if self.pointHasPiece[point] == HAS_PIECE_BLACK :
				self.createBlackPiece( point )
			elif self.pointHasPiece[point] == HAS_PIECE_WHITE :
				self.createWhitePiece( point )
	
	def destroyAllPieces( self, coords = None ) :
		"""
		销毁coords中所有棋子
		"""
		if coords is None :
			coords = self.pointHasEntity.keys()
		
		nofityIds = []
		for coord in coords :
			entityID = self.pointHasEntity[ coord ]
			if not entityID :
				continue
			
			nofityIds.append( entityID )
			self.__removePiece( coord )
		for entityID in nofityIds:
			entity = KBEngine.entities.get(entityID,None)
			if entity:
				entity.destroySelf()

	def createPiece( self, entityID ) :
		"""
		在对应坐标上创建黑白棋子（反转棋子）
		"""
		for coord,hasEntity in self.pointHasEntity.items() :
			if hasEntity == entityID :
				if self.pointHasPiece[ coord ] == HAS_PIECE_BLACK :
					self.__removePiece( coord )
					self.createWhitePiece( coord )
					self.addTimerCallBack(0.3,"checkPiece",([],[coord]))
				elif self.pointHasPiece[ coord ] == HAS_PIECE_WHITE :
					self.__removePiece( coord )
					self.createBlackPiece( coord )
					self.addTimerCallBack(0.3,"checkPiece",([coord], []))

	def checkPiece( self, blackCoords,whiteCoords ):
		"""
		检查棋子
		"""
		allLinks = self.checkGobangLink( blackCoords + whiteCoords )
		if not allLinks :
			return
		for pos in allLinks:
			entityID = self.pointHasEntity.get(pos,0)
			entity = KBEngine.entities.get(entityID,None)
			bossIDList = self.getEntityRecord(self.bossID)
			if entity == None and len(bossIDList) > 0:
				return
			entity.createEntityByScriptID(self.monsterQiZiID, Math.Vector3(entity.position), (0.0,0.0,0.0),{ "spawnPos":Math.Vector3( entity.position ),"spawnDir":(0.0,0.0,0.0)})
			entity.addTimerCallBack(0.8, "destroySelf", ())
		self.getScript().onConditionChange( self, "", "", "XC", "" )

		self.addTimerCallBack(1.0,"refreshGobangLink",(allLinks,))

	def refreshGobangLink( self, points ):
		"""
		@param points : 点列，形如[(x,y)]
		销毁五子棋中的超过5个连续相同的棋子，并重新刷出这些点
		"""
		self.destroyAllPieces( points )
		count = len( points )
		_product = list(itertools.product([HAS_PIECE_BLACK,HAS_PIECE_WHITE], repeat = len( points )))
		random.shuffle( _product )
		for it in _product:
			for index, point in enumerate(points):
				self.pointHasPiece[point] = it[index]
			result = self.checkAllGobangLink()
			if len(result):
				continue
			break
		for point in points:
			if self.pointHasPiece[point] == HAS_PIECE_BLACK:
				self.addTimerCallBack(0.3,"createBlackPiece",(point,))
			elif self.pointHasPiece[point] == HAS_PIECE_WHITE:
				self.addTimerCallBack(0.3,"createWhitePiece",(point,))

	
	def getRowAndColumnLink( self, rowRange = BOARD_COORD_X_RANGE, columnRange = BOARD_COORD_Y_RANGE ) :
		"""
		获取横竖线上连续5个相邻且相同的棋子
		"""
		allLinks = set()
		# 检查行
		for row in rowRange :
			rowLink = self.getRowLink( row, SAME_NUMBER_FIVE )
			if rowLink :
				allLinks.update( rowLink )  #将行 最少连续5个相同的棋子坐标添加到allLinks字典中
		# 检查列
		for column in columnRange :
			columnLink = self.getColumnLink( column, SAME_NUMBER_FIVE )
			if columnLink :
				allLinks.update( columnLink )  #将列 最少连续5个相同的棋子坐标添加到allLinks字典中
		
		return allLinks
	
	def checkGobangLink( self, coords ) :
		"""
		查coords中所在点是否存在连续5个相邻且相同的棋子
		"""
		needCheckRows = set()
		needCheckColumns = set()
		for coord in coords :
			needCheckRows.add( coord[0] )
			needCheckColumns.add( coord[1] )
		
		allLinks = self.getRowAndColumnLink( needCheckRows, needCheckColumns )
		allLinks.update( self.getObliqueLink( coords, SAME_NUMBER_FIVE ) )
		return list( allLinks )
	
	def checkAllGobangLink( self ) :
		"""
		检查所有棋盘是否存在连续5个相邻且相同的棋子
		"""
		needCheckCoords = set()
		for x in BOARD_COORD_X_RANGE :
			needCheckCoords.add( (x,BOARD_COORD_Y_RANGE[0]) )
			needCheckCoords.add( (x,BOARD_COORD_Y_RANGE[-1]) )
		for y in BOARD_COORD_Y_RANGE :
			needCheckCoords.add( (BOARD_COORD_X_RANGE[0],y) )
		
		return self.checkGobangLink( needCheckCoords )
	
	def getRowLink( self, rowIndex, minSameNumber ) :
		"""
		获取第rowIndex行的连续minSameNumber个以上相同的棋子
		"""
		assert rowIndex in BOARD_COORD_X_RANGE,"invalid row index:%s." % rowIndex
		rowLinks = set()
		x = rowIndex
		y_begin = BOARD_COORD_Y_RANGE[ 0 ]
		y_end = y_begin
		while y_end <= BOARD_COORD_Y_RANGE[-1] :
			while y_end <= BOARD_COORD_Y_RANGE[-1] and self.pointHasPiece[(x,y_begin)] == self.pointHasPiece[(x,y_end)] :
				y_end += 1
			pieceType = self.pointHasPiece[(x,y_begin)]
			if y_end - y_begin >= minSameNumber and pieceType != HAS_PIECE_NONE :
				for y in range(y_begin,y_end) :
					rowLinks.add( (x,y) )
			y_begin = y_end
		
		return rowLinks
	
	def getColumnLink( self, columnIndex, minSameNumber ) :
		"""
		获取第columnIndex列的连续minSameNumber个以上相同的棋子
		"""
		assert columnIndex in BOARD_COORD_Y_RANGE,"invalid row index:%s." % columnIndex
		columnLinks = set()
		y = columnIndex
		x_begin = BOARD_COORD_X_RANGE[ 0 ]
		x_end = x_begin
		while x_end <= BOARD_COORD_X_RANGE[-1] :
			while x_end <= BOARD_COORD_X_RANGE[-1] and self.pointHasPiece[(x_begin,y)] == self.pointHasPiece[(x_end,y)] :
				x_end += 1
			pieceType = self.pointHasPiece[(x_begin,y)]
			if x_end - x_begin >= minSameNumber and pieceType != HAS_PIECE_NONE :
				for x in range(x_begin,x_end) :
					columnLinks.add( (x,y) )
			x_begin = x_end
		
		return columnLinks
	
	def getObliqueLink( self, coords, minSameNumber ) :
		"""
		获取coords中所有点所在斜线上的连续minSameNumber个以上相同的棋子
		"""
		if minSameNumber > len( BOARD_COORD_X_RANGE ) or minSameNumber > len( BOARD_COORD_Y_RANGE ) :
			return []
		
		upPoints = set()
		downPoints = set()
		for coord in coords :
			x,y = coord
			while x > BOARD_COORD_X_RANGE[0] and y > BOARD_COORD_Y_RANGE[0] :
				x -= 1
				y -= 1
			upPoints.add( (x,y) )
			x,y = coord
			while x > BOARD_COORD_X_RANGE[0] and y < BOARD_COORD_Y_RANGE[-1] :
				x -= 1
				y += 1
			downPoints.add( (x,y) )
		
		obliqueLinks = set()
		for x,y in upPoints :
			obliqueLinks.update( self._getUpLink( x, y, minSameNumber ) )
		for x,y in downPoints :
			obliqueLinks.update( self._getDownLink( x, y, minSameNumber ) )
		return obliqueLinks
	
	def _getUpLink( self, rowIndex, columnIndex, minSameNumber ):
		"""
		#计算方向（1,1）的斜线
		"""
		obliqueLinks = set()
		x_begin = rowIndex
		y_begin = columnIndex
		while x_begin > BOARD_COORD_X_RANGE[0] and y_begin > BOARD_COORD_Y_RANGE[0] :
			x_begin -= 1
			y_begin -= 1
		
		x_end = x_begin
		y_end = y_begin
		while x_end <= BOARD_COORD_X_RANGE[-1] and y_end <= BOARD_COORD_Y_RANGE[-1] :
			while x_end <= BOARD_COORD_X_RANGE[-1] and y_end <= BOARD_COORD_Y_RANGE[-1] and \
			self.pointHasPiece[(x_begin,y_begin)] == self.pointHasPiece[(x_end,y_end)] :
				x_end += 1
				y_end += 1
			pieceType = self.pointHasPiece[(x_begin,y_begin)]
			if x_end - x_begin >= minSameNumber and pieceType != HAS_PIECE_NONE :
				for x in range(x_begin,x_end) :
					obliqueLinks.add( ( x, y_begin + x - x_begin ) )
			x_begin = x_end
			y_begin = y_end
		
		return obliqueLinks
	
	def _getDownLink( self, rowIndex, columnIndex, minSameNumber ):
		"""
		#计算方向（1,-1）的斜线
		"""
		obliqueLinks = set()
		x_begin = rowIndex
		y_begin = columnIndex
		while x_begin > BOARD_COORD_X_RANGE[0] and y_begin < BOARD_COORD_Y_RANGE[-1] :
			x_begin -= 1
			y_begin += 1
		
		x_end = x_begin
		y_end = y_begin
		while x_end <= BOARD_COORD_X_RANGE[-1] and y_end >= BOARD_COORD_Y_RANGE[0] :
			while x_end <= BOARD_COORD_X_RANGE[-1] and y_end >= BOARD_COORD_Y_RANGE[0] and \
			self.pointHasPiece[(x_begin,y_begin)] == self.pointHasPiece[(x_end,y_end)] :
				x_end += 1
				y_end -= 1
			pieceType = self.pointHasPiece[(x_begin,y_begin)]
			if x_end - x_begin >= minSameNumber and pieceType != HAS_PIECE_NONE :
				for x in range(x_begin,x_end) :
					obliqueLinks.add( ( x, y_begin - x + x_begin ) )
			x_begin = x_end
			y_begin = y_end
		
		return obliqueLinks
