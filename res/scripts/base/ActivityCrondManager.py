# -*- coding: utf-8 -*-
import time, datetime

import KST
import KBEngine
import KBEDebug

import Const
import csdefine
from Scheme import Scheme
from CoreObject import MgrPersistentObject
from ConfigObject.Crond.CrondDatas import CrondDatas

g_CrondDatas = CrondDatas.instance()

#活动提醒
REMIND_BEFORE_FIVE_MINUTE = 5 	#提前5分钟
REMIND_BEFORE_TEN_MINUTE = 10	#提前10分钟
REMIND_BEFORE_HALF_HOUR = 30 	#提前30分钟

#活动状态
ACTIVE_STATUS_ACTIVATING	= 0	#正在进行
ACTIVE_STATUS_END			= 1	#已结束			
ACTIVE_STATUS_NOT_START 	= 2	#未开始
ACTIVE_STATUS_ALL_DAY		= 3	#全天开放

class ActivityData:
	"""
	活动数据
	"""
	def __init__(self, scriptID):
		"""
		"""
		self.scriptID = scriptID
		self.crondList = []
		
	def getDict(self):
		"""
		"""
		table = []
		for crond in self.crondList:
			table.append({
				"status" 		: crond["status"],
				"timeTxt" 		: crond["timeTxt"],
				"nextStartTime" : str(crond["nextStartTime"]), 
			})
		
		return {
			"scriptID"	: self.scriptID,
			"crondList"	: table,
		}
		
class ActivityCrondManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	活动日程管理器
	"""
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.todayDatas = {}			#今天的活动
		self.nextSixDayDatas = []		#一周活动数据（不包括今天的活动,剩下六天）
		
		self.loadActivityDatas()
		self.loadStartActivities()
		self.loginFixedUpdate()
		self.registerCrond()
		self.onCompleteInit()
		
	def registerCrond( self ):
		"""
		将活动key 注册到Crond中
		"""
		taskEvents = {
			"ActivityCrondManager_update"		: "onUpdate",
			"ActivityCrondManager_remind"		: "onRemind",
			"ActivityCrondManager_onStart"		: "onStart",
			"ActivityCrondManager_onEnd"		: "onEnd",
			"ActivityCrondManager_onNotice"		: "onNotice",
			"ActivityCrondManager_onOpen"		: "onActivityOpen",
			"ActivityCrondManager_onFixedUpdate": "onFixedUpdate",
		}
		for taskName, callbackName in taskEvents.items():
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
				KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, callbackName, -1, (scriptID,) )
		
		#活动提醒
		for scriptID, cmdList in g_CrondDatas.getRemindTaskCmds():
			for cmd, t in cmdList:
				KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, "onRemind", -1, (scriptID, t,) )
		
	def loadActivityDatas( self ):
		"""
		加载所有活动数据
		"""
		#获取从今天开始一周的活动
		now = time.time()
		for index in range(7):
			t = now + index * 24 * 60 * 60
			year, month, day, hour, minute, second, wday = time.localtime( t )[:7]
			dct = self.getActivitiesByDay(now, year, month, day)
			
			if index == 0:
				#单独记录方便处理，另外界面一般打开的话是当天的活动，可少发送一些数据
				self.todayDatas = dct
				#更新该活动的令牌
				for activityid in self.todayDatas.keys():
					KBEngine.baseAppData[csdefine.ACTIVE_PRE_STR + activityid] = str(KBEngine.genUUID64())
				break
			#else:
			#	#后续六天的活动数据直接打包好，因为不会发生变化，减少打包流程
			#	table = [ activity.getDict() for scriptID, activity in dct.items()]
			#	datas = {"table": table, "month" : str(month), "day" : str(day), "wday" : str(wday)}
			#	self.nextSixDayDatas.append(datas)
		
		#生成令牌，标记这次更新
		KBEngine.baseAppData[csdefine.ACTIVE_KEY_ID] = str(KBEngine.genUUID64())
		
	def getActivitiesByDay(self, now, year, month, day):
		"""
		"""
		dct = {}
		hour = 0
		minute = 0
		startT = int( time.mktime( ( year, month, day, 0, 0, 0, 0, 0, 0 ) ) )
		endT = int( time.mktime( ( year, month, day, 24, 0, 0, 0, 0, 0 ) ) )
		
		activityCronds = g_CrondDatas.getAllActivities()
		for scriptID, crondDct in activityCronds.items():
			activity = ActivityData(scriptID)
			cronds = crondDct.get("activityTimes", [])
			if len(cronds) <= 0:	#没有配置的话，那就是全天开放
				timeTxt	= "全天开放"
				temp = {
					"status" 		: ACTIVE_STATUS_ALL_DAY,
					"timeTxt" 		: timeTxt,
					"nextStartTime" : 0, 
					"startcmd" 		: "",
					"endcmd"		: "",
				}
				activity.crondList.append(temp)
				dct[scriptID] = activity
				continue
			
			#跟柳爷确认不需要支持跨天的活动
			data = {}
			for crondList in cronds:
				if len(crondList) != 2:
					KBEDebug.ERROR_MSG("crond error %s:%s" %(scriptID, crondList))
					return
					
				cmds = []
				for crondID in crondList:
					cmd = self.getCmdByCrondID(crondID)
					if cmd is None: return
					cmds.append(cmd)
				
				schemeTest1 = Scheme( )
				schemeTest1.init(cmds[0])
				nextStartTime = schemeTest1.calculateNext( year, month, day, hour, minute )
				schemeTest2 = Scheme(  )
				schemeTest2.init(cmds[1])
				nextEndTime = schemeTest2.calculateNext( year, month, day, hour, minute )
				timeTxt = "{}-{}".format(time.strftime("%H:%M", time.localtime(nextStartTime)), time.strftime("%H:%M", time.localtime(nextEndTime)))
				
				#意味着不是今天的活动
				if nextStartTime >= endT:
					continue
				
				temp = {
					"status" 		: ACTIVE_STATUS_NOT_START,
					"timeTxt" 		: timeTxt,
					"nextStartTime" : nextStartTime, 
					"startcmd" 		: cmds[0],
					"endcmd" 		: cmds[1],
				}
				
				if nextStartTime > now:
					pass		#未开始
				elif nextEndTime <= now:
					temp["status"] = ACTIVE_STATUS_END 	#已结束
				else:
					temp["status"] = ACTIVE_STATUS_ACTIVATING #正在进行
				activity.crondList.append(temp)
				dct[scriptID] = activity
		
		return dct
		
	def loadStartActivities(self):
		"""
		加载当前应该处于开启状态的活动(包括处于报名开启或者活动正式开启)
		"""
		if self.logoutTime <= 0:
			return
		
		now = int(time.time())
		year, month, day, hour, minute, second, wday = time.localtime( self.logoutTime )[:7]
		activityCronds = g_CrondDatas.getAllActivities()
		for scriptID, crondDct in activityCronds.items():
			#判断当前是否需要开启报名
			signTimes = crondDct.get("signTimes", [])
			for signTime in signTimes:
				if self.isStartTime(signTime[0], signTime[1], year, month, day, hour, minute, now):
					KBEngine.globalData["CrondManager"].callSchemeByScriptID(signTime[0])	#默认第一条指令未开启报名的指令
		
			#判断当前是否需要开启活动
			openTimes = crondDct.get("openTimes", [])
			for openTime in openTimes:
				if self.isStartTime(openTime[0], openTime[1], year, month, day, hour, minute, now):
					KBEngine.globalData["CrondManager"].callSchemeByScriptID(openTime[0])	#默认第一条指令为开启的指令
					
			#开启活动分配方式设置
			openSetAllocationTimes = crondDct.get("openSetAllocationTimes", [])
			if len(openSetAllocationTimes):
				if self.isStartTime(openSetAllocationTimes[0], openSetAllocationTimes[1], year, month, day, hour, minute, now):
					self.onActivityOpen("", openSetAllocationTimes[0])
		
	def isStartTime(self, startID, endID, year, month, day, hour, minute, now):
		"""
		"""
		startCmd = self.getCmdByCrondID(startID)
		endCmd = self.getCmdByCrondID(endID)
		if startCmd is None or endCmd is None:
			return False
		
		schemeTest1 = Scheme( )
		schemeTest1.init(startCmd)
		nextStartTime = schemeTest1.calculateNext( year, month, day, hour, minute )
		schemeTest2 = Scheme( )
		schemeTest2.init(endCmd)
		nextEndTime = schemeTest2.calculateNext( year, month, day, hour, minute )
		KBEDebug.DEBUG_MSG("%s -- %s -- %s -- %s -- %s" %(startCmd, endCmd, time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(nextStartTime)), time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(nextEndTime)), time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(now))))
		#下一次开启的时间滞后于下一次关闭的时间
		#下一次的关闭时间滞后于当前时间
		#那么现在应该是处于开启的状态
		if nextStartTime > nextEndTime and nextEndTime > now:
			return True
		
		return False
		
	def getCmdByCrondID(self, crondID):
		"""
		"""
		crond = g_CrondDatas.getCrondByCrondID(crondID)
		if not crond:
			KBEDebug.ERROR_MSG("not found crond %s:%s" %(scriptID, crond))
			return None
		
		return crond["cmd"]
		
	def onRemind(self, cmd, scriptID, t):
		"""
		活动提醒
		"""
		if t == REMIND_BEFORE_FIVE_MINUTE:
			KST.g_baseAppEntity.globalBroadcastActivityRemind(scriptID, Const.CROND_BEFORE_FIVEMINUTE_REMIND)
		elif t== REMIND_BEFORE_TEN_MINUTE:
			KST.g_baseAppEntity.globalBroadcastActivityRemind(scriptID, Const.CROND_BEFORE_TENMINUTE_REMIND)
		elif t == REMIND_BEFORE_HALF_HOUR:
			KST.g_baseAppEntity.globalBroadcastActivityRemind(scriptID, Const.CROND_BEFORE_HALFHOUR_REMIND)
			
	def onUpdate(self, cmd, scriptID):
		"""
		零点更新活动
		"""
		#过了一天的话，重新加载下本周的活动
		self.todayDatas.clear()
		self.nextSixDayDatas.clear()
		self.loadActivityDatas()
		
	def onStart(self, cmd, scriptID):
		"""
		活动点亮
		"""
		activityid = g_CrondDatas.getActivityIDByCrondID(scriptID)
		if activityid is None:
			KBEDebug.ERROR_MSG("crondid %s not found activityid" %(scriptID))
			return
		
		if activityid not in self.todayDatas:
			KBEDebug.ERROR_MSG("not found activity(%s)" %(activityid))
			return
		
		for crond in self.todayDatas[activityid].crondList:
			if crond["startcmd"] == cmd:
				crond["status"] = ACTIVE_STATUS_ACTIVATING
				break
		
		startRemind = g_CrondDatas.isStartRemind(activityid) #发送活动开始提醒
		if startRemind: KST.g_baseAppEntity.globalBroadcastActivityRemind(scriptID, Const.CROND_BEFORE_OPENING_REMIND)
		KBEngine.baseAppData[csdefine.ACTIVE_PRE_STR + activityid] = str(KBEngine.genUUID64()) #更新该活动的令牌
		
	def onEnd(self, cmd, scriptID):
		"""
		活动关闭
		"""
		activityid = g_CrondDatas.getActivityIDByCrondID(scriptID)
		if activityid is None:
			KBEDebug.ERROR_MSG("crondid %s not found activityid" %(scriptID))
			return
		
		if activityid not in self.todayDatas:
			KBEDebug.ERROR_MSG("not found activity(%s)" %(activityid))
			return
		
		for crond in self.todayDatas[activityid].crondList:
			if crond["endcmd"] == cmd:
				crond["status"] = ACTIVE_STATUS_END
				break
		
		#更新该活动的令牌
		KBEngine.baseAppData[csdefine.ACTIVE_PRE_STR + activityid] = str(KBEngine.genUUID64())
		
	def onNotice(self, cmd, scriptID):
		"""
		发送活动公告
		"""
		config = g_CrondDatas.getCrondByCrondID(scriptID)
		if config is None: return
		KST.g_baseAppEntity.globalWold( int(config["param1"]), "" )
		
	def onActivityOpen(self, cmd, scriptID):
		"""
		开启/关闭活动
		针对没有活动管理器的活动
		"""
		config = g_CrondDatas.getCrondByCrondID(scriptID)
		if config is None: return
		
		if not config["param1"]: return
		temp = config["param1"].split("|")
		KBEngine.globalData[temp[0]] = temp[1]

#--------------------------------------------获取数据------------------------------------------------------			
	def requestTodayActivitiesData( self, playerMB ):
		"""
		<Define method>
		玩家请求服务器活动数据
		"""
		table = []
		tokenDict = {}
		for activityid, activity in self.todayDatas.items():
			table.append(activity.getDict())
			token = KBEngine.baseAppData.get(csdefine.ACTIVE_PRE_STR + activityid, None)
			if token:tokenDict[activityid] = token
		
		year, month, day, hour, minute, second, wday = time.localtime( time.time() )[:7]
		datas = {"table": table, "month" : str(month), "day" : str(day), "wday" : str(wday)}
		token = KBEngine.baseAppData[csdefine.ACTIVE_KEY_ID]
		playerMB.recviveTodayActivitiesData(datas, tokenDict, token)
		
	def requestUpdateTodayActivitiesData(self, playerMB, activityIDList):
		"""
		<Define method>
		玩家请求更新服务器活动数据
		"""
		table = []
		tokenDict = {}
		for activityid in activityIDList:
			if activityid not in self.todayDatas:
				continue
			
			activity = self.todayDatas[activityid]
			table.append(activity.getDict())
			
			token = KBEngine.baseAppData.get(csdefine.ACTIVE_PRE_STR + activityid, None)
			if token:tokenDict[activityid] = token
		
		year, month, day, hour, minute, second, wday = time.localtime( time.time() )[:7]
		datas = {"table": table, "month" : str(month), "day" : str(day), "wday" : str(wday)}
		playerMB.recviveUpdateTodayActivitiesData(datas, tokenDict)
		
	def requestWeekActivitiesData(self, playerMB):
		"""
		<Define method>
		获取一周的活动（除当天）
		"""
		token = KBEngine.baseAppData[csdefine.ACTIVE_KEY_ID]
		playerMB.receiveWeekActivitiesData(self.nextSixDayDatas, token)
			
#------------------------------------ 定点更新 ---------------------------------------------------------
	def loginFixedUpdate(self):
		"""
		"""
		for fixedTimeType in csdefine.FIXED_UPDATE_TOKEN_LIST:
			key = csdefine.FIXED_UPDATE_KEY + str(fixedTimeType)
			KBEngine.globalData[key] = self.tokenDict.get(key, "")
			
		nowTime = time.time()
		lastdata = datetime.datetime.fromtimestamp(self.logoutTime)
		nowdata =  datetime.datetime.fromtimestamp(time.time())
		
		for scriptID, crond in g_CrondDatas.getAllCronds().items():
			if crond["taskName"] == "ActivityCrondManager_onFixedUpdate".lower():
				#不支持X月X号更新, time:（周 月 日 时 分）
				if crond["time"][1] != "*" or crond["time"][2] != "*":	
					KBEDebug.ERROR_MSG("fixed update config error %s" %(scriptID))
					return
				
				key = csdefine.FIXED_UPDATE_KEY + str(crond["param1"])
				#服务器第一起来的时候
				if self.logoutTime == 0:
					self.onUpdateToken(key)
					continue
				
				#日更新
				if crond["time"][0] == "*":	
					#已经超过24小时了，立刻更新令牌
					if nowTime - self.logoutTime >= 86400:
						self.onUpdateToken(key)
					else:
						#服务器关闭的过程中有一次更新
						tempdata = self.findNextTimeOn24Hour(lastdata, hour = int(crond["time"][3]), minute = int(crond["time"][4]), second = 0, microsecond =0 )
						if lastdata <= tempdata and tempdata <= nowdata:
							self.onUpdateToken(key)
				else: #周更新
					#超过一个星期
					if nowTime - self.logoutTime >= 86400 * 7:
						self.onUpdateToken(key)
					else:
						schemeTest = Scheme( )
						schemeTest.init(crond["cmd"])
						year, month, day, hour, minute = time.localtime( self.logoutTime )[:7]
						nextTime = schemeTest.calculateNext( year, month, day, hour, minute )
						
						#服务器关闭过程中有一次更新
						if nextTime <= nowTime:
							self.onUpdateToken(key)
		
	def findNextTimeOn24Hour(self, logoutData, hour, minute, second, microsecond):
		"""
		寻找下一次最近的时间点
		"""
		todayData = logoutData.replace(hour = hour, minute = minute, second = second, microsecond = microsecond )
		if todayData < logoutData:
			return todayData + datetime.timedelta(1)
		return todayData
		
	def onFixedUpdate(self, cmd, scriptID):
		"""
		定点更新玩家身上的数据
		"""
		crond = g_CrondDatas.getCrondByCrondID(scriptID)
		if crond is None: return
		fixedTimeType = int(crond["param1"])
		key = csdefine.FIXED_UPDATE_KEY + str(fixedTimeType)
		self.onUpdateToken(key)
		KST.g_baseAppEntity.broadcastFixedTime(fixedTimeType, self.tokenDict[key])
		
	def onUpdateToken(self, key):
		"""
		"""
		self.tokenDict[key] = str(KBEngine.genUUID64())
		KBEngine.globalData[key] = self.tokenDict[key]
		KBEDebug.INFO_MSG("onFixedUpdate %s %s" %(key, self.tokenDict[key]))
		
	def onDestroy(self):
		"""
		"""
		self.logoutTime = time.time()