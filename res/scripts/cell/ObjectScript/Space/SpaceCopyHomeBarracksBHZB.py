# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import Const
import KBEngine
import csdefine
import KBEDebug
import csstatus
import Functions
import time

class SpaceCopyHomeBarracksBHZB( SpaceCopy ):
	"""
	帮会争霸大本营
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.delyCloseTime = 0
		self.firstRankRewardGifts = []
		self.secondRankRewardGifts = []
		self.thirdRankRewardGifts = []
		self.rankRewardMoneyStr = ""
		self.rankRewardContributionStr = ""
		self.xianFirstTongLeaderReward = ""
		self.moFirstTongLeaderReward = ""
		self.xianSecondTongLeaderReward = ""
		self.moSecondTongLeaderReward = ""

	def initData( self, configData ):
		SpaceCopy.initData( self, configData )
		self.delyCloseTime = configData["SpaceData"].get( "delyCloseTime",0 )
		self.firstRankRewardGifts = configData["SpaceData"].get("firstRankRewardGifts",[])
		self.secondRankRewardGifts = configData["SpaceData"].get("secondRankRewardGifts",[])
		self.thirdRankRewardGifts = configData["SpaceData"].get("thirdRankRewardGifts",[])
		self.rankRewardTongMoneys = configData["SpaceData"].get("rankRewardTongMoneys",[])
		self.rankRewardContributionGifts = configData["SpaceData"].get("rankRewardContributionGifts",[])
		self.xianFirstTongLeaderReward = configData["SpaceData"].get("xianFirstTongLeaderReward","")
		self.moFirstTongLeaderReward = configData["SpaceData"].get("moFirstTongLeaderReward","")
		self.xianSecondTongLeaderReward = configData["SpaceData"].get("xianSecondTongLeaderReward","")
		self.moSecondTongLeaderReward = configData["SpaceData"].get("moSecondTongLeaderReward","")

	def getFirstRankRewardGifts( self ):
		"""
		"""
		return self.firstRankRewardGifts

	def getSecondRankRewardGifts( self ):
		return self.secondRankRewardGifts

	def getThirdRankRewardGifts( self ):
		return self.thirdRankRewardGifts

	def getRankRewardTongMoneys( self ):
		return self.rankRewardTongMoneys

	def getRankRewardContributionGifts( self ):
		return self.rankRewardContributionGifts

	def getXianFirstTongLeaderReward( self ):
		return self.xianFirstTongLeaderReward

	def getMoFirstTongLeaderReward( self ):
		return self.moFirstTongLeaderReward

	def getXianSecondTongLeaderReward( self ):
		return self.xianSecondTongLeaderReward

	def getMoSecondTongLeaderReward( self ):
		return self.moSecondTongLeaderReward

	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		pass

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		selfEntity.addTongMemberData( playerRole,0 )
		selfEntity.setTemp( "login_" + str(playerRole.id), 1 )
		if playerRole.getClient():
			playerRole.client.InitBHZBNPCPointDatas( list(selfEntity.pointDataMgr.values()) )
			playerRole.client.UpdataHomeBarracksMapDataToAllMember( list(selfEntity.createArgs["distributHomeBarracks"].values()) )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		groupID = packArgs.get("groupID",-1)
		selfEntity.addTongMemberData( playerRole,groupID )
		if playerRole.getClient():
			playerRole.client.InitBHZBNPCPointDatas( list(selfEntity.pointDataMgr.values()) )
			playerRole.client.UpdataHomeBarracksMapDataToAllMember( list(selfEntity.createArgs["distributHomeBarracks"].values()) )
			for pointIndex, groupID in selfEntity.recordGroupIDAttackPointIndex.items():
				playerRole.client.ShowGroupIDAttackPointSign( pointIndex, groupID )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )

	def onTeleportCompleted( self, selfEntity, playerRole ):
		"""
		"""
		if selfEntity.queryTemp( "login_" + str(playerRole.id) ):
			selfEntity.addTimerCallBackForScript( 1.0,"onRoleLoginBHZB",(playerRole, ) )

	def onRoleLoginBHZB( self, selfEntity, playerRole ):
		if selfEntity.queryTemp( "login_" + str(playerRole.id) ):
			KBEDebug.ERROR_MSG("+++++++++++++++++onTeleportCompleted+++++++++++",playerRole.captainID)
			KBEngine.globalData["BHZBManager"].onRoleLoginBHZB( playerRole.getCamp(),playerRole.tongDBID, playerRole.playerDBID,playerRole.base, playerRole.captainID )	
			KBEngine.globalData["TongMgr"].checkIsLoginToBHZBPoint( playerRole.base, playerRole.tongDBID, self.scriptID, playerRole.playerDBID )
			selfEntity.removeTemp("login_"+ str(playerRole.id))

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + selfEntity.dynamicTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( (spaceLifeSecond + self.delyCloseTime), "closeSpace", () )
		selfEntity.addTimerCallBack( spaceLifeSecond, "showBHZBIntegralRankWnd", () )
		totalTime = spaceLifeSecond + self.delyCloseTime
		if self.getSpaceType() == csdefine.SPACE_TYPE_STORY_COPY:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( totalTime - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_PLANE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		else:
			selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( totalTime - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))
