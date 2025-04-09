# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug

class ActivityBase( object ):
	"""
	活动
	"""
	def __init__( self, actBunch, activityConfig ):
		self._actBunch = actBunch
		self._activityName = activityConfig["ActivityName"]
		self._nextActivity = activityConfig["NextActivity"]
		self._joinNumber = activityConfig.get("JoinNumber",0)
	
	def nextPickData( self, signupEntity,params):
		"""
		打包报名数据
		"""
		return {}
	
	def joinPickData( self, joinEntity, params ):
		"""
		打包参与数据
		"""
		return {}

	def join( self, joinEntity, params ):
		"""
		参加某个活动
		"""
		pickDict = self.joinPickData( joinEntity, params )
		KBEngine.globalData["ActivityBunchManager"].join( self._actBunch.getName(), self._activityName, joinEntity.base, pickDict )

	def joinNext( self, joinEntity, params ):
		"""
		"""
		nextPickData = self.nextPickData(joinEntity,params)
		nextPickData.update(params)
		KBEngine.globalData["ActivityBunchManager"].joinNext( self._actBunch.getName(), self._activityName, joinEntity.base, nextPickData )

	def onAddJoinner( self, joinEntity, result ):
		"""
		添加参与者回调
		"""
		pass

	def getNextJoinMembers( self ):
		"""
		获得允许参与该活动的人数
		"""
		return self._joinNumber
