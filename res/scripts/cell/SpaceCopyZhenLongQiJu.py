# -*- coding: utf-8 -*-

import random
import copy
import KBEDebug
from SpaceCopyMagicMaze import SpaceCopyMagicMaze
import Math
import KBEngine
import csdefine
import csstatus


BOARD_COORD_X_RANGE = range( -9,10 )	# 棋盘横轴坐标取值范围
BOARD_COORD_Y_RANGE = range( -9,10 )	# 棋盘纵轴坐标取值范围

SAME_NUMBER_FIVE = 5	# 五子棋相连相邻且相同的最小值
MAX_CREATE_NUMBER_EACH_TIME = 20	# 每次最大创建棋子数量
SWITCH_STATE_TIME = 45.0 #切换状态的时间
STATE_CHANGE_MSG = 35.0	#切换状态的提示时间
STATE_CHANGE_COUNT_DOWN = 40.0	#状态切换倒计时的时间

HAS_PIECE_NONE	=	0	# 无子
HAS_PIECE_BLACK	=	1	# 有黑子
HAS_PIECE_WHITE	=	2	# 有白子

class SpaceCopyZhenLongQiJu( SpaceCopyMagicMaze ):
	"""
	真龙棋局棋盘
	"""
	def __init__( self ) :
		SpaceCopyMagicMaze.__init__( self )
		self.createPiecesTimer = 0		#填充棋盘时，刷新一批棋子的timer
		self.checkPieceTimer = 0		#检测棋子是否连成五子的timer
		self.refreshLinkTimer = 0		#在连子销毁的格子上重新创建棋子的timer
		self.destroyLinkTimer = 0		#销毁连子的timer
		self.createOneTimerList = []	#在连子销毁的某个格子上重新创建棋子的timer
	
	def initSpaceData( self, originPos, unitLength, blackID, whiteID, bossID, effectID, skillID, refreshTime, refreshCountRates ) :
		"""
		初始化棋盘数据
		"""	
		self.originPos		= originPos
		self.unitLength		= unitLength
		self.blackID		= blackID
		self.whiteID		= whiteID
		self.bossID 		= bossID
		self.whiteStateEffectID = ""
		self.blackStateEffectID = ""
		self.refreshTime = refreshTime
		self.refreshCountRates = refreshCountRates
		if effectID != "":
			self.whiteStateEffectID = effectID.split("|")[0]
			self.blackStateEffectID = effectID.split("|")[1]
		if skillID != "":
			self.reStoreHPSkillID = int(skillID.split("|")[0])
			self.damageSkillID = int(skillID.split("|")[1])
		self.pieceState = random.randint(csdefine.ZHEN_LONG_QI_JU_BLACK_STATE,csdefine.ZHEN_LONG_QI_JU_WHITE_STATE)
		for x in BOARD_COORD_X_RANGE :
			for y in BOARD_COORD_Y_RANGE :
				self.pointHasPiece[(x,y)] = HAS_PIECE_NONE		# 棋盘坐标（x,y） : 棋子种类
				self.pointHasEntity[(x,y)] = 0					# 棋盘坐标（x,y） : 棋子entityID

	def onLogin( self, playerRole ):
		SpaceCopyMagicMaze.onLogin(self,playerRole)
		bossIDList = self.getEntityRecord(self.bossID)
		if len(bossIDList) > 0:
			for bossID in bossIDList:
				entity = KBEngine.entities.get(bossID)
				if entity:
					if self.pieceState == csdefine.ZHEN_LONG_QI_JU_BLACK_STATE:
						playerRole.client.ZhenLongQiJu_OnBossStateChange( self.pieceState, entity.id, self.whiteStateEffectID )
					else:
						playerRole.client.ZhenLongQiJu_OnBossStateChange( self.pieceState, entity.id, self.blackStateEffectID )
					playerRole.client.ZhenLongQiJu_OnBossHPChange(entity.HP_Max,entity.HP)
		
	def openChangeTimeID( self ):
		"""
		开启切换自身状态的定时器
		"""
		self.clearChangeTimeID()
		self.switchSelfState()
		self.changeStateTimeID = self.addTimerRepeat(SWITCH_STATE_TIME, "switchSelfState", ())

	def OnBossStateChange( self, effectID ):
		"""
		"""
		bossIDList = self.getEntityRecord(self.bossID)
		if len(bossIDList) > 0:
			for bossID in bossIDList:
				entity = KBEngine.entities.get(bossID)
				for player in self._spaceRoles:
					player.client.ZhenLongQiJu_OnBossStateChange( self.pieceState, entity.id, effectID )

	def switchSelfState( self ):
		"""
		切换自身状态
		"""
		self.addTimerCallBack(STATE_CHANGE_MSG,"stateChangePrompt",(csstatus.SPACE_ZLQJ_STATE_TIPS,))
		self.addTimerCallBack(STATE_CHANGE_COUNT_DOWN,"stateChangeCountDown",(5,))		#显示倒计时5秒
		self.addTimerCallBack(SWITCH_STATE_TIME,"stateChangePrompt",(csstatus.SPACE_ZLQJ_CHANGED_STATE,))
		if self.pieceState == csdefine.ZHEN_LONG_QI_JU_BLACK_STATE:
			self.pieceState = csdefine.ZHEN_LONG_QI_JU_WHITE_STATE
			self.OnBossStateChange(self.whiteStateEffectID)
		else:
			self.pieceState = csdefine.ZHEN_LONG_QI_JU_BLACK_STATE
			self.OnBossStateChange(self.blackStateEffectID)

	def stateChangePrompt( self, statusID ):
		"""
		状态切换的提示
		"""
		for player in self._spaceRoles:
			player.statusMessage(statusID)

	def stateChangeCountDown( self, countDownTime ):
		"""
		倒计时切换状态
		"""
		for player in self._spaceRoles:
			player.ShowCountDown( countDownTime )

	def clearChangeTimeID( self ):
		"""
		清除状态定时器 并停止切换Boss状态
		"""
		if self.changeStateTimeID:
			self.popTimer( self.changeStateTimeID )
			self.changeStateTimeID = 0
		bossIDList = self.getEntityRecord(self.bossID)
		if len(bossIDList) > 0:
			for bossID in bossIDList:
				entity = KBEngine.entities.get(bossID)
				for player in self._spaceRoles:
					player.client.ZhenLongQiJu_StopBossStateChange()

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
		if self.pointHasEntity[ coord ] != 0:	#如果该格子已有entity，则不再创建entity
			KBEDebug.DEBUG_MSG("Coord has entity: (%s,%s)."%(coord[0], coord[1]))
			return
		
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
		if self.pointHasEntity[ coord ] != 0:	#如果该格子已有entity，则不再创建entity
			KBEDebug.DEBUG_MSG("Coord has entity: (%s,%s)."%(coord[0], coord[1]))
			return
		
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
			self.createPiecesTimer = self.addTimerCallBack( 0.2,"createPieceEntities",(MAX_CREATE_NUMBER_EACH_TIME,) )
		elif number > 0:
			self.alreadCreateAmount += number
			self.createPartEntities( number )
		else:
			return

	def createPartEntities( self, number ):
		blackCoords = []
		whiteCoords = []
		
		for point,entityID in self.pointHasEntity.items() :
			if entityID != 0 or self.pointHasPiece[point] == HAS_PIECE_NONE :
				continue
			number -= 1
			if number < 0 :
				self.createPiecesTimer = self.addTimerCallBack( 0.2,"createPieceEntities",((self.allEntityAmount - self.alreadCreateAmount),) )
				break
			if self.pointHasPiece[point] == HAS_PIECE_BLACK :
				self.createBlackPiece( point )
				blackCoords.append( point )
			elif self.pointHasPiece[point] == HAS_PIECE_WHITE :
				self.createWhitePiece( point )
				whiteCoords.append( point )
		
		self.checkPiece( blackCoords, whiteCoords )		#还是要检查一下是否可消除，因为玩家可能已经与周围棋子对话过，使周围棋子改变了颜色
	
	def destroyAllPieces( self, coords = None ) :
		"""
		销毁coords中所有棋子
		"""
		if coords is None :
			coords = self.pointHasEntity.keys()
			
			#清空棋盘的情况，需要清空所有timer
			self.clearAllTimer()
		
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
	
	def clearAllTimer( self ):
		"""
		清空所有timer
		"""
		if self.createPiecesTimer:
			self.popTimer( self.createPiecesTimer )
		
		if self.checkPieceTimer:
			self.popTimer( self.checkPieceTimer )
		
		if self.refreshLinkTimer:
			self.popTimer( self.refreshLinkTimer )
		
		if self.destroyLinkTimer:
			self.popTimer( self.destroyLinkTimer )
		
		tempList = copy.copy(self.createOneTimerList)	#必须copy出来，因为一边遍历一边删除会有问题
		for timerArg in tempList:
			self.popTimer( timerArg )
	
	def timerValeDelCB( self, timerArg ):
		"""
		取消一个timer arg的回调，也可能是执行完了
		这里主要是处理掉一些存起来的timerArg
		"""
		if self.createPiecesTimer == timerArg:
			self.createPiecesTimer = 0
		
		elif self.checkPieceTimer == timerArg:
			self.checkPieceTimer = 0
		
		elif self.refreshLinkTimer == timerArg:
			self.refreshLinkTimer = 0
		
		elif self.destroyLinkTimer == timerArg:
			self.destroyLinkTimer = 0
		
		elif timerArg in self.createOneTimerList:
			self.createOneTimerList.remove( timerArg )

	def createPiece( self, entityID ) :
		"""
		在对应坐标上创建黑白棋子（反转棋子）
		"""
		for coord,hasEntity in self.pointHasEntity.items() :
			if hasEntity == entityID :
				if self.pointHasPiece[ coord ] == HAS_PIECE_BLACK :
					self.__removePiece( coord )
					self.createWhitePiece( coord )
					self.checkPieceTimer = self.addTimerCallBack(0.3,"checkPiece",([],[coord]))
				elif self.pointHasPiece[ coord ] == HAS_PIECE_WHITE :
					self.__removePiece( coord )
					self.createBlackPiece( coord )
					self.checkPieceTimer = self.addTimerCallBack(0.3,"checkPiece",([coord], []))

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
			if entity == None or len(bossIDList) <= 0:
				return
			if self.pieceState == self.pointHasPiece[pos]:
				entity.useSkillToEntity( self.damageSkillID, bossIDList[0] )
			else:
				entity.useSkillToEntity( self.reStoreHPSkillID, bossIDList[0] )
		self.refreshLinkTimer = self.addTimerCallBack(self.refreshTime,"refreshGobangLink",(allLinks,))
		self.destroyLinkTimer = self.addTimerCallBack( 0.5,"destroyAllPieces",(allLinks,) )

	def refreshGobangLink( self, points ) :
		"""
		@param points : 点列，形如[(x,y)]
		销毁五子棋中的超过5个连续相同的棋子，并重新刷出这些点
		"""
		count = len( points )
		randomRate = random.uniform( 0,1 )
		tempRate = 0.0
		index = 0
		for i, rate in enumerate( self.refreshCountRates ):
			tempRate += rate
			if randomRate < tempRate:
				index = i
				break
		refreshCount = count - (index+1)
		resultPoints = random.sample( points, refreshCount  )
		blackPoints = resultPoints[0:int(refreshCount/2)]
		whitePoints = resultPoints[int(refreshCount/2):refreshCount]
		for point in blackPoints:
			timerArg = self.addTimerCallBack(0.3,"createBlackPiece",(point,))
			self.createOneTimerList.append( timerArg )
		for point in whitePoints:
			timerArg = self.addTimerCallBack(0.3,"createWhitePiece",(point,))
			self.createOneTimerList.append( timerArg )
		self.checkPieceTimer = self.addTimerCallBack(1.2,"checkPiece",(blackPoints,whitePoints))
	
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
