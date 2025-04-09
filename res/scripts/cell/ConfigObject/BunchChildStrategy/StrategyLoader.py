# -*- coding: utf-8 -*-

import KBEngine
from LoadModule import *
from Singleton import Singleton
from ConfigObject.BunchChildStrategy.StrategyObject import StrategyObject

class StrategyLoader( Singleton ):
	"""
	副本串"子副本随机策略"加载模块
	"""
	def __init__( self ):
		Singleton.__init__( self )
		self._datas = {}
	
	def init( self ):
		cfgDatas = openJsonCfg("BunchChildStrategyCfg.json")
		for id, datas in cfgDatas.items():
			self._datas[ id ] = {}
			
			for stage, oneStageDatas in datas.items():
				self._datas[ id ][ stage ] = []
				for oneStrategy in oneStageDatas:
					obj = StrategyObject()
					obj.init( oneStrategy )
					self._datas[ id ][ stage ].append( obj )
	
	def reloadConfig( self ):
		"""
		热加载配置
		"""
		self._datas = {}
		self.init()
	
	def getFirstSpace( self, bunchObj, playerEntity ):
		"""
		获取第一个子副本
		"""
		try:
			stageKey = "stage1"
			strategyObjList = self._datas[ bunchObj.strategyID ][ stageKey ]
		except:
			return ""
		
		for obj in strategyObjList:
			if obj.checkConditions( bunchObj, None, playerEntity ):
				return obj.getSpace( bunchObj, None, playerEntity )
		
		return ""
	
	def getNextSpace( self, bunchObj, spaceEntity ):
		"""
		获取下一个子副本
		"""
		try:
			stageKey = "stage%s"%(spaceEntity.bunchStage + 1)
			strategyObjList = self._datas[ bunchObj.strategyID ][ stageKey ]
		except:
			return ""
		
		for obj in strategyObjList:
			if obj.checkConditions( bunchObj, spaceEntity, None ):
				return obj.getSpace( bunchObj, spaceEntity, None )
		
		return ""
	
	def testFirstSpace( self, playerID, bunchScriptID ):
		"""
		测试接口：获取第一个子副本
		"""
		from ObjectScript.ObjectScriptFactory import g_objFactory
		playerEntity = KBEngine.entities[ playerID ]
		bunchObj = g_objFactory.getBunchSpaceObject( bunchScriptID )
		destSpace = self.getFirstSpace( bunchObj, playerEntity )
		return destSpace
	
	def testNextSpace( self, playerID ):
		"""
		测试接口：获取下一个子副本
		"""
		playerEntity = KBEngine.entities[ playerID ]
		spaceEntity = playerEntity.getCurrentSpace()
		bunchObj = spaceEntity.getScript().getBunchSpaceObj()
		destSpace = self.getNextSpace( bunchObj, spaceEntity )
		return destSpace


g_bunchChildStrategyLoader = StrategyLoader()