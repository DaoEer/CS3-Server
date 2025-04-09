# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import time
import csconst
import csdefine
import json
import KST
from string import Template as STemplate
import LoadModule
from CoreObject.MgrPersistentObject import MgrPersistentObject
from ConfigObject.AntiWallowLoader import g_antiWallow


# --------------------------------------------------------------------
OLTIME_MINUTES		= 60 							# 在线时间分钟单位
OLTIME_HALF_LUCRE	= 3 * 60 * OLTIME_MINUTES		# 收益减半的在线时间点
OLTIME_NO_LUCRE		= 5 * 60 * OLTIME_MINUTES		# 零收益的在线时间点

NOTIFY_INTERVALS = {
	csdefine.WALLOW_STATE_COMMON	 : 60 * OLTIME_MINUTES,	# 正常游戏情况下，提示的时间间隔
	csdefine.WALLOW_STATE_HALF_LUCRE : 30 * OLTIME_MINUTES,	# 收益减半情况下，提示的时间间隔
	csdefine.WALLOW_STATE_NO_LUCRE	 : 15 * OLTIME_MINUTES,	# 零收益情况下，提示的时间间隔
	}

_stpNotify			= STemplate( "${accName}&${olState}&${olTime}\r\n" )	# 消息格式

# 验证服务器->游戏服务器的回复前缀：
_prefixRStart		= "0&1"												# 服务器启动回复前缀
_prefixRShut		= "0&2"												# 服务器关闭回复前缀
_prefixRLogin		= "0&3"												# 角色登录回复前缀
_prefixRLogout		= "0&4"												# 角色登出回复前缀

class AntiWallowMgr(MgrPersistentObject):
	""" 
	防沉迷检测
	本地服务器临时管理器
	用来模拟在线时间和离线时间
	"""
	def __init__(self):
		MgrPersistentObject.__init__( self )
		self.accountList = []
		self.accInfos = {}
		self.mark = {}
		self._start()
		self.onCompleteInit()

	def init(self):
		pass

	def _start(self):
		"""
		开始防沉迷
		"""
		self.accInfos = g_antiWallow.getAllData()
		isAntiWallow = self.accInfos["isAntiWallow"]
		if isAntiWallow:
			self.addTimerRepeat( csconst.ANTIWALLOWTICK, "onNotify", () )

	def onNotify( self, data = None) :
		"""
		间隔时间通知
		"""
		# -------------------------本地服务器模拟计算在线时间---------------------------------
		if not self.accountList:
			return
		if self.accInfos["role"] == {}:
			return
		if self.mark == {}:
			return
		for accName in self.accountList:
			state = self.accInfos["role"][accName]["olState"]
			self.accInfos["role"][accName]["olline"] += int(csconst.ANTIWALLOWTICK)

			if self.accInfos["role"][accName]["olline"] <= OLTIME_HALF_LUCRE:
				self.accInfos["role"][accName]["olState"] = csdefine.WALLOW_STATE_COMMON
			elif self.accInfos["role"][accName]["olline"] < OLTIME_NO_LUCRE:
				self.accInfos["role"][accName]["olState"] = csdefine.WALLOW_STATE_HALF_LUCRE
			else:
				self.accInfos["role"][accName]["olState"] = csdefine.WALLOW_STATE_NO_LUCRE

			if state != self.accInfos["role"][accName]["olState"]:
				self._sendDataToBridge(accName)

			oTime = self.accInfos["role"][accName]["olline"] + int(csconst.ANTIWALLOWTICK)
			if oTime % NOTIFY_INTERVALS[self.accInfos["role"][accName]["olState"]] == 0:
				self._sendDataToBridge(accName)

	def sendData(self, id, accName):
		"""
		添加要发送的标记
		"""
		self.mark[accName] = id

	def _sendDataToBridge(self, accName):
		"""
		发送数据
		"""
		accInfo = {
					"accName" : accName,
					"olState" : self.accInfos["role"][accName]["olState"],							
					"olTime" : self.accInfos["role"][accName]["olline"],
				}

		data = _stpNotify.substitute (accInfo)
		msg = "%s%s"%(_prefixRLogin, data)
		gwp = KBEngine.globalData["AntiWallowBridge"]
		gwp.onRespond( self.mark[accName], msg )
		self.mark.pop(accName)
		gwp.receiveData( None, accName )
	
	# ----------------------------------------------------------------
	# public
	# ----------------------------------------------------------------
	def onAccountLogin( self, accName ):
		"""
		defined.
		角色登录通知
		"""	
		if accName not in self.accountList:
			self.accountList.append(accName)

		if accName not in self.accInfos["role"]:
			self.accInfos["role"][accName] = {"accName" : accName, "olState" : 0, "olline" : 0, "offline":0, "lastline":0, "isAdult":0 }
		else:
			self.accInfos["role"][accName]["offline"] += (int(time.time()) - self.accInfos["role"][accName]["lastline"])

		if self.accInfos["role"][accName]["offline"] >= 3600 * 5:
			self.accInfos["role"][accName]["offline"] = 0
			self.accInfos["role"][accName]["olline"] = 0
			self.accInfos["role"][accName]["olState"] = 0

		self._sendDataToBridge(accName)
		
	def onAccountLogout( self, accName ):
		"""
		defined.
		角色登出通知
		"""
		if accName in self.accountList:
			self.accountList.remove(accName) 

		if accName in self.mark:
			self.mark.pop(accName)

		isAdult = 0
		if accName in self.accInfos["role"]:
			isAdult = self.accInfos["role"][accName]["isAdult"]

		self.accInfos["role"][accName]["lastline"] = int(time.time())
		if isAdult:				# 如果设置为成年账号则需要登出游戏，并将在线时间等设置为0
			self.accInfos["role"][accName] = {"accName" : accName, "olState" : 0, "olline" : 0, "offline":0, "lastline":0, "isAdult":isAdult }

		if "role" in self.accInfos:
			g_antiWallow.writeRoleData(self.accInfos["role"])

	def setRoleAdult(self,roleName, value ):
		if roleName in self.accInfos["role"]:
			self.accInfos["role"][roleName]["isAdult"] = value
			g_antiWallow.writeRoleData(self.accInfos["role"])

	def setRoleOnlineTime(self,roleName, t ):
		if roleName in self.accInfos["role"]:
			self.accInfos["role"][roleName]["olline"] = t
			g_antiWallow.writeRoleData(self.accInfos["role"])
			
	def setRoleOfflineTime(self,roleName, t ):
		if roleName in self.accInfos["role"]:
			self.accInfos["role"][roleName]["offline"] = t
			g_antiWallow.writeRoleData(self.accInfos["role"])
