# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceMultiLine import SpaceMultiLine
import Math
import KBEMath
import Functions
import csarithmetic

class SpaceHomeBarracksBHZB( SpaceMultiLine ):
	"""
	帮会争霸大本营
	"""
	def __init__( self ):
		SpaceMultiLine.__init__( self )
		self.enterCenterPos = Math.Vector3( 0.0,0.0,0.0 )
		self.enterDir = Math.Vector3( 0.0,0.0,0.0 )
		self.radius = 0.0
		self.triggerLineTongAmount = 0
	
	def initData( self, configData ):
		SpaceMultiLine.initData( self, configData )
		enterCenterPosStr = configData["SpaceData"].get( "enterCenterPos","" )
		enterCenterPos = Functions.vector3TypeConvert( enterCenterPosStr )
		self.enterCenterPos = KBEMath.Unreal2KBEnginePosition( enterCenterPos )

		enterDirStr = configData["SpaceData"].get( "enterDir","" )
		enterDir = Functions.vector3TypeConvert( enterDirStr )
		self.enterDir = KBEMath.Unreal2KBEngineDirection( enterDir )

		self.radius = configData["SpaceData"].get( "radius","" )

		self.triggerLineTongAmount = configData["SpaceData"].get("triggerLineTongAmount",0)

	def getEnterInfo( self ):
		"""
		获得进入信息
		"""
		enterPos = csarithmetic.getPositionByCircular( self.enterCenterPos, self.radius )
		return enterPos, self.enterDir

	def getTriggerLineTongAmount( self ):
		"""
		触发分线的帮会数
		"""
		return self.triggerLineTongAmount
