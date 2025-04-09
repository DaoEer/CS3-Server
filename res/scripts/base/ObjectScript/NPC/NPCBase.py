# -*- coding: utf-8 -*-

import KBEngine
#script
import random

from KBEDebug import *
import ObjectScript.ObjectScriptBase.NPCBaseScript as NPCBaseScript
from ObjectScript.NPC import NPCPropertyLoader

class NPCBase(NPCBaseScript.NPCBaseScript,NPCPropertyLoader.NPCPropertyLoader):
	"""
	NPC对象script类
	"""
	def __init__(self):
		"""
		"""
		NPCBaseScript.NPCBaseScript.__init__(self)
		NPCPropertyLoader.NPCPropertyLoader.__init__(self)
		
		self.minLv			= 0
		self.maxLv			= 0

	def initData(self, configData):
		"""
		初始化数据
		@param data: dict
		"""
		NPCBaseScript.NPCBaseScript.initData( self, configData )
		NPCPropertyLoader.NPCPropertyLoader.initData(self,configData)
		
		self.minLv			= configData["MinLevel"]
		self.maxLv			= configData["MaxLevel"]
		
	def getEntityProperties( self, params ):
		return NPCPropertyLoader.NPCPropertyLoader.getEntityProperties( self, params )
		
	def createEntity( self, spaceID, position, direction, params ) :
		"""
		创建entity
		"""
		if not 'level' in params:
			params["level"] = random.randint( self.minLv, self.maxLv )
		return NPCBaseScript.NPCBaseScript.createEntity( self, spaceID, position, direction, params )