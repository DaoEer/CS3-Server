# -*- coding: utf-8 -*-
#KBEngine
import KBEngine

#common
import csdefine
import KBEDebug
import csconst
import csstatus
import TongLoader
from Functions import Functor

import time
import math

#base
import KST
import Const

class RoleTongInterface( object ):
	def __init__( self ):
		object.__init__( self )
		self.tongMB = None
		self.tongName = ""
		self.tongTitle = 0
		self.tongGrade = 0
		self.tongDBID = self.cellData[ "tongDBID" ]
		self.onLineTimer = None
		
	def hasTong(self):
		return self.tongMB != None

	def onGetCell( self ):
		if self.tongDBID > 0:
			self.tongReqInit()
		else:
			if hasattr(self, "client") and self.client:
				if self.joinTongList:
					joinList = [ str(i) for i in self.joinTongList ]
					self.client.OnInitTongApplyList( joinList  )
				self.client.OnTongInitNotity()
			
	def onLoseCell( self ):
		if self.tongMB:
			self.tongMB.onMemberOffline( self.databaseID, self.cellData["level"], self.cellData["spaceScriptID"] )
	
	def tongGetMgr( self ):
		return KBEngine.globalData[ "TongMgr" ]
	
	def canCreateTong( self ):
		"""是否能创建帮会"""
		if time.time() - self.lastQuitTongTime < Const.TONG_REJOIN_CD_TIME:
			remainTime = int(Const.TONG_REJOIN_CD_TIME - (time.time() - self.lastQuitTongTime))
			self.sendReJoinTongFailMsgForbidByCDTime(remainTime,csstatus.TONG_REJOIN_FORBID_CD_TIME)
			return False
		return True
	
	def createTong( self, tongName ):
		"""
		创建帮会
		"""
		self.tongGetMgr().createTong( self, self.databaseID, self.getName(), self.profession, self.level, self.getCamp(), self.getTitles(), tongName)
	
	def tongReqInit( self ):
		""" 
		向帮会管理器请求初始化自己的帮会信息
		"""
		self.tongGetMgr().reqInit( self, self.databaseID, self.tongDBID )
	
	def tongOnInit( self, tongMB, tongName, leaderDBID, tongTitle, tongGrade ):
		"""
		define method
		请求初始化信息回调
		"""
		self.tongMB = tongMB
		self.tongName = tongName
		self.tongLeaderDBID = leaderDBID
		self.tongTitle = tongTitle
		self.tongGrade = tongGrade
		localTime = time.localtime()
		offLineTime = time.localtime( self.offlineTime )
		if localTime[0] != offLineTime[0] or localTime[1] != offLineTime[1] or localTime[2] != offLineTime[2]:
			self.onLineTime = 0
		
		if self.onLineTime < Const.TONG_ON_LINE_MAX_TIME_REWARD:
			self.onLineTimer = self.addTimerRepeat( 3600, "onAccumulateOnlineTime", () )
		
	def tongOnInitErr( self ):
		"""
		define method
		初始化信息失败，有可能帮会解散了
		"""
		self.cell.tongOnInitErr()
		self.tongDBID = 0
		self.tongMB = None
		
		if hasattr(self, "client") and self.client:
			self.client.OnTongInitNotity()
		
	def onDawnArrive( self ):
		"""
		define method
		0点到达
		"""
		self.onLineTime = 0
		if not self.onLineTimer:
			self.onLineTimer = self.addTimerRepeat( 3600, "onAccumulateOnlineTime", () )
		
	def onAccumulateOnlineTime( self ):
		"""累计在线时间（1小时）"""
		if not self.tongMB:
			self.popTimer( self.onLineTimer )
			self.onLineTimer = None
			return
		self.onLineTime += 1
		self.tongMB.onAccumulateOnlineTime( self.databaseID )
		if self.onLineTime >= Const.TONG_ON_LINE_MAX_TIME_REWARD:
			self.popTimer( self.onLineTimer )
			self.onLineTimer = None
	
	def tongHasGrade( self, grade ):
		"""是否有某个权限"""
		newGrage = 1 << grade
		return self.tongGrade & newGrage
		
	#-----------------------请求帮会数据---------------------------------------------------
	def RequireTongInfo( self ):
		"""
		exposed method
		帮会申请列表
		"""
		if not self.validateClientCall():
			return
		self.tongGetMgr().requireTongInfo( self, self.camp )
	
	#-----------------------帮会属性---------------------------------------------------------------------------\
	def setTitleName( self, titleID, titleName ):
		"""
		exposed method
		设置帮会成员职位名称
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_RENAME ):
			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
			self.client.OnSetTitleNameFailed()
			return
		self.tongMB.setTitleName( self, titleID, titleName )
		
	def setTitle( self, targetEntityDBID, titleID ):
		"""
		exposed method
		设置帮会成员职位
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_APPOINT ):
			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
			return
		if self.tongTitle >= titleID:
			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
			return
		self.tongMB.setTitle( self.databaseID, int(targetEntityDBID), titleID )
	
	def onSetTitle( self, titleID, grades ):
		"""
		define method
		设置玩家的帮会成员职位
		"""
		self.tongTitle = titleID
		self.tongGrade = grades
		
	def setGrade( self, titleID, grades ):
		"""
		exposed method
		设置帮会成员的权限
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_REQUEST ):
			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
			self.client.OnSetGradeFailed()
			return
		self.tongMB.setGrade( titleID, grades )
		
	def onSetGrade( self, grades ):
		"""
		define method
		设置玩家的帮会成员的权限
		"""
		self.tongGrade = grades
		
	def isTongLeader( self ):
		"""是否是帮主"""
		if self.tongMB:
			return self.tongLeaderDBID == self.databaseID
		return False
		
	def onLeaderChange( self, leaderDBID ):
		"""
		define method
		帮主改变
		"""
		if not self.validateClientCall():
			return
		self.tongLeaderDBID = leaderDBID
		
	def setAffiche( self, affiche ):
		"""
		exposed method
		设置帮会公告
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_NOTICE ):
			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
			return
		self.tongMB.setAffiche( affiche )
		
	def setRecruitAffiche( self, affiche ):
		"""
		exposed method
		设置帮会招募公告
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_NOTICE ):
			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
			return
		self.tongMB.setRecruitAffiche( affiche )
		
	def upGrowTong( self ):
		"""
		exposed method
		帮会升级
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_UPGRADE ):
			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
			return
		if self.tongMB:
			self.tongMB.tongUpGrade( self, self.databaseID )
			
	def deMiseLeader( self, dstPlayerDBID ):
		"""
		exposed method
		禅让帮主职位
		"""
		if not self.validateClientCall():
			return
		dstPlayerDBID = int( dstPlayerDBID )
		if self.tongMB:
			self.tongMB.deMiseLeader( self.databaseID, dstPlayerDBID )
			
	def setMemberGag( self, playerDBID, isGag ):
		"""
		exposed method
		设置禁言
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_SHUTUP ):
			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
			return
		if self.tongMB:
			self.tongMB.setMemberGag( int(playerDBID), isGag )
			
	def tongSign( self ):
		"""
		exposed method
		帮会签到
		"""
		if not self.validateClientCall():
			return
		if self.tongMB:
			self.tongMB.tongSign( self.databaseID )
			
	#-----------------------帮会创建---------------------------------------------------------------------------
	def onCreateTong( self, tongDBID ):
		"""
		define method
		帮会创建完成
		"""
		if tongDBID > 0: #大于0,表示创建成功
			self.tongDBID = tongDBID
#			self.writeToDB()
#			self.tongReqInit()
		else:
			pass
	#-----------------------帮会申请加入---------------------------------------------------------------------------
	def tongReqJoin( self, tongDBID ):
		"""
		exposed method
		请求加入指定帮会
		"""
		if not self.validateClientCall():
			return
		tongDBID = int( tongDBID )
		if self.tongDBID:
			self.statusMessage( csstatus.TONG_CANOT_JOIN_HAS_TONG )
			return
		if len( self.joinTongList ) >= Const.TONG_REQ_JOIN_LIST_MAX:
			self.statusMessage( csstatus.TONG_CANOT_JOIN_MAX_NUM )
			return
		if time.time() - self.lastQuitTongTime < Const.TONG_REJOIN_CD_TIME:
			remainTime = int(Const.TONG_REJOIN_CD_TIME - (time.time() - self.lastQuitTongTime))
			self.sendReJoinTongFailMsgForbidByCDTime(remainTime,csstatus.TONG_REJOIN_FORBID_CD_TIME)
			if hasattr(self, "client") and self.client:
				self.client.OnApplyJoinTongFailed( str(tongDBID) )
			return
		self.joinTongList.append( tongDBID )
		self.tongGetMgr().reqJoin( tongDBID, self, self.databaseID, self.playerName, self.level, self.profession, self.camp )
		
	def OnApplyJoinTongFailed( self, tongDBID ):
		"""
		define method
		申请失败
		"""
		if tongDBID in self.joinTongList:
			self.joinTongList.remove(tongDBID)
		self.client.OnApplyJoinTongFailed(str(tongDBID))
	
	def tongCancelJoin( self, tongDBID ):
		"""
		exposed method
		取消 加入指定帮会
		"""
		if not self.validateClientCall():
			return
		tongDBID = int( tongDBID )
		if tongDBID in self.joinTongList:
			self.joinTongList.remove( tongDBID )
			self.tongGetMgr().cancelJoin( tongDBID , self.databaseID )
	
#	def requestJoinList( self ):
#		"""
#		exposed method
#		请求 帮会申请加入列表
#		"""
#		if not self.validateClientCall():
#			return
#		if self.tongMB and self.tongHasGrade( csdefine.TONG_GRADE_REQUEST ):
#			self.tongMB.requestJoinList( self.databaseID )
	
	def replyJoinTong( self, playerDBID, canJoin ):
		"""
		exposed method
		回复加入帮会的请求
		"""
		if not self.validateClientCall():
			return
		playerDBID = int(playerDBID)
		if self.tongHasGrade( csdefine.TONG_GRADE_REQUEST ):
			KBEngine.lookUpEntityByDBID( "Role", playerDBID, Functor( self._replyMailBox, playerDBID, canJoin ) )
		else:
			self.statusMessage( csstatus.TONG_CANOT_INVITE_NOT_ENOUGH_GRADE )
		
	def refuseJoinTong( self, tongDBID, tongName ):
		"""
		define method
		拒绝 加入申请帮会
		"""
		if not self.tongMB:
			if tongDBID in self.joinTongList:
				self.joinTongList.remove( tongDBID )
				
				if hasattr(self, "client") and self.client:
					self.client.OnRefuseJoinTong( str(tongDBID), tongName )
		
	def _replyMailBox( self, playerDBID, canJoin, playerMB ):
		if self.isDestroyed:
			return
		
		if playerMB is True or playerMB is False:
			playerMB = None
		self.tongMB.replyJoinTong( self, playerMB, playerDBID, canJoin )
			
	def replyAllJoinTong( self, canJoin ):
		"""
		exposed method
		回复所有加入帮会请求
		"""
		if not self.validateClientCall():
			return
		self.tongMB.replyAllJoinTong( self, canJoin )
	
	def tongOnJoin( self, tongMB, tongDBID, tongName, tongTitle, tongGrade ):
		"""
		define method
		成功入会的回调
		"""
		self.tongDBID = tongDBID
		self.tongMB = tongMB
		self.tongName = tongName
		self.tongTitle = tongTitle
		self.tongGrade = tongGrade
		self.joinTongList = []
		
		#通知cell信息初始化完成
		if hasattr(self, "cell") and self.cell:
			self.cell.tongOnJoin( tongMB, tongDBID, tongName, tongTitle, tongGrade ) 
		#这里主要是在删除角色时，可能需要通知帮会进行一些处理（如角色时帮主需要重设帮主）
		if self.accountEntity: self.accountEntity.tongOnJoin(self.databaseID, self.tongDBID)
		
	#-----------------------帮会邀请加入---------------------------------------------------------------------------
	def remoteTongInviteJoin( self, beInbiterName ):
		"""
		exposed method
		远程邀请加入帮会
		"""
		if not self.validateClientCall():
			return
			
		if self.tongMB is None:
			self.statusMessage(csstatus.TONG_SPACE_COPY_NOT_IN_TONG)
			return
			
		if self.tongHasGrade( csdefine.TONG_GRADE_INVITE ):
			KST.g_baseAppEntity.lookupRoleBaseByName( beInbiterName, Functor( self._tongInviteMB ) )
		else:
			self.statusMessage( csstatus.TONG_CANOT_INVITE_NOT_ENOUGH_GRADE )
			
	def _tongInviteMB( self, beInviter ):
		if self.tongMB is None:
			return
		
		self.tongMB.inviteJoinTong(self.getName(), self.getCamp(), self, beInviter)
		
		"""
		if beInviter:
			beInviter.tongBeInviteJoin( self.getName(), self.tongName, self.getCamp() ,str(self.tongDBID),self, self.tongMB )
		else:
			KBEDebug.ERROR_MSG( "Player(name:%s) invite player(id:%d) err! can not get beInviter!"%( self.getName(), beInviteID ))
		"""
	
	def tongBeInviteJoin( self, inviterName, tongName, camp, tongDBID, inviteMB, tongMB ):
		"""
		define method
		被邀请加入帮会
		"""
		if self.getLevel() < csconst.TONG_JOIN_MIX_LEVEL:
			inviteMB.statusMessage( csstatus.TONG_CANOT_JOIN_NOT_ENOUGH_LEVEL, "" )
			return
		if self.tongMB:
			inviteMB.statusMessage( csstatus.TONG_CANOT_INVITE_HAS_TONG, "" )
			return
		if time.time() - self.lastQuitTongTime < Const.TONG_REJOIN_CD_TIME:
			remainTime = int(Const.TONG_REJOIN_CD_TIME - (time.time() - self.lastQuitTongTime))
			inviteMB.sendReJoinTongFailMsgForbidByCDTime(remainTime,csstatus.TONG_INVITE_FORBID_CD_TIME)
			return
		if self.getCamp() != camp:
			inviteMB.statusMessage( csstatus.TONG_CANOT_INVITE_CAMP, "" )
			return
		if self.hadBlacklist(inviterName):
			if hasattr(inviteMB, 'client') and inviteMB.client:
				inviteMB.client.statusMessage(csstatus.RELATION_MSG_FORBID_INVITE_JOIN_TONG_BLACK_LIST, self.getName())
			return
		
		#self.inquireMessage( csstatus.TONG_INVITE_TO_TONG, [ inviterName, tongName ], "replyInviteTong", inviteMB, tongMB )
		self.client.ReceiveInviteJoinTong( inviterName, inviteMB.id, tongName, tongDBID )

	def replyInviteTong(self, reply, inviteID , tongDBID):
		"""
		exposed method
		"""
		if not self.validateClientCall():
			return
		inviteMB = KBEngine.entities.get( inviteID )
		if not reply:
			if inviteMB:
				inviteMB.statusMessage( csstatus.TONG_CANOT_INVITE_REFUSE, self.getName() )
			return
		else:
			if self.tongMB:
				self.statusMessage(csstatus.TONG_HAS_JOING)
				return
			
			self.tongGetMgr().onInviteTong( int(tongDBID), inviteMB, self, self.databaseID, self.getName(), self.level, self.profession, self.getTitles())


	def sendReJoinTongFailMsgForbidByCDTime( self, remainTime, msgID ):
		"""
		发送重新加入帮会失败的消息
		"""
		def getTimeStr( value ):
			if value > 0 and value < 10:
				valueStr = "0%i"%value
			elif value >= 10:
				valueStr = str(value)
			else:
				valueStr = "00"
			return valueStr
		hour = remainTime//3600
		minutes = math.ceil((remainTime - hour * 3600)/60)
		if minutes >= 60:
			hour +=1
			minutes -= 60
		hourStr = getTimeStr( hour )
		minutesStr = getTimeStr(minutes)
		timeStr = "%s:%s"%(hourStr,minutesStr)
		self.statusMessage(msgID,timeStr)
		
	#-----------------------帮会踢出/被踢出---------------------------------------------------
	def tongKickMember( self, memberDBID ):
		"""
		exposed method
		踢人
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_KICK ):
			self.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE )
			return
		if self.tongMB:
			self.tongMB.kickMember( self.databaseID, int(memberDBID) )
	
	def tongBeKickOffLine( self, time ):
		"""
		define method
		玩家不在线时被踢下线了
		"""
		self.tongBeKick()
		self.lastQuitTongTime = time * 1.0
	
	def tongBeKick( self ):
		"""
		define method
		被踢出帮会
		"""
		self.onLeaveTong()
	
	def onLeaveTong( self ):
		"""离开帮会"""
		self.tongMB = None
		self.tongName = ""
		self.tongTitle = 0
		self.tongGrade = 0
		self.tongDBID = 0
		self.joinTongList = []
		self.lastQuitTongTime = time.time() # 记录退帮的时间
		
		if hasattr(self, "cell") and self.cell:
			self.cell.onLeaveTong()
		if hasattr(self, "client") and self.client:
			self.client.OnLeaveTong()


	#-----------------------帮会退出------------------------------------------------------
	def tongQuit( self ):
		"""
		exposed method
		退出帮会
		"""
		if not self.validateClientCall():
			return
		if self.tongMB:
			self.tongMB.tongQuit( self.databaseID )
	
	def tongOnQuit( self ):
		"""
		define method
		退出帮会
		"""
		self.onLeaveTong()

	#-----------------------帮会解散---------------------------------------------------
	def tongDismiss( self ):
		"""
		exposed method
		帮会解散
		"""
		if not self.validateClientCall():
			return
		if self.tongMB:
			if self.tongTitle == csdefine.TONG_TITLE_1:
				self.tongGetMgr().dismissTong( self.tongDBID, csdefine.TONG_DISMISS_NORMAL )
	
	def tongOnDismiss( self ):
		"""
		define method
		帮会解散
		"""
		self.statusMessage(csstatus.TONG_DISBAND_NOTIFY, self.tongName)
		self.onLeaveTong()
		
	#-----------------------帮会研发技能---------------------------------------------------
	def researchTongSkill( self, skillID ):
		"""
		exposed method
		研发技能
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_DEVELOP ):
			self.statusMessage( csstatus.TONG_CANOT_INVITE_NOT_ENOUGH_GRADE )
			return
		if self.tongMB:
			self.tongMB.researchSkill( self, self.databaseID, skillID )
		
	def pauseTongSkill( self, skillID ):
		"""
		exposed method
		暂停研发技能
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_DEVELOP ):
			self.statusMessage( csstatus.TONG_CANOT_INVITE_NOT_ENOUGH_GRADE )
			return
		if self.tongMB:
			self.tongMB.pauseSkill( self, skillID )
	#-----------------------帮会建筑--------------------------------------------------
	def upGrowTongBuild( self, tongType ):
		"""
		exposed method
		升级帮会建筑
		"""
		if not self.validateClientCall():
			return
		if not self.tongHasGrade( csdefine.TONG_GRADE_BUILDING ):
			self.statusMessage( csstatus.TONG_CANOT_INVITE_NOT_ENOUGH_GRADE )
			return
		if self.tongMB:
			self.tongMB.buildUpgrade( self, tongType )
	
	#-----------------------帮会事件--------------------------------------------------
	def requestTongEvent( self ):
		"""
		exposed method
		请求帮会事件
		"""
		if not self.validateClientCall():
			return
		if self.tongMB:
			self.tongMB.requestTongEvent( self )
			
	def requestTongStoreEvent( self ):
		"""
		exposed method
		请求帮会仓库事件
		"""
		if not self.validateClientCall():
			return
		if self.tongMB:
			self.tongMB.requestTongStoreEvent( self )

#-----------------------帮会神兽-------------------------------------------------------

	def changeNagual(self, nagualType):
		"""
		exposed method
		更换神兽
		"""
		if self.tongMB:
			self.tongMB.changeNagual(self, nagualType)


	def onChangeNagualSucceed(self, nagualType):
		"""
		"""
		if self.tongMB:
			self.tongMB.onChangeNagualSucceed(nagualType)

#-----------------------帮会掠夺战-----------------------------------------------------------------
	def signUpTongPlunder(self, targetTongDBID):
		"""
		exposed method

		向目标帮会发起掠夺战挑战
		"""
		#没有帮会
		if not self.tongMB:
			return

		if not targetTongDBID:
			self.statusMessage(csstatus.TONG_PLUNDER_NEED_SELECT_TONG)
			return

		if self.tongDBID == int(targetTongDBID):
			return

		if KBEngine.globalData["TongPlunderManager_Status"] != csdefine.TONG_PLUNDER_ACTIVITY_STATUS_SIGNUP:
			self.statusMessage(csstatus.SPARHUNTING_ACTIVITY_SIGN_UP_TIME_ERROR)
			return

		if not self.isTongLeader():
			self.statusMessage(csstatus.TONG_PLUNDER_IS_NOT_LEADER)
			return

		KBEngine.globalData["TongMgr"].signUpTongPlunder(self, self.tongDBID, int(targetTongDBID))

	def plunderAddMember(self, playerDBID):
		"""
		exposed method

		添加帮会掠夺战参与成员
		"""
		if not self.tongMB:
			return

		if not self.isTongLeader():
			return

		if KBEngine.globalData["TongPlunderManager_Status"] == csdefine.TONG_PLUNDER_ACTIVITY_STATUS_START:
			self.statusMessage(csstatus.TONG_PLUNDER_CAN_NOT_CHANGE_MEMBER)
			return

		self.tongMB.plunderAddMember(self, int(playerDBID))

	def plunderRemoveMember(self, playerDBID):
		"""
		exposed method

		移除帮会掠夺战参与成员
		"""
		if not self.tongMB:
			return

		if not self.isTongLeader():
			return

		if KBEngine.globalData["TongPlunderManager_Status"] == csdefine.TONG_PLUNDER_ACTIVITY_STATUS_START:
			self.statusMessage(csstatus.TONG_PLUNDER_CAN_NOT_CHANGE_MEMBER)
			return

		self.tongMB.plunderRemoveMember(self, int(playerDBID))


#-----------------------GM-----------------------------------------------------------------
	def clearRejoinTongForbindTime(self):
		"""
		define method
		清除限制申请帮会时间
		"""
		self.lastQuitTongTime = 0.0
