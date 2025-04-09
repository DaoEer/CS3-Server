# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import Math
import KBEMath
import Functions
import csdefine
import random

class SpaceCopySGMZ( SpaceCopy ):
	"""
	上古密阵
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.enterPosList = []
		self.enterDirList = []
	
	def initData( self, configData ):
		SpaceCopy.initData( self, configData )
		enterPosStr = configData["SpaceData"].get( "enterPos","" )
		enterDirStr = configData["SpaceData"].get( "enterDir","" )
		self.enterPosList = enterPosStr.split("|")
		self.enterDirList = enterDirStr.split("|")

	def getEnterPos( self, camp, index=0 ):
		"""
		获得进入的坐标
		"""
		if len( self.enterPosList ) > 3 and len(self.enterDirList) > 3:
			if camp == csdefine.CAMP_TAOSIM:
				xianPos = Functions.vector3TypeConvert( self.enterPosList[ index ] )
				enterXianPos = KBEMath.Unreal2KBEnginePosition( xianPos )
				xianDir = Functions.vector3TypeConvert( self.enterDirList[ index ] )
				enterXianDir = KBEMath.Unreal2KBEngineDirection( xianDir )
				return ( enterXianPos, enterXianDir )

			elif camp == csdefine.CAMP_DEMON:
				moPos = Functions.vector3TypeConvert( self.enterPosList[ index ] )
				enterMoPos = KBEMath.Unreal2KBEnginePosition( moPos )
				moDir = Functions.vector3TypeConvert( self.enterDirList[ index ] )
				enterMoDir = KBEMath.Unreal2KBEngineDirection( moDir )
				return ( enterMoPos, enterMoDir )
			else:
				return ( Math.Vector3( 0, 0, 0 ), Math.Vector3( 0, 0, 0 ) )
		else:
			return ( Math.Vector3( 0, 0, 0 ), Math.Vector3( 0, 0, 0 ) )