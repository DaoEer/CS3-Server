# -*- coding: utf-8 -*-

import KBEDebug
import Math
import KBEngine
import csdefine
from CoreObject import MgrPersistentObject
import csstatus
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()
import KST
import Const
import cschannel_msgs

TONG_PLUNDER_COPY_SPACE_NAME = "fu_ben_L_BHLD_GJJD"


class TongData:
	def __init__(self, tongInfo):
		self.dbid = tongInfo["dbid"]
		self.level = tongInfo["level"]
		self.name = tongInfo["name"]
		self.members = []

	def getDBID(self):
		return self.dbid

	def getLevel(self):
		return self.level

	def getName(self):
		return self.name

	def getMembers(self):
		return self.members

	def setMembers(self, members):
		self.members = members

	def getDictData(self):
		data = {"dbid": self.dbid, "level": self.level, "name": self.name}
		return data


class TongItem:
	"""
	掠夺战的两个帮会的数据
	"""
	def __init__( self, attackTongInfo, protectTongInfo):
		#def __init__( self, attackTongDBID, protectTongDBID, attackTongLevel, protectTongLevel):
		"""
		"""
		self.attackTongData = TongData(attackTongInfo)
		self.protectTongData = TongData(protectTongInfo)
		"""
		self.attackTongDBID = attackTongDBID #进攻方帮会dbid
		self.protectTongDBID = protectTongDBID #防守方帮会dbid
		self.attackTongLevel = attackTongLevel #进攻方帮会level
		self.protectTongLevel = protectTongLevel#防守方帮会level
		self.attackTongMembers = [] #进攻放成员dbid
		self.protectTongMembers = [] #防守方成员dbid
		"""

	def setTongMembers(self, belongSide, members):	
		if belongSide == csdefine.BELONG_SIDE_ATTACK:
			self.attackTongData.setMembers(members)
		elif belongSide == csdefine.BELONG_SIDE_PROTECT:
			self.protectTongData.setMembers(members)
		"""
		def getAttackTongDBID(self):
			return self.attackTongData.getDBID()

		def getProtectTongDBID(self):
			return self.protectTongData.getDBID()

		def getAttackTongLevel(self):
			return self.attackTongLevel

		def getProtectTongLevel(self):
			return self.protectTongLevel
		"""
	def getAttackTongInfo(self):
		return self.attackTongData.getDictData()

	def getProtectTongInfo(self):
		return self.protectTongData.getDictData()

	def isInTongItem(self, tongDBID):
		if tongDBID == self.attackTongData.getDBID() or tongDBID == self.protectTongData.getDBID():
			return True
		return False

	def isInMembers(self, playerDBID):
		if playerDBID in self.attackTongData.getMembers() or playerDBID in self.protectTongData.getMembers():
			return True
		return False

	def checkTongInfo(self, attackTongDBID, protectTongDBID):
		if attackTongDBID != self.attackTongData.getDBID() or protectTongDBID != self.protectTongData.getDBID():
			return False
		return True


class TongPlunderManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	CST-12032 帮会掠夺战 管理类
	"""
	def __init__( self ) :
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.register()
		self.init()
		self.onCompleteInit()
	
	def register( self ):
		"""
		所有帮会初始化完成
		"""
		taskEvents = {	
			"TongPlunderManager_SignUp": "onActiveSignUp",
			"TongPlunderManager_SignUpEnd": "onActiveSignUpEnd",
			"TongPlunderManager_Start": "onActiveStart",
			"TongPlunderManager_End": "onActiveEnd",		 
			"TongPlunderManager_SendMail": "onSendMail", 
			"TongPlunderManager_LockShop": "onLockTongShopStart", 
			"TongPlunderManager_UnLockShop": "onLockTongShopEnd", 
			"TongPlunderManager_ShopSellStart": "onTongPlunderShopSellStart", 
			"TongPlunderManager_ShopSellEnd": "onTongPlunderShopSellEnd",
		}
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
				KBEngine.globalData["CrondManager"].addScheme(scriptID, cmd, self, callbackName, -1, ())

	def init(self):
		"""
		"""
		KBEngine.globalData["TongPlunderManager_Status"] = csdefine.TONG_PLUNDER_ACTIVITY_STATUS_FREE
		KBEngine.globalData["TongPlunderManager_Enter_Status"] = csdefine.TONG_PLUNDER_ACTIVITY_STATUS_CAN_ENTER
		self.tongItemList = [] #
		self.signUpTongInfos = []
		self.leaveSpacePlayerInfos = [] #玩家主动离开副本，[dbid,]
		self.reviveNumUseupPlayerInfos = [] #因死亡次数已到达最大值而被传送离开副本的玩家，[dbid,]
		self.getTheResultTongList = [] #已分出胜负的帮会

	def onActiveSignUp(self, cmd, *callbackArgs):
		"""
		报名开始
		"""
		KBEngine.globalData["TongPlunderManager_Status"] = csdefine.TONG_PLUNDER_ACTIVITY_STATUS_SIGNUP
		KBEngine.globalData["TongMgr"].onTongPlunderSignUpStart()
		self.tongItemList.clear()
		self.signUpTongInfos.clear()
		self.leaveSpacePlayerInfos.clear()
		self.reviveNumUseupPlayerInfos.clear()
		self.getTheResultTongList.clear()
		KBEngine.globalData["TongPlunderManager_Enter_Status"] = csdefine.TONG_PLUNDER_ACTIVITY_STATUS_CAN_ENTER

	def onActiveSignUpEnd(self, cmd, *callbackArgs):
		"""
		报名结束
		"""
		KBEngine.globalData["TongPlunderManager_Status"] = csdefine.TONG_PLUNDER_ACTIVITY_STATUS_FREE

	def onActiveStart(self, cmd, *callbackArgs):
		"""
		活动开始
		"""
		KBEngine.globalData["TongPlunderManager_Status"] = csdefine.TONG_PLUNDER_ACTIVITY_STATUS_START
		KBEngine.globalData["TongMgr"].onTongPlunderStart(self.getSignUpTongDBIDList())
		KBEngine.globalData["SpaceManager"].remoteCallDomain(TONG_PLUNDER_COPY_SPACE_NAME, "activityStart", (self.signUpTongInfos, ))

	def onActiveEnd(self, cmd, *callbackArgs):
		"""
		活动结束
		"""
		KBEngine.globalData["TongPlunderManager_Status"] = csdefine.TONG_PLUNDER_ACTIVITY_STATUS_FREE
		KBEngine.globalData["TongMgr"].onTongPlunderEnd(self.getSignUpTongDBIDList())
		KBEngine.globalData["SpaceManager"].remoteCallDomain(TONG_PLUNDER_COPY_SPACE_NAME, "activityEnd", ())
		#self.signUpTongInfos.clear()
		#self.tongItemList.clear()

	def onSendMail(self, cmd, *callbackArgs):
		"""
		给参与活动帮会成员发邮件
		"""
		KBEngine.globalData["TongMgr"].onTongPlunderSendMail(self.getSignUpTongDBIDList())

	def onLockTongShopStart(self, cmd, *callbackArgs):
		"""
		锁定帮会商店开始
		"""
		KBEngine.globalData["TongMgr"].onLockTongShopStart(self.getSignUpTongDBIDList())

	def onLockTongShopEnd(self, cmd, *callbackArgs):
		"""
		锁定帮会商店结束
		"""
		KBEngine.globalData["TongMgr"].onLockTongShopEnd(self.getSignUpTongDBIDList())

	def onTongPlunderShopSellStart(self, cmd, *callbackArgs):
		"""
		帮会商店掠夺分页物品售卖开始
		"""
		KBEngine.globalData["TongMgr"].onTongPlunderShopSellStart(self.getSignUpTongDBIDList())

	def onTongPlunderShopSellEnd(self, cmd, *callbackArgs):
		"""
		帮会商店掠夺分页物品售卖结束
		"""
		KBEngine.globalData["TongMgr"].onTongPlunderShopSellEnd(self.getSignUpTongDBIDList())

		#这个时候再清除数据
		self.signUpTongInfos.clear()
		self.tongItemList.clear()
		
	def reqeustSetTongPlunderEnterStatus(self, status, delayTime):
		"""
		define method
		"""
		if delayTime > 0:
			self.addTimerCallBack(delayTime, "setTongPlunderEnterStatus", (status,))
		else:
			KBEngine.globalData["TongPlunderManager_Enter_Status"] = status
		
	def setTongPlunderEnterStatus(self, status):
		"""
		"""
		KBEngine.globalData["TongPlunderManager_Enter_Status"] = status
		
	def onPlayerLeaveSpace(self, playerDBID):
		"""
		define method
		玩家主动离开
		"""
		if playerDBID not in self.leaveSpacePlayerInfos:
			self.leaveSpacePlayerInfos.append(playerDBID)
			
	def onReviveNumUseup(self, playerDBID):
		"""
		define method
		玩家因死亡次数已达最大值而被传送出副本
		"""
		if playerDBID not in self.reviveNumUseupPlayerInfos:
			self.reviveNumUseupPlayerInfos.append(playerDBID)
			
	def onActivityGetTheResult(self, attackTongDBID, protectTongDBID):
		"""
		define method
		得出胜负结果
		"""
		self.getTheResultTongList.append(attackTongDBID)
		self.getTheResultTongList.append(protectTongDBID)

	def getTongItem(self, tongDBID):
		"""
		根本tongDBID获取帮会的数据
		"""
		for tongItem in self.tongItemList:
			if tongItem.isInTongItem(tongDBID):
				return tongItem
		return None

	def getSignUpTongDBIDList(self):
		"""
		获取参与活动的帮会的dbid
		"""
		tempDBIDList = []
		for tongInfo in self.signUpTongInfos:
			tempDBIDList.append(tongInfo["attackTongInfo"]["dbid"])
			tempDBIDList.append(tongInfo["protectTongInfo"]["dbid"])

		return tempDBIDList

	def signUpActivity(self, attackTongInfo, protectTongInfo):
		#def signUpActivity(self, attackTongDBID, protectTongDBID, attackTongLevel, protectTongLevel):
		"""
		define method

		帮会报名
		"""
		if KBEngine.globalData["TongPlunderManager_Status"] != csdefine.TONG_PLUNDER_ACTIVITY_STATUS_SIGNUP:
			return

		attackTongDBID = attackTongInfo["dbid"]
		protectTongDBID = protectTongInfo["dbid"]

		#如果已有报名数据，清除旧数据，用新数据，只有活动期间重启才会出现此情况
		infos = []
		isSignUp = False
		for tongInfo in self.signUpTongInfos:
			if tongInfo["attackTongInfo"]["dbid"] == attackTongDBID or tongInfo["protectTongInfo"]["dbid"] == protectTongDBID:
				infos.append(tongInfo)

		for info in infos:
			if info in self.signUpTongInfos:
				self.signUpTongInfos.remove(info)

		attackTongItem = self.getTongItem(attackTongDBID)
		protectTongItem = self.getTongItem(protectTongDBID)
		if attackTongItem or protectTongItem:
			if attackTongItem in self.tongItemList:
				self.tongItemList.remove(attackTongItem) #attackTongItem和protectTongItem可能是同一个
			if protectTongItem in self.tongItemList:
				self.tongItemList.remove(protectTongItem)

		tongItem = TongItem(attackTongInfo, protectTongInfo)
		self.tongItemList.append(tongItem)

		tempInfo = {}
		tempInfo["attackTongInfo"] = attackTongInfo
		tempInfo["protectTongInfo"] = protectTongInfo
		self.signUpTongInfos.append(tempInfo)

		KBEngine.globalData["TongMgr"].onTongPlunderSignUpSuccess(attackTongDBID, protectTongDBID)	

	def onSureMember(self, belongSide, tongDBID, members):
		"""
		define method

		确认参与活动帮会活动人员
		"""
		tongItem = self.getTongItem(tongDBID)
		if not tongItem:
			KBEDebug.ERROR_MSG("tong dbid(%s) has not sign up active" % tongDBID)
			return 

		tongItem.setTongMembers(belongSide, members)
		
	def enterTongPlunderSpace(self, playerMB, playerDBID, tongDBID):
		"""
		define method

		请求进入帮会掠夺战副本
		"""
		if not playerMB: #
			return

		if KBEngine.globalData["TongPlunderManager_Status"] != csdefine.TONG_PLUNDER_ACTIVITY_STATUS_START:
			return

		tongItem = self.getTongItem(tongDBID)
		if not tongItem:
			#KBEDebug.ERROR_MSG("tong dbid(%s) not sign up activity" % tongDBID)
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_TONG_NOT_SIGN_UP_ACTIVE, "")
			return
			
		if tongDBID in self.getTheResultTongList:
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_ACTIVITY_END, "")
			return
		
		if playerDBID in self.reviveNumUseupPlayerInfos:
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_ENTER_NUM_USE_UP, "")
			return
			
		if playerDBID in self.leaveSpacePlayerInfos:
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_ENTER_NUM_USE_UP, "")
			return
			
		if not tongItem.isInMembers(playerDBID):
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_CAN_NOT_ENTER, "")
			return
			
		if KBEngine.globalData["TongPlunderManager_Enter_Status"] == csdefine.TONG_PLUNDER_ACTIVITY_STATUS_CAN_NOT_ENTER:
			playerMB.client.statusMessage(csstatus.TONG_PLUNDER_ENTER_TIME_OUT, "")
			return
			
		params = {}
		params["spaceKey"] = str(tongDBID)
		params["belongType"] = csdefine.SPACE_BELONG_TONG
		params["playerDBID"] = playerDBID
		params["attackTongInfo"] = tongItem.getAttackTongInfo()
		params["protectTongInfo"] = tongItem.getProtectTongInfo()
		playerMB.gotoSpace(TONG_PLUNDER_COPY_SPACE_NAME, Math.Vector3(0.0, 0.0, 0.0), Math.Vector3(0.0, 0.0, 0.0), params)
