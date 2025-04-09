# -*- coding: utf-8 -*-

from ConfigObject.Reward.OnlineRewardMgr import g_onlineRewardMgr
import time
import calendar
import KBEDebug
import Const
import csdefine
import csstatus
import Functions

class RoleGiftInterface:
	"""
	礼包奖励(新手在线奖励、每日签到)
	"""
	def __init__( self ):
		""""""
		self.tempSignInMonth = []
		#self.signInDict = {}						 { 201808 : [1,2,3....]} 格式如{年月：[日]}
		
	def initClientData(self):
		"""
		初始化客户端数据
		"""
		self.initNewPlayerGift()
		self.initSignInGift()
		
	def initNewPlayerGift( self ):
		"""初始化新手玩家奖励"""
		maxDay = g_onlineRewardMgr.getOnlineRewardMaxDay( self.profession )			# 领取完奖励
		if self.gainGiftDay > maxDay:return
		if self.createTime == 0:return
		
		curTime = time.localtime()
		createTime = time.localtime(self.createTime)
		if curTime.tm_year != createTime.tm_year or curTime.tm_mon != createTime.tm_mon:
			return
		onlineDay = time.localtime().tm_mday - time.localtime(self.createTime).tm_mday + 1
		if onlineDay > maxDay:
			self.gainGiftDay = maxDay
			return
		
		if self.gainGiftDay != onlineDay or self.gainGiftDay == 0:
			self.gainGiftDay = onlineDay
			self.gainGiftCount = 0
			self.gainGiftTime = int( time.time() )
			lifeTime, reward, bindType = g_onlineRewardMgr.getOnlineRewardInfo( self.profession, self.gainGiftDay, self.gainGiftCount )
		else:										# 说明玩家当天重复登录
			# 当天的奖励，已经领完
			if self.gainGiftCount >= g_onlineRewardMgr.getOnlineRewardMaxCount( self.profession, self.gainGiftDay ):
				return
			passTime = max(self.offlineTime - self.gainGiftTime, 0 )
			self.gainGiftTime = int( time.time() ) - passTime
			lifeTime, reward, bindType = g_onlineRewardMgr.getOnlineRewardInfo( self.profession, self.gainGiftDay, self.gainGiftCount )
			lifeTime = max( lifeTime - passTime, 0 )
		
		if hasattr(self, "client") and self.client:
			self.client.OnShowOnlineReward( lifeTime, reward, bindType)
		
	def initSignInGift( self ):

		"""初始化"""
		if self.level < Const.SIGN_IN_MIN_LEVEL:					#满10级才有
			return
		month = time.localtime().tm_mon
		signDataList = { "signDatas": [] }
		for key in list(self.signInDict.keys()):
			mouKey = key % 100

			if not self._checkDstMonth( month, mouKey ):		# 只保存2个月的数据
				self.signInDict.pop( key )
			else:
				signData = {}
				signData["yearMonth"] = key
				signData["dayList"] = []
				signData["dayList"].extend(self.signInDict[key])
				
				signDataList["signDatas"].append(signData)
				 
		self._clearSignInNum(month)
		if hasattr(self, "client") and self.client:
			self.client.OnShowSignInReward( self.signInNum, self.signInRewardNum, {"signindata":self.signInRewardList}, signDataList  )

	def _clearSignInNum(self, curMonth):
		"""
		在新的月份需要重置签到累积次数，避免上月签到次数累计到本月影响本月累积签到奖励获取
		"""
		if time.localtime().tm_year*100+curMonth not in self.signInDict:   #当玩家登陆，而本月还未签到时清空之前月份累计的次数
			self.signInNum = 0
			self.signInRewardNum = 0
			self.signInRewardList = []
	
	def _checkDstMonth( self, curMonth, dstMonth ):
		"""
		检查目标月份
		（目前只支持当前月份的前两个月份）
		"""
		if curMonth == 1:
			return dstMonth in [11, 12, 1]
		elif curMonth == 2:
			return dstMonth in [12, 1, 2]
		else:
			return curMonth - dstMonth <= 2
		
	def receiveNewPlayerGift( self ):
		"""
		Exposed method
		获取新手礼包
		"""
		# 领取完奖励
		maxDay = g_onlineRewardMgr.getOnlineRewardMaxDay( self.profession )
		if self.gainGiftDay > maxDay:
			KBEDebug.ERROR_MSG("Player(id:%d,name:%s) has finish receive new player gift"%(self.id,self.playerName))
			return
		
		lifeTime, reward, bindType = g_onlineRewardMgr.getOnlineRewardInfo( self.profession, self.gainGiftDay, self.gainGiftCount )

		if lifeTime <= time.time() - self.gainGiftTime:
			self.cell.onReceiveNewPlayerGift( reward, bindType )
		else:
			KBEDebug.ERROR_MSG("Player(id:%d,name:%s) receive new player gift err!!time is not arrive!"%(self.id,self.playerName))
			
	def onReceiveNewPlayerGiftSuccess( self ):
		"""
		define method
		成功领取新手礼包
		"""
		self.gainGiftCount += 1
		if self.gainGiftCount < g_onlineRewardMgr.getOnlineRewardMaxCount( self.profession, self.gainGiftDay ):
			self.gainGiftTime = int( time.time() )
			lifeTime, reward, bindType = g_onlineRewardMgr.getOnlineRewardInfo( self.profession, self.gainGiftDay, self.gainGiftCount )
			self.client.OnShowOnlineReward( lifeTime, reward, bindType )
		else:
			self.client.OnFinishReceiveNewPlayerGift()
		
	def signInOnline( self ):
		"""
		Exposed method
		上线签到
		"""
		assert self.level >= Const.SIGN_IN_MIN_LEVEL,"player %d level(%d) cannot signIn!"%(self.id, self.level)
		year = time.localtime().tm_year
		month = time.localtime().tm_mon
		day = time.localtime().tm_mday
		key = year * 100 + month
		if not key in self.signInDict:
			self.signInDict[key] = []
		if day in self.signInDict[key]:
			KBEDebug.ERROR_MSG("Sign in fail!As player(id:%d,name:%s) has already sign in!"%(self.id, self.playerName))
			return
		reward, bindType = g_onlineRewardMgr.getSignInReward( day )
		self.cell.onSignInOnline( reward, bindType )
		
	def onSignInOnlineSuccess( self ):
		"""
		define method
		成功签到
		"""
		year = time.localtime().tm_year
		month = time.localtime().tm_mon
		day = time.localtime().tm_mday
		key = year * 100 + month
		self.signInNum += 1
		self.signInDict[key].append( day )
		self.client.OnSignInOnlineSuccess()
		
	def augmentSignIn( self, year, month, day ):
		"""
		Exposed method
		补签一天
		"""
		assert self.level >= Const.SIGN_IN_MIN_LEVEL,"player %d level(%d) cannot signIn!" % (self.id, self.level)
		if self.isPWKitBagLock():
			self.client.CLIENT_openInputKBPW()
			return

		curMonth = time.localtime().tm_mon


		if time.localtime().tm_year - year > 0:
			KBEDebug.ERROR_MSG("Can not augment sign in!as year(%d) is far away!" % year)
			return

		if month != time.localtime().tm_mon:
			KBEDebug.ERROR_MSG("you only can augment sign in current month! ")
			return



		key = year * 100 + month
		if key in self.signInDict and day in self.signInDict[key]:
			KBEDebug.ERROR_MSG("day(%d) already sign in!"%(day))
			return
			
		if self.hasEnoughShiTou( Const.SIGN_IN_REWARD_AUGMENT_DAY):
			reward, bindType = g_onlineRewardMgr.getSignInReward( day )
			self.cell.onAugmentSignIn( reward, bindType, key, day )
		else:
			self.statusMessage(csstatus.ONLINE_REWARD_LING_SHI_NOT_ENOUGH, "")
			
	def onAugmentSignInSuccess( self, key, day ):
		"""
		define method
		补签成功
		"""
		self.payShiTou( Const.SIGN_IN_REWARD_AUGMENT_DAY, csdefine.CHANGE_XIANSHI_AUGMENT_SIGNIN )
		self.signInNum += 1
		if not key in self.signInDict:
			self.signInDict[key] = []
		self.signInDict[key].append( day )
		self.client.OnAugmentSignInSuccess( int(key / 100), key % 100, day )
		
	def augmentSignInMonth( self, year, month ):
		"""
		Exposed method
		补签一个月
		"""
		assert self.level >= Const.SIGN_IN_MIN_LEVEL,"player %d level(%d) cannot signIn!" % (self.id, self.level)
		if self.isPWKitBagLock():
			self.client.CLIENT_openInputKBPW()
			return
			
		mtime = time.localtime()
		curYear = mtime.tm_year
		curMonth = mtime.tm_mon
		curDay = mtime.tm_mday
		if curYear - year > 0:
			KBEDebug.ERROR_MSG("Can not augment signin!as year(%d) is far away！" % year)
			return

		if month != time.localtime().tm_mon:
			KBEDebug.ERROR_MSG("you only can augment sign in current month! ")
			return

		temp, days = calendar.monthrange( curYear, month )
		self.tempSignInMonth = []
		rewards = []
		bindTypes = []
		key = year * 100 + month
		for i in range( 1, days + 1):
			if curMonth == month and i >= curDay:continue			# 补签
			if not key in self.signInDict or i not in self.signInDict[key]:
				self.tempSignInMonth.append( i )
				reward, bindType = g_onlineRewardMgr.getSignInReward( i )
				rewards.append(reward)
				bindTypes.append(bindType)
		if self.tempSignInMonth:
			if self.hasEnoughShiTou( len(self.tempSignInMonth) * Const.SIGN_IN_REWARD_AUGMENT_DAY ):
				self.cell.onAugmentSignInMonth( rewards, bindTypes, key )
			else:
				self.statusMessage( csstatus.ONLINE_REWARD_LING_SHI_NOT_ENOUGH, "" )
				
	def onAugmentSignInMonthSuccess( self, key ):
		"""
		define method
		成功补签一个月
		"""
		if key not in self.signInDict:
			self.signInDict[key] = []
		
		if self.payShiTou( len(self.tempSignInMonth) * Const.SIGN_IN_REWARD_AUGMENT_DAY, csdefine.CHANGE_XIANSHI_AUGMENT_SIGNIN ):
			self.signInDict[key].extend(self.tempSignInMonth)
			self.signInNum += len(self.tempSignInMonth)
			self.client.OnAugmentSignInMonthSuccess( int( key / 100), key % 100 )
		#self.writeToDB()
		
	def receiveTotalSignReward( self, accumulateNum ):
		"""
		Exposed method
		领取累计签到奖励
		"""
		if accumulateNum in self.signInRewardList:			# 已经领取过
			KBEDebug.ERROR_MSG("Receive total sign reward fail!As player(%d,%s) has already receive(num:%d)"%( self.id, self.playerName, accumulateNum))
			return
			
		cycleTime = g_onlineRewardMgr.getTotalRewardCycleTime()
		maxDay = g_onlineRewardMgr.getTotalRewardMaxDay()
		if int(self.signInRewardNum / cycleTime) * maxDay + accumulateNum > self.signInNum:	# 还没有达到领取时间
			KBEDebug.ERROR_MSG("Receive total sign reward fail!As player(%d,%s) not arrive!"%( self.id, self.playerName))
			return
		
		reward, bindType = g_onlineRewardMgr.getTotalRewardReward( accumulateNum )
		self.cell.onReceiveTotalSignReward( reward, bindType, accumulateNum )
		
	def onReceiveTotalSignRewardSuccess( self, accumulateNum ):
		"""
		define method
		成功领取累计签到奖励
		"""
		self.signInRewardNum += 1
		
		cycleTime = g_onlineRewardMgr.getTotalRewardCycleTime()
		if len( self.signInRewardList ) + 1 >= cycleTime:
			self.signInRewardList.clear()
		else:
			self.signInRewardList.append( accumulateNum )
		self.client.OnReceiveTotalSignRewardSuccess( accumulateNum )

	def onNewDayLoginSuccess( self ):
		"""玩家在新的一天登录, 更新在线礼包数据"""
		maxDay = g_onlineRewardMgr.getOnlineRewardMaxDay( self.profession )
		curTime = time.localtime()
		createTime = time.localtime(self.createTime)
		if curTime.tm_year == createTime.tm_year and curTime.tm_mon == createTime.tm_mon:
			onlineDay = time.localtime().tm_mday - time.localtime(self.createTime).tm_mday + 1
			if onlineDay == (maxDay + 1):
				self.client.OnFinishReceiveNewPlayerGift()
				return
			elif onlineDay <= maxDay:
				self.initNewPlayerGift()
