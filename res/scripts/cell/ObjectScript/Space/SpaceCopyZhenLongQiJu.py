# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyMagicMazeChild import SpaceCopyMagicMazeChild
import KBEDebug
import Math

class SpaceCopyZhenLongQiJu( SpaceCopyMagicMazeChild ):
	"""
	真龙棋局副本
	"""
	def __init__( self ):
		SpaceCopyMagicMazeChild.__init__( self )
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopyMagicMazeChild.initData( self, configData )
		originPos = configData["SpaceData"].get( "originPos", "" )
		if originPos:
			originPos = originPos.split("|")
			self._originPos = tuple( [ float(i) for i in originPos ] )
		self._unitLength = float(configData["SpaceData"].get("unitLength",0.0))
		self._blackID = configData["SpaceData"].get("blackID","")
		self._whiteID = configData["SpaceData"].get("whiteID","")
		self._bossID = configData["SpaceData"].get("bossID","")
		self.effectID = configData["SpaceData"].get("effectID","")
		self.skillID = configData["SpaceData"].get("skillID","")
		self.refreshTime = float(configData["SpaceData"].get("refreshTime",0.5))
		self.refreshCountRates = []
		if configData["SpaceData"].get("refreshCountRates",""):
			self.refreshCountRates =[ float(i) for i in configData["SpaceData"].get("refreshCountRates","").split("|")]

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyMagicMazeChild.initEntity( self, selfEntity )
		selfEntity.initSpaceData( Math.Vector3(self._originPos), self._unitLength, self._blackID,self._whiteID,self._bossID ,self.effectID,self.skillID, self.refreshTime, self.refreshCountRates )
