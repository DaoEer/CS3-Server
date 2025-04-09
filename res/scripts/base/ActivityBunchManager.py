# -*- coding: utf-8 -*-

import KBEngine
from CoreObject import MgrPersistentObject
import KBEDebug
import ActivityBunchModule
from ConfigObject.Crond.CrondDatas import CrondDatas
g_CrondDatas = CrondDatas.instance()
import KST

class ActivityBunchManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	活动串管理器
	"""
	def __init__( self ):
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		self.loadAllActiveDatas()

	def loadAllActiveDatas( self ):
		"""
		加载所有活动串的数据
		"""
		ActivityBunchModule.loadAllBunch()
		self.registerCrond()
		self.onCompleteInit()

	def registerCrond( self ):
		"""
		将活动key 注册到Crond中
		"""
		allEventKeys = ActivityBunchModule.getEventKeys()
		if not allEventKeys:
			return
		
		for taskName in allEventKeys:
			for scriptID, cmd in g_CrondDatas.getCrondTaskCmds(taskName):
				KBEngine.globalData["CrondManager"].addScheme( scriptID, cmd, self, "onEventCallBack", -1, str( [taskName,] ) )

	def onEventCallBack( self,cmd, key ):
		"""
		所有活动串Key的回调
		""" 
		if key in ActivityBunchModule.getEventKeys():
			ActivityBunchModule.doEventFunc( key )

	def signUp( self, bunchName, signUpEntityMB, params ):
		"""	
		报名某个活动串
		"""
		ActivityBunchModule.signUp( self, bunchName, signUpEntityMB, params )

	def join( self, bunchName, actName, joinEntityMB, params ):
		"""
		参加某个活动串
		"""
		ActivityBunchModule.join( self, bunchName, actName, joinEntityMB, params )

	def joinNext( self, bunchName, actName, joinEntityMB, params ):
		"""
		参加下轮
		"""
		ActivityBunchModule.joinNext( self, bunchName, actName, joinEntityMB, params )

	def abandon( self, abandonEntityMB, bunchName, actName, activityKey, playerDBID ):
		"""
		放弃
		"""
		ActivityBunchModule.abandon( self, bunchName, actName, abandonEntityMB, activityKey, playerDBID  )

	def onCompleteActivityStage( self, bunchName, actName, joinEntityMB, playerDBID, playerName, completeStage, useTime ):
		"""
		完成某个活动的某阶段
		"""
		ActivityBunchModule.onCompleteActivityStage(bunchName, actName,  joinEntityMB, playerDBID,playerName, completeStage, useTime )

	def sendWoldMsg( self, messageType, messageArg ):
		"""
		发送世界公告消息
		"""
		KST.g_baseAppEntity.globalWold( messageType, messageArg )