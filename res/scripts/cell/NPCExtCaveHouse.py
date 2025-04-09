# -*- coding: utf-8 -*-

import KBEngine
import NPC
import CoreObject.NPCObject as NPCObject
from ConfigObject.BuildDepleteLoader import g_BuildDepleteLoader
import time
import Functions
import csdefine
import csconst
import Const
import KBEDebug
import Math
import math

class NPCExtCaveHouse( NPC.NPC ):
	"""
	洞府
	"""
	def __init__( self ):
		NPC.NPC.__init__( self )
		self.buildState = csdefine.LHMJ_BUILD_STATE_NONE
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].addOccupiedFoundationPos( int(self.getCurrentSpace().spaceKey), self.group, self.getForwardPos(), self, self.getScript().getDongFuType() )

	def getForwardPos( self ):
		"""获取洞府建筑的门口的pos"""
		yaw = self.getYaw()
		position = Math.Vector3( self.position )
		position.x += math.sin( yaw ) * Const.NPC_FORWARD_DISTANCE
		position.z += math.cos( yaw ) * Const.NPC_FORWARD_DISTANCE
		return position

	def updateDongFuState( self, state, level, belongDBID, LTDatas ):
		"""
		define method
		更新洞府建筑状态
		"""
		self.belongDBID = belongDBID
		self.buildState = state
		if self.buildState == csdefine.LHMJ_BUILD_STATE_OCUPPY:
			self.delOccupyBuildFlag()
		elif self.buildState == csdefine.LHMJ_BUILD_STATE_READY:
			self.delOccupyBuildFlag()
			self.updateDongFuLevel( level )
			self.LTDatas = LTDatas
	
	def updateDongFuLevel( self, level ):
		"""
		define method
		更新洞府等级
		"""
		self.setExtraModelNumber(self.getScript().getModelByLevel(level))
	
	def updateLTDatas( self, LTDatas ):
		"""
		define method
		更新灵田数据
		"""
		self.LTDatas = LTDatas

	def CELL_onClientReady( self, srcEntityID ):
		"""
		<Expose method>
		客户端Character Actor已经准备好
		"""
		player = KBEngine.entities.get(srcEntityID)
		if player is None:return
		if self.endBuildTime:
			player.clientEntity(self.id).OnShowBuildUI( self.endBuildTime )
		if self.buildState == csdefine.LHMJ_BUILD_STATE_READY:
			player.clientEntity(self.id).OnShowLingTian( self.LTDatas )
			if self.tipsDBID and player.playerDBID == self.tipsDBID:
				player.clientEntity(self.id).CLIENT_OnPlayParticles( self.id, Const.LHMJ_CAVE_TIPS_PARTICLE, "", -1.0, Math.Vector3(0,0,0))
		elif self.buildState == csdefine.LHMJ_BUILD_STATE_OCUPPY:
			if self.tipsDBID and player.playerDBID == self.tipsDBID:
				player.clientEntity(self.id).CLIENT_OnPlayParticles( self.id, self.getScript().effectList[0], "", -1.0, Math.Vector3(0,0,0))

	def startOccupyTime( self, playerCell ):
		"""
		开始占领
		"""
		self.buildState = csdefine.LHMJ_BUILD_STATE_OCUPPY
		self.belongDBID = playerCell.playerDBID
		self.tipsDBID = playerCell.playerDBID
		self.occupyProtectTime = csconst.LHMJ_BUILD_OCCUPY_TIME * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()
		playerCell.clientEntity( self.id ).CLIENT_OnPlayParticles( self.id, self.getScript().effectList[0], "", -1.0, Math.Vector3(0,0,0))

	def updateOccupyTime( self, occupyTime ):
		"""
		define method
		更新占领时间
		"""
		if int(time.time()) - occupyTime >= csconst.LHMJ_BUILD_OCCUPY_TIME:
			self.onProtectTimeOut()
		else:
			self.buildState = csdefine.LHMJ_BUILD_STATE_OCUPPY
			self.occupyProtectTime = occupyTime * csconst.TIME_ENLARGE_MULTIPLE

	def onProtectTimeOut( self ):
		"""
		define method
		占领保护时间已过
		"""
		self.addOccupyBuildFlag()
		self.buildState = csdefine.LHMJ_BUILD_STATE_NONE
		self.occupyProtectTime = 0
		self.tipsDBID = 0

	def onStartBuildDongFu( self ):
		"""
		开始建造洞府
		"""
		self.buildState = csdefine.LHMJ_BUILD_STATE_IS_BUILD
		self.tipsDBID = 0
		spaceKey = int(self.getCurrentSpace().spaceKey)
		self.allClients.CLIENT_OnPlayParticles( self.id, self.getScript().effectList[2], "", -1.0, Math.Vector3(0,0,0))
		self.addTimerCallBack( g_BuildDepleteLoader.getBuildUpgradeTime( csdefine.LHMJ_BUIILD_LING_QUAN, 1 ), "buildCaveHouseSuccess", () )
		self.endBuildTime = str( g_BuildDepleteLoader.getBuildUpgradeTime( csdefine.LHMJ_BUIILD_LING_QUAN, 1 ) * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime() )
		self.allClients.OnShowBuildUI( self.endBuildTime )

	def buildCaveHouseSuccess( self ):
		"""
		建造完成
		"""
		self.buildState = csdefine.LHMJ_BUILD_STATE_READY
		self.endBuildTime = ""
		self.updateDongFuLevel( 1 )
		spaceKey = int(self.getCurrentSpace().spaceKey)
		self.allClients.CLIENT_OnStopParticles()
		self.allClients.CLIENT_OnPlayParticles( self.id, self.getScript().effectList[3], "", -1.0, Math.Vector3(0,0,0))
		self.allClients.OnShowLingTian( self.LTDatas )
	
	def addOccupyBuildFlag( self ):
		"""
		添加不可见标志
		"""
		self.addFlag( csdefine.FLAG_UNVISIBLE )
		self.lightWallID = 0

	def delOccupyBuildFlag( self ):
		"""
		移除地基标志位
		"""
		self.removeFlag( csdefine.FLAG_UNVISIBLE )
		self.lightWallID = Const.LHMJ_HOUSE_PARTICLE

	def stopParticles( self ):
		"""
		define method
		停止提示光效
		"""
		self.allClients.CLIENT_OnStopParticles()
		self.allClients.CLIENT_OnPlayParticles( self.id, self.getScript().effectList[1], "", -1.0, Math.Vector3(0,0,0))
		self.addTimerCallBack( 0.5, "delOccupyBuildFlag", () )
		
	def updateChallengeDBID( self, playerDBID, playerID ):
		"""
		define method
		挑战玩家的DBID
		"""
		self.tipsDBID = playerDBID
		if playerID:
			playerCell = KBEngine.entities.get( playerID )
			if playerCell and playerCell.spaceID == self.spaceID and playerCell.position.distTo( self.position ) <= Const.DEFAULT_AOI_RADIUS:
				playerCell.clientEntity(self.id).CLIENT_OnPlayParticles( self.id, Const.LHMJ_CAVE_TIPS_PARTICLE, "", -1.0, Math.Vector3(0,0,0))
		
	def onActivityEnd( self ):
		"""
		define method
		活动结束
		"""
		self.tipsDBID = 0