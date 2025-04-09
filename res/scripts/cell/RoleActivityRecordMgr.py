# -*- coding: utf-8 -*-

import time
import csdefine
import Singleton
import KBEDebug
import KBEngine

def week( t=(0,)*9 ):
	"""
	获取年份和第几周（星期天是一周的第一天）
	"""
	return time.strftime("(%Y, %W)", t)

def date( t=(0,)*9 ):
	"""
	获取当前的日期
	"""
	return time.strftime("(%Y, %m, %d)", t)


class ActRecordBase:
	"""
	"""
	def __init__( self, recordKey, degree ):
		self.recordKey = recordKey
		self.degree = degree

	def addActivityDegree( self, player ):
		"""
		virtual method
		增加活动参与记录
		"""
		pass

	def clearActivityDegree( self, player ):
		"""
		清除活动参与记录
		"""
		pass

	def getActivityDegree( self, player ):
		"""
		获取活动参与次数
		"""
		return 0
	
	def isExceedActivityDegree( self, player ):
		"""
		virtual method
		参与次数是否超过额定值
		"""
		return False

	def getMaxDegree( self ):
		"""
		获取某活动最大参与次数
		"""
		if self.recordKey in KBEngine.cellAppData:
			degree = KBEngine.cellAppData[self.recordKey]
		else:
			degree = self.degree
		return degree

class DailyActRecord( ActRecordBase ):
	"""
	每天更新的活动
	"""
	def addActivityDegree( self, player ):
		"""
		"""
		dateStr = date( time.localtime() )
		record = player.getPublicActRecord( self.recordKey, "", "", "" )
		if record:
			if record.param1 != dateStr:	# 今天的第一次
				newCount = 1
			else:
				newCount = int( record.param3 ) + 1
			conParam = [ "", "", "" ]
			valParam = [ dateStr, "", str( newCount ) ]
			player.updatePublicActRecord( self.recordKey, conParam, valParam )
		else:
			player.addPublicActRecord( self.recordKey, dateStr, "", "1" )

	def clearActivityDegree( self, player ):
		"""
		清除活动参与记录
		"""
		player.removePublicActRecord( self.recordKey, "", "", "" )

	def getActivityDegree( self, player ):
		"""
		获取今天活动参与次数
		"""
		dateStr = date( time.localtime() )
		record = player.getPublicActRecord( self.recordKey, dateStr, "", "" )
		if not record:
			return 0
		else:
			return int( record.param3 )

	def isExceedActivityDegree( self, player ):
		"""
		"""
		dateStr = date( time.localtime() )
		record = player.getPublicActRecord( self.recordKey, dateStr, "", "" )
		if not record:
			return False
		else:
			if self.recordKey in KBEngine.cellAppData:
				degree = KBEngine.cellAppData[self.recordKey]
			else:
				degree = self.degree
			return int( record.param3 ) >= degree

class WeeklyActRecord( ActRecordBase ):
	"""
	每周更新的活动
	"""
	def addActivityDegree( self, player ):
		"""
		"""
		weekStr = week( time.localtime() )
		record = player.getPublicActRecord( self.recordKey, "", "", "" )
		if record:
			if record.param1 != weekStr:	# 本周的第一次
				newCount = 1
			else:
				newCount = int( record.param3 ) + 1
			conParam = [ "", "", "" ]
			valParam = [ weekStr, "", str( newCount ) ]
			player.updatePublicActRecord( self.recordKey, conParam, valParam )
		else:
			player.addPublicActRecord( self.recordKey, weekStr, "", "1" )
	
	def clearActivityDegree( self, player ):
		"""
		清除活动参与记录
		"""
		player.removePublicActRecord( self.recordKey, "", "", "" )
	
	def getActivityDegree( self, player ):
		"""
		获取本周活动参与次数
		"""
		weekStr = week( time.localtime() )
		record = player.getPublicActRecord( self.recordKey, weekStr, "", "" )
		if not record:
			return 0
		else:
			return int( record.param3 )
	
	def isExceedActivityDegree( self, player ):
		"""
		"""
		weekStr = week( time.localtime() )
		record = player.getPublicActRecord( self.recordKey, weekStr, "", "" )
		if not record:
			return False
		else:
			if self.recordKey in KBEngine.cellAppData:
				degree = KBEngine.cellAppData[self.recordKey]
			else:
				degree = self.degree
			return int( record.param3 ) >= degree


class RoleActivityRecordMgr( Singleton.Singleton ):
	"""
	玩家日常或周常活动参与次数管理模块
	利用玩家的cell_public属性publicActRecord
	"""
	def __init__( self ):
		"""
		"""
		self.activityDict = {	csdefine.ACTIVITY_TYPE_POTENTAIL_SPACE:			DailyActRecord( csdefine.ROLE_ACT_POTENTAIL_SPACE, 5 ),
								csdefine.ACTIVITY_TYPE_CHUANCHENG_SPACE_1:		DailyActRecord( csdefine.ROLE_ACT_CHUANCHENG_SPACE_1, 999 ),
								csdefine.ACTIVITY_TYPE_CHUANCHENG_SPACE_2:		DailyActRecord( csdefine.ROLE_ACT_CHUANCHENG_SPACE_2, 999 ),
								csdefine.ACTIVITY_TYPE_MAGIC_MAZE_SPACE_1:		DailyActRecord( csdefine.ROLE_ACT_MAGIC_MAZE_SPACE_1, 3 ),
								csdefine.ACTIVITY_TYPE_MAGIC_MAZE_SPACE_2:		DailyActRecord( csdefine.ROLE_ACT_MAGIC_MAZE_SPACE_2, 3 ),
								csdefine.ACTIVITY_TYPE_TONG_SPACE_COPY :		DailyActRecord( csdefine.ROLE_ACT_TONG_SPACE_COPY, 1 ),
								csdefine.ACTIVITY_TYPE_CAMP_YXLM:				WeeklyActRecord( csdefine.ROLE_ACT_YXLM_CAMP_SPACE,3 ),
								csdefine.ACTIVITY_TYPE_CAMP_SGMZ:				WeeklyActRecord( csdefine.ROLE_ACT_SGMZ_CAMP_SPACE,3 ),
								csdefine.ACTIVITY_TYPE_CAMP_YCJMD:				WeeklyActRecord( csdefine.ROLE_ACT_YCJMD_CAMP_SPACE,1 ),
								csdefine.ACTIVITY_TYPE_CAMP_LING_MAI:			WeeklyActRecord( csdefine.ROLE_ACT_LING_MAI_CAMP_SPACE,1 ),
								csdefine.ACTIVITY_TYPE_CAMP_FIVE_YCJMD:			WeeklyActRecord( csdefine.ROLE_ACT_YCJMD_CAMP_FIVE_SPACE,3 ),
								csdefine.ACTIVITY_TYPE_CAMP_JSSLC:				DailyActRecord( csdefine.ROLE_ACT_JSSLC_CAMP_SPACE,0 ),
								csdefine.ACTIVITY_TYPE_CAMP_ZZZB:				DailyActRecord( csdefine.ROLE_ACT_ZZZB_SPACE, 1 ),
								csdefine.ACTIVITY_TYPE_CAMP_SHOOT_YCJMD:		DailyActRecord( csdefine.ROLE_ACT_CAMP_SHOOT_YCJMD, 1 ),
								csdefine.ACTIVITY_TYPE_CAMP_COPY_YCJMD:			DailyActRecord( csdefine.ROLE_ACT_CAMP_COPY_YCJMD, 1 ),
								csdefine.ACTIVITY_TYPE_COPY_ACCTACK_CITY_WAR:	DailyActRecord( csdefine.ROLE_ACT_COPY_ACCTACK_CITY_WAR, 1 ),
								csdefine.ACTIVITY_TYPE_TONG_DAILY_QUEST :		DailyActRecord( csdefine.ACTIVITY_TYPE_TONG_DAILY_QUEST, 1 ),
								}

	def addActivityDegree( self, player, activityType ):
		"""
		增加某活动参与记录
		"""
		if activityType not in self.activityDict:
			KBEDebug.ERROR_MSG("ERROR ACTIVITY TYPE %d" %(activityType))
			return
		
		self.activityDict[ activityType ].addActivityDegree( player )

	def clearActivityDegree( self, player, activityType ):
		"""
		清除某活动的参与记录
		"""
		if activityType not in self.activityDict:
			KBEDebug.ERROR_MSG("ERROR ACTIVITY TYPE %d" %(activityType))
			return
		
		self.activityDict[ activityType ].clearActivityDegree( player )

	def getActivityDegree( self, player, activityType ):
		"""
		获取某活动参与次数
		"""
		if activityType not in self.activityDict:
			KBEDebug.ERROR_MSG("ERROR ACTIVITY TYPE %d" %(activityType))
			return 1
		
		return self.activityDict[ activityType ].getActivityDegree( player )

	def isExceedActivityDegree( self, player, activityType ):
		"""
		某活动参与次数是否超过额定值
		"""
		if activityType not in self.activityDict:
			KBEDebug.ERROR_MSG("ERROR ACTIVITY TYPE %d" %(activityType))
			return False
		
		return self.activityDict[ activityType ].isExceedActivityDegree( player )

	def getMaxDegree( self, player, activityType ):
		"""
		获取某活动参与次数
		"""
		return self.activityDict[ activityType ].getMaxDegree()

#-------global instance--------------------------------------------------
g_activityRecordMgr = RoleActivityRecordMgr()