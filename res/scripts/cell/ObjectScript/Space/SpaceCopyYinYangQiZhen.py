# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyStory import SpaceCopyStory
import KBEDebug
import Math

class SpaceCopyYinYangQiZhen( SpaceCopyStory ):
	"""
	阴阳棋阵副本
	"""
	def __init__( self ):
		SpaceCopyStory.__init__( self )
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopyStory.initData( self, configData )
		originPos = configData["SpaceData"].get( "originPos", "" )
		if originPos:
			originPos = originPos.split("|")
			self._originPos = tuple( [ float(i) for i in originPos ] )
		self._unitLength = float(configData["SpaceData"].get("unitLength",0.0))
		self._blackID = configData["SpaceData"].get("blackID","")
		self._whiteID = configData["SpaceData"].get("whiteID","")
		self.bossID = configData["SpaceData"].get("bossID","")
		self.monsterQiZiID = configData["SpaceData"].get("monsterQiZiID","")

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyStory.initEntity( self, selfEntity )
		selfEntity.initSpaceData( Math.Vector3(self._originPos), self._unitLength, self._blackID,self._whiteID , self.bossID, self.monsterQiZiID )
