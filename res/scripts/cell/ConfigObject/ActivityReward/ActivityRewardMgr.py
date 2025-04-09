# -*- coding: utf-8 -*-
import KBEDebug
from Singleton import Singleton

class ActivityRewardMgr( Singleton ):
	"""
	活动奖励管理类
	"""
	def __init__( self ):
		self.activityRewards = {}

	def init( self, rewardConfig ):
		"""
		"""
		self.activityRewards.clear()
		for spaceScriptID,rewardDatas in rewardConfig.items():
			self.activityRewards[spaceScriptID] = rewardDatas

	def getRewardMailIDByRank( self, spaceScriptID,rank ):
		"""
		根据名次获得邮件ID
		"""
		if spaceScriptID not in self.activityRewards.keys():
			return ""
		rewardDatas = self.activityRewards[spaceScriptID]
		for rewardData in rewardDatas:
			if rank >= rewardData["minRank"] and rank <= rewardData["maxRank"]:
				return rewardData["mailID"]
		return ""

g_activityRewardMgr = ActivityRewardMgr()