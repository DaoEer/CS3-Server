# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import Math
import KBEMath
import Functions
import csarithmetic

class SpaceCopyHomeBarracksBHZB( SpaceCopy ):
	"""
	帮会争霸大本营
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.needTongNum = 0
		self.enterCenterPos = Math.Vector3( 0.0,0.0,0.0 )
		self.enterDir = Math.Vector3( 0.0,0.0,0.0 )
		self.radius = 0.0
	
	def initData( self, configData ):
		SpaceCopy.initData( self, configData )
		self.needTongNum = configData["SpaceData"].get("needTongNum",0)

		enterCenterPosStr = configData["SpaceData"].get( "enterCenterPos","" )
		if enterCenterPosStr:
			enterCenterPos = Functions.vector3TypeConvert( enterCenterPosStr )
			self.enterCenterPos = KBEMath.Unreal2KBEnginePosition( enterCenterPos )

		enterDirStr = configData["SpaceData"].get( "enterDir","" )
		if enterDirStr:
			enterDir = Functions.vector3TypeConvert( enterDirStr )
			self.enterDir = KBEMath.Unreal2KBEngineDirection( enterDir )

		self.radius = configData["SpaceData"].get( "radius",0.0 )

	def getEnterInfo( self ):
		"""
		获得进入信息
		"""
		enterPos = csarithmetic.getPositionByCircular( self.enterCenterPos, self.radius )
		return enterPos, self.enterDir
	
	def getNeedTongNum( self ):
		"""
		获得最少所需的帮会去开活动
		"""
		return self.needTongNum