# -*- coding: utf-8 -*-
from ActivityBunchModule.ActivityBase import ActivityBase
import csdefine
from ActivityBunchModule import ABDefine
import csstatus

class ActivityYeZhanFengQi( ActivityBase ):
	"""
	血斗凤栖镇
	"""
	def __init__( self, actBunch, bunchName, section ):
		ActivityBase.__init__( self, actBunch, bunchName, section )
		self._joinInfos = {}
	
	def addjoinner( self, actMgr, joinEntityMB, params ):
		"""
		添加本轮活动的参考者
		"""
		activityKey = params.get( "activityKey", None )
		playerDBID = params.get( "playerDBID", 0 )
		playerName = params.get("playerName","")
		if not self._joinInfos.get( activityKey,None ):
			self._joinInfos[ activityKey ] = {}
		
		if len( self._joinInfos[ activityKey ] ) >= self._joinNumber: #参与人数满
			joinEntityMB.cell.actBunch_onAddJoinner( self._bunchName, self._activityName, csdefine.ACTIVITY_BUNCH_RESULT_FULL )
			return
		
		self._joinInfos[ activityKey ][ playerDBID ] = playerName
		joinEntityMB.cell.actBunch_onAddJoinner( self._bunchName, self._activityName, csdefine.ACTIVITY_BUNCH_RESULT_OK )

	def join( self, actMgr, joinEntityMB, params ):
		"""
		进入血斗凤栖镇
		"""
		if self.getCurrentState() != ABDefine.ACTIVITY_STATE_START:
			return

		activityKey = params.get("activityKey",None)
		playerDBID = params.get("playerDBID",0)
		if not self._joinInfos.get(activityKey,None):
			return
		if not self._joinInfos[activityKey].get(playerDBID,None):
			return
		self._joinScript.join( actMgr, joinEntityMB, params )