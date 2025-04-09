# -*- coding: utf-8 -*-

from ActivityBunchModule.ActBunch import ActBunch
import KBEngine

class ActBunchZhiZunZhenBa( ActBunch ):
	"""
	至尊争霸活动群
	"""
	def __init__( self, actObj, bunchName ):
		ActBunch.__init__( self, actObj, bunchName )
		self.minLevel = 0
		self.maxLevel = 0

	def loadConfig( self, config ):
		"""
		加载数据
		"""
		ActBunch.loadConfig( self, config )
		self.minLevel = config["MinLevel"]
		self.maxLevel = config["MaxLevel"]

	def getActivityKey( self, joinEntity ):
		"""
		获得进入副本空间key
		根据玩家的等级 30-39
		"""
		return int(joinEntity.getLevel()/10)

	def signUpPickData( self, joinEntity ):
		"""
		打包报名数据
		"""
		pickData = {}
		pickData["activityKey"] = self.getActivityKey(joinEntity)
		pickData["playerDBID"] = joinEntity.playerDBID
		pickData["playerName"] = joinEntity.getName()
		return pickData

	def signUp( self, signUpEntity ):
		"""
		报名活动串
		"""
		signData = self.signUpPickData( signUpEntity )
		KBEngine.globalData["ActivityBunchManager"].signUp( self._bunchName, signUpEntity.base, signData )