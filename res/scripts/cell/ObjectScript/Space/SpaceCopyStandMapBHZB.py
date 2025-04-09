# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyHomeBarracksBHZB import SpaceCopyHomeBarracksBHZB
import Const
import KBEngine
import csdefine
import KBEDebug
from ObjectScript.SpawnPoint.SpawnPointFactory import g_spawnPointFactory

class SpaceCopyStandMapBHZB( SpaceCopyHomeBarracksBHZB ):
	"""
	帮会争霸沙盘大地图
	"""
	def __init__( self ):
		SpaceCopyHomeBarracksBHZB.__init__( self )

	def initData( self, configData ):
		SpaceCopyHomeBarracksBHZB.initData( self, configData )

	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		pass

	def createSpawnPoint( self, selfEntity ):
		"""加载刷新点"""
		KBEngine.globalData["BHZBManager"].requestBHZBPointDatas( selfEntity.createArgs["camp"] , selfEntity.base )

	def onRequestBHZBPointDatasCB( self, selfEntity, pointDatas ):
		"""
		加载刷新点数据了
		"""
		if self._spawnFile:
			pointDataDict = {}
			for pointData in pointDatas:
				pointDataDict[pointData.index] = pointData.getDictFromObj( pointData )

			g_spawnPointFactory.initSpawnPointNPCPoint( selfEntity, self._spawnFile,pointDataDict )

	def onSpaceSpawnPointLoadOver( self, selfEntity ):
		"""刷新点加载完成回调"""
		SpaceCopyHomeBarracksBHZB.onSpaceSpawnPointLoadOver( self, selfEntity )
		KBEngine.globalData["BHZBManager"].initNPCPointDataToHomeBarracks( selfEntity.createArgs["camp"], selfEntity.spaceKey,selfEntity.getAllNPCPointData() )
		selfEntity.distributHomeBarracks()

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopyHomeBarracksBHZB.onLogin( self, selfEntity, playerRole )

	def onTeleportCompleted( self, selfEntity, playerRole ):
		SpaceCopyHomeBarracksBHZB.onTeleportCompleted( self, selfEntity, playerRole )
		modelNumList = playerRole.getRoleBarracksSoldierModelNumbers()
		playerRole.setArmyModelList( modelNumList )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		"""
		SpaceCopyHomeBarracksBHZB.onLeave( self, selfEntity, playerRole, packArgs )
		playerRole.resetArmyModelList()
