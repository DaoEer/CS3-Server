# -*- coding: utf-8 -*-
from SmartImport import smartImport
from ActivityBunchModule import ABDefine

class ActBunch( object ):
	"""
	一个活动群
	"""
	def __init__( self, actObj, bunchName ):
		object.__init__( self )
		self._bunchName = bunchName
		self._startActivityKey = ""
		self._activities = {}

	def loadConfig( self, config ):
		"""
		加载数据
		"""	
		for activityConfig in config["Activities"]:
			actScript = activityConfig["ActivityScript"]
			actName = activityConfig["ActivityName"]
			ObjClass = smartImport( "ActivityBunchModule." + actScript + ":" + actScript )
			obj = ObjClass( self, activityConfig )
			self._activities[actName] = obj

		self._startActivityKey = config["StartActivity"]
	
	def getActObj( self ):
		return self._actObj

	def getName( self ):
		return self._bunchName
	
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

	def signUp( self, signUpEntity ):
		"""
		报名某个活动串
		"""
		pass

	def join( self, actName, joinEntity, params ):
		"""
		参与某个活动串
		"""
		self._activities[actName].join( joinEntity, params )

	def joinNext( self, actName, joinEntity, params ):
		"""
		参加活动串里的某个活动
		"""
		self._activities[ actName ].joinNext( joinEntity, params )

	def onAddJoinner( self, actName, joinEntity, result ):
		"""
		参加活动回调
		"""
		self._activities[ actName ].onAddJoinner( joinEntity, result )

	def getNextJoinMembers( self, actName ):
		"""
		获得允许参与该活动的人数
		"""
		return self._activities[actName].getNextJoinMembers()
