# -*- coding: utf-8 -*-

import KST
import csdefine
import KBEngine
import KBEDebug
import csstatus
import Settings

import time


GAME_TIME_BALANCE_REMIDE_1 = 30 * 60 #剩余三十分钟时提醒一次玩家
GAME_TIME_BALANCE_REMIDE_2 = 10 * 60 #剩余十分钟时提醒一次玩家
GAME_TIME_BALANCE_REMIDE_3 = 1	* 60 #剩余一分钟时提醒一次玩家
GAME_TIME_BALANCE_REMIDE_4 = 10		 #剩余十秒钟时客户端显示倒计时

GAME_TIME_BALANCE_REMIDE_KEY_1 = 1
GAME_TIME_BALANCE_REMIDE_KEY_2 = 2
GAME_TIME_BALANCE_REMIDE_KEY_3 = 3
GAME_TIME_BALANCE_REMIDE_KEY_4 = 4

GAME_TIME_CALC_TIME = 5 * 60 #5分钟扣一次时间


class RoleGameTimeInterface:
	"""
	游戏时长付费接口
	"""
	def __init__(self):
		self.isPayGameTiming = False #是否正在时间付费游戏中
		self.isInSlackTimeStatus = False #游戏打到11级后（ServerSettingConfig.json中配置），如果没有充值时间，玩家有一定的缓冲时间
		self.needRechargeTip = False #玩家开始消耗时间后，如果没有充值的时间，消耗完系统免费时间后，需要提示在客户端弹出提示
		self.lastRecordTime = 0
		self.gameTime_caclTimerID = 0
		self.gameTime_overTimerID = 0
		self.gameTime_quitTimerID = 0
		self.gameTime_messageTimerIDData = {
			GAME_TIME_BALANCE_REMIDE_KEY_1: 0,
			GAME_TIME_BALANCE_REMIDE_KEY_2: 0,
			GAME_TIME_BALANCE_REMIDE_KEY_3: 0,
			GAME_TIME_BALANCE_REMIDE_KEY_4: 0,
		}

	def onGetCell(self):
		"""
		cell 实体创建完成。
		"""
		self.requestStartPayGameTime()

	def logoff(self):
		"""
		玩家下线
		"""
		if self.isPayGameTiming:
			self.stopPayGameTime()

	def logout(self):
		"""
		玩家回到角色选择界面
		"""
		if self.isPayGameTiming:
			self.stopPayGameTime()
			
	def onLevelUp(self):
		"""
		玩家升级
		"""
		self.requestStartPayGameTime()
		
	def getGameTimeBalance(self):
		"""
		获取剩余时间
		"""
		return self.accountEntity.getGameTimeBalance()
		
	def getPayTimeBalance(self):
		"""
		"""
		return self.accountEntity.payTimeBalance
		
	def getDefaultTimeBalance(self):
		"""
		"""
		return self.accountEntity.defaultTimeBalance
				
	def requestStartPayGameTime(self):
		"""
		"""
		if Settings.open_game_time_activation and self.getLevel() >= Settings.start_billing_level:
			self.startPayGameTime()
	
	def startPayGameTime(self):
		"""
		开始时长付费
		"""
		if not self.isPayGameTiming:
			self.isPayGameTiming = True
			self.lastRecordTime = int(time.time())
			
			payTimeBalance = self.getPayTimeBalance()
			if payTimeBalance <=0:
				self.needRechargeTip = True
			else:
				self.needRechargeTip = False
			
			gameTimeBalance = int(self.getGameTimeBalance())
			
			if gameTimeBalance <= GAME_TIME_CALC_TIME: #小于5分钟
				self.checkGameTimeBalance()
			else:
				if gameTimeBalance <= GAME_TIME_CALC_TIME + GAME_TIME_BALANCE_REMIDE_1 + 5:
					self.checkGameTimeBalance()
				self.gameTime_caclTimerID = self.addTimerRepeat(GAME_TIME_CALC_TIME, "onCalcGameTimeTimerCallback", (GAME_TIME_CALC_TIME,))

	def stopPayGameTime(self, isGameTimeOver = False):
		"""
		停止时长付费
		"""
		if self.isPayGameTiming:
			self.isPayGameTiming = False

			if isGameTimeOver:
				self.calcGameTimeBalance(self.getGameTimeBalance())
			elif not self.isInSlackTimeStatus: #玩家在缓冲时间过程中，不计时间，避免玩家在缓冲时间过程中充值而导致扣掉时间
				value = int(time.time()) - self.lastRecordTime
				self.calcGameTimeBalance(value)
			
			self.clearTimer()

	def onCalcGameTimeTimerCallback(self, timeValue):
		"""
		"""
		if not self.isPayGameTiming:
			return

		self.lastRecordTime = int(time.time())
		self.calcGameTimeBalance(timeValue)
		self.checkGameTimeBalance()
		
	def checkGameTimeBalance(self):
		"""
		检查游戏剩余时间
		"""
		if not self.isPayGameTiming:
			return

		gameTimeBalance = int(self.getGameTimeBalance())
		
		if gameTimeBalance <= GAME_TIME_CALC_TIME:
			self.gameTime_overTimerID = self.addTimerCallBack(gameTimeBalance, "onGameTimeOver", ())
			if self.gameTime_caclTimerID != 0:
				self.popTimer(self.gameTime_caclTimerID)
				self.gameTime_caclTimerID = 0

		self.checkTimeBalanceTimer()

	def checkTimeBalanceTimer(self):
		"""
		检查剩余时间和设置消息timer
		"""	
		gameTimeBalance = int(self.getGameTimeBalance())

		if gameTimeBalance <= GAME_TIME_BALANCE_REMIDE_4 + GAME_TIME_CALC_TIME + 5: #多加5秒避免有误差
			if gameTimeBalance > GAME_TIME_BALANCE_REMIDE_3:
				self.setTimeBalanceTimer(GAME_TIME_BALANCE_REMIDE_KEY_3, gameTimeBalance - GAME_TIME_BALANCE_REMIDE_3)
			if gameTimeBalance > GAME_TIME_BALANCE_REMIDE_4:
				self.setTimeBalanceTimer(GAME_TIME_BALANCE_REMIDE_KEY_4, gameTimeBalance - GAME_TIME_BALANCE_REMIDE_4)
			else:
				self.client.OnGameTimeBalanceCountDown(gameTimeBalance)
				self.statusMessage(csstatus.GAME_TIME_ALL_HAS_USED)
		elif gameTimeBalance <= GAME_TIME_BALANCE_REMIDE_3 + GAME_TIME_CALC_TIME + 5:
			#小于6分钟时需要添加1分钟、10秒消息的定时器，不然有可能下一次调用checkTimeBalanceTimer之前剩余时间已经为0，不会再触发10秒的消息
			if gameTimeBalance >= GAME_TIME_BALANCE_REMIDE_KEY_3:
				self.setTimeBalanceTimer(GAME_TIME_BALANCE_REMIDE_KEY_3, gameTimeBalance - GAME_TIME_BALANCE_REMIDE_3)
				self.setTimeBalanceTimer(GAME_TIME_BALANCE_REMIDE_KEY_4, gameTimeBalance - GAME_TIME_BALANCE_REMIDE_4)
			else:
				self.setTimeBalanceTimer(GAME_TIME_BALANCE_REMIDE_KEY_4, gameTimeBalance - GAME_TIME_BALANCE_REMIDE_4)

		elif gameTimeBalance <= GAME_TIME_BALANCE_REMIDE_2 + GAME_TIME_CALC_TIME + 5:
			if gameTimeBalance >= GAME_TIME_BALANCE_REMIDE_2:
				self.setTimeBalanceTimer(GAME_TIME_BALANCE_REMIDE_KEY_2, gameTimeBalance - GAME_TIME_BALANCE_REMIDE_2)

		elif gameTimeBalance <= GAME_TIME_BALANCE_REMIDE_1 + GAME_TIME_CALC_TIME + 5:
			#小于35分钟时再开始加定时器
			if gameTimeBalance >= GAME_TIME_BALANCE_REMIDE_1: #刚上线是小于30分钟时也会走到这里，所以要判断两个值的大小
				self.setTimeBalanceTimer(GAME_TIME_BALANCE_REMIDE_KEY_1, gameTimeBalance - GAME_TIME_BALANCE_REMIDE_1)

	def setTimeBalanceTimer(self, key, timeValue):
		"""
		设置付费时间余额消息提示timer
		"""
		if key not in self.gameTime_messageTimerIDData:
			KBEDebug.ERROR_MSG("message timer id key error: %s" % key)
			return
		if self.gameTime_messageTimerIDData[key] != 0:
			return

		self.gameTime_messageTimerIDData[key] = self.addTimerCallBack(timeValue, "onTimeBalanceTimer", (key,))

	def onTimeBalanceTimer(self, key):
		"""
		"""
		if not self.isPayGameTiming: #可能已经退出游戏
			return

		self.gameTime_messageTimerIDData[key] = 0

		if key == GAME_TIME_BALANCE_REMIDE_KEY_1:
			self.statusMessage(csstatus.GAME_TIME_BLAN_HALF_HOUR)
			self.setTimeBalanceTimer(GAME_TIME_BALANCE_REMIDE_KEY_2, GAME_TIME_BALANCE_REMIDE_1 - GAME_TIME_BALANCE_REMIDE_2)
		elif key == GAME_TIME_BALANCE_REMIDE_KEY_2:
			self.statusMessage(csstatus.GAME_TIME_TEN_MINUTES)
			self.setTimeBalanceTimer(GAME_TIME_BALANCE_REMIDE_KEY_3, GAME_TIME_BALANCE_REMIDE_2 - GAME_TIME_BALANCE_REMIDE_3)
		elif key == GAME_TIME_BALANCE_REMIDE_KEY_3:
			self.statusMessage(csstatus.GAME_TIME_TEN_SECONDS)
			self.setTimeBalanceTimer(GAME_TIME_BALANCE_REMIDE_KEY_3, GAME_TIME_BALANCE_REMIDE_2 - GAME_TIME_BALANCE_REMIDE_3)
		elif key == GAME_TIME_BALANCE_REMIDE_KEY_4:
			self.statusMessage(csstatus.GAME_TIME_ALL_HAS_USED)
			self.client.OnGameTimeBalanceCountDown(GAME_TIME_BALANCE_REMIDE_4)

	def onGameTimeOver(self):
		"""
		游戏时间消耗完
		"""
		if self.isPayGameTiming:
			self.stopPayGameTime(True)
			if self.needRechargeTip:
				self.gameTime_quitTimerID = self.addTimerCallBack(Settings.slack_time, "quitGame", ())
				self.client.ShowStartBillingWnd(self.getLevel(), Settings.slack_time)
			else:
				self.quitGame()
				
	def quitGame(self):
		"""
		"""
		self.logoff()

	def calcGameTimeBalance(self, value):
		"""
		记录下消耗时间
		"""
		self.accountEntity.subGameTimeBalance(value)
		
	def onGameTimeRecharge(self, value):
		"""
		付费时间充值
		"""
		if Settings.open_game_time_activation and self.getLevel() >= Settings.start_billing_level:
			if self.isPayGameTiming:
				self.stopPayGameTime()
			self.isInSlackTimeStatus = False
			self.client.HideStartBillingWnd()
			self.startPayGameTime()
	
		self.statusMessage(csstatus.GAME_TIME_ADD_TIME, int(value / 60))
	
	def clearTimer(self):
		"""
		"""
		if self.gameTime_caclTimerID != 0:
			self.popTimer(self.gameTime_caclTimerID)
			self.gameTime_caclTimerID = 0
		if self.gameTime_overTimerID != 0:
			self.popTimer(self.gameTime_overTimerID)
			self.gameTime_overTimerID = 0
		if self.gameTime_quitTimerID != 0:
			self.popTimer(self.gameTime_quitTimerID)
			self.gameTime_quitTimerID = 0
		for key, value in self.gameTime_messageTimerIDData.items():
			if value != 0:
				self.popTimer(value)
				self.gameTime_messageTimerIDData[key] = 0
		
	def addGameTime(self, value):
		"""
		define method
		添加付费时间
		"""
		self.accountEntity.addGameTimeBalance(value)
		
	#--------------------------------GM指令------------------------------------
	def beforeGMSetGameTime(self):
		"""
		"""
		#stopPayGameTime方法里将会扣除一定的时间，所以在GM设置游戏剩余时间前先调用此方法（onGameTimeRecharge方法中会调用stopPayGameTime方法）
		self.stopPayGameTime()
		
	def GMSetPayGameTime(self, value):
		"""
		define method
		指令设置付费时间
		"""
		self.accountEntity.GMSetPayGameTime(value)
		
	def GMSetDefaultGameTime(self, value):
		"""
		define method
		指令设置付费时间
		"""
		self.accountEntity.GMSetDefaultGameTime(value)
		