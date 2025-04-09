# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine
import Functions
import KBEMath
import random
import ActivityBunchModule
import Define
import csdefine
import KST
import csstatus
import KBEDebug
import Const
import time
import csconst
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader

class SpaceCopyYeZhanFengQi5490( SpaceCopy ):
	"""
	血斗凤栖镇 JIRA CST-5490
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.delyCloseTime = 0.0
		self.initIntegral = 0
		self.revivePosList = []

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		self.delyCloseTime = configData["SpaceData"].get("delyCloseTime",0.0)
		self.initIntegral = configData["SpaceData"].get("initIntegral",0)
		revivePosInfos = configData["SpaceData"].get("revivePosList","").split("|")
		for revivePosInfo in revivePosInfos:
			pos = Functions.vector3TypeConvert(revivePosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( pos )
			self.revivePosList.append(pos)

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		selfEntity.addTimerCallBackForScript(float(self.spaceLife),"onSpaceLifeEnd",())


	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + self.delyCloseTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( spaceLifeSecond, "closeSpace", () )
		#selfEntity.addTimerCallBack( 180.0,"checkSpaceRoleNumber",() ) #3分钟之后检查一下副本人数
		selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))
		
	def onSpaceLifeEnd( self, selfEntity ):
		"""
		副本时间到达
		"""
		# for m in selfEntity._spaceRoles:
		# 	if m.id in selfEntity.memberDict: 
		# 		rank = selfEntity.getYeZhanFengQiMemberRankByKill( m )
		# 		selfEntity.showYeZhanFengQiMemberRank(m,rank,selfEntity.memberDict[m.id].kill)

		memberInfos = list(selfEntity.memberDict.values())
		kickOutMemberInfos = list(selfEntity.kickOutMember.values())
		memberInfos.extend( kickOutMemberInfos )
		memberInfos = sorted( memberInfos ,key = lambda m : m.integral, reverse = True )
		rank = 0
		for memberInfo in memberInfos:
			rank+=1
			g_mailContentDataLoader.sendActivityReward( self.scriptID,rank,memberInfo.roleName )
			
		if memberInfos:
			for m in selfEntity._spaceRoles:
				m.onYeZhanFengQiEnd()
				m.client.CLIENT_ShowFirstWindow( memberInfos[0].roleName )
			selfEntity.golbalYeZhanFengQiChampion(memberInfos[0])

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		selfEntity.addYeZhanFengQiMember( playerRole,self.initIntegral )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		if packArgs["leaveReason"] == Define.LEAVE_SPACE_REASON_TELEPORT:
			selfEntity.reduceYeZhanFengQiMember( playerRole )
			selfEntity.yeZhanFengQiKickOutMember( playerRole.playerDBID )
		else:
			selfEntity.yeZhanFengQiMemberLogOut( playerRole )
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		if selfEntity.isMemberKickOut( playerRole ):
			playerRole.gotoExitSpacePos()
			return
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		selfEntity.addYeZhanFengQiMember( playerRole,self.initIntegral )

	def getRevivePosList( self ):
		"""
		"""
		return self.revivePosList
