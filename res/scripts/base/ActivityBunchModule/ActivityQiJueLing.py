# -*- coding: utf-8 -*-

from ActivityBunchModule.ActivityBase import ActivityBase

class ActivityQiJueLing( ActivityBase ):
	"""
	七绝岭
	"""
	def __init__( self, actBunch, bunchName, section ):
		ActivityBase.__init__( self, actBunch, bunchName, section )

	def addjoinner( self, actMgr, joinEntityMB, params ):
		"""
		添加本轮活动的参考者
		"""
		activityKey = params.get("activityKey",None)
		playerDBID = params.get("playerDBID", 0)
		playerName = params.get("playerName","")
		score = params.get("score",0)
		KBEngine.globalData["QiJueLingManager"].addJoinData(activityKey,joinEntityMB,playerDBID,playerName,score)