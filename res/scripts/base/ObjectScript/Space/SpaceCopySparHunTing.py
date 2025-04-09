# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Math
import KBEngine

class SpaceCopySparHunTing( SpaceCopy ):
	"""
	晶石狩猎场
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		self.minLevel = configData["SpaceData"].get("minLevel",0)
		self.maxLevel = configData["SpaceData"].get("maxLevel",0)
		self.maxCampEnter = configData["SpaceData"].get("maxCampEnter",0)
		self.exchange = configData["SpaceData"].get("exchange",0)

	def mgrNotify( self ):
		"""
		晶石狩猎管理器创建完，配置数据发送管理器
		"""

		KBEngine.globalData["SparHunTingManager"].registerToMgr( self.scriptID, self.minLevel, self.maxLevel, self.maxCampEnter )
