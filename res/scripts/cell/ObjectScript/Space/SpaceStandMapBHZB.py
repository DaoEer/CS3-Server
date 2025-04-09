# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceBase import SpaceBase
import Const
import KBEngine
import csdefine
import KBEDebug
from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory

class SpaceStandMapBHZB( SpaceBase ):
	"""
	帮会争霸沙盘大地图
	"""
	def __init__( self ):
		SpaceBase.__init__( self )

	def initData( self, configData ):
		SpaceBase.initData( self, configData )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceBase.onEnter( self, selfEntity, playerRole, packArgs )
		playerRole.setLineNumber( int(selfEntity.spaceKey) )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceBase.onLeave( self, selfEntity, playerRole, packArgs )
		playerRole.setLineNumber( 0 )
		playerRole.resetArmyModelList()

	def onTeleportCompleted( self, selfEntity, playerRole ):
		# 播放场景语音
		SpaceBase.onTeleportCompleted( self, selfEntity, playerRole )
		
		modelNumList = playerRole.getRoleBarracksSoldierModelNumbers()
		playerRole.setArmyModelList( modelNumList )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceBase.onLogin( self, selfEntity, playerRole )
		playerRole.setLineNumber( int(selfEntity.spaceKey) )

	def getPackDomainData( self, playerEntity, args ):
		"""
		"""
		gotoArgs = SpaceBase.getPackDomainData( self, playerEntity, args )
		gotoArgs["spaceKey"] = str(playerEntity.queryTemp( "lineNumber",-1))
		
		gotoArgs[ "currSpaceScriptID" ] = playerEntity.getCurrentSpaceScriptID()

		if int(playerEntity.getCurrentSpaceData( Const.SPACE_DATA_SPACE_TYPE )) == csdefine.SPACE_TYPE_MULTILINE:
			gotoArgs[ "currSpaceLineNumber" ] = int(playerEntity.getCurrentSpaceData(Const.SPACE_DATA_LINE_NUMBER))
		else:
			gotoArgs[ "currSpaceLineNumber" ] = 0
		return gotoArgs

	def createSpawnPoint( self, selfEntity ):
		"""加载刷新点"""
		KBEngine.globalData["BHZBManager"].requestBHZBPointDatas( int(selfEntity.spaceKey), selfEntity.base )

	def onRequestBHZBPointDatasCB( self, selfEntity, pointDatas ):
		"""
		除了该分线据点数据后  加载刷新点数据了
		"""
		if self._spawnFile:
			pointDataDict = {}
			for pointData in pointDatas:
				pointDataDict[pointData.index] = pointData.getDictFromObj( pointData )

			g_spawnPointFactory.initSpawnPointNPCPoint( selfEntity, self._spawnFile,pointDataDict )
