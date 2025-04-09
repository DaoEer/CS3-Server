# -*- coding: utf-8 -*-



import KBEDebug
import KBEngine
import csstatus

class RoleActivityInterface:
	"""
	玩家活动接口
	"""
	def __init__( self ):
		self.isMatchCampYXLM = False
		self.isMatchCampLMZC = False
		self.isMatchCampFrozenFight = False
		self.isMatchCampSGMZ = False
		self.isMatchCampFHLT = False
		self.isMatchCampRandomFit = False
		self.isMatchBattleActivity = False
		#考虑到异步
		self.isCampYXLMToCreateTeam = False #是否需要创建队伍      
		self.isCampYXLMToLeaveTeam = False  #队员是否需要离开队伍
		self.campYXLMTeamInfo = None        #需要保存（队长ID,teamMailBox）
		self.isCampYXLMToJoinTeam = False	#队员是否加入队伍

		self.isBHZBToCreateTeam = False
		self.isBHZBToLeaveTeam = False
		self.BHZBTeamInfo = None
		self.isBHZBToJoinTeam = False
		self.isBHZBChangeCaptain = False

		self.isGCZToCreateTeam = False
		self.isGCZToLeaveTeam = False
		self.GCZTeamInfo = None
		self.isGCZToJoinTeam = False
		self.isMatchGCZ = False

	def onLoseCell( self ):
		"""
		cell死亡
		"""
		if self.isMatchCampYXLM:
			KBEngine.globalData["CampYXLMCopyMgr"].yingXiong_onPlayerLoginOff( self, self.getName() )
		if self.isMatchCampLMZC:
			KBEngine.globalData["CampActivityLingMaiMgr"].lingmai_onPlayerLoginOff( self, self.camp, self.level )
		if self.isMatchCampFrozenFight:
			KBEngine.globalData["CampActivityFrozenFightMgr"].frozenFight_onPlayerLoginOff( self, self.camp, self.level )
		if self.isMatchCampSGMZ:
			KBEngine.globalData["CampSGMZCopyMgr"].miZhen_onPlayerLoginOff( self, self.getName() )
		if self.isMatchCampFHLT:
			KBEngine.globalData["CampActivityLingMaiMgr"].fhlt_onPlayerLoginOff( self, self.camp, self.level )
		if self.isMatchGCZ:
			KBEngine.globalData["GCZManager"].gcz_memberLoginOff( self, self.getName() )
		if self.isMatchBattleActivity:
			KBEngine.globalData["BattleActivityMgr"].onPlayerLoginOff(self.base)
		
#-------------------------英雄联盟-------------------------
	def campYXLMOnJoin( self ):
		"""
		参与英雄联盟排队
		"""
		self.isMatchCampYXLM = True

	def campYXLMOnQuit( self ):
		"""
		退出英雄联盟排队
		"""
		self.isMatchCampYXLM = False

	def campYXLMonAffirm( self, result ):
		"""
		Exposed method
		点击确认框
		result 代表是否点击了确认
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["CampYXLMCopyMgr"].yingXiong_onAffirm(self,self.getName(),result)
		
	def campYXLMCancelSignUp( self ):
		"""
		Exposed method
		玩家取消报名
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["CampYXLMCopyMgr"].yingXiong_cancelSignUp( self )

	def campYXLMCreateTeam( self ):
		"""
		创建一个队伍
		"""
		if self.isInTeam():
			self.isCampYXLMToCreateTeam = True
			if self.isTeamCaptain():
				self.disbandTeamFB()
			else:
				self.leaveTeamFB( self.id )
		else:
			self.createSelfTeamLocally()
			KBEngine.globalData["CampYXLMCopyMgr"].yingXiong_OnCreateTeam( self, self.teamMailBox )

	def campYXLMOnLevelTeam( self ):
		"""
		队员离开队伍回调
		"""
		if self.isCampYXLMToCreateTeam:
			self.createSelfTeamLocally()
			KBEngine.globalData["CampYXLMCopyMgr"].yingXiong_OnCreateTeam( self, self.teamMailBox )
			self.isCampYXLMToCreateTeam = False

		if self.isCampYXLMToLeaveTeam:
			self.isCampYXLMToJoinTeam = True
			self.joinTeamNotify( self.campYXLMTeamInfo[0], False, self.campYXLMTeamInfo[1], self.allocation, self.quality )
			self.isCampYXLMToLeaveTeam = False
			self.campYXLMTeamInfo = None

	def campYXLMJoinTeam( self, captainID, teamMailBox ):
		"""
		define method
		加入队伍
		"""
		if self.isInTeam():
			self.isCampYXLMToLeaveTeam = True
			self.campYXLMTeamInfo = ( teamMailBox,captainID )
			if self.isTeamCaptain():
				self.disbandTeamFB()
			else:
				self.leaveTeamFB( self.id )
		else:
			self.isCampYXLMToJoinTeam = True
			self.joinTeamNotify( teamMailBox, False, captainID, self.allocation, self.quality )

	def onCampYXLMMemberJoin( self):
		"""
		"""
		if self.isCampYXLMToJoinTeam:
			self.isCampYXLMToJoinTeam = False
			KBEngine.globalData["CampYXLMCopyMgr"].yingXiong_onMemberJoinTeam( self )

#---------------------------灵脉战场 JIRA:CST-4054---------------------------------------------
	def signInLingMai( self ):
		"""
		define method
		报名参加灵脉战场
		"""
		if KBEngine.globalData.get( "LingMaiBattle", 0 ):				# 如果在活动时间
			if not self.isMatchCampLMZC:
				self.isMatchCampLMZC = True
				KBEngine.globalData["CampActivityLingMaiMgr"].signIn( self, self.camp, self.level )
			else:
				self.statusMessage( csstatus.ACTIVITY_CAMP_CANNOT_SIGNIN_AFTER_MATCHING , "" )
			
	def cancelMatchLingMai( self ):
		"""
		Exposed method
		取消匹配灵脉战场
		"""
		if not self.validateClientCall():
			return
		if self.isMatchCampLMZC:
			self.isMatchCampLMZC = False
			KBEngine.globalData["CampActivityLingMaiMgr"].cancelMatching( self, self.camp, self.level )
			
	def onLingMaiActivityEnd( self ):
		"""
		define method
		灵脉战场结束
		"""
		self.isMatchCampLMZC = False
		self.client.CLIENT_OnLingMaiActivityEnd()
			
	def beginEnterLingMai( self, key ):
		"""
		Exposed method
		立即进入战场
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["CampActivityLingMaiMgr"].beginEnterLingMai( self, key )
		self.telportLMZCActivity( key )
			
	def telportLMZCActivity( self, key ):
		"""
		define method
		传送进入战场
		"""
		if self.isMatchCampLMZC:
			self.isMatchCampLMZC = False
			self.cell.telportLMZCActivity( key )


#---------------------------------------冰雪之战（CST-4056）--------------------------
	def signInFrozenFight( self ):
		"""
		define method
		报名参加冰雪之战
		"""
		if KBEngine.globalData.get( "FrozenFight", 0 ):				# 如果在活动时间
			if not self.isMatchCampFrozenFight:
				self.isMatchCampFrozenFight = True
				KBEngine.globalData["CampActivityFrozenFightMgr"].signIn( self, self.camp, self.level )
			else:
				self.statusMessage( csstatus.ACTIVITY_CAMP_CANNOT_SIGNIN_AFTER_MATCHING , "" )
			
	def cancelMatchFrozenFight( self ):
		"""
		Exposed method
		取消匹配冰雪之战
		"""
		if not self.validateClientCall():
			return
		if self.isMatchCampFrozenFight:
			self.isMatchCampFrozenFight = False
			KBEngine.globalData["CampActivityFrozenFightMgr"].cancelMatching( self, self.camp, self.level )
			
	def onFrozenFightActivityEnd( self ):
		"""
		define method
		冰雪之战结束
		"""
		self.isMatchCampFrozenFight = False
		self.client.CLIENT_OnFrozenFightActivityEnd()
			
	def beginEnterFrozenFight( self, key ):
		"""
		Exposed method
		立即进入战场
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["CampActivityFrozenFightMgr"].beginEnterFrozenFight( self, key )
		self.telportFrozenFightActivity( key )
			
	def telportFrozenFightActivity( self, key ):
		"""
		define method
		传送进入战场
		"""
		if self.isMatchCampFrozenFight:
			self.isMatchCampFrozenFight = False
			self.cell.telportFrozenFightActivity( key )

#-------------------------上古密阵-------------------------
	def campSGMZOnJoin( self ):
		"""
		参与上古密阵排队
		"""
		self.isMatchCampSGMZ = True

	def campSGMZOnQuit( self ):
		"""
		退出上古密阵排队
		"""
		self.isMatchCampSGMZ = False

	def campSGMZCancelSignUp( self ):
		"""
		Exposed method
		玩家取消报名
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["CampSGMZCopyMgr"].miZhen_cancelSignUp( self )

	def campSGMZOnAffirm( self, result ):
		"""
		Exposed method
		点击确认框
		result 代表是否点击了确认
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["CampSGMZCopyMgr"].miZhen_onAffirm( self, self.getName(), result )

#---------------------------烽火连天---------------------------------------------
	def signUpFHLT( self ):
		"""
		define method
		报名参加烽火连天
		"""
		if KBEngine.globalData.get( "CampFHLTBattle", 0 ):				# 如果在活动时间
			if not self.isMatchCampFHLT:
				self.isMatchCampFHLT = True
				KBEngine.globalData["CampFHLTCopyMgr"].signUp( self, self.camp, self.level )
			else:
				self.statusMessage( csstatus.ACTIVITY_CAMP_FHLT_SIGNIN_AFTER_MATCHING , "" )
			
	def cancelMatchFHLT( self ):
		"""
		Exposed method
		取消匹配烽火连天
		"""
		if not self.validateClientCall():
			return
		if self.isMatchCampFHLT:
			self.isMatchCampFHLT = False
			KBEngine.globalData["CampFHLTCopyMgr"].cancelMatching( self, self.camp, self.level )
			
	def onFHLTActivityEnd( self ):
		"""
		define method
		烽火连天结束
		"""
		self.isMatchCampLMZC = False
		self.client.OnFHLTActivityEnd()
			
	def beginEnterFHLT( self, key ):
		"""
		Exposed method
		立即进入烽火连天战场
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["CampActivityLingMaiMgr"].beginEnterFHLT( self, key )
		self.telportFHLTActivity( key )
			
	def telportFHLTActivity( self, key ):
		"""
		define method
		传送进入烽火连天战场
		"""
		if self.isMatchCampLMZC:
			self.isMatchCampLMZC = False
			self.cell.telportFHLTActivity( key )


#----------------------------------------阵营战场随机匹配--------------------------------------------
	def campRandomFitJoin( self ):
		"""
		define method
		进入随机匹配排队
		"""
		self.isMatchCampRandomFit = True
		self.cell.campRandomFitJoin()

	def campRandomFitQuit( self ):
		"""
		define method
		退出随机匹配排队
		"""
		self.isMatchCampRandomFit = False
		self.cell.campRandomFitQuit()

	def campRandomFitInterrupt( self ):
		"""
		Exposed method
		申请终止随机匹配
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["CampActivityRandomFitMgr"].randomFit_cancelSignUp( self )


#----------------------------------------团队竞技匹配--------------------------------------------
	def battleActivitySignUp(self):
		"""
		define method
		进入随机匹配排队
		"""
		self.isMatchBattleActivity = True
		self.cell.battleActivitySignUp()

	def battleActivitySignOut(self):
		"""
		define method
		退出随机匹配排队
		"""
		self.isMatchBattleActivity = False
		self.cell.battleActivitySignOut()

	def battleActivityInterrupt( self ):
		"""
		Exposed method
		申请终止随机匹配
		"""
		if not self.validateClientCall():
			return
		KBEngine.globalData["BattleActivityMgr"].cancelSignUp(self)


#----------------------------------CST-11386 帮会争霸 -------------------------------------
	def onEnterBHZBCreateTeam( self ):
		"""
		进入帮会争霸创建队伍
		"""
		if self.isInTeam():
			self.isBHZBToCreateTeam = True
			if self.isTeamCaptain():
				self.disbandTeamFB()
			else:
				self.teamMailBox.onBHZBLeaveTeam( self.id, self.id )
		else:
			self.createSelfTeamLocally()
			KBEngine.globalData["BHZBManager"].onBHZBCreateTeam( self.getCamp(),self.tongDBID, self.databaseID ,self, self.teamMailBox )

	def bhzbOnLeaveTeam( self ):
		"""
		队员离开队伍回调
		"""
		if self.isBHZBToCreateTeam:
			self.createSelfTeamLocally()
			KBEngine.globalData["BHZBManager"].onBHZBCreateTeam( self.getCamp(),self.tongDBID, self.databaseID ,self, self.teamMailBox )
			self.isBHZBToCreateTeam = False

		if self.isBHZBToLeaveTeam:
			self.isBHZBToJoinTeam = True
			self.joinTeamNotify( self.BHZBTeamInfo[0], False, self.BHZBTeamInfo[1], self.allocation, self.quality )
			self.isBHZBToLeaveTeam = False
			self.BHZBTeamInfo = None

	def onBHZBJoinTeam( self, captainID, teamMailBox ):
		"""
		队员加入队伍
		"""
		if self.isInTeam():
			if teamMailBox.id == self.teamMailBox.id:
				KBEngine.globalData["BHZBManager"].onBHZBMemberJoinTeam( self.getCamp(), self.tongDBID, self.databaseID, self )
				return
			self.isBHZBToLeaveTeam = True
			self.BHZBTeamInfo = ( teamMailBox, captainID )
			if self.isTeamCaptain():
				self.disbandTeamFB()
			else:
				self.teamMailBox.onBHZBLeaveTeam( self.id, self.id )
		else:
			self.isBHZBToJoinTeam = True
			self.joinTeamNotify( teamMailBox, False, captainID, self.allocation, self.quality )

	def onBHZBMemberJoin( self ):
		"""
		"""	
		if self.isBHZBToJoinTeam:
			self.isBHZBToJoinTeam = False
			KBEngine.globalData["BHZBManager"].onBHZBMemberJoinTeam( self.getCamp(), self.tongDBID, self.databaseID, self )

	def onBHZBChangeCaptain( self, teamMailBox ):
		"""
		帮会争霸移交队长
		"""
		if teamMailBox == None:
			return
		self.isBHZBChangeCaptain = True
		teamMailBox.changeCaptain( self.id )

	def onBHZBChangeCaptainCB( self ):
		"""
		帮会争霸移交队长回调
		"""
		if self.isBHZBChangeCaptain:
			self.isBHZBChangeCaptain = False
			KBEngine.globalData["BHZBManager"].onBHZBChangeCaptain( self.getCamp(), self.tongDBID, self.databaseID, self )

	def bhzbTeamMemberLoginOut( self ):
		"""
		帮会争霸组队成员下线
		"""
		if KBEngine.globalData.get("BHZBStart",0):
			if self.tongMB:
				KBEngine.globalData["TongMgr"].bhzbTeamMemberLoginOut( self.getCamp(), self.tongDBID, self.databaseID )

#-------------------------------攻城战--------------------------------------
	def notfiyToJoinGCZ( self, joinPlayerDBIDs ):
		"""
		提示参加攻城战
		"""
		if self.isMatchGCZ:
			self.statusMessage( csstatus.GCZ_IS_ALREADY_TO_MATCH,"" )
			return
		if self.isInTeam():
			self.notfiyToJoinGCZTeam(joinPlayerDBIDs)
		else:
			self.inquireMessage( csstatus.IS_JOIN_GCZ_MATCH, [],"onNotfiyToJoinGCZ" ) 

	def onNotfiyToJoinGCZ( self, reply ):
		"""
		是否参与攻城战匹配
		"""
		if not reply:
			return
		KBEngine.globalData["GCZManager"].joinGCZMatchPerson( self, self.databaseID, self.getLevel() )

	def notfiyToJoinGCZTeam( self, joinPlayerDBIDs ):
		"""
		通知参加攻城战的队伍
		"""
		if self.isTeamCaptain():
			if self.isTeamHasMemberLogout(): # 队伍中有成员离开直接
				return

			notJoinGCZDBIDs = self.getNotJoinGCZTeamMember(joinPlayerDBIDs)
			if len( notJoinGCZDBIDs ):
				self.inquireMessage( csstatus.IS_KICK_OUT_NOT_JOIN_GCZ_TO_MATCH, [],"onKickOutNotJoinGCZMemberToMatch",joinPlayerDBIDs )
			else:
				self.inquireMessage( csstatus.IS_JOIN_GCZ_MATCH,[],"onKickOutNotJoinGCZMemberToMatch",joinPlayerDBIDs )
		else:
			captainMB = self.getTeamCaptainMailBox()
			if not captainMB:
				return
			captainDBID = self.getTeamMemberDBID( captainMB.id )
			if captainDBID in joinPlayerDBIDs:
				return
			self.inquireMessage(csstatus.IS_LEAVE_TEAM_TO_MATCH,[],"onLeaveTeamToMatch",joinPlayerDBIDs)

	def onKickOutNotJoinGCZMemberToMatch( self, reply, joinPlayerDBIDs ):
		"""
		剔出没有报名参战攻城战的成员 后匹配
		"""
		if not reply:
			return
		if not self.isInTeam():
			return
		if not self.isTeamCaptain():
			return
		if self.isTeamHasMemberLogout():
			self.statusMessage( csstatus.GCZ_MATCH_FORBID_TEAM_MEMBER_OFFLINE )
			return
		notJoinGCZDBIDs = self.getNotJoinGCZTeamMember(joinPlayerDBIDs)
		allMemberDBIDs = self.getTeamMemberPlayerDBIDs()
		for playerDBID in notJoinGCZDBIDs:
			member = self.getTeamMemberByPlayerDBID( playerDBID )
			if not member:
				continue
			self.leaveTeamFB(  member["playerMailBox"].id )
		if len(notJoinGCZDBIDs) == len(allMemberDBIDs) - 1:
			KBEngine.globalData["GCZManager"].joinGCZMatchPerson( self, self.databaseID,self.getLevel() )
			return
		
		memberDataList = []
		for playerDBID in self.getTeamMemberPlayerDBIDs():
			if playerDBID in notJoinGCZDBIDs:
				continue
			member = self.getTeamMemberByPlayerDBID( playerDBID )
			if not member:
				continue
			tempDict = {}
			tempDict["playerMB"] = member["playerMailBox"]
			tempDict["playerDBID"] = playerDBID
			tempDict["playerLevel"] = member["level"]
			memberDataList.append( tempDict )
		KBEngine.globalData["GCZManager"].joinGCZMahchTeam( self, self.teamMailBox, memberDataList,self.id )

	def onLeaveTeamToMatch( self, reply, joinPlayerDBIDs ):
		"""
		是否离开队伍进行匹配
		"""
		if not reply:
			return
		if not self.isInTeam():
			return
		if self.isTeamCaptain():
			return
		self.leaveTeamFB( self.id )
		KBEngine.globalData["GCZManager"].joinGCZMatchPerson( self, self.databaseID,self.getLevel() )

	def getNotJoinGCZTeamMember( self, joinPlayerDBIDs ):
		"""
		是否有队员没有参加攻城战
		"""
		playerDBIDs = self.getTeamMemberPlayerDBIDs()
		notJoinGCZDBIDs = []				# 是否有队员没有参加
		for playerDBID in playerDBIDs:
			if playerDBID not in joinPlayerDBIDs:
				notJoinGCZDBIDs.append( playerDBID )
		return notJoinGCZDBIDs

	def isTeamHasMemberLogout( self ):
		"""
		是否有队员离线了
		"""
		playerDBIDs = self.getTeamMemberPlayerDBIDs()
		hasMemberLogout = False
		for playerDBID in playerDBIDs:
			member = self.getTeamMemberByPlayerDBID( playerDBID )
			if not member:
				continue
			if member["playerMailBox"] == None:
				hasMemberLogout = True
				break
		return hasMemberLogout

	def GCZCreateTeam( self ):
		"""
		创建一只队伍
		"""
		if self.isInTeam():
			if self.isTeamFull():
				return
			self.isGCZToCreateTeam = True
			if self.isTeamCaptain():
				self.disbandTeamFB()
			else:
				self.leaveTeamFB( self.id )
		else:
			self.createSelfTeamLocally()
			KBEngine.globalData["GCZManager"].gcz_onCreateTeam( self, self.teamMailBox )

	def GCZOnJoinTeam( self, captainID, teamMailBox ):
		"""
		加入队伍
		"""
		if self.isInTeam():
			self.isGCZToLeaveTeam = True
			self.GCZTeamInfo = ( teamMailBox, captainID )
			if self.isTeamCaptain():
				self.disbandTeamFB()
			else:
				self.leaveTeamFB( self.id )
		else:
			self.isGCZToJoinTeam = True
			self.joinTeamNotify( teamMailBox, False, captainID, self.allocation, self.quality )

	def GCZOnLeaveTeam( self ):
		"""
		队员离开队伍的回调
		"""
		if self.isGCZToCreateTeam:
			self.isGCZToCreateTeam = False
			self.createSelfTeamLocally()
			KBEngine.globalData["GCZManager"].gcz_onCreateTeam( self, self.teamMailBox )

		if self.isGCZToLeaveTeam:
			self.isGCZToJoinTeam = True
			self.joinTeamNotify( self.GCZTeamInfo[0], False, self.GCZTeamInfo[1], self.allocation, self.quality )
			self.isGCZToLeaveTeam = False
			self.GCZTeamInfo = None
		if self.isMatchGCZ:
			KBEngine.globalData["GCZManager"].gcz_MatchTeamChange( self )

	def onGCZMemberJoin( self ):
		"""
		"""
		if self.isGCZToJoinTeam:
			self.isGCZToJoinTeam = False
			KBEngine.globalData["GCZManager"].onGCZMemberJoin( self )
		if self.isMatchGCZ:
			KBEngine.globalData["GCZManager"].gcz_MatchTeamChange( self )

	def notifyToStartMatchGCZ( self, curNumber ):
		"""
		通知开始匹配 显示匹配界面
		"""
		self.isMatchGCZ = True
		if hasattr( self, "client" ) and self.client:
			self.client.NotifyToStartMatchGCZ( curNumber )

	def notifyCancelMatchGCZ( self ):
		"""
		取消匹配 关闭匹配界面
		"""
		self.isMatchGCZ = False
		if hasattr( self, "client" ) and self.client:
			self.client.NotifyCancelMatchGCZ()

	def cancelMatchGCZ( self ):
		"""
		Exposed method
		取消匹配攻城战
		"""
		if not self.validateClientCall():
			return
		if self.isInTeam():
			if self.isTeamCaptain():
				KBEngine.globalData["GCZManager"].gcz_cancelMatch( self )
		else:
			KBEngine.globalData["GCZManager"].gcz_cancelMatch( self )

	
