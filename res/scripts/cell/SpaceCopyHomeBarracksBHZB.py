# -*- coding: utf-8 -*-

from SpaceCopy import SpaceCopy
import Const
import KBEDebug
import csdefine
import KBEngine
from CoreInterface.SpaceBHZBWarDetailInterface import SpaceBHZBWarDetailInterface

class SpaceCopyHomeBarracksBHZB( SpaceCopy, SpaceBHZBWarDetailInterface ):
	"""
	帮会争霸大本营
	"""
	def __init__( self ):
		self.pointDataMgr = self.createArgs["pointDatas"]
		SpaceCopy.__init__( self )
		SpaceBHZBWarDetailInterface.__init__( self )
		self.recordGroupIDAttackPointIndex = {} # 记录某一队进攻某个据点
		self.addBHZBWarDetailData( int(self.spaceKey) )

	def addTongMemberData( self, role, groupID ):
		"""
		增加帮会成员
		"""
		self.spaceMemberMgr.addTongMemberData( role.tongDBID, role.playerDBID, role, groupID )

	def getMemberGroupIDByPlayerDBID( self, role ):
		"""
		获得玩家所在的组
		"""
		return self.spaceMemberMgr.getMemberGroupIDByPlayerDBID( role.tongDBID, role.playerDBID )

	def getMemberByPlayerDBID( self, role ):
		"""
		获得玩家通过playerDBID
		""" 
		return self.spaceMemberMgr.getMemberByPlayerDBID( role.tongDBID, role.playerDBID )

	def callTeamToProtect( self, tongDBID,groupTeamID, pointIndex,pointName ):
		"""
		召唤某一队去防守
		"""
		self.spaceMemberMgr.callTeamToProtect(tongDBID, groupTeamID, pointIndex,pointName )

	def callTeamToAttack( self, tongDBID, groupTeamID, pointIndex,pointName ):
		"""
		召唤某一队进攻
		"""
		self.spaceMemberMgr.callTeamToAttack( tongDBID, groupTeamID, pointIndex,pointName )

	def isTeamToProtect( self, tongDBID, groupTeamID, pointIndex ):
		"""
		某一队是否防守
		"""
		return self.spaceMemberMgr.isTeamToProtect( tongDBID, groupTeamID, pointIndex )

	def isTeamToAttack( self, tongDBID, groupTeamID, pointIndex ):
		"""
		某一队是否防守
		"""
		return self.spaceMemberMgr.isTeamToAttack( tongDBID, groupTeamID, pointIndex )

	def changeMemberGroup( self, tongDBID,groupDict ):
		"""
		改变玩家所在的组
		"""
		self.spaceMemberMgr.changeMemberGroup( tongDBID, groupDict )

	def initNPCPointDatas( self, npcPointDatas ):
		"""
		初始化沙盘大地图的据点数据
		"""
		for npcPointData in npcPointDatas:
			self.pointDataMgr[npcPointData.index] = npcPointData

		members = self.spaceMemberMgr.getTongAllMemberByTongDBID( int(self.spaceKey) )
		for member in members:
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.InitBHZBNPCPointDatas( list(self.pointDataMgr.values()) )

	def updataNPCPointRestEndTime( self, pointIndex, restEndTime ):
		"""
		更新据点重置时间
		"""
		self.pointDataMgr.updataNPCPointRestEndTime( pointIndex, restEndTime )
		allMembers = self.spaceMemberMgr.getAllMembers()
		for member in allMembers:
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataNPCPointRestEndTime( pointIndex, restEndTime )

	def updataNPCPointReadyEndTime( self, pointIndex, readyEndTime ):
		"""
		更新据点准备时间
		"""
		self.pointDataMgr.updataNPCPointReadyEndTime( pointIndex, readyEndTime )
		allMembers = self.spaceMemberMgr.getAllMembers()
		for member in allMembers:
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataNPCPointReadyEndTime( pointIndex, readyEndTime )

	def updataNPCPointDeclareWarState( self, pointIndex, declareWarState ):
		"""
		更新据点状态
		"""
		lastPointState = self.pointDataMgr.getLastPointDeclareWarState(pointIndex)
		if (lastPointState == csdefine.NPCEXTPOINT_STATE_FIGHT and declareWarState == csdefine.NPCEXTPOINT_STATE_REST) or lastPointState == csdefine.NPCEXTPOINT_STATE_CAN_NOT_BE_DECLARE and declareWarState == csdefine.NPCEXTPOINT_STATE_CAN_BE_DECLARE:
			self.removeRecordGroupIDAttackPointIndex( pointIndex )
		self.pointDataMgr.updataNPCPointDeclareWarState( pointIndex, declareWarState )
		allMembers = self.spaceMemberMgr.getAllMembers()
		for member in allMembers:
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataNPCPointDeclareWarState( pointIndex, declareWarState )

	def updateNPCPointAttackGroupTeamID( self, pointIndex, attackGroupTeamID, declareTongDBID ):
		"""
		更新据点进攻队伍数据
		"""
		self.pointDataMgr.updateNPCPointAttackGroupTeamID( pointIndex, attackGroupTeamID, declareTongDBID )
		allMembers = self.spaceMemberMgr.getAllMembers()
		for member in allMembers:
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdateNPCPointAttackGroupTeamID( pointIndex, attackGroupTeamID,declareTongDBID )

	def updataNPCPointOccupyData( self, pointIndex,playerDBID,playerName,tongDBID,tongName ):
		"""
		更新据点占领帮会
		"""
		self.pointDataMgr.updataNPCPointOccupyData( pointIndex,playerDBID,playerName,tongDBID,tongName )
		allMembers = self.spaceMemberMgr.getAllMembers()
		for member in allMembers:
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataNPCPointOccupyData( pointIndex, tongDBID,playerDBID,playerName, tongName)

	def updataBHZBPointJoinAttackMembers( self, pointIndex, joinAttackMembers ):
		"""
		更新据点攻占成员
		"""
		self.pointDataMgr.updataBHZBPointJoinAttackMembers( pointIndex, joinAttackMembers )
		allMembers = self.spaceMemberMgr.getAllMembers()
		playerDBIDStrs = [ str(i) for i in joinAttackMembers ]
		for member in allMembers:
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataBHZBPointJoinAttackMembers( pointIndex, playerDBIDStrs )

	def updataBHZBPointJoinProtectMembers( self, pointIndex, joinProtectMembers ):
		"""
		更新据点防守成员
		"""
		self.pointDataMgr.updataBHZBPointJoinProtectMembers( pointIndex, joinProtectMembers )
		allMembers = self.spaceMemberMgr.getAllMembers()
		playerDBIDStrs = [ str(i) for i in joinProtectMembers ]
		for member in allMembers:
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataBHZBPointJoinProtectMembers( pointIndex, playerDBIDStrs )

	def updataBHZBPointJoinProtectTeamID( self, pointIndex, joinProtectTeamID ):
		"""
		更新参与防守的队伍编号
		"""
		self.pointDataMgr.updataBHZBPointJoinProtectTeamID( pointIndex, joinProtectTeamID )
		allMembers = self.spaceMemberMgr.getAllMembers()
		for member in allMembers:
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataBHZBPointJoinProtectTeamID( pointIndex, joinProtectTeamID )

	def updataHomeBarracksDataToAllMember( self, homeBarrackDatas ):
		"""
		更新大本营地图数据到客户端
		"""
		self.mapHomeBarrrackDatas = homeBarrackDatas
		allMembers = self.spaceMemberMgr.getAllMembers()
		for member in allMembers:
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataHomeBarracksMapDataToAllMember( homeBarrackDatas )

	def updataMemberPositionToClient( self, tongDBID,memberPosDatas ):
		"""
		更新成员坐标信息到客户端
		"""
		for member in self.spaceMemberMgr.getTongAllMemberByTongDBID( tongDBID ):
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.UpdataMemberPositionToClient( memberPosDatas )

	def onEnterBHZBPointWar( self, tongDBID,spaceSciptID, pointDict, playerDBIDs ):
		"""
		进入据点争夺战
		"""
		for playerDBID in playerDBIDs:
			member = self.spaceMemberMgr.getMemberByPlayerDBID( tongDBID,playerDBID )
			if not member:
				continue

			if member.roleMB:
				declareTongDBID = pointDict.get("declareTongDBID")
				if int(self.spaceKey) == declareTongDBID:
					pointDict.update( {"attackWarDetailData":self.warDetailMgr[int(self.spaceKey)]} )
				else:
					pointDict.update( {"protectWarDetailData":self.warDetailMgr[int(self.spaceKey)]} )
				# if playerDBIDs.index(member.roleDBID) == 0:
				# 	member.roleMB.setIsDeclarePointBHZB(False)
				# 	self.addRecordGroupIDAttackPointIndex( member.getGroupID(), pointDict["pointIndex"] )
				member.roleMB.onEnterBHZBPointWar( spaceSciptID, pointDict )

	def defenseBHZBPoint( self, tongDBID,spaceSciptID, pointDict, playerDBIDs ):
		"""
		进入布防
		"""
		self.onEnterBHZBPointWar( tongDBID,spaceSciptID, pointDict, playerDBIDs )

	def addRecordGroupIDAttackPointIndex( self, groupID, pointIndex ):
		"""
		增加记录某一队进攻某个据点
		"""
		self.recordGroupIDAttackPointIndex[pointIndex] = groupID
		for member in self.spaceMemberMgr.getTongAllMemberByTongDBID( int(self.spaceKey) ):
			if member.roleMB and member.roleMB.getClient():
				member.roleMB.client.ShowGroupIDAttackPointSign( pointIndex, groupID )

	def removeRecordGroupIDAttackPointIndex( self, pointIndex ):
		"""
		移除记录某一队进攻某个据点
		"""
		if pointIndex in self.recordGroupIDAttackPointIndex:
			del self.recordGroupIDAttackPointIndex[pointIndex]
			for member in self.spaceMemberMgr.getTongAllMemberByTongDBID( int(self.spaceKey) ):
				if member.roleMB and member.roleMB.getClient():
					member.roleMB.client.HideGroupIDAttackPointSign( pointIndex )

	def statusMsgToMember( self, msgID, msgArgs ):
		"""
		广播消息
		"""
		for role in self._spaceRoles:
			if role.getClient():
				role.client.statusMessage( msgID, msgArgs )

	def showBHZBIntegralRankWnd( self ):
		"""
		显示帮会争霸积分排行榜
		"""
		for role in self._spaceRoles:
			KBEngine.globalData["BHZBManager"].showBHZBIntegralRankWin( role.getCamp(), role.base, self.getScript().delyCloseTime )

		firstRankRewardGifts = self.getScript().getFirstRankRewardGifts()
		secondRankRewardGifts = self.getScript().getSecondRankRewardGifts()
		thirdRankRewardGifts = self.getScript().getThirdRankRewardGifts()
		rankRewardTongMoneys = self.getScript().getRankRewardTongMoneys()
		rankRewardContributionGifts =self.getScript().getRankRewardContributionGifts()
		memberDBIDs = self.spaceMemberMgr.getTongAllMemberDBIDsByTongDBID( int(self.spaceKey) )
		if self.createArgs["camp"] == csdefine.CAMP_TAOSIM:
			firstTongLeaderReward = self.getScript().getXianFirstTongLeaderReward()
			secondTongLeaderReward = self.getScript().getXianSecondTongLeaderReward()
		else:
			firstTongLeaderReward = self.getScript().getMoFirstTongLeaderReward()
			secondTongLeaderReward = self.getScript().getMoSecondTongLeaderReward()
		KBEngine.globalData["BHZBManager"].sendBHZBRewardToMembers( self.createArgs["camp"],int(self.spaceKey),memberDBIDs, firstRankRewardGifts,secondRankRewardGifts,thirdRankRewardGifts,rankRewardTongMoneys,rankRewardContributionGifts,firstTongLeaderReward,secondTongLeaderReward)

	def onEnter( self, playerRole, packArgs ):
		SpaceCopy.onEnter( self, playerRole, packArgs )
		self.addTimerCallBack( 1.0,"onRestartJoinTeam",(playerRole,) )

	def onRestartJoinTeam( self, playerRole ):
		"""
		重新加入队伍
		"""
		if playerRole.isInTeam():
			return
		KBEngine.globalData["BHZBManager"].onRoleLoginBHZB( playerRole.getCamp(),playerRole.tongDBID, playerRole.playerDBID,playerRole.base, playerRole.captainID )	

	def onTeleportCompleted( self, playerRole ):
		SpaceCopy.onTeleportCompleted( self, playerRole )
		SpaceBHZBWarDetailInterface.onTeleportCompleted( self, playerRole )
