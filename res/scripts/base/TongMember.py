# -*- coding: utf-8 -*-

import csdefine
import csstatus
import TongLoader
import Functions
import Const
import KBEDebug
import KBEngine
import cschannel_msgs
from MsgLogger import g_logger

class TongMember( object ):
	def __init__( self, playerMB, DBID, name, level, profession, title, localSpace = "", weekCon = 0,\
	offTime=0, exp=0, contribution=0, totalContribution=0, isGag=False, signTime =0, dMoney = 0, soldierAmount = 0,militaryRank = 0, isSign = False, isGetSalary = False, personTitle = ""):
		self.baseMailBox = playerMB
		self.DBID = DBID
		self.name = name
		self.profession = profession
		self.level = level
		self.title = title							# 职位ID、
		self.localSpace = localSpace				# 所在地
		self.offLineTime = offTime					# 最近上线
		self.exp = exp								# 帮会经验
		self.weekContribution = weekCon				# 每周帮贡
		self.contribution = contribution			# 剩余帮贡
		self.totalContribution = totalContribution	# 总帮贡
		self.isGag = isGag							# 是否被禁言
		self.signTime = signTime					# 累计签到次数
		self.dMoney = dMoney					# 捐献金钱
		# 不存数据库
		self.isSign = isSign						# 是否已签到
		self.isGetSalary = isGetSalary				# 是否领取俸禄
		self.chatTime = False						# 第一次聊天
		self.id = 0
		self.dMoneyDay = 0							# 每日累计捐献
		self.personTitle = ""						# 个人称号（只显示23、24、25、26对应的称号）

		self.soldierAmount = soldierAmount 			# 兵力
		self.militaryRank = militaryRank			# 军衔
		self.tongBlocklist = []						# 存放屏蔽的用户的DBID
		if playerMB:
			self.id = playerMB.id
		if offTime == 0:
			self.offLineTime = Functions.getTime()
		
	def saveTong( self, tongDBID ):
		"""玩家不在线，保存数据"""
		saveInfo = "UPDATE tbl_Role SET sm_tongDBID = '%d' WHERE id = '%d'"%(tongDBID,self.DBID)
		KBEngine.executeRawDatabaseCommand( saveInfo, self._saveTongCB )
		
	def _saveTongCB( self, result, rows, insertid, errstr ):
		""""""
		if errstr:
			KBEDebug.ERROR_MSG("Save Tong Err:%s"%errstr)
		
	def reqInit( self, playerMB ):
		self.baseMailBox = playerMB
		self.id = playerMB.id
	
	def offLine( self, level, birthSpace ):
		self.baseMailBox = None
		self.id = 0
		self.offLineTime = Functions.getTime()
		self.level = level
		self.localSpace = birthSpace
	
	def onDawnArrive( self ):
		self.isSign = False
		self.chatTime = 0
		self.dMoneyDay = 0
		self.isGetSalary = False
		if self.baseMailBox:
			self.baseMailBox.onDawnArrive()
			if self.getClient():
				self.baseMailBox.client.onDawnArrive()
		
	def onWeekArrive( self ):
		self.weekContribution = 0
		
	def getPackMemberDatas( self ):
		"""获取打包到客户端数据"""
		temp = {}
		temp.update( {"id" : self.id } )
		temp.update( {"DBID" : str(self.DBID) } )
		temp.update( {"name" : self.name } )
		temp.update( {"profession" : self.profession } )
		temp.update( {"level" : self.level } )
		temp.update( {"title" : self.title } )
		temp.update( {"localSpace" : self.localSpace })
		temp.update( {"offLineTime" : str(self.offLineTime) } )
		temp.update( {"exp" : self.exp } )
		temp.update( {"weekContribution" : self.weekContribution } )
		temp.update( {"contribution" : self.contribution } )
		temp.update( {"totalContribution" : self.totalContribution } )
		temp.update( {"isGag" : self.isGag } )
		temp.update( {"soldierAmount":self.soldierAmount} )
		temp.update( {"militaryRank":self.militaryRank} )
		temp.update( {"tongBlocklist":self.tongBlocklist} )
		return temp
	#-----------------------------------------帮会属性---------------------------------------------------
	def onSetTitleName( self, titleID, titleName ):
		"""设置职位名称"""
		if self.getClient():
			self.baseMailBox.client.OnSetTitleName( titleID, titleName )

	def onSetTitle( self, targetEntityDBID, titleID, grades ):
		"""设置职位"""
		if self.DBID == targetEntityDBID:
			self.title = titleID
			if self.baseMailBox:
				self.baseMailBox.onSetTitle( titleID, grades )
				self.baseMailBox.cell.onSetTitle( titleID, grades )
		if self.getClient():
			self.baseMailBox.client.OnSetTongTitle( str(targetEntityDBID), titleID )
		
	def onSetGrade( self, titleID, grades ):
		"""设置帮会权限"""
		if titleID == self.title:
			if self.baseMailBox:
				self.baseMailBox.onSetGrade( grades )
		if self.getClient():
			self.baseMailBox.client.OnSetGrade( titleID, grades )

	def addTongBlocklist( self, memberDBID):
		if memberDBID not in self.tongBlocklist:
			self.tongBlocklist.append(memberDBID)
			self.onTongBlocklistChange()
		else:
			return

	def removeTongBlocklist(self, memberDBID):
		if memberDBID in self.tongBlocklist:
			self.tongBlocklist.remove(memberDBID)
			self.onTongBlocklistChange()
		else:
			return

	def onTongBlocklistChange(self):
		if self.getClient():
			self.baseMailBox.client.OnTongBlocklistChange(self.tongBlocklist)

	def addExp( self, tongEntity, exp, isPrompt = True ):
		self.exp += exp
		self.onExpChange( tongEntity, isPrompt = True )
		
	def onExpChange( self, tongEntity, isPrompt = True ):
		for member in tongEntity.members.values():
			if member.getClient() and isPrompt:
				member.baseMailBox.client.onTongMemberExpChange( str(self.DBID), self.exp )
		
		if self.title > csdefine.TONG_TITLE_4:
			newTitle = TongLoader.getTitleByExp( self.exp )
			if self.title == newTitle:return
			
			self.title = newTitle
			for member in tongEntity.members.values():
				if member.getClient():
					member.baseMailBox.client.OnSetTongTitle( str(self.DBID), int(newTitle) )
		
	def addContribution( self, tongEntity, num, isPrompt = True, order = "" ):
		"""添加帮贡"""
		oldValue = self.contribution
		self.contribution += num
		self.weekContribution += num
		self.totalContribution += num
		if isPrompt and self.baseMailBox:
			self.baseMailBox.statusMessage( csstatus.TONG_MEMBER_GET_CONTRIBUTION, str(num) )
		self.onContributionChange( tongEntity, oldValue, order )
		
	def sudContribution( self, tongEntity, num, isPrompt = True, order = "" ):
		oldValue = self.contribution
		if self.contribution >= num:
			self.contribution -= num
			if isPrompt and self.baseMailBox:
				self.baseMailBox.statusMessage( csstatus.TONG_MEMBER_COST_CONTRIBUTION, str(num) )
			self.onContributionChange( tongEntity, oldValue, order )
			return True
		return False
		
	def onContributionChange( self, tongEntity, oldValue, order = "" ):
		if self.baseMailBox:
			self.baseMailBox.cell.onContributionChange( self.contribution )
		for member in tongEntity.members.values():
			if member.getClient() :
				member.baseMailBox.client.OnContributionChange( str(self.DBID), self.contribution )
				
		g_logger.tongContributeChangeLog(tongEntity.databaseID, tongEntity.tongName, self.DBID, self.name, oldValue, self.contribution, order)
		
	def hasEnoughContribution( self, num ):
		return self.contribution >= num
		
	def donateMoney( self, tongEntity, playerDBID, name, money, contribution, exp ):
		"""捐献"""
		if self.DBID == playerDBID:
			tongEntity.addRecord( csdefine.TONG_EVENT_DONATE, name, Functions.moneyToStr( money ), contribution )
			self.addContribution( tongEntity, contribution, False )
			self.addExp( tongEntity, exp, False )
			if self.getClient():
				self.baseMailBox.client.statusMessage( csstatus.TONG_DONATE_MONEY_SELF_RESULT, "%s|%s|%s"%( Functions.moneyToStr( money ), contribution, exp) )
			self.baseMailBox.cell.onDonateMoney( money )
			self.dMoney += money
			self.dMoneyDay += money
			if self.getClient():
				self.baseMailBox.client.OnDonateMoney( money )
		else:
			if self.getClient():
				self.baseMailBox.client.statusMessage( csstatus.TONG_DONATE_MONEY_OTHER_RESULT, "%s|%s|%s|%s"%( name, Functions.moneyToStr( money ), contribution, exp) )
			
	def onTongLevelChange( self, tongLevel ):
		if self.getClient():
			self.baseMailBox.client.OnUpgrowTong( tongLevel, TongLoader.getUpgradeUseActivity( tongLevel) )
			
	def onBuildLevelChange( self, tongEntity, buildType, buildLevel ):
		if self.baseMailBox:
			if self.getClient():
				self.baseMailBox.client.OnUpgrowBuild( buildType, buildLevel )
			if buildType == csdefine.TONG_BUILDING_TYPE_SD:
				maxLevel = tongEntity.builds[buildType].getMaxLevel( tongEntity )
				if maxLevel == buildLevel:					# 等于说明帮会等级与 帮会商店等级相等
					self.baseMailBox.cell.onTongShopLevelChange( buildLevel )
			elif buildType == csdefine.TONG_BUILDING_TYPE_TJP:
				maxLevel = tongEntity.builds[buildType].getMaxLevel( tongEntity )
				if maxLevel == buildLevel:					# 等于说明帮会等级与 帮会商店等级相等
					self.baseMailBox.cell.onTongSmithyLevelChange( buildLevel )
					
	def onBuildShopLevelChange( self, maxLevel ):
		if self.baseMailBox:
			self.baseMailBox.cell.onTongShopLevelChange( maxLevel )
			
	def onBuildSmithyLevelChange( self, maxLevel ):
		if self.baseMailBox:
			self.baseMailBox.cell.onTongSmithyLevelChange( maxLevel )
			
	def onConferenceHallLevelChange( self, limitNum ):
		if self.baseMailBox:
			self.baseMailBox.client.OnConferenceHallLevelChange(limitNum)
		
	def onMoneyChange( self, money ):
		if self.getClient():
			self.baseMailBox.client.OnTongMoneyChange( money )
		
	def OnResearchTongSkill( self, skillID ):
		if self.getClient():
			skillName = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "SkillName" )
			self.baseMailBox.client.statusMessage( csstatus.TONG_SKILL_BEGIN_RESEARCH, skillName )
			self.baseMailBox.client.OnResearchTongSkill( skillID )
			
	def onPauseSkill( self, skillID ):
		if self.getClient():
			self.baseMailBox.client.OnPauseTongSkill( skillID )
			
	def tryStudyTongSkill( self, tongEntity, skillID ):
		if self.baseMailBox:
			reqContribution = TongLoader.g_TongLoader.getSkillReqConditionByName( skillID, "StudyReqContribution")
			if self.sudContribution( tongEntity, reqContribution ):
				self.baseMailBox.cell.remoteSuccessPay( )
				return
			else:
				if self.getClient():
					self.baseMailBox.client.statusMessage( csstatus.TONG_STUDY_SKILL_NO_ENOUGH_CONTRIBUYION,"" )
		else:
			KBEDebug.ERROR_MSG("Try to study tong skill(%d) err!base MailBox is None!"%skillID)
		self.baseMailBox.cell.remoteFailPay( )
		
	def onTongSkillProgressChange( self, progress ):
		if self.getClient():
			self.baseMailBox.client.OnTongSkillProgressChange( progress )
			
	def onFinishResearchSkill( self, skillID ):
		if self.getClient():
			self.baseMailBox.client.OnFinishResearchSkill( skillID )
		
	def setGag( self, playerDBID, isGag ):
		if self.DBID == playerDBID:
			self.isGag = isGag
		if self.getClient():
			self.baseMailBox.client.OnSetGag( str(playerDBID), isGag )
			
	def tongSign( self ):
		if not self.isSign:
			self.isSign = True
			self.signTime += 1
			if self.getClient():
				self.baseMailBox.client.OnTongSign()
				
	def UpdateTongMemberInfo( self, level, localSpace, soldierAmount, militaryRank ):
		"""
		define method
		更新信息
		"""
		self.level = level
		self.localSpace = localSpace
		self.soldierAmount = soldierAmount
		self.militaryRank = militaryRank

	def onChangeNagual(self, nagualType):
		"""
		"""
		if self.baseMailBox:
			if self.getClient():
				self.baseMailBox.client.UpdateNagualType(nagualType)
				
	def UpdateTongMemberPersonTitle(self, personTitle):
		"""
		"""
		self.personTitle = personTitle

	#-----------------------------------------加入帮会---------------------------------------------------
	def tongOnMemberJoin( self, tongEntity, playerDBID, playerName, tongName ):
		"""玩家加入帮会"""
		if playerDBID == self.DBID:
			if self.title != csdefine.TONG_TITLE_1:
				if self.getClient(): self.baseMailBox.client.statusMessage( csstatus.TONG_JOIN_SUCCESS_SELF, tongName )
				tongEntity.addRecord( csdefine.TONG_EVENT_JOIN, playerName, tongName )
			tongEntity.notifyClientTongDatas( self.baseMailBox, playerDBID )
			if self.getClient():
				self.baseMailBox.client.OnJoinTong()
		else:
			if self.baseMailBox:
				if self.getClient():
					self.baseMailBox.client.statusMessage( csstatus.TONG_JOIN_SUCCESS_OTHER, playerName )
				tongEntity.notifyClientTongMemberDatas( self.baseMailBox, playerDBID )
			
	#-----------------------------------------离开帮会---------------------------------------------------
	def onKick( self, kickMem, beKickMem ):
		"""踢人"""
		if self.baseMailBox:
			if beKickMem.DBID == self.DBID:
				self.baseMailBox.tongBeKick()
				if self.getClient():
					self.baseMailBox.client.statusMessage( csstatus.TONG_BEKICK_OUT_TONG , kickMem.name )
			if self.getClient():
				self.baseMailBox.client.OnKickTongMember( str(kickMem.DBID), str(beKickMem.DBID) )
			
	def tongQuit( self, quitDBID ):
		"""离开帮会"""
		if self.baseMailBox:
			if self.DBID == quitDBID:
				self.baseMailBox.tongOnQuit()
			if self.getClient():
				self.getClient().OnQuitTong( str(quitDBID) )
			
	def tongOnDismiss( self ):
		"""解散帮会"""
		money = int( self.contribution / Const.TONG_MONEY_TO_CONTRIBUTE )
		money = 1 if money < 1 else money	#跟柳爷沟通之后，不足1的话发1（CST-12078）
		#self.baseMailBox.cell.tongDismissChangeConToMoney( money )
		KBEngine.globalData["MailManager"].sendWithMailbox(None, self.baseMailBox, self.name, csdefine.MAIL_SENDER_TYPE_SYS, cschannel_msgs.MAIL_SEND_SYSTEM, \
			cschannel_msgs.TONG_DISMISS_CHANGE_CON_TO_MONEY_MAIL_TITLE, cschannel_msgs.TONG_DISMISS_CHANGE_CON_TO_MONEY_MAIL_CONTENT, 0, money, [], 0, 0)
		
		if self.baseMailBox:
			self.baseMailBox.tongOnDismiss()
			self.baseMailBox = None
	
	def getClient( self ):
		""""""
		if self.baseMailBox and hasattr(self.baseMailBox, "client") and self.baseMailBox.client:
			return self.baseMailBox.client
		return None