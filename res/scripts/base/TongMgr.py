# -*- coding: utf-8 -*-
import KBEngine
from CoreObject.MgrPersistentObject import MgrPersistentObject

from MsgLogger import g_logger
import TongData
import csdefine
import KBEDebug
import Functions
import Const
import csstatus
import time
import random
import KST
import json
import csconst
import math

from ConfigObject.Shop.ShopMgr import g_shopMgr
from ConfigObject.Crond.CrondDatas import CrondDatas
from Scheme import Scheme

g_CrondDatas = CrondDatas.instance()

TONG_ENTITY_NAME = "TongEntity"
QUERY_TONG_DBIDS_SQL = "SELECT `id` FROM `tbl_%s`"%( TONG_ENTITY_NAME )

	
class TongMgr( MgrPersistentObject ):
	def __init__( self ):
		MgrPersistentObject.__init__( self )
		self.tongs = {}
		self.tongSpaces = {}
		self.loadAllTongInfo()
	
	def loadAllTongInfo( self ):
		"""
		加载帮会
		"""
		taskEvents = { "TongMgr_OnDawnArrive":"onDawnArrive",
		 }
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
		 		KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1,() )
		KBEngine.executeRawDatabaseCommand( QUERY_TONG_DBIDS_SQL, self.onLoadAllTongInfo )
	
	def onLoadAllTongInfo( self, result, rows, insertid, errstr ):
		"""
		数据库查询帮会id回调
		"""
		if len( result ):
			allTongDBIDs = [ int( rowData[0] )  for rowData in result ]
			if len(allTongDBIDs) <= 0:
				self.onCompleteInit()
				return
			
			self.initTong = len(allTongDBIDs)
			for tongDBID in allTongDBIDs:
				KBEngine.createEntityFromDBID( TONG_ENTITY_NAME, tongDBID, self.onLoadTongFormDBOver )
		else:
			self.onCompleteInit()
	
	def onLoadTongFormDBOver( self, baseRef, databaseID, wasActive ):
		"""
		从数据库创建一个TongEntity完成
		"""
		assert not wasActive, "(%i): the target entity was active, I can't do it." % databaseID
		if baseRef != None:
			self.tongs[ baseRef.databaseID ] = baseRef
		else:
			KBEDebug.ERROR_MSG( "load tong:%i failure!!"%databaseID )
			
		self.initTong -= 1
		if self.initTong <= 0:
			self.onCompleteInit()
	
	def getTong( self, tongDBID ):
		return self.tongs.get( tongDBID, None )
		
	def onDawnArrive( self, cmd, *callbackArgs ):
		"""晚上0点"""
		for tong in list(self.tongs.values()):
			tong.onDawnArrive()
		if time.localtime()[6] == 1:
			self.onWeekArrive()
			
	def onWeekArrive( self ):
		"""周一 0点"""
		for tong in self.tongs.values():
			tong.onWeekArrive()
	
	def checkHasTongName( self, tongName ):
		"""
		检查是否有相同帮会名称
		"""
		result = False
		for tongDBID, tongEntity in self.tongs.items():
			if tongEntity.tongName == tongName:
				result = True
				break
		return result
		
	def checkTongCamp( self, camp ):
		"""
		检查阵营数量
		"""
		num = 0
		for tongEntity in self.tongs.values():
			if tongEntity.camp == camp:
				num += 1
		return num < Const.TONG_CREATE_MAX_CAMP_NUM
		
	def reqInit( self, playerMB, playerDBID, tongDBID ):
		"""
		define method
		玩家请求初始化帮会
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.reqInit( playerMB, playerDBID )
		elif tongDBID in self.dismissTongDatas:
			playerMB.tongBeKickOffLine( self.dismissTongDatas[tongDBID] )		# 帮会解散了，当作是踢出帮会
		else:										# 有可能帮会已经解散了
			playerMB.tongOnInitErr()
	
	def onTongSpaceCreateFinish( self, tongDBID, spaceMB ):
		"""
		define method
		"""
		if tongDBID in self.tongs:
			if tongDBID in self.tongSpaces and self.tongSpaces[tongDBID]:
				KBEDebug.ERROR_MSG("Tong(%d) space create err!space has create again!"%tongDBID)
				return
			self.tongSpaces[tongDBID] = spaceMB
			self.tongs[tongDBID].onTongSpaceCreateFinish( spaceMB )
		else:
			self.addTimerCallBack( 1.0, "delayDestroyTong", ( spaceMB,))
#			spaceMB.tongOnDismiss()					# 玩家在帮会领地下线，然后帮会解散了
#			KBEDebug.ERROR_MSG("Tong space create err!can not find tong(%d)"%tongDBID)
	
	def delayDestroyTong( self, spaceMB ):
		"""延迟销毁帮会"""
		spaceMB.tongOnDismiss()
	#-----------------------帮会创建---------------------------------------------------------------------------
	def createTong( self, creatorMailBox, creatorDBID, creatorName, profession, level, camp, personTitle, tongName ):
		"""
		define method
		请求创建帮会
		"""
		if self.checkHasTongName( tongName ):
			creatorMailBox.client.statusMessage( csstatus.TONG_HAS_ALREADY_EXISTED, "" )
			creatorMailBox.cell.remoteFailPay( )
			return
		if not self.checkTongCamp( camp ):
			creatorMailBox.client.statusMessage( csstatus.TONG_AMOUNT_REACH_MAX, "" )
			creatorMailBox.cell.remoteFailPay( )
			return
			
		tongEntity = KBEngine.createEntityLocally( TONG_ENTITY_NAME, { "tongName":tongName, "camp":camp } )
		tongEntity.writeToDB( Functions.Functor( self.onCreateTong, creatorMailBox, creatorDBID, creatorName, profession, level, personTitle ) )
		creatorMailBox.cell.remoteSuccessPay( )
		
	def onCreateTong( self, creatorMailBox, creatorDBID, creatorName, profession, level, personTitle, success, tongEntity ):
		"""
		帮会创建，完成写数据库的回调
		"""
		if success: #如果帮会名字重复，这个则为fase
			tongEntity.initDatas( creatorMailBox, creatorDBID, creatorName, profession, level, personTitle )
			self.tongs[ tongEntity.databaseID ] = tongEntity
			creatorMailBox.onCreateTong( tongEntity.databaseID )
			
			KST.g_baseAppEntity.globalWold( csstatus.TONG_CREATE_WORLD_NOTICE, creatorName + "|" + tongEntity.tongName )
			g_logger.tongCreateLog( tongEntity.databaseID, tongEntity.tongName, creatorDBID, creatorName )
		else:
			if tongEntity:
				tongEntity.destroy()
	
	#-----------------------帮会申请加入---------------------------------------------------------------------------
	def reqJoin( self, tongDBID, roleMB, roleDBID, roleName, level, profession, camp ):
		"""
		define method
		玩家请求加入帮会
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.reqJoin( roleMB, roleDBID, roleName, level, profession, camp )
		else:
			KBEDebug.ERROR_MSG("player(%s) request join tong(DBID:%d) error!!"%(roleName,tongDBID))
			
	def cancelJoin( self, tongDBID, roleDBID ):
		"""
		define method
		取消加入帮会
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.cancelJoin( roleDBID )
		else:
			KBEDebug.ERROR_MSG("player(DBID:%d) request join tong(DBID:%d) error!!"%(roleDBID,tongDBID))
			
	def onJoinResult( self, roleDBID ):
		"""
		define method
		玩家加入帮会
		"""
		for tong in self.tongs.values():
			tong.onJoinResult( roleDBID )

	def onInviteTong( self, tongDBID, inviteMB, beInviteMB, beInviteDBID, beInviteName, beInviteLevel, beInviteProfession, beInvitePersonTitle ):
		"""
		define method
		玩家被邀请加入帮会
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.replyInviteTong( inviteMB, beInviteMB, beInviteDBID, beInviteName, beInviteLevel, beInviteProfession, beInvitePersonTitle )
		else:
			KBEDebug.ERROR_MSG("player(DBID:%d) request join tong(DBID:%d) error!!"%(roleDBID,tongDBID))
		
	def dismissTong( self, tongDBID, reason ):
		"""
		define method
		解散帮会
		"""
		tongEntity = self.tongs.pop( tongDBID )
		tongName = tongEntity.tongName
		tongEntity.tongOnDismiss()
		self.dealDismissTong(tongDBID)
		if tongDBID in self.tongSpaces and self.tongSpaces[tongDBID]:
			self.tongSpaces[tongDBID].tongOnDismiss() 
		g_logger.tongDismissLog( tongDBID, tongName, reason )
		
	def dealDismissTong( self, tongDBID ):
		"""统一处理解散帮会的DBID"""
		for dbid in list(self.dismissTongDatas):
			if time.time() - self.dismissTongDatas[dbid] >= Const.TONG_REJOIN_CD_TIME:				# 解散了1天的帮会，就不记录了
				self.dismissTongDatas.pop( dbid )
		self.dismissTongDatas[tongDBID] = int( time.time() )
		
	def deleteRole( self, roleDBID, tongDBID ):
		"""
		define method
		删除角色
		"""
		for id, tong in self.tongs.items():
			if id == tongDBID:
				tong.deleteRole(roleDBID)
				break
		
	#-----------------------请求帮会数据---------------------------------------------------------------------------
	def requireTongInfo( self, playerMB, camp ):
		"""
		define method
		帮会申请列表
		"""
		tongInfo = {"tongDatas":[]}
		for tong in self.tongs.values():
			if tong.camp == camp:
				tongInfo["tongDatas"].append( tong.getJoinTongInfo() )
		playerMB.client.CLIENT_OnReceiveAllTong( tongInfo ) 

	#------------------------------帮会争霸-----------------------------------------------
	def firstQuerySignUp( self, tongDBIDs, playerMB ):
		"""
		查询帮会争霸第一场报名消息
		"""
		tempArray = []
		for tongDBID in tongDBIDs:
			tongEntity = self.getTong( tongDBID )
			if tongEntity:
				tempDict = {}
				tempDict["tongName"] = tongEntity.tongName
				tempDict["tongLevel"] = tongEntity.level
				tempArray.append(tempDict)
		playerMB.client.CLIENT_ShowTongSignSuccessWindow( Functions.toJsonString(tempArray) )

	def queryPassFirstTongStarcraft( self, passTongDict, playerMB ):
		"""
		查询帮会争霸通过第一场信息
		"""
		tempArray = []
		for tongDBID,passTime in passTongDict.items():
			tongEntity = self.getTong( tongDBID )
			tempDict = {}
			if tongEntity:
				tempDict["tongName"] = tongEntity.tongName
				tempDict["tongLevel"] = tongEntity.level
				tempDict["passTime"] = passTime
				tempArray.append(tempDict)

		playerMB.client.CLIENT_ShowPassFirstTongStarcraft(Functions.toJsonString( tempArray ))

	def openSecondTongStarcraftGroup( self, groupOne,groupTwo, playerMB ):
		"""
		打开帮会争霸第二场的分组
		"""
		def getGroupNames( groupDBID ):
			tempArray = []
			for tongDBID in groupDBID:
				tongEntity = self.getTong( tongDBID )
				if tongEntity:
					tempArray.append( tongEntity.tongName )
			return tempArray
		groupOneNames = getGroupNames( groupOne )
		groupTwoNames = getGroupNames( groupTwo )
		
		playerMB.client.CLIENT_OpenSecondTongStarcraftGroup( groupOneNames,groupTwoNames )

	#------------------------------CST-11386 帮会争霸---------------------------
	def sureBHZBTongSendMail( self, tongDBID ):
		"""
		确认参与的帮会发送邮件
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.sureBHZBTongSendMail()

	def sureBHZBTongMemberSendMail( self, tongDBID, tongMemberDBIDs ):
		"""
		给确认帮会参与人员发送邮件
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.sureBHZBTongMemberSendMail( tongMemberDBIDs )

	def sendBHZBRewardToMembers( self, tongDBID, memberDBIDs,rankRewardGifts, rankRewardTongMoney,rankRewardContributionGift, index ):
		"""
		发送帮会争霸奖励给成员
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.sendBHZBRewardToMembers( memberDBIDs,rankRewardGifts, rankRewardTongMoney,rankRewardContributionGift, index )

	def sendTongLeaderReward( self, tongDBID, leaderReward, rank ):
		"""
		发送奖励给帮主
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.sendTongLeaderReward( leaderReward, rank )

	def onBHZBPointWarEnd( self, tongDBID, pointIndex ):
		"""
		帮会争霸据点地图争夺结束
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.onBHZBPointWarEnd( pointIndex )

	def clearTongSignMemberData( self, tongDBID ):
		"""
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.clearTongSignMemberData()

	def checkIsLoginToBHZBPoint( self, roleMB, tongDBID, spaceScriptID,playerDBID ):
		"""
		检查是否重新进入帮会争霸据点
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.checkIsLoginToBHZBPoint( roleMB, tongDBID, spaceScriptID,playerDBID )

	def bhzbTeamMemberLoginOut( self, camp, tongDBID, playerDBID ):
		"""
		帮会争霸组队成员下线
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.bhzbTeamMemberLoginOut( camp, tongDBID, playerDBID )

	def cancelProtectBHZBPoint( self, tongDBID, groupTeamID ):
		"""
		敌方取消宣战  防守方取消防守
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.setbhzbSignUpMembersIsActive( groupTeamID, False,0)

	def clearAllTongSignMemberData( self ):
		"""
		清除所有报名数据
		"""
		for tong in self.tongs.values():
			tong.clearAllTongSignMemberData()

	def joinBHZBWarFail( self, tongDBID ):
		"""
		参与帮会争霸帮会失败 反还资金
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.joinBHZBWarFail()

	def sendToJoinCampWarMail( self, tongDBID, month, day, side ):
		"""
		决出最终获得阵营争霸资格 发送邮件
		"""
		tongEntity = self.getTong( tongDBID )
		if tongEntity:
			tongEntity.sendToJoinCampWarMail( month, day, side )

	#------------------------------CST-12032 帮会掠夺战----------------------------
	def checkSignUpTongPlunder(self, playerMB, attackTongDBID, protectTongDBID):
		"""
		检查报名活动条件
		"""
		attackTong = self.getTong(attackTongDBID)
		protectTong = self.getTong(protectTongDBID)

		if not attackTong or not protectTong:
			return False

		#等级
		if attackTong.level < csconst.TONG_PLUNDER_MIN_TONG_LEVEL:
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_LEVEL_NOT_ENOUGH, "")
			return False
		#最低活跃度
		if not attackTong.checkMinActivity():
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_ACTIVITY_NOT_ENOUGH, "")
			return False
		#最低维持帮会资金
		if not attackTong.checkMinTongMoney():
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_MONEY_NOT_ENOUGH, "")
			return False
		#是否已经报名参与活动
		if attackTong.checkSignUpStatus():
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_LOCKED_BY_OTHER, "")
			return False

		#对方等级
		if protectTong.level < csconst.TONG_PLUNDER_MIN_TONG_LEVEL:
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_TARGET_LEVEL_NOT_ENOUGH, "")
			return False
		#对方最低活跃度
		if not protectTong.checkMinActivity():
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_TARGET_ACTIVITY_NOT_ENOUGH, "")
			return False
		#对方最低维持帮会资金
		if not protectTong.checkMinTongMoney():
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_TARGET_MONEY_NOT_ENOUGH, "")
			return False
		#对方是否已经报名参与活动
		if protectTong.checkSignUpStatus():
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_TARGET_LOCKED_BY_OTHER, "")
			return False

		if abs(attackTong.level - protectTong.level) > csconst.TONG_PLUNDER_BOTH_MAX_DIFF_LEVEL:
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_LEVEL_DIFF_TOO_BIG, "")
			return False

		return True

	def onTongPlunderSignUpStart(self):
		"""
		define method

		帮会掠夺战报名开始
		"""
		#通知原来已经参与活动的帮会清除数据
		for tongEntity in list(self.tongs.values()):
			if tongEntity:
				tongEntity.onTongPlunderSignUpStart()

	def signUpTongPlunder(self, playerMB, attackTongDBID, protectTongDBID):
		"""
		define method

		参加帮会掠夺战
		"""
		if not self.checkSignUpTongPlunder(playerMB, attackTongDBID, protectTongDBID):
			return

		attackTong = self.getTong(attackTongDBID)
		protectTong = self.getTong(protectTongDBID)

		if not attackTong or not protectTong:
			return

		attackTongInfo = {"dbid": attackTongDBID, "level": attackTong.level, "name": attackTong.tongName}
		protectTongInfo = {"dbid": protectTongDBID, "level": protectTong.level, "name": protectTong.tongName}

		KBEngine.globalData["TongPlunderManager"].signUpActivity(attackTongInfo, protectTongInfo)

	def onTongPlunderSignUpSuccess(self, attackTongDBID, protectTongDBID):
		"""
		报名帮会掠夺成功
		"""

		attackTong = self.getTong(attackTongDBID)
		protectTong = self.getTong(protectTongDBID)

		if not attackTong or not protectTong:
			return

		crondInfo = g_CrondDatas.getCrondTaskCmds("TongPlunderManager_Start")
		nextStartTime = 0
		if crondInfo:
			scriptID = crondInfo[0][0]
			cmd = crondInfo[0][1]
			scheme = Scheme()
			if scheme.init(cmd):
				year, month, day, hour, minute = time.localtime()[:5]
				nextMinute = minute + 1
				nextStartTime = scheme.calculateNext(year, month, day, hour, nextMinute)

		attackTong.onTongPlunderSignUpSuccess(csdefine.BELONG_SIDE_ATTACK, protectTong.tongName, nextStartTime)
		protectTong.onTongPlunderSignUpSuccess(csdefine.BELONG_SIDE_PROTECT, attackTong.tongName, nextStartTime)

	def onTongPlunderStart(self, tongDBIDList):
		"""
		define method

		帮会掠夺战开始
		"""
		for tongDBID in tongDBIDList:
			tongEntity = self.getTong(tongDBID)
			if tongEntity:
				tongEntity.onTongPlunderStart()

	def onTongPlunderEnd(self, tongDBIDList):
		"""
		define method

		帮会掠夺战结束
		"""
		for tongDBID in tongDBIDList:
			tongEntity = self.getTong(tongDBID)
			if tongEntity:
				tongEntity.onTongPlunderEnd()

	def onTongPlunderSendMail(self, tongDBIDList):
		"""
		define method

		帮会掠夺战开始前给参与人员发邮件
		"""
		for tongDBID in tongDBIDList:
			tongEntity = self.getTong(tongDBID)
			if tongEntity:
				tongEntity.onTongPlunderSendMail()

	def onLockTongShopStart(self, tongDBIDList):
		"""
		锁定帮会商店
		define method
		"""
		for tongDBID in tongDBIDList:
			tongEntity = self.getTong(tongDBID)
			if tongEntity:
				tongEntity.lockTongShop()

	def onLockTongShopEnd(self, tongDBIDList):
		"""		
		解锁帮会商店
		define method
		"""
		for tongDBID in tongDBIDList:
			tongEntity = self.getTong(tongDBID)
			if tongEntity:
				tongEntity.unLockTongShop()
		
	def onTongPlunderShopSellStart(self, tongDBIDList):
		"""
		帮会掠夺战所获商品售卖开始
		define method
		"""
		crondInfo = g_CrondDatas.getCrondTaskCmds("TongPlunderManager_ShopSellEnd")
		nextStartTime = 0
		if crondInfo:
			scriptID = crondInfo[0][0]
			cmd = crondInfo[0][1]
			scheme = Scheme()
			if scheme.init(cmd):
				year, month, day, hour, minute = time.localtime()[:5]
				nextMinute = minute + 1
				nextStartTime = scheme.calculateNext(year, month, day, hour, nextMinute)


		for tongDBID in tongDBIDList:
			tongEntity = self.getTong(tongDBID)
			if tongEntity:
				tongEntity.tongPlunderShopSellStart(nextStartTime)

	def onTongPlunderShopSellEnd(self, tongDBIDList):
		"""
		帮会掠夺战所获商品售卖结束
		define method
		"""
		for tongDBID in tongDBIDList:
			tongEntity = self.getTong(tongDBID)
			if tongEntity:
				tongEntity.tongPlunderShopSellEnd()

	def tongPlunderResultReward(self, spaceMB, winnerTongDBID, loserTongDBID, winnerRewardInfo, loserGifgID):
		"""
		帮会掠夺战结果奖励
		define method
		"""
		winnerTong = self.getTong(winnerTongDBID)
		loserTong = self.getTong(loserTongDBID)

		if winnerTong and loserTong:

			#帮会商店的奖励
			number = len(loserTong.members)
			datas = g_shopMgr.getShopConfig("TongShop")
			tempDatas = []
			for key, value in datas.items():
				data = {}
				data["id"] = value["id"]
				data["itemID"] = value["itemID"]
				if value["buyLimit"] == -1:
					data["amount"] = math.ceil(number * Const.TONG_PLUNDER_SHOP_RATIO)
				else:
					data["amount"] = math.ceil(value["buyLimit"] * number * Const.TONG_PLUNDER_SHOP_RATIO)
				tempDatas.append(data)

			giftID = ""
			#根据打赢的帮会等级获得奖励，只有胜利法获得
			if winnerRewardInfo:
				winnerRewardList = winnerRewardInfo.split("|")
				for reward in winnerRewardList:
					level, id = reward.split(":")
					if int(level) == loserTong.level:
						#winnerTong.sendTongPlunderRewardMail(mailID)
						giftID = id
						break

			money = loserTong.tongPlunderData.getLockMoney() * Const.TONG_PLUNDER_SHOP_RATIO

			winnerTong.tongPlunderVictory(spaceMB, tempDatas, giftID, money)
			loserTong.tongPlunderFailed(loserGifgID)
			
	def openTongPlunderSignUpWnd(self, playerMB, tongDBID):
		"""
		打开报名界面
		"""
		tongInfo = {"tongDatas":[]}
		for tong in self.tongs.values():
			if tong.databaseID != tongDBID:
				tongInfo["tongDatas"].append(tong.getJoinTongInfo())
		
		if playerMB and playerMB.client:
			playerMB.client.OpenPlunderTongListWnd(tongInfo)

	#---------------------------------------- 测试接口 -------------------------------------------------------------
	def disbandAllTong( self ):
		"""
		define method
		解散所有帮会(测试)
		"""
		for id in list(self.tongs.keys()):
			self.dismissTong(id, csdefine.TONG_DISMISS_NORMAL)
		