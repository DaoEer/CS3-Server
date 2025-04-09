# -*- coding: utf-8 -*-

from SmartImport import smartImport

from ActivityBunchModule.ActivityJoinStyle import JoinStyleBase
from ActivityBunchModule import ABDefine


class ActivityBase( object ):
	"""
	活动
	"""
	def __init__( self, actBunch, bunchName, activityConfig ):
		self._actBunch = actBunch
		self._bunchName = bunchName
		self._activityName = activityConfig[ "ActivityName" ]
		self._nextActivity = activityConfig[ "NextActivity" ]
		self._noticeFuncKey = ""
		self._signupFuncKey = ""
		self._signupEndFuncKey = ""
		self._startFuncKey = ""
		self._endFuncKey = ""
		if activityConfig.get("EventKey",None):
			#加载event key
			eventKeySec = activityConfig[ "EventKey" ]
			self._noticeFuncKey = eventKeySec.get( "noticeKey","" )
			self._signupFuncKey = eventKeySec.get("signUpKey","")
			self._signupEndFuncKey = eventKeySec.get("signEndKey","")
			self._startFuncKey = eventKeySec.get("startKey","")
			self._endFuncKey = eventKeySec.get("endKey","")
			actObj = self._actBunch.getActObj()
			if self._noticeFuncKey: #公告
				actObj.registerEventFunc( self._noticeFuncKey, self.onNotice )
			if self._signupFuncKey: #报名
				actObj.registerEventFunc( self._signupFuncKey, self.onSignUp )
			if self._signupEndFuncKey: #结束报名
				actObj.registerEventFunc( self._signupEndFuncKey, self.onSignUpEnd )
			if self._startFuncKey: #开始
				actObj.registerEventFunc( self._startFuncKey, self.onStart )
			if self._endFuncKey:#结束
				actObj.registerEventFunc( self._endFuncKey, self.onEnd )
		
		#notify string
		self._notifySignup = ""
		self._notifySignupEnd = ""
		self._notifyStart = ""
		self._notifyEnd = ""
		#加载提示
		if activityConfig.get("NotifyKey",None):
			notifyKey = activityConfig["NotifyKey"]
			self._notifySignup = notifyKey.get("signUpMsg","")
			self._notifySignupEnd = notifyKey.get("signEndMsg","")
			self._notifyStart = notifyKey.get("startMsg","")
			self._notifyEnd = notifyKey.get("endMsg","")
		
		if activityConfig.get("JoinStyle",None):
			self._joinScript = JoinStyleBase.getObject( activityConfig[ "JoinStyle" ] )
		
		self._joinNumber = activityConfig.get("JoinNumber",999999)
		
		self.currentState = ABDefine.ACTIVITY_STATE_FREE
	
	def getBunch( self ):
		return self._actBunch
	
	def getNextActivity( self ):
		return self._actBunch.getActivity( self._nextActivity )
	
	def getCurrentState( self ):
		"""
		获取状态
		"""
		return self.currentState
	
	def getJoinNumber( self ):
		return self._joinNumber

#------------日程管理器回调接口----------------------------
	def onNotice( self ):
		"""
		公告
		"""
		pass

	def onSignUp( self ):
		"""
		开始报名
		"""
		if self._notifySignup:
			pass
			
		self.currentState = ABDefine.ACTIVITY_STATE_SIGNUP
	
	def onSignUpEnd( self ):
		"""
		报名结束
		"""
		if self._notifySignupEnd:
			pass
		
		self.currentState = ABDefine.ACTIVITY_STATE_FREE
	
	def onStart( self ):
		"""
		开始活动
		"""
		if self._notifyStart:
			pass
		
		self.currentState = ABDefine.ACTIVITY_STATE_START
	
	def onEnd( self ):
		"""
		活动结束
		"""
		if self._notifyEnd:
			pass
		
		self.currentState = ABDefine.ACTIVITY_STATE_FREE
		
#-----------------活动接口------------------------------
	def signUp( self, actMgr, signupEntityMB, params ):
		"""
		添加本轮报名名单
		"""
		pass
		
	def join( self, actMgr, joinEntityMB, params ):
		"""
		参加本轮活动
		"""
		if self.getCurrentState() != ABDefine.ACTIVITY_STATE_START:
			return
		self._joinScript.join(actMgr,joinEntityMB,params)

	def addjoinner( self, actMgr, joinEntityMB, params ):
		"""
		添加本轮活动的参考者
		"""
		pass

	def joinNext( self, actMgr, joinEntityMB, params ):
		"""
		添加下轮名单
		"""
		self.getNextActivity().addjoinner(actMgr, joinEntityMB, params)

	def abandon( self, actMgr, abandonEntityMB, activityKey, playerDBID ):
		"""
		放弃
		"""
		pass
		