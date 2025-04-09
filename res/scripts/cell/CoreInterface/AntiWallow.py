#-*-coding:utf-8-*-
#
"""
防沉迷系统模块
"""

import KBEngine
import csdefine
import csstatus
import csconst
import KBEDebug

# --------------------------------------------------------------------
OLTIME_MINUTES		= 60 						# 在线时间分钟单位
OLTIME_HALF_LUCRE	= 3 * 60 * OLTIME_MINUTES	# 收益减半的在线时间点
OLTIME_NO_LUCRE		= 5 * 60 * OLTIME_MINUTES	# 零收益的在线时间点


NOTIFY_INTERVALS = {
	csdefine.WALLOW_STATE_COMMON	 : 60 * OLTIME_MINUTES,	# 正常游戏情况下，提示的时间间隔
	csdefine.WALLOW_STATE_HALF_LUCRE : 30 * OLTIME_MINUTES,	# 收益减半情况下，提示的时间间隔
	csdefine.WALLOW_STATE_NO_LUCRE	 : 15 * OLTIME_MINUTES,	# 零收益情况下，提示的时间间隔
	}

NOTIFY_MSGS = {
	csdefine.WALLOW_STATE_COMMON	 : csstatus.ANTI_WALLOW_COMMON,
	csdefine.WALLOW_STATE_HALF_LUCRE : csstatus.ANTI_WALLOW_HALF_LUCRE,
	csdefine.WALLOW_STATE_NO_LUCRE	 : csstatus.ANTI_WALLOW_NO_LUCRE,
	}

class AntiWallow :
	"""
	未成年人防沉迷系统
	"""
	def __init__( self ) :
		"""
		初始化
		"""
		self.__lucreRate = 1.0					# 收益率（CELL_PUBLIC）
		self.__notifyTimerID = 0
		self.cWallow_isAdult = False			# 是否是成年人（CELL_PRIVATE）

#----------沉迷处理--------------------------------------
	def __enterCommonState( self ) :
		"""
		进入正常状态
		"""
		self.__lucreRate = 1.0


	def __enterTiredState( self ) :
		"""
		进入疲劳状态
		"""
		self.__leaveUnhealthyState()
		self.__lucreRate = 0.5

	def __leaveTiredState( self ) :
		"""
		离开疲劳状态
		"""
		self.__lucreRate = 1.0

	def __enterUnhealthyState( self ) :
		"""
		进入不健康状态
		"""
		self.__leaveTiredState()
		self.__lucreRate = 0.0

	def __leaveUnhealthyState( self ) :
		"""
		离开不健康状态
		"""
		self.__lucreRate = 1.0

#----------防沉迷接口------------------------------------
	def wallow_setAgeState( self, isAdult ) :
		"""
		defined.
		设置年龄状态
		@type			isAdult : BOOL
		@param			isAdult : 是否是成年
		注意：只给 base 调用
		"""
		self.cWallow_isAdult = isAdult
		if self.cWallow_isAdult:
			self.__enterCommonState()
		else:
			self.__lucreRate = self.__oldLucreRate


	def wallow_onWallowNotify( self, state, olTime ) :
		"""
		defined.
		沉迷提醒
		@type			state  : MACRO DEFINATION
		@param			state  : 收益状态，在 csdefine 中定义：WALLOW_XXX
		@type			olTime : INT64
		@param			olTime : 在线时间
		注意：只给 base 调用
		"""
		if not self.wallow_isEffected() :
			return
		assert state in csconst.WALLOW_STATES, "Error anti-wallow state: %i" % state
		notifyInterval = NOTIFY_INTERVALS[state]									# 下次通知时间间隔
		nextNotifyTime = notifyInterval

		if state == csdefine.WALLOW_STATE_COMMON :
			self.__enterCommonState()
			if olTime > 0 :
				nextNotifyTime = notifyInterval - ( olTime % notifyInterval )
		elif state == csdefine.WALLOW_STATE_HALF_LUCRE :
			self.__enterTiredState()
			startTime = olTime - OLTIME_HALF_LUCRE
			if startTime > 0 :
				nextNotifyTime = notifyInterval - ( startTime % notifyInterval )
		elif state == csdefine.WALLOW_STATE_NO_LUCRE :
			self.__enterUnhealthyState()
			startTime = olTime - OLTIME_NO_LUCRE
			if startTime > 0 :
				nextNotifyTime = notifyInterval - ( startTime % notifyInterval )

		self.__onlineTime = olTime + int(csconst.ANTIWALLOWTICK)

		if self.__oldLucreRate != self.__lucreRate:
			self.__oldLucreRate = self.__lucreRate

			self.addTimerCallBack(nextNotifyTime, "onWallowNotify", ())
			

	def onWallowNotify( self ) :
		"""
		定期通知客户端
		"""
		state = csdefine.WALLOW_STATE_COMMON
		msgArg = ()
		if self.__onlineTime >= OLTIME_NO_LUCRE :
			state = csdefine.WALLOW_STATE_NO_LUCRE
		elif self.__onlineTime > OLTIME_HALF_LUCRE :
			state = csdefine.WALLOW_STATE_HALF_LUCRE
		else :
			t = round(self.__onlineTime / (60 * OLTIME_MINUTES))
			t = t if t > 0 else 1
			msgArg = ( t, )
		interval = NOTIFY_INTERVALS[state]
		if hasattr(self, "client") and self.client:
			self.statusMessage( NOTIFY_MSGS[state], *msgArg )

		self.delWallowNotify()
		self.__notifyTimerID = self.addTimerCallBack(interval,"onWallowNotify",())

	def delWallowNotify(self):
		"""
		<define method>
		删除客户端通知
		"""
		if self.__notifyTimerID:
			self.popTimer(self.__notifyTimerID)
			self.__notifyTimerID = 0

	def wallow_isEffected( self ) :
		"""
		是否受防沉迷系统影响
		for real & ghost
		"""
		# return KBEngine.globalData["AntiWallow_isApply"] and not self.cWallow_isAdult
		return not self.cWallow_isAdult

	def wallow_getLucreRate( self ) :
		"""
		获取收益率
		for real & ghost
		"""
		return self.__lucreRate


	def gmSetAgeState( self, isAdult ) :
		"""
		GM指令设置未成年
		"""
		self.base.wallow_setAgeState(isAdult)
		if isAdult:
			self.delWallowNotify()