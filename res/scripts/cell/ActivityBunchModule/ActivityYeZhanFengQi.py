# -*- coding: utf-8 -*-
from ActivityBunchModule.ActivityBase import ActivityBase
import csdefine
from ActivityBunchModule import ABDefine
import csstatus

class ActivityYeZhanFengQi( ActivityBase ):
	"""
	血斗凤栖镇
	"""
	def __init__( self, actBunch, section ):
		ActivityBase.__init__( self, actBunch, section )
		
	def onAddJoinner( self, joinEntity, result ):
		"""
		添加参与者回调
		"""
		if result == csdefine.ACTIVITY_BUNCH_RESULT_OK:
			joinEntity.getCurrentSpace().passSuccess()
		else:
			joinEntity.getCurrentSpace().passFailure()

	def nextPickData( self, joinEntity, params ):
		"""
		打包报名数据
		"""
		pickData = {}
		pickData[ "activityKey" ] = self._actBunch.getActivityKey( joinEntity ) #活动的key
		pickData["playerDBID"] = joinEntity.playerDBID
		pickData[ "playerName" ] = joinEntity.playerName
		return pickData
	
	def joinPickData( self, joinEntity, params ):
		"""
		打包参与数据
		"""
		pickData = {}
		pickData[ "activityKey" ] = self._actBunch.getActivityKey( joinEntity ) #活动的key
		pickData["playerDBID"] = joinEntity.playerDBID
		return pickData