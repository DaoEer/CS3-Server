# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import Math
import KBEMath
import Functions
import csdefine

class SpaceCopyYXLM( SpaceCopy ):
	"""
	英雄联盟
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

		self._enterXianPos = Math.Vector3(0.0, 0.0, 0.0)
		self._enterXianDir = Math.Vector3(0.0, 0.0, 0.0)
		self._enterMoPos = Math.Vector3(0.0, 0.0, 0.0)
		self._enterMoDir = Math.Vector3(0.0, 0.0, 0.0)
	
	def initData( self, configData ):
		SpaceCopy.initData( self, configData )
		enterPosStr = configData["SpaceData"].get( "enterPos","" )
		enterDirStr = configData["SpaceData"].get( "enterDir","" )
		enterPosList = enterPosStr.split("|")
		enterDirList = enterDirStr.split("|")
		if len(enterPosList) > 1:
			xianPos = Functions.vector3TypeConvert( enterPosList[0] )
			if xianPos:
				self._enterXianPos = KBEMath.Unreal2KBEnginePosition( xianPos )

			moPos = Functions.vector3TypeConvert( enterPosList[1] )
			if moPos:
				self._enterMoPos = KBEMath.Unreal2KBEnginePosition( moPos )

		if len(enterDirList) > 1:
			xianDir = Functions.vector3TypeConvert( enterDirList[0] )
			if xianDir:
				self._enterXianDir = KBEMath.Unreal2KBEngineDirection( xianDir )

			moDir = Functions.vector3TypeConvert( enterDirList[1] )
			if moDir:
				self._enterMoDir = KBEMath.Unreal2KBEngineDirection( moDir )


	def getEnterPos( self, camp ):
		"""
		获得进入的坐标
		"""
		if camp == csdefine.CAMP_TAOSIM:
			return ( self._enterXianPos, self._enterXianDir )
		elif camp == csdefine.CAMP_DEMON:
			return ( self._enterMoPos, self._enterMoDir )
