# -*- coding: utf-8 -*-
import time
import KBEngine
from KBEDebug import *

import Functions
import Const

from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()

class RoleCrondInterface:
	def __init__( self ):
		"""
		"""
		self.todayCrondKey = None	#当日活动数据总更新令牌
		self.todayCrondKeys = {}	#当日单个活动数据更新令牌
		self.weekCrondKey = None	#一周活动数据更新令牌(不包括当日的活动)
		
	def requestSetCrondRemind( self, scriptID, remindType ):
		"""
		Exposed method
		设置活动提醒类型
		"""
		if not self.validateClientCall():
			return
		
		if scriptID not in self.crondRemindDatas:
			self.crondRemindDatas[scriptID] = remindType
	
	def requestCrondRemindData( self ):
		"""
		Exposed method
		请求获取活动提醒设置数据
		"""
		if not self.validateClientCall():
			return
		
		table = []
		for scriptID in self.crondRemindDatas:
			table.append({
				"scriptID" : scriptID,
				"remindType" : self.crondRemindDatas[scriptID],
			})
		self.client.receiveCrondRemindData({"items" : table})
		
	def remindRoleCrond( self, scriptID, remindType ):
		"""
		define method
		活动提醒
		"""
		#没有设置的话，那就是默认的10分钟提醒
		if scriptID not in self.crondRemindDatas and remindType != Const.CROND_BEFORE_TENMINUTE_REMIND:
			return
		
		if scriptID in self.crondRemindDatas  and remindType != self.crondRemindDatas[scriptID]:
			return
		
		activityCronds = g_CrondDatas.getAllActivities()
		level = activityCronds.get(scriptID, {}).get("level", 0)
		if self.getLevel() < level:
			return
			
		hasTong = activityCronds.get(scriptID,{}).get("hasTong", 0)
		if hasTong and not self.hasTong():
			return
		
		#通知客户端,收到活动提醒
		if self.getClient():
			self.client.receiveCrondRemind(scriptID, remindType)
	
	def requestTodayActivitiesData( self ):
		"""
		<Exposed method>
		玩家请求当天活动数据
		"""
		if not self.validateClientCall():
			return
		
		todayCrondKey = KBEngine.baseAppData.get(csdefine.ACTIVE_KEY_ID, None)
		if self.todayCrondKey != todayCrondKey:
			KBEngine.globalData["ActivityCrondManager"].requestTodayActivitiesData( self )
			self.cell.getActivityTimes()
			return
		
		self.updateTodayActivitiesData()
		
	def updateTodayActivitiesData( self ):
		"""
		"""
		table = []
		for id, key in self.todayCrondKeys.items():
			k = KBEngine.baseAppData.get(csdefine.ACTIVE_PRE_STR+str(id), None)
			if k == key: continue 
			table.append(id)
		
		if len(table) <= 0:
			year, month, day, hour, minute, second, wday = time.localtime( time.time() )[:7]
			datas = {"table": [], "month" : str(month), "day" : str(day), "wday" : str(wday)}
			self.client.recviveUpdateTodayActivitiesData(datas)
			return
		
		#只更新发生了变化的活动数据
		KBEngine.globalData["ActivityCrondManager"].requestUpdateTodayActivitiesData( self, table )
		
	def recviveTodayActivitiesData(self, datas, tokenDict, crondtoken):
		"""
		define method
		取得当天活动数据
		"""
		#更新令牌
		self.todayCrondKey = crondtoken
		for id, token in tokenDict.items():
			self.todayCrondKeys[id] = token
		
		if self.getClient():
			self.client.recviveTodayActivitiesData(datas)
			
	def recviveUpdateTodayActivitiesData(self, datas, tokenDict):
		"""
		define method
		更新当天活动数据
		"""
		#更新令牌
		for id, token in tokenDict.items():
			self.todayCrondKeys[id] = token
		
		if self.getClient():
			self.client.recviveUpdateTodayActivitiesData(datas)
		
	def requestWeekActivitiesData(self):
		"""
		Exposed method
		获取一周的活动（除当天）
		"""
		if not self.validateClientCall():
			return
		
		crondKey = KBEngine.baseAppData.get(csdefine.ACTIVE_KEY_ID, None)
		if self.weekCrondKey == crondKey:
			self.client.receiveWeekActivitiesData([], False)
			return
		
		KBEngine.globalData["ActivityCrondManager"].requestWeekActivitiesData( self )
		
	def receiveWeekActivitiesData(self, datas, token):
		"""
		define method
		获取一周的活动数据(除当天)
		"""
		self.weekCrondKey = token
		if self.getClient():
			self.client.receiveWeekActivitiesData(datas, True)
