# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
from Singleton import Singleton
from LoadModule import *

class OnlineRewardMgr( Singleton ):
	"""
	在线奖励
	"""
	def __init__( self ):
		self._onlineReward = {}
		self._signInReward = {}
		self._totalSignInReward = {}
		
	def init( self ):
		""""""
		onlineReward = openJsonCfg("Reward/OnlineReward/OnlineRewardData.json")
		for reward in onlineReward:
			Profession = reward.pop("Profession")
			if not Profession in self._onlineReward:
				self._onlineReward[Profession] = {}
			day = int(reward.pop("Day"))
			self._onlineReward[Profession].update( {day : reward} )
		
		signInReward = openJsonCfg("Reward/OnlineReward/SignInRewardCfg.json")
		for reward in signInReward:
			self._signInReward[reward["Name"]] = reward
		
		totalSignInReward = openJsonCfg("Reward/OnlineReward/TotalSignInRewardCfg.json")
		for reward in totalSignInReward:
			self._totalSignInReward[reward["Name"]] = reward
	
	def getOnlineRewardMaxDay( self, Profession ):
		"""获取最大的在线奖励天数"""
		return max( self._onlineReward[Profession] )
		
	def getOnlineRewardMaxCount( self, Profession, day ):
		"""获取一天的最大奖励次数"""
		return len( self._onlineReward[Profession][day]["Time"].split("|"))
		
	def getOnlineRewardInfo( self, Profession, day, count ):
		"""获取奖励数据"""
		times = self._onlineReward[Profession][day]["Time"].split("|")
		rewards = self._onlineReward[Profession][day]["Gift"].split("|")
		bindType = self._onlineReward[Profession][day].get("BindType", 0)
		return int(times[count]), rewards[count], int(bindType)
		
	def getSignInReward( self, day ):
		"""获取签到奖励"""
		if str(day) in self._signInReward:
			return self._signInReward[str(day)]["Gift"], self._signInReward[str(day)].get("BindType", 0)
		return ("", 0)
		
	def getTotalRewardCycleTime( self ):
		"""获取累计签到奖励周期"""
		return len( self._totalSignInReward )
		
	def getTotalRewardMaxDay( self ):
		"""获取累计签到奖励最大累计天数"""
		temp = []
		for i in self._totalSignInReward.keys():
			temp.append( int(i))
		return max( temp )
		
	def getTotalRewardReward( self, day ):
		"""获取累计N天的奖励"""
		if str(day) in self._totalSignInReward:
			return self._totalSignInReward[str(day)]["Gift"], self._totalSignInReward[str(day)].get("BindType", 0)
		return ("", 0)
		
	
g_onlineRewardMgr = OnlineRewardMgr()