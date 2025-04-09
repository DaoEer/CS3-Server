# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import random
import Math
import KBEMath
import Functions
from ObjectScript import Space
from SpaceCopyMagicMaze import SpaceCopyMagicMaze

ROOM_GRID_INTERVAL = range( 1, 10 ) 	# 房间格子区间

class SpaceCopyMagicMazeChildGYMZ( SpaceCopyMagicMaze ):
	"""
	幻阵迷宫 鬼域迷阵
	"""
	def __init__( self ):
		SpaceCopyMagicMaze.__init__( self )
		self.hasEntityPoint = {}
		self.direction = Math.Vector3(0,0,0)
		
	def initSpaceData( self, oneCenterPos, twoCenterPos, threeCenterPos, fourCenterPos, fiveCenterPos, sixCenterPos, sevenCenterPos, eightCenterPos, nineCenterPos, unitLength, redPortalID, greenPortalID, yellowPortalID):
		"""
		初始化数据
		"""														
		self.oneCenterPos = oneCenterPos		# 1号房间中心位置
		self.twoCenterPos = twoCenterPos		# 2号房间中心位置
		self.threeCenterPos = threeCenterPos	# 3号房间中心位置
		self.fourCenterPos = fourCenterPos		# 4号房间中心位置
		self.fiveCenterPos = fiveCenterPos		# 5号房间中心位置
		self.sixCenterPos = sixCenterPos		# 6号房间中心位置	
		self.sevenCenterPos = sevenCenterPos	# 7号房间中心位置
		self.eightCenterPos = eightCenterPos	# 8号房间中心位置
		self.nineCenterPos = nineCenterPos		# 9号房间中心位置
		self.unitLength = unitLength			# 房间的宽度
		self.redPortalID = redPortalID			# 红色传送门-spellboxID
		self.greenPortalID = greenPortalID		# 绿色传送门-spellboxID
		self.yellowPortalID = yellowPortalID	# 黄色传送门-spellboxID
		for gird in ROOM_GRID_INTERVAL:
			self.girdPiece[gird] = []				#房间编号 : 传送门entityID列表

	def initCreatePortal( self ):
		"""
		初始化创建传送门
		"""
		allPosList = self.getMultipleListMerge()
		yellowPos = allPosList[ random.randint(0,len(allPosList)-1)]
		for coord, pos in yellowPos.items():
			strpos = pos
			tempCoord = coord
			break
		state = { "spawnPos" : Math.Vector3(strpos) }
		if tempCoord == (0,1) or tempCoord == (0,-1):
			direction = Math.Vector3( 0.0, 0.0, 92.0 )
		else:
			direction = Math.Vector3( 0.0, 0.0, 0.0)
		self.createSpellBox( str(self.yellowPortalID), KBEMath.Unreal2KBEnginePosition( Math.Vector3(strpos) ), KBEMath.Unreal2KBEngineDirection(direction), state )
		#创建一号房间的传送门
		onePosList = self.getRoomPosition( self.oneCenterPos )
		if strpos in onePosList.values():
			onePosList.pop( tempCoord )
		self.creatPortal( onePosList, 1 )
		#创建二号房间的传送门
		twoPosList = self.getRoomPosition( self.twoCenterPos )
		if strpos in twoPosList.values():
			twoPosList.pop( tempCoord )
		self.creatPortal( twoPosList, 2 )
		#创建三号房间的传送门
		threePosList = self.getRoomPosition( self.threeCenterPos )
		if strpos in threePosList.values():
			threePosList.pop( tempCoord )
		self.creatPortal( threePosList, 3 )
		#创建四号房间的传送门
		fourPosList = self.getRoomPosition( self.fourCenterPos )
		if strpos in fourPosList.values():
			fourPosList.pop( tempCoord )
		self.creatPortal( fourPosList, 4 )
		#创建五号房间的传送门
		fivePosList =  self.getRoomPosition( self.fiveCenterPos )
		self.creatPortal( fivePosList, 5 )
		#创建六号房间的传送门
		sixPosList = self.getRoomPosition( self.sixCenterPos )
		if strpos in sixPosList.values():
			sixPosList.pop( tempCoord )
		self.creatPortal( sixPosList, 6 )
		#创建七号房间的传送门
		sevenPosList = self.getRoomPosition( self.sevenCenterPos )
		if strpos in sevenPosList.values():
			sevenPosList.pop( tempCoord )
		self.creatPortal( sevenPosList, 7 )
		#创建八号房间的传送门
		eightPosList = self.getRoomPosition( self.eightCenterPos )
		if strpos in eightPosList.values():
			eightPosList.pop( tempCoord )
		self.creatPortal( eightPosList, 8 )
		#创建九号房间的传送门
		ninePosList = self.getRoomPosition( self.nineCenterPos )
		if strpos in ninePosList.values():
			ninePosList.pop( tempCoord )
		self.creatPortal( ninePosList, 9 )

	def creatPortal( self, posList, index ):
		"""
		创建对应的传送门
		"""
		portalList = self.getPortalTypeList()
		for coord, pos in posList.items():
			portalID = random.sample( portalList, 1 )
			if coord == (0,1) or coord == (0,-1):
				direction = Math.Vector3( 0.0, 0.0, 92.0 )
			else:
				direction = Math.Vector3( 0.0, 0.0, 0.0 )
			entity = self.createSpellBox( portalID[0], KBEMath.Unreal2KBEnginePosition( Math.Vector3(pos) ), KBEMath.Unreal2KBEngineDirection(direction), {} )
			self.girdPiece[index].append(entity.id)
			self.hasEntityPoint[entity.id] =  coord

	def onSendTheResults( self, entityID, playerEntityID ):
		"""
		交互结果
		"""
		entity = KBEngine.entities.get(entityID,None)
		if entity.scriptID == str(self.redPortalID):
			for key, value in self.girdPiece.items():
				if entityID in value:
					newPos = self.getRoomRedLocation( key, self.hasEntityPoint[entityID] )
					self.onTeleportSpace( newPos, playerEntityID)
		else:
			for key, value in self.girdPiece.items():
				if entityID in value:
					newPos = self.getRoomGreenLocation( key, self.hasEntityPoint[entityID] )
					self.onTeleportSpace( newPos, playerEntityID)

	def onTeleportSpace( self, position, playerEntityID ):
		"""
		传送到指定位置
		"""
		playerCell = KBEngine.entities.get(playerEntityID,None)
		spaceEntity = playerCell.getCurrentSpace()
		playerCell.gotoSpaceUE4( spaceEntity.scriptID, position, self.direction )

	def getRoomPosition( self, centerPos ):
		"""
		获取每个房间传送门的位置
		"""
		positionList = {}
		upwardPos = ( centerPos[0], centerPos[1] + self.unitLength * 1, centerPos[2] )
		positionList[(0,1)] = upwardPos
		downPos = ( centerPos[0], centerPos[1] + self.unitLength * -1, centerPos[2] )
		positionList[(0,-1)] = downPos
		leftPos = ( centerPos[0] + self.unitLength * -1, centerPos[1], centerPos[2] )
		positionList[(-1,0)] = leftPos
		rightPos= ( centerPos[0] + self.unitLength * 1, centerPos[1], centerPos[2] )
		positionList[(1,0)] = rightPos
		return positionList

	def getPortalTypeList( self ):
		"""
		获取传送门类型列表
		"""
		portalList = []
		portalList.append(self.redPortalID)
		portalList.append(self.greenPortalID)
		return portalList

	def getMultipleListMerge( self ):
		"""
		获取全部房间的位置除了五号房间
		"""
		allPosList = []
		onePosList = self.getRoomPosition( self.oneCenterPos )
		allPosList.append(onePosList)
		twoPosList = self.getRoomPosition( self.twoCenterPos )
		allPosList.append(twoPosList)
		threePosList = self.getRoomPosition( self.threeCenterPos )
		allPosList.append(threePosList)
		fourPosList = self.getRoomPosition( self.fourCenterPos )
		allPosList.append(fourPosList)
		sixPosList = self.getRoomPosition( self.sixCenterPos )
		allPosList.append(sixPosList)
		sevenPosList = self.getRoomPosition( self.sevenCenterPos )
		allPosList.append(sevenPosList)
		eightPosList = self.getRoomPosition( self.eightCenterPos )
		allPosList.append(eightPosList)
		ninePosList = self.getRoomPosition( self.nineCenterPos )
		allPosList.append(ninePosList)
		return allPosList

	def getRoomRedLocation( self, index, position ):
		"""
		获取交互的红色entity位置
		"""
		if index == 1:
			if position[0] == 0 and position[1] == 1:
				return self.sevenCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.fourCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.twoCenterPos
			else:
				return self.threeCenterPos
		if index == 2:
			if position[0] == 0 and position[1] == 1:
				return self.eightCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.fiveCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.threeCenterPos
			else:
				return self.oneCenterPos
		if index == 3:
			if position[0] == 0 and position[1] == 1:
				return self.nineCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.sixCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.oneCenterPos
			else:
				return self.twoCenterPos
		if index == 4:
			if position[0] == 0 and position[1] == 1:
				return self.oneCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.sevenCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.fiveCenterPos
			else:
				return self.sixCenterPos
		if index == 5:
			if position[0] == 0 and position[1] == 1:
				return self.twoCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.eightCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.sixCenterPos
			else:
				return self.fourCenterPos
		if index == 6:
			if position[0] == 0 and position[1] == 1:
				return self.threeCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.nineCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.fourCenterPos
			else:
				return self.fiveCenterPos
		if index == 7:
			if position[0] == 0 and position[1] == 1:
				return self.fourCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.oneCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.eightCenterPos
			else:
				return self.nineCenterPos
		if index == 8:
			if position[0] == 0 and position[1] == 1:
				return self.fiveCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.twoCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.nineCenterPos
			else:
				return self.sevenCenterPos
		if index == 9:
			if position[0] == 0 and position[1] == 1:
				return self.sixCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.threeCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.sevenCenterPos
			else:
				return self.eightCenterPos

	def getRoomGreenLocation( self, index, position ):
		"""
		获取交互的绿色entity位置
		"""
		if index == 1:
			if position[0] == 0 and position[1] == 1:
				return self.fourCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.sevenCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.threeCenterPos
			else:
				return self.twoCenterPos
		if index == 2:
			if position[0] == 0 and position[1] == 1:
				return self.fiveCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.eightCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.oneCenterPos
			else:
				return self.threeCenterPos
		if index == 3:
			if position[0] == 0 and position[1] == 1:
				return self.sixCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.nineCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.twoCenterPos
			else:
				return self.oneCenterPos
		if index == 4:
			if position[0] == 0 and position[1] == 1:
				return self.sevenCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.oneCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.sixCenterPos
			else:
				return self.fiveCenterPos
		if index == 5:
			if position[0] == 0 and position[1] == 1:
				return self.eightCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.twoCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.fourCenterPos
			else:
				return self.sixCenterPos
		if index == 6:
			if position[0] == 0 and position[1] == 1:
				return self.nineCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.threeCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.fiveCenterPos
			else:
				return self.fourCenterPos
		if index == 7:
			if position[0] == 0 and position[1] == 1:
				return self.oneCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.fourCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.nineCenterPos
			else:
				return self.eightCenterPos
		if index == 8:
			if position[0] == 0 and position[1] == 1:
				return self.twoCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.fiveCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.sevenCenterPos
			else:
				return self.nineCenterPos
		if index == 9:
			if position[0] == 0 and position[1] == 1:
				return self.threeCenterPos
			elif position[0] == 0 and position[1] == -1:
				return self.sixCenterPos
			elif position[0] == -1 and position[1] == 0:
				return self.eightCenterPos
			else:
				return self.sevenCenterPos

	def displayLocationAndColor( self ):
		"""
		显示小地图标识
		"""
		#获取黄色传送门位置
		yellowIdList = self.getEntityRecord(str(self.yellowPortalID))
		for id in yellowIdList:
			yellowEntity = KBEngine.entities.get( id )
			if not yellowEntity:
				return
			for playerCell in self._spaceRoles:
				playerCell.client.ClIENT_DisplayLocationAndColor(KBEMath.KBEngine2UnrealPosition(yellowEntity.position), 1 )

		#获取红色传送门位置
		redIdList = self.getEntityRecord(str(self.redPortalID))
		for id in redIdList:
			redEntity = KBEngine.entities.get( id )
			if not redEntity:
				return
			for playerCell in self._spaceRoles:
				playerCell.client.ClIENT_DisplayLocationAndColor(KBEMath.KBEngine2UnrealPosition(redEntity.position), 2 )

		#获取绿色传送门位置
		greenIdList = self.getEntityRecord(str(self.greenPortalID))
		for id in greenIdList:
			greenEntity = KBEngine.entities.get( id )
			if not greenEntity:
				return
			for playerCell in self._spaceRoles:
				playerCell.client.ClIENT_DisplayLocationAndColor(KBEMath.KBEngine2UnrealPosition(greenEntity.position), 3 )

