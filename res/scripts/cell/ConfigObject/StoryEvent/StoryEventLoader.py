# -*- coding: utf-8 -*-

import HotUpdate
from ConfigObject.StoryEvent.StoryEvent import *
from StoryEventConfig import Datas
from Singleton import Singleton
import KBEDebug

class StoryEventLoader( Singleton ):
	"""
	过场动画事件加载模块
	"""
	def __init__( self ):
		Singleton.__init__( self )
		self.storyEvents = {}	#{ storyID:{orderIndex:[event1,event2,...]}}
	
	def init( self ):
		for storyID, infoCfg in Datas.items():
			self.storyEvents[ storyID ] = {}
			
			for orderIndex, eventsCfg in infoCfg.items():
				self.storyEvents[ storyID ][ orderIndex ] = []
				
				for eventDictCfg in eventsCfg:
					eventClass = eval( eventDictCfg["script"] )
					eventObj = eventClass( storyID, orderIndex )
					try:
						eventObj.init( eventDictCfg )
					except:
						KBEDebug.ERROR_MSG("StoryEvent is error storyID =%s, orderIndex = %s eventClass=%s"%( storyID,orderIndex,eventClass ))
					self.storyEvents[ storyID ][ orderIndex ].append( eventObj )
	
	def reloadConfig( self ):
		"""
		热加载配置
		"""
		import StoryEventConfig
		newModule = HotUpdate.reloadByModule( StoryEventConfig )
		self.storyEvents.clear()
		for storyID, infoCfg in newModule.Datas.items():
			self.storyEvents[ storyID ] = {}
			
			for orderIndex, eventsCfg in infoCfg.items():
				self.storyEvents[ storyID ][ orderIndex ] = []
				
				for eventDictCfg in eventsCfg:
					eventClass = eval( eventDictCfg["script"] )
					eventObj = eventClass( storyID, orderIndex )
					eventObj.init( eventDictCfg )
					self.storyEvents[ storyID ][ orderIndex ].append( eventObj )
	
	def getEvents( self, storyID, orderIndex ):
		try:
			return self.storyEvents[ storyID ][ orderIndex ]
		except:
			return None

g_storyEventLoader = StoryEventLoader()