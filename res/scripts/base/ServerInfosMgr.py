# -*- coding: utf-8 -*-
import urllib, json, platform, os, time

import KST
import KBEngine
from KBEDebug import *

import csdefine
import Utils
import Settings
from Functions import Functor
from CoreObject import MgrObject
from Extra import KBEExtend


#连接超时时间
CONNECT_TIMEOUT = 3
#请求超时时间
REQUEST_TIMEOUT = 5


class ServerInfosMgr( MgrObject.MgrObject ):
	def __init__( self  ):
		MgrObject.MgrObject.__init__( self )
		
		self.timeoutID = 0			#初始化超时时间
		self.startProcess = 0		#初始化进度
		
		self.sysStages = []
		self.curSysStage = -1		#当前正在初始化的阶段
		self.curInitSys = set()		#当前正在初始化的系统
		self.curHasInitSys = set()	#当前已经初始化的系统
		
		self.serverInfos = {}
		self.__serverInfosOutputTimeVal = 0
		self.__calculateServerInfoTimeVal = 0
		
		self.__initflag = False
		
	def init( self ):
		"""
		"""
		self.initSysEntity()
		self.addTimeOutTimer()
	
	#----------------------server start status----------------------------------------------
	def addTimeOutTimer( self ):
		"""
		"""
		if self.timeoutID > 0: return
		self.timeoutID = self.addTimerCallBack( 5 * 60, "onTimeOut", () )
		
	def initSysEntity( self ):
		"""
		"""
		self.sysStages = list(g_ServerEntity.keys())
		self.sysStages.sort()
		if len(self.sysStages) <= 0:
			self.setStartProcess(1.0)
			return
		
		self.startSysEntity()
		
	def startSysEntity( self ):
		"""
		"""
		#如果已经是最后阶段了并且该阶段系统已经初始化完毕
		if len(self.sysStages) <= 0 and self.isSysStageInitComplete():
			self.setStartProcess(1.0)
			return
		
		#当前已经是最后一个阶段的系统初始化了
		if len(self.sysStages) <= 0:
			return
		
		#当前还有正在进行初始化的系统
		if len(self.curInitSys) > 0 and not self.isSysStageInitComplete():
			return
		
		self.curHasInitSys = set()
		self.curSysStage = self.sysStages.pop(0)
		sysEntityDct = g_ServerEntity[self.curSysStage]
		self.curInitSys = set(list(sysEntityDct.keys()))
		
		for key, value in sysEntityDct.items():
			if value[0]:
				KBEExtend.CreateMgrFromDB(key)
			else:
				KBEngine.createEntityLocally(key, value[1])
		
		#如果开启了测试标记并且不等待系统初始化
		if Settings.test_flag and not Settings.wait_system_init:
			self.curHasInitSys = self.curInitSys
			self.startSysEntity()
		
	def isSysStageInitComplete( self ):
		"""
		"""
		return len(list(self.curHasInitSys ^ self.curInitSys)) == 0
		
	def isAllSysInitComlete( self ):
		"""
		"""
		return len(self.sysStages) <= 0 and self.isSysStageInitComplete()
		
	def registerReadySysEntity( self, sysEntity ):
		"""
		"""
		if sysEntity in self.curHasInitSys:
			return
		
		self.curHasInitSys.add(sysEntity)
		self.startSysEntity()
		
	#-----------------------------server start process-----------------------------------------
	def setStartProcess(self, value):
		"""
		"""
		self.startProcess = value

	def getStartProcessPCT( self ):
		"""
		获取启动的百分比
		"""
		return self.startProcess
		
	def onTimeOut( self ):
		"""
		"""
		self.printLog()
		self.clearTimer()
		self.addTimeOutTimer()

	def clearTimer(self):
		"""
		"""
		if self.timeoutID > 0:
			self.popTimer(self.timeoutID)
			self.timeoutID = 0
			
	def printLog( self ):
		"""
		"""
		if self.isAllSysInitComlete():
			if platform.system() == "Windows":
				os.system('echo ---- Server Init over!!! ----')
			else:
				INFO_MSG("---- SERVER INIT OVER ------")
		else:
			lst = list(self.curHasInitSys ^ self.curInitSys)
			ERROR_MSG("System stage[%d], init system [%s]" %(self.curSysStage, lst))
			
	#----------------------------------------------------------------------
	def onServerReady(self):
		"""
		开服
		"""
		self.setServerFlag(True)
		self.calculateServerInfo()
		self.serverInfosOutputStart()
		
	def onServerShutDown(self):
		"""
		关服
		"""
		self.setServerFlag(False)
	
	def setServerFlag(self, flag):
		"""
		"""
		if flag:
			self.clearTimer()
			self.sendServerState(1)
			self.printLog()
			KBEngine.globalData["LoginAttemperMgr"].updateLoginInfoToSrv()
		else:
			self.sendServerState(0)

	def sendServerState(self, state):
		"""
		"""
		params = {
			"ServerName"	: Settings.cs_server_name,
			"ServerState"	: str(state),
		}

		#计算签名
		sign = Utils.SecretMD5Sign(Settings.cs_secret_key, ("ServerName",params["ServerName"]), ("ServerState", params["ServerState"]))
		params["sign"] = sign
		
		postdata = urllib.parse.urlencode(params)
		full_uri = "%s?%s" % (Settings.cs_login_addr, postdata)
		#ERROR_MSG(full_uri)
		
		# 向服务器发送数据
		from tornado.simple_httpclient import SimpleAsyncHTTPClient
		client = SimpleAsyncHTTPClient()
		client.fetch(full_uri, Functor(self.responseHandler, state), True, method="POST", allow_nonstandard_methods=True, connect_timeout = CONNECT_TIMEOUT, request_timeout = REQUEST_TIMEOUT)
		KBEngine.baseAppData[csdefine.SERVER_INIT_STATE] = state
	
	def responseHandler(self, state, response):
		"""
		"""
		if self.isDestroyed: 
			return
		
		if response.error:
			if Settings.test_flag:
				WARNING_MSG("send server state[{}] error, {}".format(state, response.error))
				return
			
			ERROR_MSG("send server state[{}] error, {}".format(state, response.error))
			#如果是开服的话则重试;关服的不重试是因服务器关闭不会等待
			if state: self.addTimerCallBack( 10, "sendServerState", (state,) )
			return
		
		#取出数据
		body = response.body.decode( "utf-8" )
		body = json.loads( body )
		result = body.get("result", False)
		if not result:
			ERROR_MSG("send Server State[{}] error".format(state))
			#如果是开服的话则重试；关服的不重试是因服务器关闭不会等待
			if state: self.addTimerCallBack( 10, "sendServerState", (state,) )
	
	#------------------------------  DEBUG LOG  ----------------------------------------
	def serverInfosOutputStart( self ):
		if not Settings.ServerTest or Settings.record_Process_Info_Time  <= 0:
			return
		
		#开始广播进程输出日记
		self.addTimerRepeatExt( 0, Settings.record_Process_Info_Time , 'serverInfosOutputStartLoop', () )
	
	def serverInfosOutputStartLoop( self ):
		#广播进程日志输出循环
		KST.OutputProcessInfos() #本进程的话，好像不会调用onGlobalData的回调函数
		KBEngine.globalData[csdefine.GLOBAL_CHANNEL_KEY_OUTPUT_PROCESS_INFOS] = str(KBEngine.genUUID64())
		
	def calculateServerInfo( self ):
		"""
		增加统计服务器数据
		"""
		if not Settings.test_flag or Settings.culate_Server_Info_Time <= 0:
			return
		
		self.addTimerRepeatExt( 0, Settings.culate_Server_Info_Time, 'onCalculateServerInfoLoop', () )
		
	def onCalculateServerInfoLoop(self):
		"""
		"""
		KBEngine.globalData[ csdefine.GLOBAL_CHANNEL_KEY_CALCULATE_SERVER_INFO ] = str(KBEngine.genUUID64())
		if self.__calculateServerInfoTimeVal:
			self.popTimer(self.__calculateServerInfoTimeVal)
			self.__calculateServerInfoTimeVal = 0
		self.__calculateServerInfoTimeVal = self.addTimerCallBack( 30, "onCalculateServerInfo", () )
		
	def recvServerInfo(self, cid, useSkillTimes, createSpaceTimes, destroySpceTimes, createEntityTimes, destroyEntityTimes, useSkillTimes_list, createEntityTimes_list, destroyEntityTimes_list):
		"""
		define method
		收到某个cellapp的数据
		"""
		self.serverInfos[cid] = (int(useSkillTimes), int(createSpaceTimes), int(destroySpceTimes), int(createEntityTimes), int(destroyEntityTimes), useSkillTimes_list, createEntityTimes_list, destroyEntityTimes_list)
		
	def onCalculateServerInfo(self):
		"""
		"""
		self.popTimer(self.__calculateServerInfoTimeVal)
		self.__calculateServerInfoTimeVal = 0
		
		_useSkillTimes = 0
		_createSpaceTimes = 0
		_destroySpceTimes = 0
		_createEntityTimes = 0
		_destroyEntityTimes = 0
		_useSkillTimes_list = [0, 0]
		_createEntityTimes_list = [0 for i in range(csdefine.ENTITY_FLAG_MAX)]
		_destroyEntityTimes_list = [0 for i in range(csdefine.ENTITY_FLAG_MAX)]
		
		for v in self.serverInfos.values():
			_useSkillTimes += v[0]
			_createSpaceTimes += v[1]
			_destroySpceTimes += v[2]
			_createEntityTimes += v[3]
			_destroyEntityTimes += v[4]
			
			_useSkillTimes_list[0] += v[5][0]
			_useSkillTimes_list[1] += v[5][1]
			
			for index, value in enumerate(v[6]):
				if index >= len(_createEntityTimes_list):
					continue
				_createEntityTimes_list[index] += value
				
			for index, value in enumerate(v[7]):
				if index >= len(_destroyEntityTimes_list):
					continue
				_destroyEntityTimes_list[index] += value
		
		msg_list = []
		if not self.__initflag: 
			self.__initflag = True
			msg_list.append(['time', 'teleport space', 'use skill', 'create space', 'destroy space', 'create entity', 'destroy entity'])
		
		t = time.strftime("%Y/%m/%d-%H:%M", time.localtime(int(time.time())))
		temp_list = [t, str(KST.g_teleportTimes), str(_useSkillTimes), str(_createSpaceTimes), str(_destroySpceTimes), str(_createEntityTimes), str(_destroyEntityTimes)]
		temp_list.append(' ')
		temp_list.extend(_useSkillTimes_list)
		temp_list.append(' ')
		temp_list.extend(_createEntityTimes_list)
		temp_list.append(' ')
		temp_list.extend(_destroyEntityTimes_list)
		
		msg_list.append(temp_list)
		DEBUG_TO_CSV(msg_list)
		
		self.serverInfos = {}
		KST.resetTeleportTimes()
		

#待初始化的服务器系统	
g_ServerEntity = {
	1 : {
		#Mgrname				CreateFromDB	Params
		"KBEIOLoopEntity"		: ( False, 		{} ),
		"CrondManager"			: ( False, 		{} ),
		"GMToolsManager"		: ( False, 		{} ),
		"LoginAttemperMgr"		: ( False, 		{} ),
		"CrossServiceManager"	: ( False, 		{} ),
		"DropBoxManager"		: ( False, 		{} ),
	},
	
	2 : {
		#Mgrname					CreateFromDB	Params
		"SpawnManager"				: ( False, 		{} ),
		"ChatManager"				: ( False, 		{} ),
		"RelationManager"			: ( False, 		{} ),
		"TeamManager"				: ( False, 		{} ),
		"BunchSpaceManager"			: ( False, 		{} ),
	
		"AntiWallowBridge"			: ( False, 		{} ),
		"AntiWallowMgr"				: ( False, 		{} ),
		"MagicMazeSpaceManager"		: ( False, 		{} ),
		"CampActivityLingMaiMgr"	: ( False, 		{} ),
		"CampActivityFrozenFightMgr": ( False, 		{} ),
		"MailManager"				: ( False, 		{} ),
		"GameRankingManager"		: ( True, 		None ),
		"ShopManager"				: ( True, 		None ),
		"ShopMallManager"			: ( True, 		None ),
		"TongStarcraftManager"		: ( True, 		None ),
		"PersonStarcraftMgr"		: ( True,		None ),
		"StoreManager"				: ( True,		None ),
		"RareMonsterMgr"			: ( False, 		{} ),
		"TongStarcraftManager7904"	: ( False, 		{} ),
		"RingTaskSpaceMgr"			: ( False, 		{} ),
		"TongCampWarManager"		: ( False,		{} ),
		"CampFHLTCopyMgr"			: ( False, 		{} ),
	},
	
	3 : {
		#Mgrname					CreateFromDB	Params
		"TongMgr"					: ( False, 		{} ),
		"SpaceManager"				: ( False, 		{} ),
		"SpaceLunHuiMiJinMgr"		: ( True, 		None ),
		"TrainSoldierGroundManager"	: ( True,		None ),
		"ActivityBunchManager"		: ( False, 		{} ),
		"CampYXLMCopyMgr"			: ( False, 		{} ),
		"CrondTestMgr"				: ( False, 		{} ),
		"SparHunTingManager"		: ( False, 		{} ),
		"FastTeamMgr"				: ( False, 		{} ),
		"CampMgr"					: ( False, 		{} ),
		"GMNoticeManager" 			: ( False, 		{} ),
		"PointCardMgr" 				: ( False, 		{} ),
		"CampSGMZCopyMgr"			: ( False, 		{} ),
		"SpaceTongTianDaMgr"		: ( False, 		{} ),
		"CampActivityRandomFitMgr"	: ( False, 		{} ),
		"BHZBManager"				: ( True,		None ),
		"LbcMgr" 					: ( True, 		None ),
		"TongPlunderManager"		: ( True,		None ),
		"GCZManager"				: ( True, 		None ),
		"MsgLogMgr"					: ( False, 		{} ),
		"BattleActivityMgr"			: ( False, 		{} ),
	},

	4 : {
		"ActivityCrondManager"		: ( True, 		{} ),
	}
}
