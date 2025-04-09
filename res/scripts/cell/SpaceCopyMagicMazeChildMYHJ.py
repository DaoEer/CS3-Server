# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import random
import Math
from ObjectScript import Space
from ObjectScript.ObjectScriptFactory import g_objFactory
from SpaceCopyMagicMaze import SpaceCopyMagicMaze
import KBEMath

NIGHTMARE_COORD_X_RANGE	= range( -5,5 )	#横轴坐标取值范围
NIGHTMARE_COORD_Y_RANGE	= range( -5,5 )	#纵轴坐标取值范围

SAME_NUMBER_THREE = 3	# 光效模型相连相邻且相同的最小值
MAX_CREATE_NUMBER_EACH_TIME = 20	# 每次最大创建模型数量

HAS_MODEL_NONE	=	0	# 无
HAS_MODEL_MEI	=	1	# 梅
HAS_MODEL_LAN	=	2	# 兰
HAS_MODEL_ZHU	=	3	# 竹
HAS_MODEL_JU	=	4	# 菊

class SpaceCopyMagicMazeChildMYHJ( SpaceCopyMagicMaze ):
	"""
	幻阵迷宫 梦魇画卷
	"""
	def __init__( self ):
		SpaceCopyMagicMaze.__init__( self )
		self.coord_A = (0,0)
		self.coord_B = (0,0)

	def initSpaceData( self, originPos, unitLength, damageSkillID, clubID, orchidID, banbooID, chryID, meiBossID, lanBossID, zhuBossID, juBossID ):
		"""
		初始化数据
		"""	
		self.originPos = originPos
		self.unitLength = unitLength
		self.damageSkillID = damageSkillID
		self.clubID = clubID			# 梅
		self.orchidID = orchidID		# 兰
		self.banbooID = banbooID		# 竹
		self.chryID = chryID			# 菊
		self.meiBossID = meiBossID		# 梅·画卷
		self.lanBossID = lanBossID		# 兰·画卷
		self.zhuBossID = zhuBossID		# 竹·画卷
		self.juBossID = juBossID		# 菊·画卷

		for x in NIGHTMARE_COORD_X_RANGE :
			for y in NIGHTMARE_COORD_Y_RANGE :
				self.pointHasPiece[(x,y)] = HAS_MODEL_NONE		# 模型坐标（x,y） : 模型种类
				self.pointHasEntity[(x,y)] = 0					# 模型坐标（x,y） : 模型entityID

	def initPlantModel( self ):
		"""
		初始化一个总共有number个的梅兰竹菊四种光效模型，要求不能有连续3个相邻且相同的光效模型。
		"""
		for hasPiece in list( self.pointHasPiece.values() ):
			if hasPiece != HAS_MODEL_NONE:
				return
		allPoints = list(self.pointHasPiece.keys())
		self.randomInitPoints( allPoints )
		#去除连续3个相邻且相同的光效模型
		gobangLinks = self.checkAllModelLink()
		while gobangLinks :
			self.randomInitPoints( gobangLinks )
			gobangLinks = self.checkModelLink( gobangLinks )
		self.allEntityAmount = len(allPoints)
		self.alreadCreateAmount = 0
		self.createPieceEntities( len(allPoints) )
		
	def randomInitPoints( self, points ):
		"""
		@param points : 点列，形如[(x,y)]
		随机初始化梅兰竹菊模型光效
		"""
		count = len( points )
		random.shuffle( points )  #随机重新排列坐标点
		meiPoints = points[0:int(count/4)]
		lanPoints = points[int(count/4):int(count/2)]
		zhuPoints = points[int(count/2):int(3*count/4)]
		juPoints = points[int(3*count/4):count]
		for point in meiPoints:
			self.pointHasPiece[point] = HAS_MODEL_MEI
		for point in lanPoints:
			self.pointHasPiece[point] = HAS_MODEL_LAN
		for point in zhuPoints:
			self.pointHasPiece[point] = HAS_MODEL_ZHU
		for point in juPoints:
			self.pointHasPiece[point] = HAS_MODEL_JU

	def createPieceEntities( self, number ):
		"""
		@param number : 数量
		创建平台中一定数量的梅兰竹菊entity
		"""
		if number > MAX_CREATE_NUMBER_EACH_TIME:
			self.addTimerCallBack( 0.2,"createPieceEntities",(MAX_CREATE_NUMBER_EACH_TIME,) )
		elif number > 0:
			self.alreadCreateAmount += number
			self.createPartEntities( number )
		else:
			return

	def createPartEntities( self, number ):
		"""
		创建对应位置的梅兰竹菊entity
		"""
		for point,entityID in self.pointHasEntity.items():
			if entityID != 0 or self.pointHasPiece[point] == HAS_MODEL_NONE:
				continue
			number -= 1
			if number < 0:
				self.addTimerCallBack( 0.2,"createPieceEntities",((self.allEntityAmount - self.alreadCreateAmount),) )
				break
			if self.pointHasPiece[point] == HAS_MODEL_MEI :
				self.createMeiPiece( point )
			elif self.pointHasPiece[point] == HAS_MODEL_LAN:
				self.createLanPiece( point )
			elif self.pointHasPiece[point] == HAS_MODEL_ZHU:
				self.createZhuPiece( point )
			elif self.pointHasPiece[point] == HAS_MODEL_JU:
				self.createJuPiece( point)

	def destroyAllPieces( self, coords = None ) :
		"""
		销毁场上所有光效模型
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

	def __removePiece( self, coord ) :
		"""
		从平台上移除光效模型
		"""
		self.pointHasPiece[ coord ] = HAS_MODEL_NONE
		self.pointHasEntity[ coord ] = 0

	def getPlatPosition( self, coord_x, coord_y ):
		"""
		获取平台坐标为( coord_x,coord_y )的点在游戏中的位置
		"""
		originPos = self.originPos
		unitLength = self.unitLength
		position = ( originPos[0] + unitLength * coord_x, originPos[1] + unitLength * coord_y, originPos[2] )
		return position

	def createMeiPiece( self, coord ):
		"""
		在坐标coord上创建梅
		"""
		if self.pointHasEntity[ coord ] != 0 or self.isComplete:
			return
		position = self.getPlatPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = self.createSpellBox( str(self.clubID), KBEMath.Unreal2KBEnginePosition( Math.Vector3(position) ), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_MODEL_MEI
		self.pointHasEntity[ coord ] = entity.id
		self.deleteModelEndCheckLink( coord )

	def createLanPiece( self, coord ):
		"""
		在坐标coord上创建兰
		"""
		if self.pointHasEntity[ coord ] != 0 or self.isComplete:
			return
		position = self.getPlatPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = self.createSpellBox( str(self.orchidID), KBEMath.Unreal2KBEnginePosition( Math.Vector3(position) ), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_MODEL_LAN
		self.pointHasEntity[ coord ] = entity.id
		self.deleteModelEndCheckLink( coord )

	def createZhuPiece( self, coord ):
		"""
		在坐标coord上创建竹
		"""
		if self.pointHasEntity[ coord ] != 0 or self.isComplete:
			return
		position = self.getPlatPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = self.createSpellBox( str(self.banbooID), KBEMath.Unreal2KBEnginePosition( Math.Vector3(position) ), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_MODEL_ZHU
		self.pointHasEntity[ coord ] = entity.id
		self.deleteModelEndCheckLink( coord )

	def createJuPiece( self, coord ):
		"""
		在坐标coord上创建菊
		"""
		if self.pointHasEntity[ coord ] != 0 or self.isComplete:
			return
		position = self.getPlatPosition( coord[0], coord[1] )
		state = { "spawnPos" : Math.Vector3(position)}
		entity = self.createSpellBox( str(self.chryID), KBEMath.Unreal2KBEnginePosition( Math.Vector3(position) ), Math.Vector3(0,0,0), state )
		self.pointHasPiece[ coord ] = HAS_MODEL_JU
		self.pointHasEntity[ coord ] = entity.id
		self.deleteModelEndCheckLink( coord )

	def exChangeModelLink( self ):
		"""
		交换两个相邻的光效模型
		"""
		if len(self.sceneObjectCoordList) <= 1:
			return

		for i in range(len(self.sceneObjectCoordList) - 1):
			for j in range(i+1, len(self.sceneObjectCoordList)):
				for coord, entityID in self.pointHasEntity.items():
					if entityID == self.sceneObjectCoordList[i]:
						self.coord_A = coord
					if j < len(self.sceneObjectCoordList) and entityID == self.sceneObjectCoordList[j]:
						self.coord_B = coord
				if (abs(self.coord_A[0] - self.coord_B[0]) == 1 and self.coord_A[1] == self.coord_B[1]) or (abs(self.coord_A[1] - self.coord_B[1]) == 1 and self.coord_A[0] == self.coord_B[0]):
					self.exChangeTypePosition( self.coord_A, self.coord_B )
					correct_A = self.checkModel( [self.coord_A], [self.coord_B] )
					if not correct_A:
						self.exChangeTypePosition( self.coord_A, self.coord_B )
					break

	def exChangeTypePosition( self, coord_A, coord_B ):
		"""
		交换类型位置
		"""
		temp = self.pointHasPiece[coord_A]
		self.pointHasPiece[coord_A] = self.pointHasPiece[coord_B]
		self.pointHasPiece[coord_B] = temp

	def exChangeEntityPosition( self, coord_A, coord_B ):
		"""
		交换entity位置
		"""
		temp = self.pointHasEntity[coord_A]
		self.pointHasEntity[coord_A] = self.pointHasEntity[coord_B]
		self.pointHasEntity[coord_B] = temp

	def checkModel( self, coord_A, coord_B ):
		"""
		检查光效模型
		"""
		allLinks = self.checkModelLink( coord_A + coord_B )
		if not allLinks:
			return False
		position_A = self.getPlatPosition( self.coord_A[0], self.coord_A[1])
		position_B = self.getPlatPosition( self.coord_B[0], self.coord_B[1])
		entity_A = KBEngine.entities.get( self.pointHasEntity[self.coord_A], None )
		entity_B = KBEngine.entities.get( self.pointHasEntity[self.coord_B], None )
		entity_A.moveStart( KBEMath.Unreal2KBEnginePosition(Math.Vector3(position_B)) )
		entity_B.moveStart( KBEMath.Unreal2KBEnginePosition(Math.Vector3(position_A)) )
		self.exChangeEntityPosition( self.coord_A, self.coord_B )
		self.sceneObjectCoordList.remove(self.pointHasEntity[self.coord_A])
		self.sceneObjectCoordList.remove(self.pointHasEntity[self.coord_B])
		self.addTimerCallBack( 1.2, "damageToMonsters", (allLinks,))
		self.addTimerCallBack( 1.5, "refreshModelLink", (allLinks,) )
		
		return True

	def damageToMonsters( self, allLinks ):
		"""
		对梅兰竹菊四种怪物造成伤害
		"""
		for point in allLinks:
			entityID = self.pointHasEntity.get( point,0 )
			entity = KBEngine.entities.get( entityID, None )
			if not entity:
				return
			if self.pointHasPiece[point] == HAS_MODEL_MEI:
				meiBossIDList = self.getEntityRecord(str(self.meiBossID))
				if len(meiBossIDList) > 0:
					entity.useSkillToEntity( self.damageSkillID, meiBossIDList[0] )
			elif self.pointHasPiece[point] == HAS_MODEL_LAN:
				lanBossIDList = self.getEntityRecord(str(self.lanBossID))
				if len(lanBossIDList) > 0:
					entity.useSkillToEntity( self.damageSkillID, lanBossIDList[0] )
			elif self.pointHasPiece[point] == HAS_MODEL_ZHU:
				zhuBossIDList = self.getEntityRecord(str(self.zhuBossID))
				if len(zhuBossIDList) > 0:
					entity.useSkillToEntity( self.damageSkillID, zhuBossIDList[0] )
			elif self.pointHasPiece[point] == HAS_MODEL_JU:
				juBossIDList = self.getEntityRecord(str(self.juBossID))
				if len(juBossIDList) > 0:
					entity.useSkillToEntity( self.damageSkillID, juBossIDList[0] )

	def refreshModelLink( self, points ):
		"""
		@param points : 点列，形如[(x,y)]
		销毁平台中的超过3个连续相同的模型，并重新刷出这些点
		"""
		self.destroyAllPieces( points )
		count = len( points )
		random.shuffle( points )
		meiPoints = points[0:int(count/4)]
		lanPoints = points[int(count/4):int(count/2)]
		zhuPoints = points[int(count/2):int(3*count/4)]
		juPoints = points[int(3*count/4):count]
		meiBossIDList = self.getEntityRecord(str(self.meiBossID))
		lanBossIDList = self.getEntityRecord(str(self.lanBossID))
		zhuBossIDList = self.getEntityRecord(str(self.zhuBossID))
		juBossIDList = self.getEntityRecord(str(self.juBossID))
		if len(meiBossIDList) > 0 or len(lanBossIDList) > 0 or len(zhuBossIDList) > 0 or len(juBossIDList) > 0:
			for point in meiPoints:
				self.addTimerCallBack(9.0,"createMeiPiece",(point,))
			for point in lanPoints:
				self.addTimerCallBack(9.0,"createLanPiece",(point,))
			for point in zhuPoints:
				self.addTimerCallBack(9.0,"createZhuPiece",(point,))
			for point in juPoints:
				self.addTimerCallBack(9.0,"createJuPiece",(point,))

	def deleteModelEndCheckLink( self, coord ):
		"""
		销毁后重新生成之后重新刷新是否存在连续3个相邻且相同的光效模型
		"""
		gobangLinks = self.checkModelLink( [coord] )
		if gobangLinks:
			self.destroyAllPieces( gobangLinks )
			count = len( gobangLinks )
			random.shuffle( gobangLinks )
			meiPoints = gobangLinks[0:int(count/4)]
			lanPoints = gobangLinks[int(count/4):int(count/2)]
			zhuPoints = gobangLinks[int(count/2):int(3*count/4)]
			juPoints = gobangLinks[int(3*count/4):count]
			for point in meiPoints:
				self.createMeiPiece(point)
			for point in lanPoints:
				self.createLanPiece(point)
			for point in zhuPoints:
				self.createZhuPiece(point)
			for point in juPoints:
				self.createJuPiece(point)

	def checkAllModelLink( self ):
		"""
		检查平台所有的点是否存在连续3个相邻且相同的光效模型
		"""
		needCheckCoords = set()
		for x in NIGHTMARE_COORD_X_RANGE :
			needCheckCoords.add( (x,NIGHTMARE_COORD_Y_RANGE[0]) )
			needCheckCoords.add( (x,NIGHTMARE_COORD_Y_RANGE[-1]) )
		for y in NIGHTMARE_COORD_Y_RANGE :
			needCheckCoords.add( (NIGHTMARE_COORD_X_RANGE[0],y) )
		
		return self.checkModelLink( needCheckCoords )

	def checkModelLink( self, coords ):
		"""
		查coords中所在点是否存在连续3个相邻且相同的模型
		"""
		needCheckRows = set()
		needCheckColumns = set()
		for coord in coords :
			needCheckRows.add( coord[0] )
			needCheckColumns.add( coord[1] )
		
		allLinks = self.getRowAndColumnLink( needCheckRows, needCheckColumns )
		return list( allLinks )

	def getRowAndColumnLink( self, rowRange = NIGHTMARE_COORD_X_RANGE, columnRange = NIGHTMARE_COORD_Y_RANGE ) :
		"""
		获取横竖线上连续3个相邻且相同的模型
		"""
		allLinks = set()
		# 检查行
		for row in rowRange :
			rowLink = self.getRowLink( row, SAME_NUMBER_THREE )
			if rowLink :
				allLinks.update( rowLink )  #将行 最少连续3个相同的模型坐标添加到allLinks字典中
		# 检查列
		for column in columnRange :
			columnLink = self.getColumnLink( column, SAME_NUMBER_THREE )
			if columnLink :
				allLinks.update( columnLink )  #将列 最少连续3个相同的模型坐标添加到allLinks字典中
		
		return allLinks

	def getRowLink( self, rowIndex, minSameNumber ) :
		"""
		获取第rowIndex行的连续minSameNumber个以上相同的模型
		"""
		assert rowIndex in NIGHTMARE_COORD_X_RANGE,"invalid row index:%s." % rowIndex
		rowLinks = set()
		x = rowIndex
		y_begin = NIGHTMARE_COORD_Y_RANGE[ 0 ]
		y_end = y_begin
		while y_end <= NIGHTMARE_COORD_Y_RANGE[-1] :
			while y_end <= NIGHTMARE_COORD_Y_RANGE[-1] and (x,y_begin) in self.pointHasPiece and\
			(x,y_end) in self.pointHasPiece and self.pointHasPiece[(x,y_begin)] == self.pointHasPiece[(x,y_end)] :
				y_end += 1
			if (x,y_begin) in self.pointHasPiece:
				pieceType = self.pointHasPiece[(x,y_begin)]
				if y_end - y_begin >= minSameNumber and pieceType != HAS_MODEL_NONE :
					for y in range(y_begin,y_end) :
						rowLinks.add( (x,y) )
			y_begin = y_end
		
		return rowLinks
	
	def getColumnLink( self, columnIndex, minSameNumber ) :
		"""
		获取第columnIndex列的连续minSameNumber个以上相同的模型
		"""
		assert columnIndex in NIGHTMARE_COORD_Y_RANGE,"invalid row index:%s." % columnIndex
		columnLinks = set()
		y = columnIndex
		x_begin = NIGHTMARE_COORD_X_RANGE[ 0 ]
		x_end = x_begin
		while x_end <= NIGHTMARE_COORD_X_RANGE[-1] :
			while x_end <= NIGHTMARE_COORD_X_RANGE[-1] and (x_begin,y) in self.pointHasPiece and\
			(x_end,y) in self.pointHasPiece and self.pointHasPiece[(x_begin,y)] == self.pointHasPiece[(x_end,y)] :
				x_end += 1
			if (x_begin,y) in self.pointHasPiece:
				pieceType = self.pointHasPiece[(x_begin,y)]
				if x_end - x_begin >= minSameNumber and pieceType != HAS_MODEL_NONE :
					for x in range(x_begin,x_end) :
						columnLinks.add( (x,y) )
			x_begin = x_end
		
		return columnLinks