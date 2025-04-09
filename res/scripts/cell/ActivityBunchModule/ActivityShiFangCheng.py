# -*- coding: utf-8 -*-

from ActivityBunchModule.ActivityBase import ActivityBase

import csstatus
from ActivityBunchModule import ABDefine
import csdefine


class ActivityShiFangCheng( ActivityBase ):
	def __init__( self, actBunch, section ):
		ActivityBase.__init__( self, actBunch, section )

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
	