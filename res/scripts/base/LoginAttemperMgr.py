# -*- coding: utf-8 -*-

import time, urllib, json

import Utils
import KST
import Const
import KBEngine
import Settings
import csdefine
from KBEDebug import *

from CoreObject import MgrPersistentObject
from tornado.simple_httpclient import SimpleAsyncHTTPClient


#销毁角色时间间隔	
TIMER_LOGOUT_ROLE_INTERVAL		= 0.1		
#更新角色登陆时长信息时间间隔
TIMER_UPDATE_LOGIN_INTERVAL		= 60

# 普通登录最大人数(config/ServerSettingConfig.json)
MAX_NORMAL_LOGIN_NUM = Settings.NormalLoginRole
# 绿色通道(额外)登录最大人数(config/ServerSettingConfig.json)
MAX_GREEN_LOGIN_NUM = Settings.GreenLoginRole

#连接超时时间
CONNECT_TIMEOUT = 3
#请求超时时间
REQUEST_TIMEOUT = 5
#更新时间间隔
UPDATE_LOGIN_ROLE_INFO_TIME = 3 * 60
class LoginAttemperMgr( MgrPersistentObject.MgrPersistentObject ):
	"""
	玩家登录调度管理器
	"""
	def __init__( self ):
		"""
		"""
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		
		#等待登出列表
		self.waitLogoutRoleQueue = [] 
		self.waitLogoutRoleDict = {} 
		#等待登出角色timerID
		self.checkLogoutTimerID = 0
		self.curHasLogoutRole = False
		
		#当前普通等待登录的玩家队列
		self.commonQueue = []
		#当前绿色通道等待登录的玩家队列
		self.greenQueue = []
		#当前已登录的账号
		self.loginAccoutDict = {}
		#记录账号登陆的时间
		self.loginTimeList = []
		self.updateLoginTimerID = 0
		
		self.addTimerRepeat( UPDATE_LOGIN_ROLE_INFO_TIME, "onUpdateLoginInfo", () )
		self.onUpdateLoginInfo()	#起来之后，更新一下服务器相关信息
		self.onCompleteInit()

	#--------------------------------------  下线排队  ---------------------------------------------------
	def requestLogoutRole( self, roleDBID, roleMB ):
		"""
		define method
		请求销毁角色
		"""
		if roleDBID in self.waitLogoutRoleDict:
			id = self.waitLogoutRoleDict[roleDBID].id
			#同一角色登陆了两次？？
			if id != roleMB.id:
				ERROR_MSG("Role[%d] has two entity, id:[%d],[%d]" %(roleDBID, id, roleMB.id))
				roleMB.recvLogout()	#不管怎样，这里先让其走下线流程
			return
		
		self.waitLogoutRoleQueue.append( roleDBID )
		self.waitLogoutRoleDict[roleDBID] = roleMB
		self.onCheckLogoutRole()
	
	def onCheckLogoutRole( self ):
		"""
		检查要登出角色
		"""
		if self.checkLogoutTimerID <= 0:
			self.checkLogoutTimerID = self.addTimerRepeat( TIMER_LOGOUT_ROLE_INTERVAL, "onLogoutRole", () )
		
		#没有人排队下线，记得清理定时器
		if len(self.waitLogoutRoleDict) <= 0:
			self.popTimer(self.checkLogoutTimerID)
			self.checkLogoutTimerID = 0
			return
		
		self.doLogoutRole()
		
	def doLogoutRole( self ):
		"""
		执行角色登出处理
		"""
		#当前有人在进行下线处理
		if self.curHasLogoutRole:
			return
		
		if len( self.waitLogoutRoleDict ) <= 0:
			self.waitLogoutRoleQueue = []
			return
		
		#如果出错的话，这里纠正一下相应的数据
		if len(self.waitLogoutRoleQueue) <= 0:
			self.waitLogoutRoleQueue = list(self.waitLogoutRoleDict.keys())
		
		while 1:
			roleDBID = self.waitLogoutRoleQueue.pop( 0 )
			if roleDBID not in self.waitLogoutRoleDict:
				continue
			
			self.curHasLogoutRole = True
			roleMB = self.waitLogoutRoleDict.pop( roleDBID )
			roleMB.destroyRole()
			break
	
	def onLogoutRole( self ):
		"""
		"""
		self.curHasLogoutRole = False
		self.onCheckLogoutRole()

	#--------------------------------------  上线排队  ---------------------------------------------------
	def _loginAccount( self ):
		"""
		调度一个正在等待的account登录
		""" 
		#登录人数已达上限了
		if len(self.loginAccoutDict) >= MAX_NORMAL_LOGIN_NUM + MAX_GREEN_LOGIN_NUM :
			return
			
		#先登录绿色通道的玩家
		if len(self.greenQueue):
			mb = self.greenQueue.pop(0)
			self.loginAccoutDict[mb.id] = mb
			self.loginTimeList.append(time.time())
			mb.loginRole()
			return
		
		#普通登录通道已经满了
		if len(self.loginAccoutDict) >= MAX_NORMAL_LOGIN_NUM:
			return
		
		#普通通道的玩家开始登录
		if len(self.commonQueue):
			mb = self.commonQueue.pop(0)
			self.loginAccoutDict[mb.id] = mb
			self.loginTimeList.append(time.time())
			mb.loginRole()
			return
		
	def requestLoginRole( self, isVIP, accountMB ):
		"""
		define method
		请求登录角色
		"""
		if accountMB.id in self.loginAccoutDict:
			ERROR_MSG("Account[%d] has login" %(accountMB.id))
			return
		
		if self._checkWaitLoginRole(accountMB):
			ERROR_MSG("Account[%d] has join login queue" %(accountMB.id))
			return
		
		waitQueue = self.greenQueue if isVIP else self.commonQueue
		waitQueue.append(accountMB)
		self._loginAccount()
		
		#如果要是队列中有人，肯定在队尾，刷新下最后面的
		if len(waitQueue):
			self._refleshWaitTime(waitQueue, len(waitQueue) - 1)
			if self.updateLoginTimerID == 0:
				self.updateLoginTimerID = self.addTimerRepeat( TIMER_UPDATE_LOGIN_INTERVAL, "onUpdateLogin", () )
				
	def onUpdateLogin( self ):
		"""
		"""
		if len(self.greenQueue) <= 0 and len(self.commonQueue) <= 0:
			self.popTimer(self.updateLoginTimerID)
			self.updateLoginTimerID = 0
			return
			
		#刷新下等待时间
		self._refleshWaitTime(self.commonQueue)
		self._refleshWaitTime(self.greenQueue)
		
	def removeLoginAcc( self, accountMB ):
		"""
		define method
		将账号移出已登录列表
		"""
		if accountMB.id in self.loginAccoutDict:
			self.loginAccoutDict.pop(accountMB.id)
			self._loginAccount()
			return
		
		ERROR_MSG("Account[%d] not in loginAccoutDict" %(accountMB.id))
		
	def removeLoginQueue( self, accountMB ):
		"""
		define method
		请求移除登录列表
		"""
		if accountMB.id in self.loginAccoutDict:
			self.loginAccoutDict.pop(accountMB.id)
			self._loginAccount()
			
			if accountMB.client:
				accountMB.client.OnCancelLoginQueue(False)
			return
		
		for mb in self.greenQueue:
			if mb.id == accountMB.id:
				self.greenQueue.remove(mb)
				
				if accountMB.client:
					accountMB.client.OnCancelLoginQueue(False)
				return
		
		for mb in self.commonQueue:
			if mb.id == accountMB.id:
				self.commonQueue.remove(mb)
				
				if accountMB.client:
					accountMB.client.OnCancelLoginQueue(False)
				return
	
	def _checkWaitLoginRole( self, accountMB ):
		"""
		检查等待登陆玩家是否已经请求过
		"""
		for mb in self.greenQueue:
			if mb.id == accountMB.id:
				return True
				
		for mb in self.commonQueue:
			if mb.id == accountMB.id:
				return True
				
		return False
	
	def _sendWaitTime( self, order, waitQueue, waitTime ):
		"""
		给帐号发送等待登录的时间
		"""
		try:
			waitCount = len( waitQueue )
			accountMB = waitQueue[order]
		except:
			return
		
		#通知客户端
		if hasattr(accountMB, "client") and accountMB.client:
			accountMB.client.ReceiveWattingInfo( order+1, waitTime, waitCount )

	def _getWaitTime( self ):
		"""
		获得平均需要等待的时间
		"""
		tempList = self.loginTimeList
		self.loginTimeList = []
		loginCheckTime = time.time() - Const.LOGIN_CALCULATE_TIME_INTERVAL	# 计算一段时间内登录个数的有效时刻
		for fTime in tempList:
			if loginCheckTime < fTime:
				self.loginTimeList.append( fTime )
		
		# Const.LOGIN_CALCULATE_TIME_INTERVAL时间段内登录的玩家个数
		count = len( self.loginTimeList )		
		if count == 0:		# 最近都没有成功的登录，那么返回一个比较长的时间
			count = 1

		# 需要等待的时间 = 平均登录时间×等待的序号
		return Const.LOGIN_CALCULATE_TIME_INTERVAL / count

	def _refleshWaitTime( self, waitQueue, fromOrder = 0 ):
		"""
		define method
		刷新等待时间
		"""
		waitCount = len( waitQueue )
		if waitCount == 0:
			return
		
		waitTime = self._getWaitTime()
		for i in range( waitCount - fromOrder ):
			index = i + fromOrder
			self._sendWaitTime( index, waitQueue, waitTime )
			
	def onUpdateLoginInfo( self ):
		"""
		更新登录信息，并将其推送到登录服务器
		"""
		self.updateLoginInfoToSrv()
		
	def updateLoginInfoToSrv( self ):
		"""
		"""
		#服务器还未初始化完毕的话不推送人数信息到web服务器
		state = KBEngine.baseAppData.get(csdefine.SERVER_INIT_STATE, False)
		if not state: return
		
		params = {
			"ServerName"	: Settings.cs_server_name,
			"RoleNum"		: str(len(self.loginAccoutDict)),
			"RoleMax"		: str(MAX_NORMAL_LOGIN_NUM),
		}
		
		#计算签名
		sign = Utils.SecretMD5Sign(Settings.cs_secret_key, ("ServerName",params["ServerName"]), ("RoleNum", params["RoleNum"]), ("RoleMax", params["RoleMax"]))
		params["sign"] = sign
		
		postdata = urllib.parse.urlencode(params)
		full_uri = "%s?%s" % (Settings.cs_login_addr, postdata)
		#ERROR_MSG(full_uri)
		
		# 向服务器发送数据
		client = SimpleAsyncHTTPClient()
		client.fetch(full_uri, self.responseHandler, True, method="POST", allow_nonstandard_methods=True, connect_timeout = CONNECT_TIMEOUT, request_timeout = REQUEST_TIMEOUT)
	
	def responseHandler(self, response):
		"""
		"""
		if self.isDestroyed: 
			return
		
		if response.error:
			if Settings.test_flag:
				WARNING_MSG(response.error)
				return
			
			ERROR_MSG(response.error)
			return
		
		#取出数据
		body = response.body.decode( "utf-8" )
		body = json.loads( body )
		result = body.get("result", False)
		if not result:  ERROR_MSG("Recv login information error, {%s}" %(body))
