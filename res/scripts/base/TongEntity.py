# -*- coding: utf-8 -*-
import KBEngine
import KST
from CoreObject.GameObject import GameObject

from ImpInterface import TongUpgradeInterface
from ImpInterface import TongContributionInterface
from ImpInterface import TongShopInterface
from ImpInterface import TongStorageInterface
from ImpInterface import TongSkillInterface
from ImpInterface import TongSpaceInterface
from ImpInterface import TongRecordInterface

import TongMember

import time
import TongLoader
import Const
import csdefine
import csconst
import csstatus
import KBEDebug
import Functions
import cschannel_msgs
import functools
import ItemFactory
import math
import random

from ConfigObject.MailContentDataLoader import g_mailContentDataLoader
from ConfigObject.BHZBPointDataLoader import g_BHZBPointDataLoader

class TongEntity( 
		KBEngine.Entity,
		GameObject,
		TongUpgradeInterface.TongUpgradeInterface,
		TongContributionInterface.TongContributionInterface,
		TongShopInterface.TongShopInterface,
		TongStorageInterface.TongStorageInterface,
		TongSkillInterface.TongSkillInterface,
		TongSpaceInterface.TongSpaceInterface,
		TongRecordInterface.TongRecordInterface,
		 ):
	def __init__( self ):
		KBEngine.Entity.__init__( self )
		GameObject.__init__( self )
		TongUpgradeInterface.TongUpgradeInterface.__init__( self )
		TongContributionInterface.TongContributionInterface.__init__( self )
		TongShopInterface.TongShopInterface.__init__( self )
		TongStorageInterface.TongStorageInterface.__init__( self )
		TongSkillInterface.TongSkillInterface.__init__( self )
		TongSpaceInterface.TongSpaceInterface.__init__( self )
		TongRecordInterface.TongRecordInterface.__init__( self )
		
		self.reqJoinDict = {}
	
	def initDatas( self, memberMB, memberDBID, memberName, profession, level, personTitle ):
		if len( self.members ): #初始化过的，几进行初始化，则无效
			return
		self.titleNames = cschannel_msgs.TONG_TITLE_NAME										# 设置默认职位名称
		self.grades = TongLoader.g_TongLoader.getAllSysGrades()						# 设置默认权限
		self.leaderDBID = memberDBID												# 设置帮主DBID
		self.builds.init( self )
		self.join( memberMB, memberDBID, memberName, level, profession, csdefine.TONG_TITLE_1, personTitle )
		self.safeTime = Const.TONG_CREATE_SAFETIME
		self.addRecord( csdefine.TONG_EVENT_CREATE, memberName, self.tongName )
		
		if self.camp == csdefine.CAMP_TAOSIM:
			memberMB.statusMessage( csstatus.TONG_CREATE_SUCCESS_XIAN, self.tongName )
		else:
			memberMB.statusMessage( csstatus.TONG_CREATE_SUCCESS_MO, self.tongName )
		
		memberMB.tongOnInit( self, self.tongName, self.leaderDBID, csdefine.TONG_TITLE_1, self.grades[csdefine.TONG_TITLE_1] )
		memberMB.cell.tongOnCreate( self, self.leaderDBID, csdefine.TONG_TITLE_1, self.grades[csdefine.TONG_TITLE_1], \
		0, self.builds[csdefine.TONG_BUILDING_TYPE_SD].getMaxLevel(self),self.builds[csdefine.TONG_BUILDING_TYPE_TJP].getMaxLevel(self), self.allocation, self.BHLDAllocation )
		self.writeToDB()
	
	def reqInit( self, playerMB, playerDBID ):
		"""
		deifne method
		玩家请求初始化帮会信息
		"""
		memberInfos = self.members.get( playerDBID )
		if memberInfos:
			memberInfos.reqInit( playerMB )
			playerMB.tongOnInit( self, self.tongName, self.leaderDBID, memberInfos.title, self.grades[memberInfos.title] )
			playerMB.cell.tongOnInit( self, self.leaderDBID, memberInfos.title, self.grades[memberInfos.title], \
			memberInfos.contribution, self.builds[csdefine.TONG_BUILDING_TYPE_SD].getMaxLevel(self),\
			self.builds[csdefine.TONG_BUILDING_TYPE_TJP].getMaxLevel(self), self.allocation, self.BHLDAllocation )
			self.notifyClientTongDatas( playerMB, playerDBID )
			for member in self.members.values():
				if member.DBID == playerDBID:continue
				if member.getClient():
					member.baseMailBox.client.OnMemberOnline( str(playerDBID), playerMB.id )
			if self.reqJoinDict and self.hasGrade( playerDBID, csdefine.TONG_GRADE_REQUEST):
				for DBID, info in self.reqJoinDict.items():
					playerMB.client.OnOtherReqJoinTong( str(DBID), info[1], info[2], info[3] )
		else:
			#这里的话是因为玩家下线后，帮会管理人员有可能将自己踢出帮会
			if playerDBID in self.kickOffPlayers:
				initTime = self.kickOffPlayers.pop(playerDBID)
			else:
				initTime = int(time.time())
			playerMB.tongBeKickOffLine( initTime )

		#已参与帮会掠夺战
		if self.tongPlunderData.hasSignUpActive():
			memberIDList = [str(DBID) for DBID in self.tongPlunderData.getMembers()]
			playerMB.client.OnPlunderMemberChange(memberIDList)
			if self.tongPlunderData.hasLockedTongShop(): #是否已经锁定帮会商店
				playerMB.cell.lockTongShop()
		if self.tongPlunderData.tongShopStartSell() and self.tongPlunderData.isVictory():		
			endTimeStr = str(self.tongPlunderData.getSellEndTime() - time.time())
			playerMB.cell.onTongPlunderShopSellStart(self.tongPlunderData.getShopData(), endTimeStr)

	def onMemberOffline( self, playerDBID, playerLevel, birthSpace ):
		"""
		define method
		帮会成员下线
		"""
		self.onBHZBMemberOffLine( playerDBID )
		memberInfos = self.members.get( playerDBID )
		if memberInfos:
			memberInfos.offLine( playerLevel, birthSpace )
			
			for member in self.members.values():
				if member.DBID == playerDBID:continue
				if member.getClient():
					member.baseMailBox.client.OnMemberOffline( str(playerDBID), playerLevel, birthSpace, str(memberInfos.offLineTime) )
		else:
			KBEDebug.ERROR_MSG( "player request init error!! ( error tongDBID:%d, playerDBID:%d)"% ( self.databaseID, playerDBID ) )

	def notifyClientTongDatas( self, playerMB, playerDBID ):
		"""同步客户端帮会数据"""
		member = self.members[playerDBID]
		temp = { "TongDBID" : str(self.databaseID), "TongName":self.tongName, "TongMoney":str(self.money), "TongAffiche":self.affiche,\
		"TongGrades":list(self.grades), "TitleNames":list(self.titleNames), "TongActivity":self.activity, "TongLeader":str(self.leaderDBID), \
		"TongGrow":self.grow, "level":self.level, "TongBuild":self.notifyClientTongBuild(), "TongSkill":self.notifyClientTongSkill(),\
		"TotalNum":self.getMaxMember(), "UpGradeActivity":TongLoader.getUpgradeUseActivity(self.level), "League":"", "City":"",\
		"ShenShou":self.nagualType, "Sign" : int(member.isSign), "signTime" : member.signTime, "donateMoney" : member.dMoney, \
		"Salary" : int(member.isGetSalary), "recruitAffiche" : self.recruitAffiche, "minActivity" : TongLoader.getMinActivity(self.level), \
		"Allocation" : self.allocation, "BHLDAllocation" : self.BHLDAllocation }
		
		if hasattr(playerMB, "client") and playerMB.client:
			playerMB.client.UpdateTongDatas( temp) 
		for member in self.members.values():
			self.notifyClientTongMemberDatas( playerMB, member.DBID )
		self.updateTongBHZBSignMember( playerMB )
		
	def getJoinTongInfo( self ):
		"""申请帮会数据"""
		return { "TongDBID":str(self.databaseID), "Name":self.tongName, "Level":self.level,\
		"Activity":self.activity,"TongNum":len(self.members),"Money":str(self.money),\
		"Recruit":self.recruitAffiche, "LeaderName":self.members[self.leaderDBID].name,\
		"TotalNum":self.getMaxMember(), "League":"", "City":"", "ShenShou" : self.nagualType, "PersonTitle": self.members[self.leaderDBID].personTitle }
		
	def notifyClientTongMemberDatas( self, playerMB, memberDBID ):
		"""更新帮会成员"""
		member = self.members.get( memberDBID )
		if hasattr(playerMB, "client") and playerMB.client:
			playerMB.client.CLIENT_UpdateTongMember(  member.getPackMemberDatas() )

	def notifyClientNagualType( self, nagualType ):
		"""更新神兽类型"""
		for member in self.members.values():
			member.onChangeNagual(nagualType)
		
	def notifyOffLine( self, playerMB, playerDBID ):
		"""
		define method
		玩家下线
		"""
		self.members.get( playerDBID ).offLine()

	def notifyAddTongBlockMember(self, playerDBID, memberDBID):
		#通过DBID 角色自身的，以及对方的 进行增加 帮会屏蔽名单的操作。
		for member in self.members.values():
			if str(member.DBID) == playerDBID:
				if member:
					member.addTongBlocklist(memberDBID)
				else:
					return

	def notifyRemoveTongBlockMember(self, playerDBID, memberDBID):
		# 通过DBID 角色自身的，以及对方的 进行删除 帮会屏蔽名单的操作。
		for member in self.members.values():
			if str(member.DBID) == playerDBID:
				if member:
					member.removeTongBlocklist(memberDBID)
				else:
					return

	def onDawnArrive( self ):
		"""晚上0点"""
		self.safeDeal()
		self.protectDeal()
		self.offLineDeal()
		for member in self.members.values():
			member.onDawnArrive()
		
	def onWeekArrive( self ):
		"""每周一 0点"""
		for member in self.members.values():
			member.onWeekArrive()
		
	def safeDeal( self ):
		"""安全期处理"""
		if self.safeTime:				# 安全期 不扣除活跃度
			self.safeTime -= 1
			self.addRecord( csdefine.TONG_EVENT_SAFE_TIME_NOTICE, self.safeTime )
			if self.safeTime == 0:
				if self.level == 1:
					self.addRecord( csdefine.TONG_EVENT_PROTECT_DAY_OVER_NORMAL )
				else:
					self.addRecord( csdefine.TONG_EVENT_PROTECT_DAY_OVER_ONE )
		else:
			#帮会每日扣除活跃度=（帮会升级需要活跃度*10%）+（帮会升级需要活跃度*10%）*帮会资金过低扣除活跃度比例 CST-12058
			activity = TongLoader.getPerDayUseActivity( self.level )
			if TongLoader.getLowMoney( self.level ) > self.money: 
				activity += int(activity * TongLoader.getPerActivityForLowMoney( self.level ) / 100)
			
			subValue = self.subActivityUntillZero( activity )
			if subValue > 0:
				self.addRecord( csdefine.TONG_EVENT_SUB_ACTIVITY , activity )
			
			if self.activity > 0 and self.activity >= TongLoader.getMinActivity( self.level ):
				self.protectDay = 0	
				return
			
			if not self.protectDay:
				if self.level > 1:
					self.protectDay = Const.TONG_LEVEL_PROTECTTIME
				else:
					self.protectDay = Const.TONG_DISMISS_PROTECTIME
				
	def protectDeal( self ):
		"""保护期处理"""
		if not self.safeTime and self.protectDay:
			self.protectDay -= 1
			if self.protectDay <= 0:
				if self.level > 1:
					self.tongDownGrade()
				else:
					KBEngine.globalData["TongMgr"].dismissTong( self.databaseID, csdefine.TONG_DISMISS_PROTECT_OVER )
			else:
				activity = TongLoader.getMinActivity( self.level )
				if self.level > 1:
					self.addRecord( csdefine.TONG_EVENT_DOWN_GRADE_NOTICE, self.protectDay, activity, self.level - 1 )
				else:
					self.addRecord( csdefine.TONG_EVENT_PROTECT_DAY_SUB_ONELEVEL, self.protectDay, activity )
				
	def offLineDeal( self ):
		"""不在线处理"""
		if self.isDestroyed: return
		oldLeader = self.members[self.leaderDBID]
		if not oldLeader.baseMailBox:
			demiseTime = Const.TONG_OFFLINE_DEMISE_LEADER * csconst.TIME_ENLARGE_MULTIPLE
			if demiseTime + oldLeader.offLineTime <= Functions.getTime():			# 长时间不在线，强制罢免
				newLeader = self.filterLeader()
				if newLeader:
					self.leaderDBID = newLeader.DBID
					self.onLeaderChange( oldLeader.DBID )
					self.addRecord( csdefine.TONG_EVENT_FORCE_CHANGE_LEADER, oldLeader.name, newLeader.name )
					
	def onTongSpaceCreateFinish( self, spaceMB ):
		"""帮会 驻地创建完成"""
		self.spaceMB = spaceMB
		self.createNagual()
		
	def createNagual( self ):
		"""创建帮会神兽"""
		scriptID = TongLoader.getNagualScriptID( self )

		if scriptID:
			self.spaceMB.cell.createTongNagual(scriptID)
		

	def changeNagual(self, playerBaseEntityCall, nagualType):
		"""
		"""
		if self.nagualType == nagualType or not self.spaceMB:
			playerBaseEntityCall.client.OnChangeNagualCB(False)
			return

		#通知space替换nagual
		scriptID = TongLoader.getNagualScriptIDByType( self, nagualType )

		if scriptID:
			self.spaceMB.cell.changeTongNagual(playerBaseEntityCall, nagualType, scriptID)


	def onChangeNagualSucceed(self, nagualType):

		self.nagualType = nagualType
		self.notifyClientNagualType(nagualType)
		
	def onAccumulateOnlineTime( self, playerDBID ):
		"""
		define method
		帮会成员在线满1小时
		"""
		if playerDBID in self.members:
			TongLoader.addRewardsByPlayType( self, playerDBID, csdefine.TONG_PLAY_TYPE_ONLINE )
				
	def onLeaderChange( self, oldDBID ):
		"""更换帮主之位"""
		leader = self.members[self.leaderDBID]
		oldLeader = self.members[oldDBID]
		titleID = TongLoader.getTitleByExp( oldLeader.exp )
		srcGrade = self.grades[titleID]
		dstGrade = self.grades[csdefine.TONG_TITLE_1]
		for member in self.members.values():
			member.onSetTitle( oldLeader.DBID, titleID, srcGrade )
			member.onSetTitle( leader.DBID, csdefine.TONG_TITLE_1, dstGrade )
			if member.baseMailBox:
				member.baseMailBox.cell.onLeaderChange( leader.DBID )
				member.baseMailBox.onLeaderChange( leader.DBID )
				
				if member.getClient():
					member.baseMailBox.client.OnLeaderChange( str(leader.DBID) )
		
		#如果新任帮主不在线，则发一封邮件提醒
		if leader.baseMailBox is None:
			KBEngine.globalData["MailManager"].sendWithMailbox(None, leader.baseMailBox, leader.name, csdefine.MAIL_SENDER_TYPE_SYS, cschannel_msgs.MAIL_SEND_SYSTEM, \
				cschannel_msgs.TONG_CHANGE_LEADER_MAIL_TITLE.format(self.tongName), cschannel_msgs.TONG_CHANGE_LEADER_MAIL_CONTENT.format(oldLeader.name, self.tongName), 0, 0, [], 0, 0)
			
	def filterLeader( self ):
		if len( self.members ) == 1:return None
		
		def reversed_cmp(x,y):
			if x.title < y.title:return 1
			if x.title > y.title:return -1
			if x.exp > y.exp:return 1
			if x.exp < y.exp:return -1
			return -1
		
		candidate = []
		for member in self.members.values():
			if member.baseMailBox:
				candidate.append( member )
		
		if not candidate:
			candidate = list( self.members.values() )
		sorted( candidate, key = functools.cmp_to_key( reversed_cmp ), reverse = True)
		if candidate[0].DBID == self.leaderDBID:
			return candidate[1]
		return candidate[0]
		
	def deleteRole( self, roleDBID ):
		"""
		"""
		#只有一个人了的话，就直接解散帮会
		if len(self.members) <= 1: 
			KBEngine.globalData["TongMgr"].dismissTong( self.databaseID, csdefine.TONG_DISMISS_NORMAL )
			return
		
		#重选帮主
		if roleDBID == self.leaderDBID:
			oldLeader = self.members[self.leaderDBID]
			newLeader = self.filterLeader()
			self.leaderDBID = newLeader.DBID
			self.onLeaderChange( oldLeader.DBID )
			self.addRecord( csdefine.TONG_EVENT_FORCE_CHANGE_LEADER, oldLeader.name, newLeader.name )
		 
		#不是帮主直接退出就完事了
		self.tongQuit(roleDBID)
		
	#----------------------帮会个体属性--------------------------------------------------------------------------------
	def hasGrade( self, playerDBID, grade ):
		"""是否有某种权限"""
		if playerDBID in self.members:
			titleID = self.members[playerDBID].title
			return self.grades[titleID] & ( 1<< grade )
		return False
		
	def setTitleName( self, playerMB, titleID, titleName ):
		"""
		define method
		设置帮会成员职位名称
		"""
		if titleName in self.titleNames:
			playerMB.client.statusMessage( csstatus.TONG_CANNOT_RENAME_NAME_IS_EXIT, "" )
			playerMB.client.OnSetTitleNameFailed()
			return
		
		self.titleNames.pop( titleID )
		self.titleNames.insert( titleID, titleName )
		for member in self.members.values():
			member.onSetTitleName( titleID, titleName )
		
	def setTitle( self, sourceDBID, targetDBID, titleID ):
		"""
		define method
		设置帮会成员职位
		"""
		if sourceDBID in self.members and targetDBID in self.members:
			sourceMember = self.members[sourceDBID]
			targetMember = self.members[targetDBID]
			oldTitle = targetMember.title
			if targetMember.title == titleID:return
			if sourceMember.title >= targetMember.title:
				sourceMember.baseMailBox.client.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE, "" )
				return
			if titleID in Const.TONG_NUM_LIMIT:
				limitNum = Const.TONG_NUM_LIMIT[titleID]
				memberList = self.getMemberByTitle( titleID )
				if len( memberList ) >= limitNum:
					sourceMember.baseMailBox.client.statusMessage( csstatus.TONG_TITLE_MEMBER_HAS_ENOUGH, "" )
					return
				
			if titleID > csdefine.TONG_TITLE_4 :				# 采用经验 命名方式
				titleID = TongLoader.getTitleByExp( targetMember.exp )
			newGrade = self.grades[titleID]
			if titleID > csdefine.TONG_TITLE_4:
				eventType = csdefine.TONG_EVENT_RECALL
				titleName = self.titleNames[targetMember.title]
				sourceMember.baseMailBox.client.statusMessage( csstatus.YOU_DISMISS_MEMBER_TONG_DUTY, targetMember.name )
				if targetMember.baseMailBox:
					targetMember.baseMailBox.client.statusMessage( csstatus.YOU_BE_DISMISS_MEMBER_TONG_DUTY, "%s|%s|%s"%(\
					self.titleNames[targetMember.title], self.titleNames[sourceMember.title], sourceMember.name))
					
			else:
				eventType = csdefine.TONG_EVENT_APPOINT
				titleName = self.titleNames[titleID]
				sourceMember.baseMailBox.client.statusMessage( csstatus.TONG_DUTY_SET_SUCCESS, "" )
				if targetMember.baseMailBox:
					targetMember.baseMailBox.client.statusMessage( csstatus.YOU_TONG_DUTY_BE_SET_SUCCESS, "%s|%s|%s"%(\
					self.titleNames[sourceMember.title], sourceMember.name, self.titleNames[titleID]) )
			self.addRecord( eventType, sourceMember.name, targetMember.name, titleName)
			for member in self.members.values():
				member.onSetTitle( targetDBID, titleID, newGrade )
				
			if self.reqJoinDict:
				if not self.grades[oldTitle] & (1<<csdefine.TONG_GRADE_REQUEST) and self.hasGrade( targetDBID, csdefine.TONG_GRADE_REQUEST):
					for DBID, info in self.reqJoinDict.items():
						targetMember.baseMailBox.client.OnOtherReqJoinTong( str(DBID), info[1], info[2], info[3] )
		else:
			KBEDebug.ERROR_MSG("Cannot find member!srcMember is None(%r), dstMember is None(%r)"
			%(sourceDBID in self.members, targetDBID in self.members))
			
	def getMemberByTitle( self, titleID ):
		"""获取相关职位的成员"""
		memberList = []
		for member in self.members.values():
			if member.title == titleID:
				memberList.append( member )
		return memberList
	
	def setGrade( self, titleID, grades ):
		"""
		define method
		设置帮会成员的权限
		"""
		fobGrades = TongLoader.g_TongLoader.getFobGrades(titleID)
		if grades & fobGrades:							# 如果设置的权限跟禁止权限有交集，有错误
			KBEDebug.ERROR_MSG("Set grade err!forbid grade is set!")
			grades &= ~fobGrades						# 可能因为权限配置修改导致
		if self.grades[titleID] == grades:return
		oldGrades = self.grades[titleID]
		self.grades.insert(titleID+1, grades )
		self.grades.pop(titleID)
		for member in self.members.values():
			member.onSetGrade( titleID, grades )
		# 
		if self.reqJoinDict:
			if not oldGrades & (1<<csdefine.TONG_GRADE_REQUEST) and grades & (1<<csdefine.TONG_GRADE_REQUEST):
				for member in self.members.values():
					if member.baseMailBox and member.title == titleID:
						for DBID, info in self.reqJoinDict.items():
							member.baseMailBox.client.OnOtherReqJoinTong( str(DBID), info[1], info[2], info[3] )
	
	def addMemberExp( self, playerDBID, exp ):
		"""
		define method
		添加帮会个人经验
		"""
		if playerDBID in self.members:
			self.members[playerDBID].addExp( self, exp )
		else:
			KBEDebug.ERROR_MSG("addMemberExp error!can not find member(dbid:%d)"%playerDBID)
			
	def deMiseLeader( self, srcPlayerDBID, dstPlayerDBID ):
		"""
		define method
		禅让帮主
		"""
		if srcPlayerDBID == self.leaderDBID and dstPlayerDBID in self.members:
			srcMember = self.members[srcPlayerDBID]
			dstMember = self.members[dstPlayerDBID]
#			if dstMember.title > csdefine.TONG_TITLE_6:
#				srcMember.baseMailBox.client.statusMessage( csstatus.TONG_DEMISE_FAIL_NO_ENOUGH_EXP, "" )
#				return
			
			self.leaderDBID = dstPlayerDBID
			self.onLeaderChange( srcPlayerDBID )
			if dstMember.getClient(): dstMember.getClient().statusMessage( csstatus.TONG_DEMISE_LEADER_FOR_YOU, srcMember.name )
			self.addRecord( csdefine.TONG_EVENT_CHANGE_LEADER, srcMember.name, dstMember.name )
			
	def setMemberGag( self, playerDBID, isGag ):
		"""
		define method
		设置禁言
		"""
		for member in self.members.values():
			member.setGag( playerDBID, isGag )
			
	def tongSign( self, playerDBID ):
		"""
		define method
		帮会签到
		"""
		if playerDBID in self.members:
			if not self.members[playerDBID].isSign:
				TongLoader.addRewardsByPlayType( self, playerDBID, csdefine.TONG_PLAY_TYPE_SIGN )
				self.members[playerDBID].tongSign()
				
	def getSalary( self, playerDBID ):
		"""
		define method
		领取俸禄
		"""
		if playerDBID in self.members:
			member = self.members[playerDBID]
			if not member.isGetSalary:
				member.isGetSalary = True
				itemID = self.builds[csdefine.TONG_BUILDING_TYPE_YSDT].getSalary( self, member.title )
				member.baseMailBox.cell.onGetTongSalary( itemID )
				
	def onGetSalaryFail( self, playerDBID ):
		"""
		define method
		领取俸禄失败
		"""
		if playerDBID in self.members:
			member = self.members[playerDBID]
			member.isGetSalary = False
		
	def onTongChat( self, playerMB, playerName,chatData ):
		"""帮会频道发言"""
		if chatData.playerDBID in self.members:
			selfMember = self.members[chatData.playerDBID]
			if selfMember.isGag:
				playerMB.client.statusMessage( csstatus.TONG_CHAT_IS_GAG, "" )
				return
			else:
				if selfMember.chatTime == 0:
					selfMember.chatTime += 1
					TongLoader.addRewardsByPlayType( self, selfMember.DBID, csdefine.TONG_PLAY_TYPE_CHAT )

				for member in self.members.values():
					if member.baseMailBox and str(chatData.playerDBID) not in member.tongBlocklist: # 屏蔽列表里的不接受。
						member.baseMailBox.cell.onReceiveChatMessageWithDBID( chatData.playerDBID, chatData )
		else:
			KBEngine.ERROR_MSG("onTongChat error!can not find member(dbid:%d)"%chatData.playerDBID)

	def onTongSpaceComplete( self, playerDBID ):
		"""
		define method
		完成帮会副本
		"""
		if playerDBID in self.members:
			TongLoader.addRewardsByPlayType( self, playerDBID, csdefine.TONG_PLAY_TYPE_COPY )

	def UpdateTongMemberInfo( self, dbid, level, localSpace, soldierAmount, militaryRank ):
		"""
		define method
		更新信息
		"""
		
		memberInfos = self.members.get( dbid )
		if memberInfos:
			memberInfos.UpdateTongMemberInfo( level, localSpace, soldierAmount, militaryRank )
			
			for member in self.members.values():
				if member.getClient():
					member.getClient().UpdateTongMemberInfo(str(dbid), level, localSpace,soldierAmount, militaryRank)
					
	def updatePlayerTitle( self, dbid, personTitle ):
		"""
		更新个人称号
		"""
		memberInfos = self.members.get( dbid )
		if memberInfos:
			memberInfos.UpdateTongMemberPersonTitle(personTitle)
				
	#----------------------帮会群体属性--------------------------------------------------------------------------------
	def addTongMoney( self, money, reason = csdefine.TONG_MONEY_ADD_REASON_NORMAL ):
		"""
		define method
		添加帮会金钱
		"""
		oldValue = self.money
		newValue = self.money + money
		limitMoney = self.builds[csdefine.TONG_BUILDING_TYPE_CK].getTongMoneyLimit(self)
		self.money = min( newValue, limitMoney )
		if self.money != oldValue:
			self.onMoneyChange( oldValue )
			if reason != csdefine.TONG_MONEY_ADD_REASON_PERSON:			# 个人原因，导致帮会金币增加的，不会广播给帮会所有人
				for member in self.members.values():
					if member.baseMailBox and member.baseMailBox.client:
						member.baseMailBox.client.statusMessage( csstatus.TONG_MONEY_GET_MONEY, Functions.moneyToStr(money))
		
	def subTongMoney( self, money ):
		"""
		define method
		减少帮会金钱
		"""
		if self.hasEnoughMoney( money ):
			oldValue = self.money
			self.money -= money
			self.onMoneyChange( oldValue )
			return True
		else:
			KBEDebug.ERROR_MSG("Sub money err!!has not enough money")
			return False
			
	def hasEnoughMoney( self, money ):
		return self.money - self.getLockedMoney() >= money
		
	def onMoneyChange( self, oldValue ):
		for member in self.members.values():
			member.onMoneyChange( self.money )

	def getLockedMoney(self):
		lockMoney = 0
		if self.tongPlunderData.hasSignUpActive():
			lockMoney += self.tongPlunderData.getLockMoney()
		return lockMoney

	def donateMoney( self, playerDBID, money ):
		"""
		define method
		捐献
		"""
		if playerDBID in self.members and self.members[playerDBID].baseMailBox:
			playerMember = self.members[playerDBID]
			limitMoney = self.builds[csdefine.TONG_BUILDING_TYPE_CK].getTongMoneyLimit(self)
			if self.money >= limitMoney:
				playerMember.baseMailBox.client.statusMessage( csstatus.TONG_MONEY_IS_FULL_ALREADY, "" )
				return
			if playerMember.dMoneyDay >= Const.TONG_DONATE_MONEY_TOTAL:
				playerMember.baseMailBox.client.statusMessage( csstatus.TONG_DONATE_MONEY_IS_FULL, "" )
				return
			if self.money + money > limitMoney or playerMember.dMoneyDay + money > Const.TONG_DONATE_MONEY_TOTAL:
				if limitMoney - self.money < Const.TONG_DONATE_MONEY_TOTAL - playerMember.dMoneyDay:
					money = limitMoney - self.money
					playerMember.baseMailBox.client.statusMessage( csstatus.TONG_MONEY_IS_FULL, Functions.moneyToStr( money ))
				else:
					money = Const.TONG_DONATE_MONEY_TOTAL - playerMember.dMoneyDay
					playerMember.baseMailBox.client.statusMessage( csstatus.TONG_DONATE_MONEY_IS_FULL_ALREADY, Functions.moneyToStr( money ))
			self.addTongMoney( money, csdefine.TONG_MONEY_ADD_REASON_PERSON )
			contribution = int( money * Const.TONG_MONEY_TO_CONTRIBUTE )
			exp = int( money * Const.TONG_MONEY_TO_EXP )
			for member in self.members.values():
				member.donateMoney( self, playerDBID, playerMember.name, money, contribution, exp )
		else:
			KBEDebug.ERROR_MSG("donateMoney error!!can not find member(%d)"%playerDBID)
			
	def setAffiche( self, affiche ):
		"""
		define method
		设置帮会公告
		"""
		self.affiche = affiche
		for member in self.members.values():
			if member.getClient():
				member.baseMailBox.client.OnSetAffiche( affiche )
		
	def setRecruitAffiche( self, affiche ):
		"""
		define method
		设置帮会招募公告
		"""
		self.recruitAffiche = affiche
		for member in self.members.values():
			if member.getClient():
				member.baseMailBox.client.OnSetRecruitAffiche( affiche )
		
	def getMaxMember( self ):
		"""获取帮会最大加入人数"""
		return self.builds[csdefine.TONG_BUILDING_TYPE_YSDT].getTongLimitNum( self )
	#----------------------帮会加入--------------------------------------------------------------------------------
	def reqJoin( self, roleMB, roleDBID, roleName, level, profession, camp ):
		"""请求加入"""
		if roleDBID in self.reqJoinDict:return			#需要记录（不存储）请求加入玩家的信息
		
		if len( self.members ) >= self.getMaxMember():
			roleMB.client.statusMessage( csstatus.TONG_CANOT_JOIN_MAX_MEMBER, "" )
			roleMB.OnApplyJoinTongFailed(self.databaseID)
			return
			
		if camp != self.camp:
			roleMB.client.statusMessage( csstatus.TONG_CANOT_JOIN_DIFFER_CAMP, "" )
			roleMB.OnApplyJoinTongFailed(self.databaseID)
			return
		
		if hasattr( roleMB, "client" ) and roleMB.client:
			roleMB.client.OnApplyJoinTongSuccess( str( self.databaseID ) )
		self.reqJoinDict[roleDBID] = ( roleDBID, roleName, level, profession )
		for memberDBID, member in self.members.items():
			if member.getClient() and self.hasGrade( memberDBID, csdefine.TONG_GRADE_REQUEST):
				member.baseMailBox.client.OnOtherReqJoinTong( str(roleDBID), roleName, level, profession )
			
	def cancelJoin( self, roleDBID ):
		"""取消加入"""
		if roleDBID in self.reqJoinDict:
			self.reqJoinDict.pop( roleDBID )
			for memberDBID, member in self.members.items():
				if member.getClient() and self.hasGrade( memberDBID, csdefine.TONG_GRADE_REQUEST):
					member.baseMailBox.client.OnOtherCancelJoinTong( str(roleDBID ))
	
#	def requestJoinList( self, roleDBID ):
#		if roleDBID in self.members:
#			playerMB = self.members[roleDBID].baseMailBox
#			if playerMB:
#				DBIDList = []
#				nameList = []
#				levelList = []
#				proList = []
#				for joinData in self.reqJoinDict.values():
#					DBIDList.append( str( joinData[0] ))
#					nameList.append( joinData[1] )
#					levelList.append( joinData[2] )
#					proList.append( joinData[3] )
#				playerMB.client.OnRequestJoinList( DBIDList, nameList, levelList, proList )
	
	def replyAllJoinTong( self, replayMB, canJoin ):
		"""
		define method
		一键回复 申请加入帮会
		"""
		for playerDBID in self.reqJoinDict.keys():
			replayMB.replyJoinTong( str(playerDBID), canJoin )
		
	def replyJoinTong( self, replayMB, beReplayMB, beReplayDBID, canJoin ):
		"""
		define method
		回复 申请加入帮会
		"""
		if beReplayDBID not in self.reqJoinDict:
			replayMB.client.statusMessage( csstatus.TONG_CANOT_INVITE_HAS_TONG, "" )			# 如果不在申请加入帮会列表，说明已经加入其它帮会
			return
		
		reqInfo = self.reqJoinDict.pop(beReplayDBID)	#不管怎样先移除
		if not canJoin:
			if beReplayMB: beReplayMB.refuseJoinTong( self.databaseID, self.tongName )
		else:	
			if len( self.members ) >= self.getMaxMember():
				if beReplayMB: beReplayMB.refuseJoinTong( self.databaseID, self.tongName )
				replayMB.client.statusMessage( csstatus.TONG_CANOT_INVITE_MAX_MEMBER, "" )
			else:
				self.join( beReplayMB, reqInfo[0], reqInfo[1], reqInfo[2], reqInfo[3], csdefine.TONG_TITLE_9, "" )			# 玩家下线了，
		
		#通知帮会的管理人员，更新帮会申请列表数据
		for memberDBID, member in self.members.items():
			if memberDBID == beReplayDBID: continue
			if member.getClient() and self.hasGrade( memberDBID, csdefine.TONG_GRADE_REQUEST):
				member.baseMailBox.client.OnRemoveApplyJoinTongMember( str(beReplayDBID) )
	
	def onJoinResult( self, playerDBID ):
		if playerDBID in self.reqJoinDict:
			del self.reqJoinDict[playerDBID]
			
	def replyInviteTong( self, inviteMB, beInviteMB, beInviteDBID, name, level, profession, personTitle ):
		"""
		define method
		回复 邀请加入帮会
		"""
		if len( self.members ) >= self.getMaxMember():
			if hasattr(inviteMB, "client") and inviteMB.client:
				inviteMB.client.statusMessage( csstatus.TONG_CANOT_INVITE_MAX_MEMBER, "" )
			if hasattr(beInviteMB, "client") and beInviteMB.client:
				beInviteMB.client.statusMessage( csstatus.TONG_CANOT_JOIN_AS_MAX_MEMBER, "" )
			return
		
		self.join( beInviteMB, beInviteDBID, name, level, profession, csdefine.TONG_TITLE_9, personTitle )
	
	def join( self, playerMailbox, playerDBID, playerName, level, profession, title, _personTitle  ):
		"""
		加入帮会
		"""
		member = TongMember.TongMember( playerMailbox, playerDBID, playerName, level, profession, title, personTitle = _personTitle )
		self.members[ playerDBID ] = member
		if playerMailbox:								# 玩家有可能下线了
			playerMailbox.tongOnJoin( self,  self.databaseID, self.tongName, member.title, self.grades[member.title] )
#			self.notifyClientTongDatas( playerMailbox, playerDBID )
		else:
			member.saveTong( self.databaseID )
		self.onJoin( member )
	
	def onJoin( self, member ):
		"""
		新成员加入帮会
		"""
		KBEngine.globalData["TongMgr"].onJoinResult( member.DBID )
		for m in self.members.values():
			m.tongOnMemberJoin( self, member.DBID, member.name, self.tongName ) #广播有新玩家加入
		
	def inviteJoinTong(self, playerName, camp, inviterMB, target):
		"""
		"""
		if len( self.members ) >= self.getMaxMember():
			inviterMB.client.statusMessage( csstatus.TONG_CANOT_INVITE_MAX_MEMBER, "" )
			return
			
		if target:
			target.tongBeInviteJoin( playerName, self.tongName, camp ,str(self.databaseID),inviterMB, self )
		
	#----------------------帮会离开--------------------------------------------------------------------------------
	def kickMember( self, kickDBID, beKickDBID ):
		"""
		define method
		踢人
		"""
		kickMem = self.members.get( kickDBID, None )
		beKickMem = self.members.get( beKickDBID, None )
		if kickMem and beKickMem:
			if kickMem.title < beKickMem.title:
				for member in self.members.values():
					member.onKick( kickMem, beKickMem )
				self.members.pop( beKickDBID )
				if not beKickMem.baseMailBox:			# 玩家下线了
					self.kickOffPlayers[beKickDBID] = int( time.time() )
					KBEngine.globalData["MailManager"].sendWithMailbox(None, beKickMem.baseMailBox, beKickMem.name, csdefine.MAIL_SENDER_TYPE_SYS, cschannel_msgs.MAIL_SEND_SYSTEM, \
				cschannel_msgs.TONG_KICK_MENBER_MAIL_TITLE%self.tongName, cschannel_msgs.TONG_KICK_MENBER_MAIL_CONTENT%(kickMem.name, self.tongName), 0, 0, [], 0, 0)
				
				self.addRecord( csdefine.TONG_EVENT_TICK, kickMem.name, beKickMem.name )
			else:
				if kickMem.getClient():
					kickMem.baseMailBox.client.statusMessage( csstatus.TONG_NOT_ENOUGH_GRADE, "" )
		else:
			KBEDebug.ERROR_MSG("Tong kick member error!!kicker(DBID:%d) is None(%r), beKickMem(DBID:%d) is None(%r)"\
			%( kickDBID, kickMem is None, beKickDBID, beKickMem is None ))
		
	def tongQuit( self, quitDBID ):
		"""
		define method
		退出帮会
		"""
		if quitDBID in self.members:
			member = self.members[quitDBID]
			if member.title == csdefine.TONG_TITLE_1:
				if len( self.members ) > 1:
					if member.getClient():
						member.baseMailBox.client.statusMessage( csstatus.TONG_CANOT_LEAVE_TITLE_1, "" )
					return
				else:
					KBEngine.globalData["TongMgr"].dismissTong( self.databaseID, csdefine.TONG_DISMISS_NORMAL )
					return
				
			for memberMB in self.members.values():
				memberMB.tongQuit( quitDBID )
			self.addRecord( csdefine.TONG_EVENT_LEAVE, member.name )
			self.members.pop( quitDBID )

			#帮会掠夺战
			if self.tongPlunderData.hasSignUpActive():
				if quitDBID in self.tongPlunderData.getMembers():
					self.tongPlunderData.removeMember(quitDBID)
	
	def tongOnDismiss( self ):
		"""
		帮会解散
		"""
		for member in self.members.values():
			member.tongOnDismiss()
		self.members.clear()
		self.destroy(deleteFromDB = True)
		
	def GM_CommandSetAttr( self, playerDBID, attr, value ):
		"""
		define method
		GM指令设置帮会属性
		"""
		if playerDBID in self.members:
			if attr == "exp":
				self.members[playerDBID].addExp( self, value )
			elif attr == "contribution":
				self.members[playerDBID].addContribution( self, value )
			elif attr == "level":
				oldValue = self.level
				self.level = value
				self.onLevelChange( oldValue, playerDBID )
			elif attr == "activity":
				self.addActivity( value )
			elif attr == "grow":
				self.addGrow( value )
			elif attr == "money":
				self.addTongMoney( value )
			elif attr == "skill":
				self.finishResearchSkill()
		else:
			KBEDebug.ERROR_MSG("GM Command set tong attr fail!!can not find player(%d)"%playerDBID)


	def getMemberByName( self, name ):
		"""
		通过名字获得Member
		"""
		for member in self.members.values():
			if member.name == name:
				return member
		return None

	def getMemberByDBID( self, dbid ):
		"""
		通过DBID获得Member
		"""
		if dbid in self.members:
			return self.members[dbid]
		return None
	
	#---------------------------帮会争霸---------------------------
	def tongStarcraft_firstSignUp( self, playerMB, playerDBID, firstTeamNames,secondTeamNames,thirdTeamNames,fourTeamNames ):
		"""
		报名帮会争霸
		"""
		signUpMemberInfos = []
		def addJoinMember( teamNames, groupID ):
			for name in teamNames:
				member = self.getMemberByName( name )
				if not member:
					playerMB.statusMessage( csstatus.TONG_STARCRAFT_SIGNUP_LEVEL_TONG, name )
					return
				signUpMemberInfos.append( {"groupID":groupID,"name":name,"dbid":member.DBID} )


		addJoinMember( firstTeamNames,0 )
		addJoinMember( secondTeamNames,1 )
		addJoinMember( thirdTeamNames,2 )
		addJoinMember( fourTeamNames,3 )

		KBEngine.globalData["TongStarcraftManager"].tongStarcraft_firstSignUp( self.camp,self.databaseID,self,playerDBID,playerMB,signUpMemberInfos )

	def signUpStarcraftSuccess( self, signUpDBIDs ):
		"""
		报名成功后回调
		"""
		for playerDBID in signUpDBIDs:
			if playerDBID not in self.members:
				KBEDebug.ERROR_MSG("tong has not this player%i"%playerDBID)
				return
			if self.members[playerDBID].baseMailBox:
				self.members[playerDBID].baseMailBox.statusMessage(csstatus.TONG_STARCRAFT_JOIN_NOTIFY,"")
			KBEngine.globalData["MailManager"].send(None, self.members[playerDBID].name, csdefine.MAIL_SENDER_TYPE_SYS, cschannel_msgs.MAIL_SEND_SYSTEM, cschannel_msgs.TONG_STARCRAFT_SIGN_UP_SUCC_MAIL_TITLE,cschannel_msgs.TONG_STARCRAFT_SIGN_UP_SUCC_MAIL_CONTENT,0, 0,[],0,0 )

	def tongStarcraft_SecondSignUp( self, playerMB, playerDBID, signUpNames ):
		"""
		报名帮会争霸第二场
		"""
		signUpMemberInfos = []
		for name in signUpNames:
			member = self.getMemberByName( name )
			if not member:
				playerMB.statusMessage( csstatus.TONG_STARCRAFT_SIGNUP_LEVEL_TONG, name )
				return
			signUpMemberInfos.append( {"name":name,"dbid":member.DBID} )

		KBEngine.globalData["TongStarcraftManager"].tongStarcraft_SecondSignUp( self.camp, self.databaseID, self, playerDBID, playerMB, signUpMemberInfos)

	def testEnterThirdTongStarcraft( self, side, spaceName, enterPos, enterDir ):
		"""
		测试进入帮会争霸第三场
		"""
		members = []
		for member in self.members.values():
			if member.baseMailBox == None:
				continue
			members.append(member.baseMailBox)
		KBEngine.globalData["TongStarcraftManager"].tongStarcraft_gotoThirdStarcraft( self.camp, self.databaseID, side, spaceName, enterPos, enterDir, members )

	def firstTongStarcraftSignUp( self, playerMB, playerDBID, signUpPlayerNames ):
		"""
		报名帮会争霸第一场
		"""
		signUpMemberInfos = []
		for name in signUpPlayerNames:
			member = self.getMemberByName( name )
			if not member:
				playerMB.statusMessage( csstatus.TONG_STARCRAFT_SIGNUP_LEVEL_TONG, name )
				continue
			signUpMemberInfos.append( {"name":name,"dbid":member.DBID} )

		KBEngine.globalData["TongStarcraftManager7904"].firstTongStarcraftSignUp(self.tongName,self.camp,self.databaseID,self,playerDBID,playerMB,signUpMemberInfos  )


	def tongCampWarSignUp( self, playerMB, signUpPlayerNames ):
		"""
		报名帮会阵营战
		"""
		signUpMemberInfos = []
		for name in signUpPlayerNames:
			member = self.getMemberByName( name )
			if not member:
				continue
			signUpMemberInfos.append( {"name":name,"dbid":member.DBID} )

		KBEngine.globalData["TongCampWarManager"].tongCampWarSignUp( self.camp, self.databaseID, self, playerMB, signUpMemberInfos, self.tongName, self.level )


	def readyToSignUpBHZBMember( self, signUpMemberDatas, playerMB ):
		"""
		确认帮会争霸成员
		"""
		if KBEngine.globalData.get( "BHZBSignUpMem", 0 ) and KBEngine.globalData.get( "BHZBStart",0 ):
			KBEngine.globalData["BHZBManager"].sureAllIsBHZBMember( self.camp, self.databaseID,signUpMemberDatas,playerMB, self )
		else:
			self.bhzbSignUpMembers.clear()
			totalSignUpMemberDBIDs = []
			for signUpMemberData in signUpMemberDatas:
				if signUpMemberData.captainDBID and int(signUpMemberData.captainDBID) in self.members and signUpMemberData.captainDBID not in totalSignUpMemberDBIDs:
					totalSignUpMemberDBIDs.append( signUpMemberData.captainDBID )
				for memberDBIDStr in signUpMemberData.memberDBIDs:
					if memberDBIDStr and int( memberDBIDStr ) in self.members and memberDBIDStr not in totalSignUpMemberDBIDs:
						totalSignUpMemberDBIDs.append( memberDBIDStr )

			for signUpMemberData in signUpMemberDatas:
				self.bhzbSignUpMembers[signUpMemberData.groupID] = signUpMemberData

			self.updateTongBHZBSignMembrToAllMem()
			KBEngine.globalData["BHZBManager"].changeSignUpBHZBMember( self.camp,self.databaseID,list(self.bhzbSignUpMembers.values()) )
			#self.writeToDB()

	def OnSureAllIsBHZBMember( self, signUpMemberDatas ):
		"""
		BHZBManger 验证完后通知过来
		"""
		dstGroupIDs = []
		for signUpMemberData in signUpMemberDatas:
			dstGroupIDs.append( signUpMemberData.groupID )
			if signUpMemberData.groupID in self.bhzbSignUpMembers and self.bhzbSignUpMembers[signUpMemberData.groupID].getIsActive():
				continue
			self.bhzbSignUpMembers[signUpMemberData.groupID] = signUpMemberData
		srcGroupIDs = list(self.bhzbSignUpMembers.keys())
		for groupID in srcGroupIDs:
			if groupID not in dstGroupIDs and groupID in self.bhzbSignUpMembers and not self.bhzbSignUpMembers[groupID].getIsActive():
				del self.bhzbSignUpMembers[groupID]

		self.updateTongBHZBSignMembrToAllMem()
		#self.writeToDB()
		KBEngine.globalData["BHZBManager"].changeBHZBMemberTeam( self.camp, self.databaseID,list(self.bhzbSignUpMembers.values()) )

	def updateTongBHZBSignMember( self, playerMB ):
		"""
		更新参与帮会争霸成员到客户端
		"""
		if hasattr(playerMB, "client") and playerMB.client:
			playerMB.client.OnSureSignUpBHZBMember( list(self.bhzbSignUpMembers.values()) )

	def updateTongBHZBSignMembrToAllMem( self ):
		"""
		"""
		for member in self.members.values():
			if member.baseMailBox and member.baseMailBox.client:
				member.baseMailBox.client.OnSureSignUpBHZBMember( list(self.bhzbSignUpMembers.values()) )

	def declareBHZBPoint( self, pointIndex,groupID,playerMB ):
		"""
		宣战帮会争霸据点
		"""
		if groupID not in self.bhzbSignUpMembers:
			return
		if self.bhzbSignUpMembers[groupID].getIsActive():
			return
		playerDBIDs = [ int(i) for i in self.bhzbSignUpMembers[groupID].getAllMemberDBIDs() if i ]
		if not len(playerDBIDs):
			return
		isAllMemberOffLine = True
		for playerDBID in playerDBIDs:
			member = self.getMemberByDBID( playerDBID )
			if member == None:
				continue
			if member.baseMailBox != None:
				isAllMemberOffLine = False
				break
		if isAllMemberOffLine:
			playerMB.statusMessage( csstatus.BHZB_TEAM_ALL_MEMBER_OFF_LINE,"" ) 
			return
		allMemLocalSpaceScriptID = []
		for playerDBID in playerDBIDs:
			member = self.getMemberByDBID( playerDBID )
			if member == None:
				continue
			allMemLocalSpaceScriptID.append( member.localSpace )
		#self.setbhzbSignUpMembersIsActive( groupID,True, pointIndex )
		KBEngine.globalData["BHZBManager"].declareBHZBPoint( self.databaseID,self.camp,pointIndex,playerMB, playerDBIDs,self.tongName,self.tongName, groupID, self, allMemLocalSpaceScriptID )

	def onBHZBMemberOffLine( self, playerDBID ):
		"""
		帮会争霸成员下线
		"""
		if not KBEngine.globalData.get("BHZBStart",0):
			return

		dstGroupID = 0
		pointIndex = 0
		for groupID, bhzbSignUpMember in self.bhzbSignUpMembers.items():
			playerDBIDs = [ int(i) for i in bhzbSignUpMember.getAllMemberDBIDs() if i ]
			if bhzbSignUpMember.getIsActive() and playerDBID in playerDBIDs:
				dstGroupID = groupID
				pointIndex = bhzbSignUpMember.pointIndex
				break
		if pointIndex > 0:
			KBEngine.globalData["BHZBManager"].onBHZBMemberOffLine( self.databaseID, self.camp, pointIndex, dstGroupID, self )

	def callBHZBTeamToAttack( self, groupID, pointName ):
		"""
		进攻某据点
		"""
		self.statusMsgToBHZBTeamMember( groupID, pointName, csstatus.BHZB_TONG_CALL_TO_ATTACK_POINT )

	def callBHZBTeamToProtect( self, groupID, pointName ):
		"""
		防守某据点
		"""
		self.statusMsgToBHZBTeamMember( groupID, pointName, csstatus.BHZB_TONG_CALL_TO_PROTECT_POINT )

	def statusMsgToBHZBTeamMember( self, groupID, pointName, statusID ):
		"""
		"""
		if groupID not in self.bhzbSignUpMembers:
			return
		playerDBIDs = [ int(i) for i in self.bhzbSignUpMembers[groupID].getAllMemberDBIDs() if i ]
		for playerDBID in playerDBIDs:
			member = self.getMemberByDBID( playerDBID )
			if member == None:
				continue
			if member.baseMailBox:
				member.baseMailBox.statusMessage( statusID, pointName )

	def cancelDeclareBHZBPoint( self, pointIndex ):
		"""
		取消宣战某个据点
		"""
		dstID = 0
		for groupID, bhzbSignUpMember in self.bhzbSignUpMembers.items():
			if bhzbSignUpMember.getIsActive() and bhzbSignUpMember.pointIndex == pointIndex:
				dstID = groupID
				break

		#self.setbhzbSignUpMembersIsActive( dstID,False, 0 )
		KBEngine.globalData["BHZBManager"].cancelDeclareBHZBPoint( self.databaseID ,self.camp,pointIndex, dstID,self )

	def joinBHZBPointFight( self, pointIndex, groupID, playerMB ):
		"""
		参与据点争夺战斗
		"""
		if groupID not in self.bhzbSignUpMembers:
			return
		if self.bhzbSignUpMembers[groupID].getIsActive():
			KBEDebug.ERROR_MSG("joinBHZBPointFight  teamID = %i is busy"%groupID)
			return
		playerDBIDs = [ int(i) for i in self.bhzbSignUpMembers[groupID].getAllMemberDBIDs() if i ]
		if not len(playerDBIDs):
			return
		#self.setbhzbSignUpMembersIsActive( groupID,True, pointIndex )
		KBEngine.globalData["BHZBManager"].joinBHZBPointFight( self.databaseID, self.camp, pointIndex, playerMB, playerDBIDs,groupID,self )

	def cancelJoinBHZBPointFight( self, pointIndex ):
		"""
		撤销回防
		"""
		KBEngine.globalData["BHZBManager"].cancelJoinBHZBPointFight( self.databaseID, self.camp, pointIndex, self )

	def defenseBHZBPoint( self, pointIndex,groupID,playerMB ):
		"""
		布防帮会争霸据点
		"""
		if groupID not in self.bhzbSignUpMembers:
			return
		if self.bhzbSignUpMembers[groupID].getIsActive():
			return
		playerDBIDs = [ int(i) for i in self.bhzbSignUpMembers[groupID].getAllMemberDBIDs() if i ]
		if not len( playerDBIDs ):
			return
		#self.setbhzbSignUpMembersIsActive( groupID,True, pointIndex )
		KBEngine.globalData["BHZBManager"].defenseBHZBPoint( self.databaseID, self.camp, pointIndex, playerMB, groupID,playerDBIDs, self )

	def setbhzbSignUpMembersIsActive( self, groupID,isActive, pointIndex ):
		"""
		设置帮会争霸队伍是否进入争夺地图
		"""
		if groupID not in self.bhzbSignUpMembers:
			return
		playerDBIDs = [ int(i) for i in self.bhzbSignUpMembers[groupID].getAllMemberDBIDs() if i ]
		if not len( playerDBIDs ):
			return
		self.bhzbSignUpMembers[groupID].setIsActive(isActive,pointIndex)
		for member in self.members.values():
			if member.baseMailBox and member.baseMailBox.client:
				member.baseMailBox.client.SetbhzbSignUpMembersIsActive( groupID, isActive, pointIndex )

	def onBHZBPointWarEnd( self, pointIndex ):
		"""
		帮会争霸据点地图争夺结束
		"""
		dstID = 0
		for groupID, bhzbSignUpMember in self.bhzbSignUpMembers.items():
			if bhzbSignUpMember.getIsActive() and bhzbSignUpMember.pointIndex == pointIndex:
				dstID = groupID
				break
		self.setbhzbSignUpMembersIsActive( dstID, False, 0 )

	def checkIsLoginToBHZBPoint( self, roleMB, tongDBID, spaceScriptID,playerDBID ):
		"""
		检查是否重新进入帮会争霸据点
		"""
		dstGroupID = 0
		dstPointNumber = 0
		for groupID, bhzbSignUpMember in self.bhzbSignUpMembers.items():
			playerDBIDs = [ int(i) for i in bhzbSignUpMember.getAllMemberDBIDs() if i ]
			if bhzbSignUpMember.getIsActive() and playerDBID in playerDBIDs:
				dstGroupID = groupID
				dstPointNumber = bhzbSignUpMember.pointIndex
				break
		if dstPointNumber > 0:
			KBEngine.globalData["BHZBManager"].checkIsLoginToBHZBPoint( roleMB, tongDBID, spaceScriptID,playerDBID, dstGroupID, dstPointNumber )

	def clearTongSignMemberData( self ):
		"""
		"""
		for groupID, bhzbSignUpMember in self.bhzbSignUpMembers.items():
			self.setbhzbSignUpMembersIsActive( groupID, False, 0 )

	def bhzbTeamMemberLoginOut( self, camp, tongDBID, playerDBID ):
		"""
		帮会争霸组队成员下线
		"""
		member = self.getMemberByDBID( playerDBID )
		if not member:
			return
		if member.localSpace not in csconst.BHZB_HOME_BARRACKS_SPACE or member.localSpace not in g_BHZBPointDataLoader.getAllBHZBPVEAndPVPSpace():
			return
		KBEngine.globalData["BHZBManager"].bhzbTeamMemberLoginOut( camp, tongDBID, playerDBID )

	def signUPBHZB( self, tongLevel, costMoney, playerMB, playerDBID, needTongMemAmount):
		"""
		报名帮会争霸
		"""
		member = self.getMemberByDBID( playerDBID )
		if not member:
			return
		if member.title not in [csdefine.TONG_TITLE_1,csdefine.TONG_TITLE_3]:
			playerMB.statusMessage( csstatus.BHZB_TONG_SIGN_UP_FORBID_TITLE, "" )
			return
		if not KBEngine.globalData.get("BHZBSignUpStart",0):
			playerMB.statusMessage( csstatus.BHZB_TONG_SIGN_UP_FORBID_TIME,"" )
			return
		KBEngine.globalData["BHZBManager"].signUPBHZB( self.camp,self.databaseID, self.tongName,self.level, costMoney,self, playerMB, list(self.bhzbSignUpMembers.values()),playerDBID,needTongMemAmount,tongLevel,self.money,self.getActivity(),len( self.members ))

	def signUpBHZBSuccess( self, memberDBIDList, signCostMoney ):
		"""
		报名帮会争霸成功
		"""
		self.subTongMoney( signCostMoney )

	def joinBHZBWarFail( self ):
		"""
		参与帮会争霸帮会失败 反还资金
		"""
		self.addTongMoney( csconst.BHZB_SIGN_UP_COST_MONEY, csdefine.TONG_MONEY_ADD_REASON_JOIN_BHZB_FAIL )
		for member in self.members.values():
			g_mailContentDataLoader.sendMail( csconst.BHZB_NOT_TO_JOIN_TONG_MAIL_ID, member.name )

	def gmSignUpBHZB( self, info, playerMB, playerDBID ):
		"""
		GM 测试报名帮会争霸
		"""
		KBEngine.globalData["BHZBManager"].signUPBHZB( self.camp,self.databaseID, self.tongName,self.level, 0, self, playerMB, [info],playerDBID)

	def sureBHZBTongSendMail( self ):
		"""
		确认参与的帮会发送邮件
		"""
		for member in self.members.values():
			g_mailContentDataLoader.sendMail( csconst.BHZB_SIGN_UP_SUCCESS_MAIL_ID, member.name )

	def sureBHZBTongMemberSendMail( self, tongMemberDBIDs ):
		"""
		给确认帮会参与人员发送邮件
		"""
		for dbid in tongMemberDBIDs:
			if dbid in self.members:
				g_mailContentDataLoader.sendMail( csconst.BHZB_SIGN_UP_MEB_MAIL_ID,self.members[dbid].name )

	def sendBHZBRewardToMembers( self, memberDBIDs,rankRewardGifts, rankRewardTongMoney,rankRewardContributionGift, rank ):
		"""
		发送帮会争霸奖励给成员
		"""
		rewardGifts = []
		if len( rankRewardGifts ) >= len(memberDBIDs):
			rewardGifts = random.sample(list(rankRewardGifts), len(memberDBIDs))
		for dbid in memberDBIDs:
			if dbid not in self.members:
				continue
			index = memberDBIDs.index(dbid)
			if len(rewardGifts) > index:
				g_mailContentDataLoader.sendMail( rewardGifts[index], self.members[dbid].name )
			g_mailContentDataLoader.sendMail( rankRewardContributionGift,self.members[dbid].name)
		self.addTongMoney( int(rankRewardTongMoney) )
		
		#创建帮会争霸胜利宝箱
		if self.spaceMB:
			if rank == 0:
				rewardKey = csdefine.TONG_DROPBOX_BHZBFIRST
			elif rank == 1:
				rewardKey = csdefine.TONG_DROPBOX_BHZBSECOND
			elif rank == 2:
				rewardKey = csdefine.TONG_DROPBOX_BHZBTHIRD
			else:
				return
			
			self.spaceMB.cell.createBHDropBox( self.databaseID, self.allocation, memberDBIDs, rewardKey, self.level )
			voice = Const.BHZB_VOICE_DICT.get(rank+1, {}).get(self.allocation, None)
			if voice: self.addTimerCallBack( 10, "onSendBHZBVoiceMsg", (voice,) )
	
	def onSendBHZBVoiceMsg(self, voiceID):
		"""
		"""
		if self.isDestroyed:
			return
		
		for member in self.members.values():
			if member.baseMailBox and member.baseMailBox.client:
				member.baseMailBox.client.ShowMessagePlaySound(voiceID)
				member.baseMailBox.client.ShowMessagePlaySound(Const.BHZB_DROPBOX_OPEN_VOICE)

	def sendTongLeaderReward( self, leaderReward, rank ):
		"""
		发送奖励给帮主
		"""
		if self.camp == csdefine.CAMP_TAOSIM:
			campName = cschannel_msgs.CAMP_TAOSIM
		else:
			campName = cschannel_msgs.CAMP_DEMON
		if rank == 2:
			msgArg = "{0}|{1}".format( campName, self.tongName )
			KST.g_baseAppEntity.globalWold(csstatus.BHZB_TONG_SUCCESS_THIRD,msgArg)
			return
		leader = self.members[self.leaderDBID]
		g_mailContentDataLoader.sendMail( leaderReward, leader.name )
		messageArg = "{0}|{1}|{2}|{3}".format( campName,self.tongName,leader.name,campName)
		if rank == 0:
			KST.g_baseAppEntity.globalWold(csstatus.BHZB_TONG_SUCCESS_FIRST,messageArg)
		elif rank == 1:
			KST.g_baseAppEntity.globalWold(csstatus.BHZB_TONG_SUCCESS_SECOND,messageArg)

	def onActivityChange( self, oldValue ):
		TongUpgradeInterface.TongUpgradeInterface.onActivityChange( self, oldValue )
		if KBEngine.globalData.get("BHZBSignUpStart",0):
			KBEngine.globalData["BHZBManager"].updateWarTongActivity( self.camp,self.databaseID, self.getActivity() )
			
	def clearAllTongSignMemberData( self ):
		"""
		清除帮会争霸成员数据
		"""
		self.bhzbSignUpMembers.clear()
		for member in self.members.values():
			if member.baseMailBox and member.baseMailBox.client:
				member.baseMailBox.client.ClearAllTongSignMemberData()

	def sendToJoinCampWarMail( self, month, day, side ):
		"""
		给所有帮会成员发送获得参加阵营争霸的资格
		"""
		for member in self.members.values():
			g_mailContentDataLoader.sendMailByContentArgs( csconst.BHZB_TO_JOIN_CAMP_WAR_MAIL_ID, member.name,( month, day,  cschannel_msgs.BELONG_SIDE.get(side,"") ) )

	#---------------------------帮会掠夺战---------------------------
	def onTongPlunderSignUpStart(self):
		"""
		活动报名开始，清除数据
		"""
		self.tongPlunderData.resetData()

	def onTongPlunderSignUpSuccess(self, belongSide, targetTongName, startTime):
		"""
		报名参与帮会掠夺战成功
		"""
		lockMoney = TongLoader.getLockMoney(self.level)
		self.tongPlunderData.onSignUpSuccess(belongSide,  lockMoney)

		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			self.tongPlunderAttackNotice(targetTongName, startTime)
		elif belongSide == csdefine.BELONG_SIDE_PROTECT:
			self.tongPlunderProtectNotice(targetTongName, startTime)

	def onTongPlunderStart(self):
		"""
		define method

		帮会掠夺战开始
		"""
		if self.tongPlunderData.hasSignUpActive():
			belongSide = self.tongPlunderData.getBelongSide()
			members = self.tongPlunderData.getMembers()
			KBEngine.globalData["TongPlunderManager"].onSureMember(belongSide, self.databaseID, members)

	def onTongPlunderEnd(self):
		"""
		define method

		帮会掠夺战结束
		"""
		self.tongPlunderData.resetSignUpData()

		for member in self.members.values():
			if member.getClient():
				member.baseMailBox.client.OnPlunderMemberChange([])

	def tongPlunderAttackNotice(self, targetTongName, startTime):
		"""
		进攻方活动公告
		"""
		year,month,day,hour,minute = time.localtime(startTime)[:5]
		message = targetTongName + "|" + str(year) + "|" + str(month) + "|" + str(day) + "|" + str(hour) + ":"
		if minute >= 10:
			message += str(minute) 
		else:
			message = message + "0" + str(minute) 
		for member in self.members.values():
			if member.getClient(): 
				member.baseMailBox.client.statusMessage(csstatus.TONG_PLUNDER_CHALLENGE_NOTIFY, message)

		leader = self.members[self.leaderDBID]
		if leader.getClient(): #目前只有帮主才能发起掠夺
			leader.baseMailBox.client.statusMessage(csstatus.TONG_PLUNDER_CHALLENGE_NOTIFY_TO_LEADER, targetTongName)

	def tongPlunderProtectNotice(self, targetTongName, startTime):
		"""
		防守方活动公告
		"""
		year,month,day,hour,minute = time.localtime(startTime)[:5]
		message = targetTongName + "|" + str(year) + "|" + str(month) + "|" + str(day) + "|" + str(hour) + ":"
		if minute >= 10:
			message += str(minute) 
		else:
			message = message + "0" + str(minute) 
		for member in self.members.values():
			if member.getClient():
				member.baseMailBox.client.statusMessage(csstatus.TONG_PLUNDER_BE_PLUNDER_CHALLENGE_NOTIFY, message)

	def onTongPlunderSendMail(self):
		"""
		帮会掠夺战开始前给参与人员发邮件
		"""
		if self.tongPlunderData.hasSignUpActive():
			for DBID in self.tongPlunderData.getMembers():
				if DBID in self.members:
					member = self.members[DBID]
					g_mailContentDataLoader.sendMail(csconst.TONG_PLUNDER_START_MAIL_ID, member.name)


	def lockTongShop(self):
		"""
		define method

		锁定帮会商店
		"""
		self.tongPlunderData.setLockTongShop(True)
		for member in self.members.values():
			if member.baseMailBox:
				member.baseMailBox.cell.lockTongShop()

	def unLockTongShop(self):
		"""
		define method

		解锁帮会商店
		"""
		self.tongPlunderData.setLockTongShop(False)
		for member in self.members.values():
			if member.baseMailBox:
				member.baseMailBox.cell.unLockTongShop()

	def tongPlunderShopSellStart(self, endTime):
		"""
		define method

		帮会掠夺战所获商品售卖开始
		"""
		if self.tongPlunderData.isVictory():
			self.tongPlunderData.setShopDataSell(True)
			self.tongPlunderData.setSellEndTime(endTime)
			endTimeStr = str(self.tongPlunderData.getSellEndTime() - time.time())
			for member in self.members.values():
				if member.baseMailBox:
					member.baseMailBox.cell.onTongPlunderShopSellStart(self.tongPlunderData.getShopData(), endTimeStr)

	def tongPlunderShopSellEnd(self):
		"""
		define method

		帮会掠夺战所获商品售卖结束
		"""
		if self.tongPlunderData.isVictory():
			self.tongPlunderData.resetData() #这个时候再清除数据
			for member in self.members.values():
				if member.baseMailBox:
					member.baseMailBox.cell.onTongPlunderShopSellEnd()

	def tongPlunderVictory(self, spaceMB, shopData, giftID, money):
		"""
		胜利
		"""
		self.tongPlunderData.onActiveVictory(shopData)
		memberIDList = [member for member in self.tongPlunderData.getMembers() if member in self.members]
		extraData = {}
		if len(memberIDList) > 0:
			extraData = {"money": math.ceil(money / len(memberIDList))}
		if giftID != "":
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(int(giftID), 1, {})
			extraData["itemList"] = [itemInst]

		self.sendTongPlunderRewardMail(csconst.TONG_PLUNDER_REWARD_MAIL_ID, extraData)
		spaceMB.cell.onTongPlunderVictory(self.tongPlunderData.getShopData())
		
		#创建帮会掠夺胜利宝箱
		if self.spaceMB:
			rewardKey = csdefine.TONG_DROPBOX_BHLD
			memberDBIDs = self.tongPlunderData.getMembers()
			self.spaceMB.cell.createBHDropBox( self.databaseID, self.allocation, memberDBIDs, rewardKey, self.level)

		"""
		#由于是一半物品直接发给玩家，一半放到帮会商店的掠夺战分页出售，所以用同一份数据
		memberIDList = [member for member in self.tongPlunderData.getMembers() if member in self.members]

		sender = g_mailContentDataLoader.getMailDataSenderNameByMailID(csconst.TONG_PLUNDER_REWARD_MAIL_ID)
		title = g_mailContentDataLoader.getMailDataTitleByMailID(csconst.TONG_PLUNDER_REWARD_MAIL_ID)
		content = g_mailContentDataLoader.getMailDataContentByMailID(csconst.TONG_PLUNDER_REWARD_MAIL_ID)

		money = math.ceil(money / len(memberIDList))
		itemList = []
		for data in shopData:
			itemID = int(data["itemID"])
			amount = math.ceil(data["amount"] / len(memberIDList))
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount, {})
			itemList.append(itemInst)
			if len(itemList) == 4: #一封邮件最多4个物品
				for ID in memberIDList:
					KBEngine.globalData["MailManager"].send(None, self.members[ID].name, csdefine.MAIL_SENDER_TYPE_SYS, sender, title, content, money, itemList, 0, 0)				
				itemList .clear()
				money = 0 #只有第一封邮件发金钱
		if len(itemList) > 0:
			for ID in memberIDList:
				KBEngine.globalData["MailManager"].send(None, self.members[ID].name, csdefine.MAIL_SENDER_TYPE_SYS, sender, title, content, money, itemList, 0, 0)
		"""

	def tongPlunderFailed(self, giftID):
		"""
		失败
		"""
		money = self.tongPlunderData.getLockMoney()
		self.tongPlunderData.onActiveFailed()
		self.subTongMoney(money)

		if giftID:
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(int(giftID), 1, {})
			extraData = {"itemList": [itemInst]}
			self.sendTongPlunderRewardMail(csconst.TONG_PLUNDER_REWARD_MAIL_ID, extraData)

	def sendTongPlunderRewardMail(self, mailID, extraData = {}):
		"""
		发送奖励邮件
		"""
		memberIDList = [member for member in self.tongPlunderData.getMembers() if member in self.members]
		for DBID in memberIDList:
			member = self.members[DBID]					
			g_mailContentDataLoader.sendMail(mailID, member.name, extraData)

	def requestBuyTongPlunderShopItem(self, playerDBID, id, itemID, amount):
		"""
		define method
		请求购买物品
		"""
		if playerDBID not in self.members:
			return
		if self.tongPlunderData.checkShopData(id, itemID, amount):
			member = self.members[playerDBID]
			if member.baseMailBox:
				member.baseMailBox.cell.requestBuyTongPlunderShopItemCB(id, itemID, amount)

	def onTongPlunderShopSell(self, id, itemID, amount, cost):
		"""
		define method

		商品出售
		"""
		self.addTongMoney(cost)
		self.tongPlunderData.tongPlunderShopSell(self, id, itemID, amount)

	def onTongPlunderShopDataChange(self, id, itemID, amount):
		"""
		"""
		for member in self.members.values():
			if member.baseMailBox:
				member.baseMailBox.client.OnTongPlunderShopItemBuySuccess(id, itemID, amount)

	def checkMinActivity(self):
		"""
		检查帮会最低活跃度
		"""
		activity = TongLoader.getMinActivity(self.level)
		return self.activity > activity

	def checkMinTongMoney(self):
		"""
		检查帮会最低资金
		"""
		#暂时还没有支持帮会最低资金功能
		return True

	def checkSignUpStatus(self):
		"""
		检查是否已参与该活动
		"""
		return self.tongPlunderData.hasSignUpActive()

	def plunderAddMember(self, playerMB, playerDBID):
		"""
		define method

		添加参与掠夺战成员
		"""
		if playerDBID not in self.members:
			KBEDebug.ERROR_MSG("player dbid(%s) is not in tong(%s)" % (playerDBID, self.databaseID))
			return

		if not self.tongPlunderData.hasSignUpActive():
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_CAN_NOT_ADD_MEMBER, "")
			return

		#人数已满
		if len(self.tongPlunderData.getMembers()) >= Const.TONG_PLUNDER_JOIN_MEMBER_NUM:
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_MEMBER_NUM_IS_FULL, "")
			return
			
		member = self.members[playerDBID]
		if playerDBID in self.tongPlunderData.getMembers():
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_MEMBER_ALREADY_ADD, member.name)
			return
			
		self.tongPlunderData.addMember(playerDBID)
		
		playerMB.client.statusMessage(csstatus.TONG_PLUNDER_ADD_MEMBER_SUCCESS, member.name)
		
		memberIDList = [str(DBID) for DBID in self.tongPlunderData.getMembers()]
		for member in self.members.values():
			if member.getClient():
				member.baseMailBox.client.OnPlunderMemberChange(memberIDList)

	def plunderRemoveMember(self, playerMB, playerDBID):
		"""
		define method
		移除参与掠夺战成员
		"""
		if playerDBID not in self.members:
			KBEDebug.ERROR_MSG("player dbid(%s) is not in tong(%s)" % (playerDBID, self.databaseID))
			return

		if not self.tongPlunderData.hasSignUpActive():
			return

		self.tongPlunderData.removeMember(playerDBID)

		member = self.members[playerDBID]
		playerMB.client.statusMessage(csstatus.TONG_PLUNDER_REMOVE_MEMBER_SUCCESS, member.name)
		
		memberIDList = [str(DBID) for DBID in self.tongPlunderData.getMembers()]
		for member in self.members.values():
			if member.getClient():
				member.baseMailBox.client.OnPlunderMemberChange(memberIDList)
				
	def setTongAllocation( self, playerDBID, allocation ):
		"""
		define method
		设置帮会争霸分配方式
		"""
		if allocation == self.allocation:
			return
			
		member = self.getMemberByDBID( playerDBID )
		if not member:
			return
		
		if member.title not in [csdefine.TONG_TITLE_1, csdefine.TONG_TITLE_3]:
			return
		
		if allocation != csdefine.TONG_PICKUP_TYPE_FREEDOM and allocation != csdefine.TONG_PICKUP_TYPE_LEADER \
			and allocation != csdefine.TONG_PICKUP_TYPE_RALLDOM and allocation != csdefine.TONG_PICKUP_TYPE_AUCTION :
			return
			
		self.allocation = allocation
		for member in self.members.values():
			if member.baseMailBox:
				member.baseMailBox.cell.OnUpdateTongAllocation(self.allocation)
				
	def setTongBHLDAllocation( self, playerDBID, allocation ):
		"""
		define method
		设置帮会掠夺分配方式
		"""
		if allocation == self.BHLDAllocation:
			return

		member = self.getMemberByDBID( playerDBID )
		if not member:
			return
		
		if member.title not in [csdefine.TONG_TITLE_1, csdefine.TONG_TITLE_3]:
			return
		
		if allocation != csdefine.TONG_PICKUP_TYPE_FREEDOM and allocation != csdefine.TONG_PICKUP_TYPE_LEADER \
			and allocation != csdefine.TONG_PICKUP_TYPE_RALLDOM and allocation != csdefine.TONG_PICKUP_TYPE_AUCTION :
			return
			
		self.BHLDAllocation = allocation
		for member in self.members.values():
			if member.baseMailBox:
				member.baseMailBox.cell.OnUpdateTongBHLDAllocation(self.BHLDAllocation)
		
	def gmAddMember( self, amount, playerCell ):
		"""
		GM增加帮会成员
		"""
		for i in range(amount):
			if len( self.members ) >= self.getMaxMember():
				return
			
			uid = KBEngine.genUUID64()
			name = self.tongName + "_" + str(uid)
			self.join( None, uid, name, 20, 1, csdefine.TONG_TITLE_9, "" )

	def gmSetSafeTime( self, time ):
		"""
		GM设置帮会安全期剩余天数
		"""
		self.safeTime = time
		self.addRecord( csdefine.TONG_EVENT_SAFE_TIME_NOTICE, self.safeTime )

	def gmSetProtectDay( self, day ):
		"""
		GM设置帮会保护期剩余天数
		"""
		self.protectDay = day
		activity = TongLoader.getMinActivity( self.level )
		self.addRecord( csdefine.TONG_EVENT_DOWN_GRADE_NOTICE, self.protectDay, activity, self.level - 1 )
		
	def gmCreateTongDropBox( self ):
		"""
		GM创建帮会宝箱
		"""
		memberDBIDList = []
		for member in self.members.values():
			memberDBIDList.append(member.DBID)
		
		if self.spaceMB:
			self.spaceMB.cell.createBHDropBox(self.databaseID, self.allocation, memberDBIDList, csdefine.TONG_DROPBOX_BHLD, self.level)
