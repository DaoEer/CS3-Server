# -*- coding: utf-8 -*-


import KBEDebug
import Math
import csdefine
import Functions
import random
import KBEMath
from ConfigObject import PatrolRouteLoader
from ObjectScript.Space.SpaceCopy import SpaceCopy

class SpaceCopyLingQi( SpaceCopy ):
	"""
	收集灵气
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self._reviveData = []
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		reviveData = configData["SpaceData"].get( "reviveLingQiData", "" )
		if reviveData:
			for string in reviveData.split("|"):
				strList  = string.split(":")
				Position = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert( strList[0]))
				Direction = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert( strList[1]))
				self._reviveData.append((Position, Direction))

		if self._patrolRouteFile:
			PatrolRouteLoader.g_patrolRouteLoader.initSpaceMazeRoute( self.scriptID )
		
	def getEnterInfo(self):
		"""
		获得复活信息
		"""
		if not len(self._reviveData):
			return None
		reviveData = list(self._reviveData)
		random.shuffle(reviveData)
		return reviveData[0]
