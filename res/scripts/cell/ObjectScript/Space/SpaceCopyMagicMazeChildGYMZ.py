# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import random
import Math
import Functions
from ObjectScript import Space
from ObjectScript.Space.SpaceCopyMagicMazeChild import SpaceCopyMagicMazeChild

class SpaceCopyMagicMazeChildGYMZ( SpaceCopyMagicMazeChild ):
	"""
	幻阵迷宫 鬼域迷阵
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChild.__init__( self )
		
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyMagicMazeChild.initData( self, configData )
		oneCenterPos = configData["SpaceData"].get( "oneCenterPos", "" )
		if oneCenterPos:													# 1号房间中心位置
			oneCenterPos = oneCenterPos.split("|")
			self.oneCenterPos = tuple( [ float(i) for i in oneCenterPos ] )
		twoCenterPos = configData["SpaceData"].get( "twoCenterPos", "" )
		if twoCenterPos:													# 2号房间中心位置
			twoCenterPos = twoCenterPos.split("|")
			self.twoCenterPos = tuple( [ float(i) for i in twoCenterPos ] )
		threeCenterPos = configData["SpaceData"].get( "threeCenterPos", "" )
		if threeCenterPos:													# 3号房间中心位置
			threeCenterPos = threeCenterPos.split("|")
			self.threeCenterPos = tuple( [ float(i) for i in threeCenterPos ] )
		fourCenterPos = configData["SpaceData"].get( "fourCenterPos", "" )
		if fourCenterPos:													# 4号房间中心位置
			fourCenterPos = fourCenterPos.split("|")
			self.fourCenterPos = tuple( [ float(i) for i in fourCenterPos ] )
		fiveCenterPos = configData["SpaceData"].get( "fiveCenterPos", "" )
		if fiveCenterPos:													# 5号房间中心位置
			fiveCenterPos = fiveCenterPos.split("|")
			self.fiveCenterPos = tuple( [ float(i) for i in fiveCenterPos ] )
		sixCenterPos = configData["SpaceData"].get( "sixCenterPos", "" )
		if sixCenterPos:													# 6号房间中心位置
			sixCenterPos = sixCenterPos.split("|")
			self.sixCenterPos = tuple( [ float(i) for i in sixCenterPos ] )
		sevenCenterPos = configData["SpaceData"].get( "sevenCenterPos", "" )
		if sevenCenterPos:													# 7号房间中心位置
			sevenCenterPos = sevenCenterPos.split("|")
			self.sevenCenterPos = tuple( [ float(i) for i in sevenCenterPos ] )
		eightCenterPos = configData["SpaceData"].get( "eightCenterPos", "" )
		if eightCenterPos:													# 8号房间中心位置
			eightCenterPos = eightCenterPos.split("|")
			self.eightCenterPos = tuple( [ float(i) for i in eightCenterPos ] )
		nineCenterPos = configData["SpaceData"].get( "nineCenterPos", "" )
		if nineCenterPos:													# 9号房间中心位置
			nineCenterPos = nineCenterPos.split("|")
			self.nineCenterPos = tuple( [ float(i) for i in nineCenterPos ] )
		self.unitLength = float(configData["SpaceData"].get( "unitLength", 0.0) )	# 房间的宽度
		self.redPortalID = configData["SpaceData"].get( "redPortalID", "" )			# 红色传送门-spellboxID
		self.greenPortalID = configData["SpaceData"].get( "greenPortalID", "" )		# 绿色传送门-spellboxID
		self.yellowPortalID = configData["SpaceData"].get( "yellowPortalID", "" )		# 黄色传送门-spellboxID

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyMagicMazeChild.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.oneCenterPos, self.twoCenterPos, self.threeCenterPos, self.fourCenterPos, self.fiveCenterPos,\
			self.sixCenterPos, self.sevenCenterPos, self.eightCenterPos, self.nineCenterPos, self.unitLength, self.redPortalID, self.greenPortalID, self.yellowPortalID)

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		DEBUG_MSG( "Player(%s) leave space(%s)! reason:%s." % ( playerRole.id, selfEntity.id, packArgs[ "leaveReason" ] ) )
		SpaceCopyMagicMazeChild.onLeave( self, selfEntity, playerRole, packArgs )
		for playerCell in selfEntity._spaceRoles:
			playerCell.client.ClIENT_ClearLocationAndColor()