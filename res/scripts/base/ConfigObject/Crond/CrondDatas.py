# -*- coding: utf-8 -*-
#




#"""
#任务计划时间数据
#"""

import KBEngine
import LoadModule
import csconst
import KBEDebug
import Functions
import time
import json

class CrondDatas:
	_instance = None
	def __init__( self, configPath1 = None, configPath2 = None ):
		"""
		构造函数。
		@param configPath:	配置文件路径
		@type  configPath:	string

		"""
		assert CrondDatas._instance is None		# 不允许有两个以上的实例
		self._crondDatas = {}
		self._taskName2id = {}
		self._activities = {}
		self._crondid2activityid = {}
		self._remindDatas = {}
		CrondDatas._instance = self
		self.load( configPath1, configPath2 )

	@staticmethod
	def instance():
		"""
		"""
		if CrondDatas._instance is None:
			CrondDatas._instance = CrondDatas()
		return CrondDatas._instance
		
	def load( self, configPath1, configPath2 ):
		"""
		加载任务计划时间数据。
		@param configPath1:	活动日程配置文件路径
		@type ： 	string
		@param configPath2：活动配置文件路径
		@type：		string
		"""
		if configPath1:
			sections = LoadModule.openJsonCfg( configPath1 )
			for section in sections:
				scriptID = section["scriptID"]
				taskName = section["key"].strip().lower()
				param1 	= section.get("param1", "").strip()
				param2 	= section.get("param2", "").strip()
				
				week 	= section["week"]
				month 	= section["month"]
				day 	= section["day"]
				hour 	= section["hour"]
				minute 	= section["minute"]
				taskCMD = "{} {} {} {} {}".format(minute, hour, day, month, week)
				
				if taskName not in  self._taskName2id:
					self._taskName2id[ taskName ] = []
				self._taskName2id[ taskName ].append( scriptID )
				self._crondDatas[scriptID] = {"cmd" : taskCMD, "taskName" : taskName, "time" : (week, month, day, hour, minute), "param1" : param1, "param2" : param2}
		
		if configPath2:
			sections = LoadModule.openJsonCfg( configPath2 )
			for section in sections:
				scriptID		= section["scriptID"]
				activityTimes	= section["time"].split(":")	#活动点亮|关闭时间:活动点亮|关闭时间:....
				reminds			= section["remind"].split("|")	#活动提醒 like：30|10|5|0
				signTimes		= section["signTime"].split(":")
				openTimes		= section["openTime"].split(":")
				level 			= int(section["level"]) if section["level"] else 0
				hasTong			= int(section.get("hasTong")) if section.get("hasTong", "") else 0
				self._activities[scriptID] = {"level" : level, "hasTong" : hasTong}
				
				#如果没有配置，意味着全天开放
				if section["time"]:
					for activityTime in activityTimes:
						times = activityTime.split("|")
						#肯定是开始时间|结束时间一起配对
						if len(times) != 2:			
							KBEDebug.ERROR_MSG("activity time error %s" %(scriptID))
							return
							
						for timeID in times:
							if timeID not in self._crondDatas:
								KBEDebug.ERROR_MSG("%s time error, not found cmdscriptid %s" %(scriptID, timeID))
								return
							#建立日程配置ID与活动ID的映射
							self._crondid2activityid[timeID] = scriptID
						
						if "activityTimes" not in self._activities[scriptID]:
							self._activities[scriptID]["activityTimes"] = []
						self._activities[scriptID]["activityTimes"].append(times)
						
						#跟进活动点亮时间，计算活动提醒时间
						self._remindDatas[scriptID] = {"startRemind" : False, "cmdList" : []}
						startTime = self._crondDatas[times[0]]["time"]
						for remind in reminds:
							t = int(remind)
							if t == 0:
								self._remindDatas[scriptID]["startRemind"] = True
								continue
							
							#分钟位大于提醒时间
							if int(startTime[4]) >= t:
								cmd = "{} {} {} {} {}".format(int(startTime[4])-t, startTime[3], startTime[2], startTime[1], startTime[0])
								self._remindDatas[scriptID]["cmdList"].append((cmd, t))
								continue
							
							#分钟位小于提醒时间
							hour = int(startTime[3]) - 1 if int(startTime[3]) - 1 >= 0 else 0
							minute = int(startTime[4]) + 60 - t
							cmd = "{} {} {} {} {}".format(minute, hour, startTime[2], startTime[1], startTime[0])
							self._remindDatas[scriptID]["cmdList"].append((cmd, t))
							
				if section["signTime"]:
					for signTime in signTimes:
						times = signTime.split("|")
						#肯定是开始报名时间|结束报名时间一起配对
						if len(times) != 2:			
							KBEDebug.ERROR_MSG("sign time error %s" %(scriptID))
							return
							
						for timeID in times:
							if timeID not in self._crondDatas:
								KBEDebug.ERROR_MSG("%s time error, not found cmdscriptid %s" %(scriptID, timeID))
								return
								
						if "signTimes" not in self._activities[scriptID]:
							self._activities[scriptID]["signTimes"] = []
						self._activities[scriptID]["signTimes"].append(times)
					
				if section["openTime"]:
					for openTime in openTimes:
						times = openTime.split("|")
						#肯定是开始时间|结束时间一起配对
						if len(times) != 2:			
							KBEDebug.ERROR_MSG("open time error %s" %(scriptID))
							return
						
						for timeID in times:
							if timeID not in self._crondDatas:
								KBEDebug.ERROR_MSG("%s time error, not found cmdscriptid %s" %(scriptID, timeID))
								return
								
						if "openTimes" not in self._activities[scriptID]:
							self._activities[scriptID]["openTimes"] = []
						self._activities[scriptID]["openTimes"].append(times)
					
				#分配方式设置开启
				if section.get("openSetAllocationTimes", None):
					openSetAllocationTimes = section["openSetAllocationTimes"].split("|")
					#肯定是开始时间|结束时间一起配对
					if len(openSetAllocationTimes) != 2:			
						KBEDebug.ERROR_MSG("open time error %s" %(scriptID))
						return
						
					for timeID in openSetAllocationTimes:
						if timeID not in self._crondDatas:
							KBEDebug.ERROR_MSG("%s time error, not found cmdscriptid %s" %(scriptID, timeID))
							return
						
					self._activities[scriptID]["openSetAllocationTimes"] = openSetAllocationTimes
	
	def addCrond( self, taskName, cmd ):
		"""
		添加一条计划
		"""
		return False
			
	def getTaskCmds( self, taskName ):
		cmdList = []
		taskName = taskName.lower()
		if taskName in self._taskName2id:
			for id in self._taskName2id[taskName]:
				if id in self._crondDatas:
					cmdList.append(self._crondDatas[id]["cmd"])
		return cmdList
	
	def getCrondTaskCmds( self, taskName ):
		cmdList = []
		taskName = taskName.lower()
		if taskName in self._taskName2id:
			for id in self._taskName2id[taskName]:
				if id in self._crondDatas:
					cmdList.append((id, self._crondDatas[id]["cmd"]))
		return cmdList
		
	def getRemindTaskCmds( self ):
		cmdList = []
		for k,v in self._remindDatas.items():
			cmdList.append((k, v["cmdList"]))
		return cmdList
		
	def getAllActivities( self ):
		return self._activities
		
	def isStartRemind( self, scriptID ):
		"""
		是否在活动开始的时候提醒
		"""
		if scriptID not in self._remindDatas:
			return False
		return self._remindDatas[scriptID]["startRemind"]
		
	def getActivityIDByCrondID(self, scriptID):
		return self._crondid2activityid.get(scriptID, None)
		
	def getCrondByCrondID(self, scriptID):
		return self._crondDatas.get(scriptID, None)
		
	def getAllCronds(self):
		return self._crondDatas

def instance():
	return CrondDatas.instance()

#
# $Log: not supported by cvs2svn $
#
#
