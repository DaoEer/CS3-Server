# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import KBEngine
import csdefine
import csstatus
import csarithmetic
from ObjectScript.ObjectScriptFactory import g_objFactory
import time

SPAW_EFFECTID = "BirthBlack"
COORD_N = 15
COORD_S = -14
COORD_W = -14
COORD_E = 15
COORD_O = 0

BOARD_COORD_X_RANGE = range( COORD_W,COORD_E+1 )	# 棋盘横轴坐标取值范围
BOARD_COORD_Y_RANGE = range( COORD_S,COORD_N+1 )	# 棋盘纵轴坐标取值范围

HAS_PIECE_NONE			=	0	# 无子
HAS_PIECE_GREEN_HEYE	=	1	# 有绿荷叶
HAS_PIECE_WHITE_HEHUA	=	2	# 有白荷花
HAS_PIECE_RED_HEHUA		= 	3	# 有红荷花
HAS_PIECE_HEBAO			=	4	# 有荷包


class SpaceCopyHeHuaFaZhen( SpaceCopy ):
	"""
	荷花法阵
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.upLeftRouteList1 = [] #棋盘上左路线1
		self.upRightRouteList1 = [] #棋盘上右路线1
		self.downLeftRouteList1 = [] #棋盘下左路线1
		self.downRightRouteList1 = [] #棋盘下右路线1

		self.needHeHuaType = 2		#白荷花

	def setNeedHeHuaType( self, type ):
		"""
		"""
		self.needHeHuaType = type
	
	def initSpaceData( self, originPos, unitLength, heYeID, whiteHeHuaID, redHeHuaID, whiteHeBaoID, redHeBaoID, whiteHeHuaMonsterID, redHeHuaMonsterID, effectMonsterID, bossID, whiteHeHuaSkillID, redHeHuaSkillID, mixHeHuaSkillID ) :
		"""
		初始化棋盘数据
		"""	
		self.originPos		= originPos
		self.unitLength		= unitLength
		self.greenHeYeID 	= heYeID
		self.whiteHeHuaID  	= whiteHeHuaID
		self.redHeHuaID 	= redHeHuaID
		self.redHeBaoID 	= redHeBaoID
		self.whiteHeBaoID   = whiteHeBaoID
		self.bossID = bossID
		self.whiteHeHuaMonsterID = whiteHeHuaMonsterID
		self.redHeHuaMonsterID = redHeHuaMonsterID
		self.effectMonsterID = effectMonsterID
		self.redHeHuaSkillID = redHeHuaSkillID
		self.whiteHeHuaSkillID = whiteHeHuaSkillID
		self.mixHeHuaSkillID	= mixHeHuaSkillID

		for x in BOARD_COORD_X_RANGE :
			for y in BOARD_COORD_Y_RANGE :
				self.pointHasPiece[(x,y)] = HAS_PIECE_NONE		# 棋盘坐标（x,y） : 棋子种类
				self.pointHasEntity[(x,y)] = 0					# 棋盘坐标（x,y） : 棋子entityID


	def initBoard( self ):
		"""
		初始化棋盘
		将棋盘分为4部分
		"""
		upLeftAllPosList = []
		upRightAllPosList = []
		downLeftAllPosList = []
		downRightAllPosList = []

		for x in BOARD_COORD_X_RANGE:
			for y in BOARD_COORD_Y_RANGE:
				if x in range(COORD_W, COORD_O+1):
					if y in range(COORD_S, COORD_O+1):
						downLeftAllPosList.append((x,y))
					else:
						upLeftAllPosList.append((x,y))
				else:
					if y in range(COORD_S, COORD_O + 1):
						downRightAllPosList.append((x,y))
					else:
						upRightAllPosList.append((x,y))

		
		self.upLeftRouteList1 = self.getRouteList( upLeftAllPosList,(-1,1), 20 )
		self.upRightRouteList1 = self.getRouteList( upRightAllPosList,(2,2), 20 )
		self.downLeftRouteList1 = self.getRouteList( downLeftAllPosList,(-3,-3),20 )
		self.downRightRouteList1 = self.getRouteList( downRightAllPosList,(4,-4),20 )

		hehuaTypeList = [HAS_PIECE_WHITE_HEHUA, HAS_PIECE_RED_HEHUA, HAS_PIECE_WHITE_HEHUA, HAS_PIECE_RED_HEHUA]
		random.shuffle(hehuaTypeList)
		self.createPartPieceEntity(self.upLeftRouteList1,upLeftAllPosList, hehuaTypeList[0])
		self.createPartPieceEntity( self.upRightRouteList1,upRightAllPosList, hehuaTypeList[1] )
		self.createPartPieceEntity( self.downLeftRouteList1,downLeftAllPosList, hehuaTypeList[2] )
		self.createPartPieceEntity( self.downRightRouteList1,downRightAllPosList, hehuaTypeList[3] )

		self.createPieceEntity(BOARD_COORD_X_RANGE[0])

	def createPartPieceEntity( self, routeList1,partAllPosList, hehuaType ):
		"""
		创建荷花、荷叶创建Entity
		"""
		totalRoutePointList = []
		totalRoutePointList.extend(routeList1)
		totalRoutePointList = list( set(totalRoutePointList) )
		for point in totalRoutePointList:
			if point in partAllPosList:
				partAllPosList.remove(point)
		pointList = random.sample(partAllPosList, 50)	#取50个荷叶点
		randomPoints = random.sample(pointList,4)		#随机取4个点随机创建荷花 荷包
		for point in randomPoints:
			pointList.remove(point)
		for pos in pointList:
			if self.pointHasPiece[pos] == HAS_PIECE_NONE:
				self.pointHasPiece[pos] = HAS_PIECE_GREEN_HEYE
		samePoints = random.sample(totalRoutePointList,2) #一条线上随机取2个点创建相同荷花

		for point in samePoints:
			self.pointHasPiece[point] = hehuaType

		self.randomInitPoints(randomPoints)
		randomPoints.extend(samePoints)
		links = self.checkCoordsLink( randomPoints )
		if len(links) > 0 and self.pointHasPiece[links[0]] not in [HAS_PIECE_WHITE_HEHUA,HAS_PIECE_RED_HEHUA]:
			links = []
		while links:
			self.randomInitPoints(randomPoints)
			links = self.checkCoordsLink( randomPoints )
			if len(links) > 0 and self.pointHasPiece[links[0]] not in [HAS_PIECE_WHITE_HEHUA,HAS_PIECE_RED_HEHUA]:
				links = []

		
	def createPieceEntity( self, index ):
		"""
		"""
		if index < BOARD_COORD_X_RANGE[-1]:
			self.createPartLineEntity([index,index+1])
			self.addTimerCallBack(0.2,"createPieceEntity",(index + 2,))
		else:
			for point, entityID in self.pointHasEntity.items():
				if self.pointHasPiece[point] == HAS_PIECE_WHITE_HEHUA:
					self.createWhiteHeHua( point )
				elif self.pointHasPiece[point] == HAS_PIECE_RED_HEHUA:
					self.createRedHeHua(point)
				elif self.pointHasPiece[point] == HAS_PIECE_HEBAO:
					radio = random.uniform(0,1)
					if radio > 0.5:
						self.createRedHeBao(point)
					else:
						self.createWhiteHeBao(point)

	def createPartLineEntity( self, lines ):
		"""
		创建多行Entity 以X为准
		"""
		for line in lines:
			for point, entityID in self.pointHasEntity.items():
				if entityID == 0 and self.pointHasPiece[point] == HAS_PIECE_GREEN_HEYE and point[0] == line:
					self.createGreenHeYe(point)

	def randomInitPoints( self, points ):
		"""
		这个是2条路线有交集的情况：随机初始化白荷花、红荷花、荷包
		"""
		count = len(points)
		random.shuffle( points )  #随机重新排列坐标点
		whiteHeHuaPoints = points[0:int(count/2)]
		redHeHudaPoints = points[int(count/2):count - 1]
		heBaoPoint = points[count - 1]
		for point in whiteHeHuaPoints:
			self.pointHasPiece[point] = HAS_PIECE_WHITE_HEHUA
		for point in redHeHudaPoints:
			self.pointHasPiece[point] = HAS_PIECE_RED_HEHUA
		self.pointHasPiece[heBaoPoint] = HAS_PIECE_HEBAO

	def getRouteList( self, allPosList, firstPos,length ):
		"""
		获得路线
		allPosList 所有路线点
		length 路线长度
		"""
		routeList = []
		if len(allPosList) < length:
			return routeList

		routeList.append(firstPos)
		allPosList.remove(firstPos)
		while len(routeList) < length:
			nextPos = self.getNextPos( routeList[len(routeList)-1], allPosList)
			if nextPos != None:
				routeList.append(nextPos)
				allPosList.remove(nextPos)
			else:
				break
		return routeList

	def getNextPos( self, srcPos, allPosList ):
		"""
		获得下个路线点
		"""
		tempList = []
		for pos in allPosList:
			if (pos[0] == srcPos[0] or pos[1] == srcPos[1]) and (abs(pos[0] + pos[1] - srcPos[0] - srcPos[1]) == 1) and self.pointHasPiece[pos] == HAS_PIECE_NONE: #每次走一格
				tempList.append(pos)
		if len(tempList) > 0:
			return random.choice(tempList)
		return None

	def getBoardPosition( self, coord_x, coord_y ):
		"""
		获取棋盘坐标为( coord_x,coord_y )的点在游戏中的位置
		"""
		originPos = self.originPos
		unitLength = self.unitLength
		position = ( originPos[0] + unitLength * coord_x, originPos[1], originPos[2] + unitLength * coord_y )
		return position

	def getPointByPosition(self, position):
		"""
		获取position在棋盘中的坐标 ( coord_x,coord_y )
		"""
		originPos = self.originPos
		unitLength = self.unitLength
		coord_x = (position[0] - originPos[0])//unitLength
		coord_y = (position[2] - originPos[2])//unitLength
		return (coord_x, coord_y)

	def createMonsterByPosition(self, scriptIDList):
		"""
		刷怪
		"""
		if not len(self._spaceRoles):
			return
		position = self._spaceRoles[0].position
		routeList = []

		x,y = self.getPointByPosition(position)

		if x in range(COORD_W,COORD_O+1):
			if y in range(COORD_S,COORD_O+1):
				routeList= self.downLeftRouteList1
			else:
				routeList= self.upLeftRouteList1
		else:
			if y in range(COORD_S,COORD_O+1):
				routeList = self.downRightRouteList1
			else:
				routeList = self.upRightRouteList1
		if not len(routeList):
			KBEDebug.ERROR_MSG("routeList is None")
			return
		posList = []
		for coord in routeList:
			if not len(scriptIDList):
				KBEDebug.ERROR_MSG("scriptIDList is None")
				return
			if self.pointHasPiece[coord] == HAS_PIECE_NONE:
				_position = self.getBoardPosition(coord[0], coord[1])
				posList.append(_position)

		if len( posList ) < len( scriptIDList ):
			return
		spawnPosList =[]	
		spawnPosList = random.sample(posList,len(scriptIDList))
		if not len (spawnPosList):
			KBEDebug.ERROR_MSG("spawnPosList is None")
			return
		for _position in spawnPosList:
			direction = (0.0,0.0,0.0)
			params = {}
			params.update( {"spawnPos":tuple(Math.Vector3(_position))} )
			g_objFactory.createEntity(scriptIDList[0], self, tuple(Math.Vector3(_position)),direction,params)
			scriptIDList.pop(0)


	def createHeHuaHeBaoCallBack(self, coord):
		"""
		创建荷叶荷包回调
		"""
		links = self.checkCoordsLink([coord])
		if not links:
			return
		self.addTimerCallBack(1.0,"coordLinkUseSkill",([coord]))
	def createGreenHeYe( self, coord ):
		"""
		在坐标coord上创建绿荷叶
		"""
		position = Math.Vector3(self.getBoardPosition( coord[0], coord[1] ))
		position.y += -0.07  #为了磨合地图
		state = { "spawnPos" : Math.Vector3(position)}
		entity = g_objFactory.createEntity( self.greenHeYeID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_PIECE_GREEN_HEYE
		self.pointHasEntity[ coord ] = entity.id


	def createWhiteHeHua( self, coord ):
		"""
		在坐标coord上创建白荷花
		"""
		position = self.getBoardPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = g_objFactory.createEntity( self.effectMonsterID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		
		self.addTimerCallBack(1.0, "createWhiteHeHuaCB",(coord,))


	def createWhiteHeHuaCB( self, coord ):
		"""
		在坐标coord上创建白荷花
		"""
		position = self.getBoardPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = g_objFactory.createEntity( self.whiteHeHuaID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_PIECE_WHITE_HEHUA
		self.pointHasEntity[ coord ] = entity.id
		self.createHeHuaHeBaoCallBack(coord)


	def createRedHeHua( self, coord ):
		"""
		在坐标coord上创建红荷花
		"""
		
		position = self.getBoardPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = g_objFactory.createEntity( self.effectMonsterID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		self.addTimerCallBack(1.0, "createRedHeHuaCB",(coord,))

	def createRedHeHuaCB( self, coord ):
		"""
		在坐标coord上创建红荷花
		"""
		
		position = self.getBoardPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = g_objFactory.createEntity( self.redHeHuaID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_PIECE_RED_HEHUA
		self.pointHasEntity[ coord ] = entity.id
		self.createHeHuaHeBaoCallBack(coord)

	def createRedHeBao( self, coord ):
		"""
		在坐标coord上创建红荷包
		"""
		position = self.getBoardPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = g_objFactory.createEntity( self.effectMonsterID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		
		self.addTimerCallBack(1.0, "createRedHeBaoCB",(coord,))


	def createRedHeBaoCB( self, coord ):
		"""
		在坐标coord上创建红荷包
		"""
		position = self.getBoardPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = g_objFactory.createEntity( self.redHeBaoID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_PIECE_HEBAO
		self.pointHasEntity[ coord ] = entity.id

	def createWhiteHeBao( self, coord ):
		"""
		在坐标coord上创建白荷包
		"""
		position = self.getBoardPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = g_objFactory.createEntity( self.effectMonsterID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		
		self.addTimerCallBack(1.0, "createWhiteHeBaoCB",(coord,))

	def createWhiteHeBaoCB( self, coord ):
		"""
		在坐标coord上创建白荷包
		"""
		position = self.getBoardPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = g_objFactory.createEntity( self.whiteHeBaoID, self, Math.Vector3(position), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_PIECE_HEBAO
		self.pointHasEntity[ coord ] = entity.id


	def checkCoordsLink( self, coords ):
		"""	
		检查coords中所在点是否存在连续3个相邻的荷花
		"""
		needCheckRows = set()
		needCheckColumns = set()
		for coord in coords:
			needCheckRows.add( coord[0] )
			needCheckColumns.add( coord[1] )

		allLinks = self.getRowAndColumnLink( needCheckRows, needCheckColumns )
		allLinks.update( self.getObliqueLink( coords, 3 ))
	
		return list(allLinks)

	def getRowAndColumnLink( self, rowRange, columnRange ):
		"""
		获取横竖线上连续3个相邻荷花
		"""
		allLinks = set()
		# 检查行
		for row in rowRange:
			rowLink = self.getRowLink( row, 3 )
			if rowLink:
				allLinks.update( rowLink )
		# 检查列
		for column in columnRange:
			columnLink = self.getColumnLink( column, 3 )
			if columnLink:
				allLinks.update( columnLink )

		return allLinks


	def getRowLink( self, rowIndex, minSameNumber ):
		"""
		获取第rowIndex行的连续minSameNumber以上相邻荷花
		"""
		if minSameNumber > len( BOARD_COORD_Y_RANGE ) :
			return ()
		rowLinks = set()
		x = rowIndex
		y_begin = BOARD_COORD_Y_RANGE[ 0 ]
		y_end = y_begin
		
		while y_begin <= BOARD_COORD_Y_RANGE[-1] - minSameNumber +1:
			if self.pointHasPiece[(x,y_begin)] not in [HAS_PIECE_RED_HEHUA, HAS_PIECE_WHITE_HEHUA]:
				y_begin += 1
				y_end = y_begin
				continue
			while y_end <= BOARD_COORD_Y_RANGE[-1] and self.pointHasPiece[(x,y_end)] in [HAS_PIECE_RED_HEHUA, HAS_PIECE_WHITE_HEHUA]:
				y_end += 1
	
			if y_end - y_begin >= minSameNumber:
				for y in range( y_begin, y_end ):
					rowLinks.add( (x,y) )
			y_begin = y_end
		return rowLinks



	def getColumnLink( self, columnIndex, minSameNumber ):
		"""
		获取第rowIndex行的连续minSameNumber以上相邻荷花
		"""
		if minSameNumber > len( BOARD_COORD_X_RANGE ):
			return ()
		rowLinks = set()
		y = columnIndex
		x_begin = BOARD_COORD_X_RANGE[ 0 ]
		x_end = x_begin
		
		while x_begin <= BOARD_COORD_X_RANGE[-1] - minSameNumber + 1:
			if self.pointHasPiece[(x_begin,y)] not in [HAS_PIECE_RED_HEHUA, HAS_PIECE_WHITE_HEHUA]:
				x_begin += 1
				x_end = x_begin
				continue
			while x_end <= BOARD_COORD_X_RANGE[-1] and self.pointHasPiece[(x_end,y)]  in [HAS_PIECE_RED_HEHUA, HAS_PIECE_WHITE_HEHUA]:
				x_end += 1
	
			if x_end - x_begin >= minSameNumber:
				for x in range( x_begin, x_end):
					rowLinks.add( (x,y) )
			x_begin = x_end
		return rowLinks


	def getObliqueLink( self, coords, minSameNumber ):
		"""
		获取coords中所有点所在斜线上的连续minSameNumber个以上相邻荷花
		"""
		if minSameNumber > len( BOARD_COORD_X_RANGE ) or minSameNumber > len( BOARD_COORD_Y_RANGE ) :
			return ()
		obliqueLinks = set()
		for coord in coords:
			obliqueLinks.update( self.getUpLink( coord[0], coord[1], minSameNumber ) )
			obliqueLinks.update( self.getDownLink( coord[0], coord[1], minSameNumber ) )

		return obliqueLinks


	def getUpLink( self, rowIndex, columnIndex, minSameNumber ):
		"""
		计算方向（1,1）的斜线
		"""
		obliqueLinks = set()
		x_begin = rowIndex
		y_begin = columnIndex
		while x_begin > BOARD_COORD_X_RANGE[0] and y_begin > BOARD_COORD_Y_RANGE[0] :
			x_begin -= 1
			y_begin -= 1
		
		x_end = x_begin
		y_end = y_begin
		
		while x_begin <= BOARD_COORD_X_RANGE[-1] - minSameNumber + 1 and y_begin<= BOARD_COORD_Y_RANGE[-1] - minSameNumber +1:
			if self.pointHasPiece[(x_begin,y_begin)] not in [HAS_PIECE_RED_HEHUA, HAS_PIECE_WHITE_HEHUA]:
				x_begin += 1
				y_begin += 1
				x_end = x_begin
				y_end = y_begin
				continue

			while x_end <= BOARD_COORD_X_RANGE[-1] and y_end <= BOARD_COORD_Y_RANGE[-1] and self.pointHasPiece[(x_end,y_end)] in [HAS_PIECE_RED_HEHUA, HAS_PIECE_WHITE_HEHUA]:
				x_end += 1
				y_end += 1

			if x_end - x_begin >= minSameNumber:
				for x in range(x_begin,x_end) :
					obliqueLinks.add( ( x, y_begin + x - x_begin ) )

			x_begin = x_end
			y_begin = y_end
		
		return obliqueLinks


	def getDownLink( self, rowIndex, columnIndex, minSameNumber ):
		"""
		计算方向（1,-1）的斜线
		"""
		obliqueLinks = set()
		x_begin = rowIndex
		y_begin = columnIndex
		while x_begin > BOARD_COORD_X_RANGE[0] and y_begin < BOARD_COORD_Y_RANGE[-1] :
			x_begin -= 1
			y_begin += 1
		x_end = x_begin
		y_end = y_begin
		
		while x_begin <= BOARD_COORD_X_RANGE[-1] - minSameNumber + 1 and y_begin >=BOARD_COORD_Y_RANGE[0] + minSameNumber -1:
			if self.pointHasPiece[(x_begin,y_begin)] not in [HAS_PIECE_RED_HEHUA, HAS_PIECE_WHITE_HEHUA]:
				x_begin += 1
				y_begin -= 1
				x_end = x_begin
				y_end = y_begin
				continue
			while x_end <= BOARD_COORD_X_RANGE[-1]  and y_end >= BOARD_COORD_Y_RANGE[0] and self.pointHasPiece[(x_end,y_end)] in [HAS_PIECE_RED_HEHUA, HAS_PIECE_WHITE_HEHUA]:
				x_end += 1
				y_end -= 1
				
			if x_end - x_begin >= minSameNumber:
				for x in range(x_begin,x_end) :
					obliqueLinks.add( ( x, y_begin - x + x_begin ) )

			x_begin = x_end
			y_begin = y_end
		
		return obliqueLinks


	def destroyAllPieces( self, coords = None ) :
		"""
		销毁场上所有棋子
		"""
		if coords is None :
			coords = self.pointHasEntity.keys()
		
		nofityIds = []
		for coord in coords :
			entityID = self.pointHasEntity[ coord ]
			if not entityID :
				continue
			
			nofityIds.append( entityID )
			self.removePiece( coord )
		for entityID in nofityIds:
			entity = KBEngine.entities.get(entityID,None)
			if entity:
				entity.destroySelf()

	def removePiece( self, coord ) :
		"""
		从棋盘上移除棋子
		"""
		self.pointHasPiece[ coord ] = HAS_PIECE_NONE
		self.pointHasEntity[ coord ] = 0

	def getPointInCoord( self, entityID ):
		"""
		获得棋盘上的点
		"""
		entityIDList = list(self.pointHasEntity.values())
		if entityID in entityIDList:
			index = entityIDList.index(entityID)
			return list( self.pointHasEntity.keys() )[index]
		return None


	def createPieceByPieceType( self, data ):
		"""
		data[0] 代表：位置 如：(0,0)
		data[1] 代表：类型
		HAS_PIECE_WHITE_HEHUA	=	2	# 有白荷花
		HAS_PIECE_RED_HEHUA		= 	3	# 有红荷花
		"""
		if data[1] == HAS_PIECE_WHITE_HEHUA:
			self.createWhiteHeHuaCB(data[0])
		elif data[1] == HAS_PIECE_RED_HEHUA:
			self.createRedHeHuaCB(data[0])

	def getPointPiece( self, coord ):
		"""
		获得棋盘种类
		"""
		return self.pointHasPiece.get(coord,None)

	def setPointPiece( self, coord, pieceType ):
		"""
		设置棋盘种类
		"""
		self.pointHasPiece[coord] = pieceType

	def checkMoveforward( self, coord ):
		"""
		检查是否可向前移动
		"""
		if coord[1] + 1 <= BOARD_COORD_Y_RANGE[-1]:
			if self.pointHasEntity[(coord[0],coord[1] + 1)] <= 0 and self.pointHasPiece[(coord[0],coord[1] + 1)] == HAS_PIECE_NONE:
				return True
		return False

	def checkMoveDown( self, coord ):
		"""
		检查是否可向后移动
		"""
		if coord[1] - 1 >= BOARD_COORD_Y_RANGE[0]:
			if self.pointHasEntity[(coord[0],coord[1] - 1)] <= 0 and self.pointHasPiece[(coord[0],coord[1] - 1)] == HAS_PIECE_NONE:
				return True
		return False

	def checkMoveRight( self, coord ):
		"""
		检查是否可向右移动
		"""
		if coord[0] + 1 <= BOARD_COORD_X_RANGE[-1]:
			if self.pointHasEntity[(coord[0] + 1,coord[1])] <= 0 and self.pointHasPiece[(coord[0] + 1,coord[1])] == HAS_PIECE_NONE:
				return True
		return False

	def checkMoveLeft( self, coord ):
		"""
		检查是否可向左移动
		"""
		if coord[0] - 1 >= BOARD_COORD_X_RANGE[0]:
			if self.pointHasEntity[(coord[0] - 1,coord[1])] <= 0 and self.pointHasPiece[(coord[0] - 1,coord[1])] == HAS_PIECE_NONE:
				return True
		return False

	def coordLinkUseSkill( self, coords ):
		"""
		检查并释放技能
		"""
		links = self.checkCoordsLink([coords])
		if not links:
			return
		pieceTypeList = []
		for link in links:
			pieceTypeList.append( self.pointHasPiece[link] )
		isSuccess = True
		if HAS_PIECE_WHITE_HEHUA in pieceTypeList and HAS_PIECE_RED_HEHUA in pieceTypeList:
			isSuccess = False

		for link in links:
			entityID = self.pointHasEntity.get(link,0)
			entity = KBEngine.entities.get(entityID,None)
			bossIDList = self.getEntityRecord(self.bossID)
			if entity == None or len(bossIDList) <= 0:
				return
			if isSuccess:
				_tuple = (self.whiteHeHuaSkillID, self.whiteHeHuaMonsterID) if entity.scriptID == self.whiteHeHuaID else (self.redHeHuaSkillID, self.redHeHuaMonsterID)
				skillID, scriptID = _tuple
				entity.useSkillToEntity(skillID, bossIDList[0])
				entity.createEntityByScriptID(scriptID,entity.position,entity.direction,{})
			else:
				entity.useSkillToPosition(self.mixHeHuaSkillID,entity.position)
				
		if isSuccess:
			self.getScript().onConditionChange( self,"",self.scriptID,"True", "" )
		else:
			self.getScript().onConditionChange( self,"",self.scriptID,"False", "" )
		#self.getScript().spaceEvent_addCount( self,"HasLink" ,1 )  #这个计数是为了做重刷的 比如达到4次 就在4条路线上重刷
		self.addTimerCallBack(1.2,"destroyAllPieces",(links,))

	def getForwardDir( self ):
		"""
		获得朝向
		"""
		srcPos = self.getBoardPosition(-2,5) #这里可随便取点，但必须x值一致，为了获得玩家在上荷花的朝向
		dstPos = self.getBoardPosition(-2,8)
		yaw = csarithmetic.getYawByVector3( Math.Vector3(dstPos) - Math.Vector3(srcPos) )
		return yaw

	def refreshHeHua( self ):
		"""
		重刷荷花
		"""
		self.clearRouteListHeHuaPieceType( self.upLeftRouteList1 )
		self.clearRouteListHeHuaPieceType( self.upRightRouteList1 )
		self.clearRouteListHeHuaPieceType( self.downLeftRouteList1 )
		self.clearRouteListHeHuaPieceType( self.downRightRouteList1 )

		#这段逻辑是重新刷荷花 随机1000次，1000次不行就跳过
		oldtime = time.time()
		for i in range(1000):
			result = []
			result.extend(random.sample(self.upLeftRouteList1,3)) #一条线上随机取3个点创建相同荷花
			result.extend(random.sample(self.upRightRouteList1,3))
			result.extend(random.sample(self.downLeftRouteList1,3))
			result.extend(random.sample(self.downRightRouteList1,3))
			self.randomInitPoints(result)
			links = self.checkCoordsLink( result )
			#如果这些荷花都符合要求（都不会相消） 就退出循环
			if not links:
				newtime = time.time()
				KBEDebug.INFO_MSG("refreshHeHua run times = %d, sec = %s "%(i+1, newtime-oldtime))
				break
		else:
			newtime = time.time()
			KBEDebug.ERROR_MSG("refreshHeHua run 1000 times!, sec = %s"%(newtime-oldtime))

		routeList = self.upLeftRouteList1 + self.upRightRouteList1 + self.downLeftRouteList1 + self.downRightRouteList1
		for point in routeList:
			if self.pointHasPiece[point] == HAS_PIECE_WHITE_HEHUA:
				self.createWhiteHeHua( point )
			elif self.pointHasPiece[point] == HAS_PIECE_RED_HEHUA:
				self.createRedHeHua(point)
			elif self.pointHasPiece[point] == HAS_PIECE_HEBAO:
				radio = random.uniform(0,1)
				if radio > 0.5:
					self.createRedHeBao(point)
				else:
					self.createWhiteHeBao(point)

	def clearRouteListHeHuaPieceType( self, routeList ):
		"""
		获得路线上的荷花或者荷包的列表 并清除
		"""
		result = []
		for point in routeList:
			pieceType = self.getPointPiece(point)
			if pieceType in [HAS_PIECE_WHITE_HEHUA,HAS_PIECE_RED_HEHUA,HAS_PIECE_HEBAO]:
				result.append(point)
		self.destroyAllPieces(result)

