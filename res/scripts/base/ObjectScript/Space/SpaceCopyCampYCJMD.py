# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import Math
import Functions
import KBEMath
import csdefine

class SpaceCopyCampYCJMD( SpaceCopy ):
	"""
	阵营战场“勇闯绝命岛” JIRA CST-9960
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self._enterPos = Math.Vector3(0.0, 0.0, 0.0)
		self._enterDir = Math.Vector3(0.0, 0.0, 0.0)
	
	def initData( self, configData ):
		SpaceCopy.initData( self, configData )
		enterPosStr = configData["SpaceData"].get( "enterPos","" )
		enterDirStr = configData["SpaceData"].get( "enterDir","" )
		self._enterPos = KBEMath.Unreal2KBEnginePosition(Functions.vector3TypeConvert( enterPosStr ))
		self._enterDir = KBEMath.Unreal2KBEngineDirection(Functions.vector3TypeConvert( enterDirStr ))


	def getEnterPos( self, camp ):
		"""
		获得进入的坐标
		"""
		return ( self._enterPos, self._enterDir )
