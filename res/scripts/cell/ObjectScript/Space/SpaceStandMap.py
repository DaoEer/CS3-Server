# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceBase import SpaceBase
import Const
import KBEngine
import csdefine
import KBEDebug
from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory
import Math
import Functions

class SpaceStandMap( SpaceBase ):
	"""
	沙盘大地图
	"""
	def __init__( self ):
		SpaceBase.__init__( self )
		self.armLength = 0.0
		self.cameraRotation = Math.Vector3(0,0,0)

	def initData( self, configData ):
		SpaceBase.initData( self, configData )
		self.armLength = configData["SpaceData"].get("armLength",0.0)
		cameraRotationStr = configData["SpaceData"].get( "cameraRotation","" )
		self.cameraRotation = Functions.vector3TypeConvert( cameraRotationStr )

	def getEnterTrainGrounModeData( self ):
		"""
		"""
		return self.armLength, self.cameraRotation

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
		KBEngine.globalData["SpaceManager"].remoteCallDomain( selfEntity.scriptID,"decPlayerAmount",(int(selfEntity.spaceKey),playerRole.playerDBID))
		playerRole.resetArmyModelList()
		if playerRole.getClient():
			playerRole.getClient().CLIENT_OnLeaveTrainSoldierGround()

	def onTeleportCompleted( self, selfEntity, playerRole ):
		# 播放场景语音
		SpaceBase.onTeleportCompleted( self, selfEntity, playerRole )
		
		modelNumList = playerRole.getRoleBarracksSoldierModelNumbers()
		playerRole.setArmyModelList( modelNumList )
		if playerRole.getClient():
			playerRole.getClient().CLIENT_OnEnterTrainSoldierGround( self.armLength, self.cameraRotation )

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
		KBEngine.globalData["TrainSoldierGroundManager"].requestTrainSoldierGroundDatas( int(selfEntity.spaceKey), selfEntity.base )
		
	def onRequestTrainSoldierGroundDatasCB( self, selfEntity, trainSoldierGroundDatas ):
		"""
		请求该分线练兵场的数据回调后  加载刷新点数据了
		"""
		if self._spawnFile:
			trainSoldierGroundDict = {}
			for trainSoldierGroundData in trainSoldierGroundDatas:
				trainSoldierGroundDict[ trainSoldierGroundData.index ] = trainSoldierGroundData.getDictFromObj( trainSoldierGroundData )
			g_spawnPointFactory.initSpawnPointTrainSoldierGround( selfEntity, self._spawnFile, trainSoldierGroundDict )

