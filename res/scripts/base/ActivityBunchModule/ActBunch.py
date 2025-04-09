# -*- coding: utf-8 -*-

from SmartImport import smartImport
from ActivityBunchModule import ABDefine
import KST
import KBEDebug

class ActBunch( object ):
	"""
	一个活动群
	"""
	def __init__( self, actObj, bunchName ):
		object.__init__( self )
		self._actObj = actObj
		self._bunchName = bunchName
		self._activities = {}
		self._startActivityKey = ""
		self.currentState = ABDefine.ACTIVITY_STATE_FREE
		#Crond event key
		self._noticeFuncKey = ""
		self._signupFuncKey = ""
		self._signupEndFuncKey = ""
		self._startFuncKey = ""
		self._endFuncKey = ""
		self._statusMsgAreadyKey = "" #准备比赛提示的
		#notify string
		self._notifySignup = ""
		self._notifySignupEnd = ""
		self._notifyStart = ""
		self._notifyEnd = ""

	def loadConfig( self, config ):
		"""
		加载数据
		"""	
		for activity in config["Activities"]:
			actScript = activity["ActivityScript"]
			actName = activity["ActivityName"]
			ObjClass = smartImport( "ActivityBunchModule." + actScript + ":" + actScript )
			obj = ObjClass( self, self._bunchName, activity )
			self._activities[actName] = obj

		self._startActivityKey = config["StartActivity"]

		if config.get("EventKey",None):
			eventKey = config["EventKey"]
			self._noticeFuncKey = eventKey.get("noticeKey","")
			self._signupFuncKey = eventKey.get("signUpKey","")
			self._signupEndFuncKey = eventKey.get("signEndKey","")
			self._startFuncKey = eventKey.get("startKey","")
			self._endFuncKey = eventKey.get("endKey","")
			if self._noticeFuncKey: #提示
				self.getActObj().registerEventFunc( self._noticeFuncKey,self.onNotice )
			if self._signupFuncKey: # 报名
				self.getActObj().registerEventFunc( self._signupFuncKey,self.onSignUp )
			if self._signupEndFuncKey: #结束报名
				self.getActObj().registerEventFunc( self._signupEndFuncKey, self.onSignUpEnd )
			if self._startFuncKey:	#开始
				self.getActObj().registerEventFunc( self._startFuncKey, self.onStart )
			if self._endFuncKey:	#结束
				self.getActObj().registerEventFunc( self._endFuncKey, self.onEnd )

			if self._statusMsgAreadyKey: #
				self.getActObj().registerEventFunc( self._statusMsgAreadyKey, self.statusMsgAready )
		
		if config.get("NotifyKey",None):
			notifyKey = config["NotifyKey"]
			self._notifySignup = notifyKey.get("signUpMsg","")
			self._notifySignupEnd = notifyKey.get("signEndMsg","")
			self._notifyStart = notifyKey.get("startMsg","")
			self._notifyEnd = notifyKey.get("endMsg","")
	
	def getActObj( self ):
		return self._actObj
	
	def getStartActivity( self ):
		"""
		获取开始活动
		"""
		return self._activities[ self._startActivityKey ]
	
	def getActivity( self, activityName ):
		return self._activities[ activityName ]
	
	def getCurrentState( self ):
		"""
		获取状态
		"""
		return self.currentState


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
		self.currentState = ABDefine.ACTIVITY_STATE_SIGNUP
		if self._notifySignup:
			pass

	def onSignUpEnd( self ):
		"""
		报名结束
		""" 
		self.currentState = ABDefine.ACTIVITY_STATE_FREE
		if self._notifyEnd:
			pass

	def onStart( self ):
		"""
		活动开始
		"""
		self.currentState = ABDefine.ACTIVITY_STATE_START
		if self._notifyStart:
			pass

	def onEnd( self ):
		"""
		活动结束
		"""
		self.currentState = ABDefine.ACTIVITY_STATE_FREE
		if self._notifyEnd:
			pass

	def statusMsgAready( self ):
		"""
		"""
		pass
	
#-----------------活动接口------------------------------
	def signUp( self, actMgr, signUpEntityMB, params ):
		"""
		报名活动串
		"""
		pass

	def join( self, actMgr, actName, joinEntityMB, params ):
		"""
		参加某活动
		"""
		self._activities[actName].join( actMgr, joinEntityMB, params )

	def joinNext( self, actMgr, actName, joinEntityMB, params ):
		"""
		参加下轮活动
		"""
		self._activities[actName].joinNext( actMgr, joinEntityMB, params )

	def onNoticeJoin( self, actMgr, actName, playerMB, playerDBID, isGoto ):
		"""
		确认是否参加
		"""
		pass

	def abandon( self, actMgr, actName, abandonEntityMB, activityKey, playerDBID ):
		"""
		放弃
		"""
		self._activities[actName].abandon( actMgr, abandonEntityMB, activityKey, playerDBID )

