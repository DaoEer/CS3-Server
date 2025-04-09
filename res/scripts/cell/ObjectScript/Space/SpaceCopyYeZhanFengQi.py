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

class SpaceCopyYeZhanFengQi( SpaceCopy ):
	"""
	血斗凤栖镇
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.enterInfos = []
		self.activityBunch  = ""
		self.nextActivity = ""
		self.delyCloseTime = 0.0
		self.endAddBuffID = 0

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		#self.activityBunch = configData["SpaceData"].get("activityBunch","")
		#self.nextActivity = configData["SpaceData"].get("nextActivity","")
		self.initIntegral = configData["SpaceData"].get("initIntegral",0)
		self.delyCloseTime = configData["SpaceData"].get("delyCloseTime",0.0)
		self.endAddBuffID = configData["SpaceData"].get("endAddBuffID",0)
		enterPosInfos = configData["SpaceData"].get("enterPosList","").split("|")
		enterDirInfos = configData["SpaceData"].get("enterDirList","").split("|")
		enterPosList = []
		enterDirList = []
		for enterPosInfo in enterPosInfos:
			pos = Functions.vector3TypeConvert(enterPosInfo)
			pos = KBEMath.Unreal2KBEnginePosition( pos )
			enterPosList.append(pos)

		for enterDirInfo in enterDirInfos:
			dir = Functions.vector3TypeConvert(enterDirInfo)
			dir = KBEMath.Unreal2KBEnginePosition( dir )
			enterDirList.append(dir)
		for i in range(0,len(enterPosList)):
			self.enterInfos.append( (enterPosList[i], enterDirList[i]) )

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		selfEntity.addTimerCallBackForScript(self.spaceLife,"onSpaceLifeEnd",())

	def startSpaceLife( self, selfEntity ):
		"""
		开始计时
		"""
		spaceLifeSecond = self.spaceLife + self.delyCloseTime
		selfEntity.lifeTime = self.spaceLife		# 副本时长
		selfEntity.lifeStartTime = time.time()		# 副本计时开始时间
		selfEntity.lifeTimer = selfEntity.addTimerCallBack( spaceLifeSecond, "closeSpace", () )
		selfEntity.lifeNotifyTimer = selfEntity.addTimerCallBackForScript( spaceLifeSecond - Const.SPACE_LIFE_NOTIFY_TIME, "showTimeCountDown", ( csstatus.SPACE_CLOSE_NOTIFY, Const.SPACE_LIFE_NOTIFY_TIME ) )
		for e in selfEntity._spaceRoles:
			e.client.ShowSpaceLife( str(spaceLifeSecond * csconst.TIME_ENLARGE_MULTIPLE + Functions.getTime()), self.isSpaceLifeMoveDown,str( Functions.getTime() ))
		
	def onSpaceLifeEnd( self, selfEntity ):
		"""
		副本时间到达
		"""
		firstName = ""
		member = selfEntity.memberDatas.getFirstMember()
		if member:
			firstName = member.roleName
		for m in selfEntity._spaceRoles:
			m.onYeZhanFengQiEnd()
			m.client.CLIENT_ShowFirstWindow( firstName )
			if self.endAddBuffID:
				m.addBuff(m,self.endAddBuffID)

		KBEngine.globalData["ActivityBunchManager"].sendWoldMsg( csstatus.ZHIZUNZHENBA_THE_FIRST,firstName)
		# nextJoinNumber = ActivityBunchModule.getNextJoinMembers( self.activityBunch, self.nextActivity )
		# memberList = selfEntity.memberDatas.getMembersByJoinNumber(nextJoinNumber)
		# for member in memberList:
		# 	if member.roleMB:
		# 		member.roleMB.actBunch_joinNext( self.activityBunch, self.nextActivity, {"score":member.integral} )

	def onEnter( self, selfEntity, playerRole, packArgs ):
		SpaceCopy.onEnter( self, selfEntity, playerRole, packArgs )
		selfEntity.addYeZhanFengQiMemberData( playerRole, self.initIntegral )

	def onLeave( self, selfEntity, playerRole, packArgs ):
		if packArgs["leaveReason"] == Define.LEAVE_SPACE_REASON_TELEPORT:
			selfEntity.removeYeZhanFengQiMemberData( playerRole )
		playerRole.hideStatusMessage( csstatus.YE_ZHAN_FENG_QI_MEMBER_OUT )
		playerRole.hideStatusMessage( csstatus.YE_ZHAN_FENG_QI_END_MESSAGE )
		SpaceCopy.onLeave( self, selfEntity, playerRole, packArgs )

	def onLogin( self, selfEntity, playerRole ):
		"""
		"""
		SpaceCopy.onLogin( self, selfEntity, playerRole )
		selfEntity.addYeZhanFengQiMemberData( playerRole, self.initIntegral )

	def getEnterInfo( self ):
		"""
		获得进入信息
		"""
		return random.choice(self.enterInfos)
			
	def setReviverInfo( self, reviverInfo ):
		"""
		设置复活
		"""
		self.enterInfos = []
		self.enterInfos.extend( reviverInfo )