# -*- coding: utf-8 -*-

from ActivityBunchModule.ActBunch import ActBunch
import KBEngine
import csstatus
from ActivityBunchModule import ABDefine
from Functions import Functor
import KST

class ActBunchZhiZunZhenBa( ActBunch ):
	"""
	至尊争霸活动群
	"""
	def __init__( self, actObj, bunchName ):
		ActBunch.__init__( self, actObj, bunchName )
		self.minLevel = 0
		self.maxLevel = 0
		self._signupInfos = {}

	def loadConfig( self, config ):
		"""
		加载数据
		"""
		ActBunch.loadConfig( self, config )
		self.minLevel = config["MinLevel"]
		self.maxLevel = config["MaxLevel"]

	def onNotice( self ):
		"""
		公告
		"""
		ActBunch.onNotice( self )
		KST.g_baseAppEntity.globalWold( csstatus.ZHIZUNZHENBA_ACTIVITY_START,"" )

	def onSignUp( self ):
		"""
		开始报名
		"""
		ActBunch.onSignUp( self )
		KST.g_baseAppEntity.globalWold( csstatus.ZHIZUNZHENBA_ACTIVITY_START,"" )
		self._signupInfos = {}

	def onSignUpEnd( self ):
		"""
		报名结束
		""" 
		ActBunch.onSignUpEnd( self )

	def signUp( self, actMgr, signUpEntityMB, params ):
		"""
		报名
		"""
		ActBunch.signUp( self, actMgr, signUpEntityMB, params )
		if self.getStartActivity().getCurrentState() == ABDefine.ACTIVITY_STATE_FREE:
			signUpEntityMB.statusMessage( csstatus.ZHIZUNZHENBA_NOT_SIGN_UP_START,"" )
			return
		if self.getStartActivity().getCurrentState() != ABDefine.ACTIVITY_STATE_SIGNUP:
			signUpEntityMB.statusMessage( csstatus.SHI_FANG_CHENG_SIGN_UP_END,"" )
			return
		
		activityKey = params.get("activityKey",None)
		if not self._signupInfos.get(activityKey,None):
			self._signupInfos[activityKey] = {}

		if len( self._signupInfos[activityKey] ) >= self.getStartActivity().getJoinNumber():
			signUpEntityMB.statusMessage( csstatus.ZHIZUNZHENBA_SIGN_UP_LIMIT_NUMBER,"" )
			return

		signUpEntityDBID = params.get("playerDBID",0)
		signUpEntityPlayerName = params.get("playerName","")
		if signUpEntityDBID:
			if signUpEntityDBID in self._signupInfos[activityKey]: #已报名
				signUpEntityMB.statusMessage( csstatus.SHI_FANG_CHENG_SIGN_UP_AREADY,"" )
			else:
				self._signupInfos[activityKey][signUpEntityDBID] = signUpEntityPlayerName
				self.getStartActivity().addjoinner(actMgr, signUpEntityMB, params)
				signUpEntityMB.statusMessage( csstatus.SHI_FANG_CHENG_SIGN_UP_SUCCESS,"" )

	def join( self, actMgr, actName, joinEntityMB, params ):
		"""
		参加某活动
		"""
		if self.getCurrentState() != ABDefine.ACTIVITY_STATE_START:
			joinEntityMB.statusMessage( csstatus.ZHIZUNZHENBA_NOT_SIGN_UP_START,"" )
			return

		ActBunch.join( self, actMgr, actName, joinEntityMB, params )
				

	def onCompleteActivityStage( self,actName, joinEntityMB,playerDBID,playerName,completeStage, useTime ):
		"""
		完成某个活动的某阶段
		"""
		self._activities[actName].onCompleteActivityStage(joinEntityMB,playerDBID,playerName,completeStage , useTime )
