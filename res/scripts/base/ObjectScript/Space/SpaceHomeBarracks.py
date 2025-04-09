# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceMultiLine import SpaceMultiLine
import Math
import KBEMath
import Functions
import csarithmetic

class SpaceHomeBarracks( SpaceMultiLine ):
	"""
	大本营
	"""
	def __init__( self ):
		SpaceMultiLine.__init__( self )
		self.enterCenterPos = Math.Vector3( 0.0,0.0,0.0 )
		self.enterDir = Math.Vector3( 0.0,0.0,0.0 )
		self.radius = 0.0
	
	def initData( self, configData ):
		SpaceMultiLine.initData( self, configData )
		enterCenterPosStr = configData["SpaceData"].get( "enterCenterPos","" )
		enterCenterPos = Functions.vector3TypeConvert( enterCenterPosStr )
		self.enterCenterPos = KBEMath.Unreal2KBEnginePosition( enterCenterPos )

		enterDirStr = configData["SpaceData"].get( "enterDir","" )
		enterDir = Functions.vector3TypeConvert( enterDirStr )
		self.enterDir = KBEMath.Unreal2KBEngineDirection( enterDir )

		self.radius = configData["SpaceData"].get( "radius","" )

	def getEnterInfo( self ):
		"""
		获得进入信息
		"""
		enterPos = csarithmetic.getPositionByCircular( self.enterCenterPos, self.radius )
		return enterPos, self.enterDir