# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Math
import KBEngine

class SpaceCopyTongCampWarBase( SpaceCopy ):
	"""
	CST-8722 帮会阵营战  大本营
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self._enterPos = Math.Vector3( 0,0,0 )
		self._enterDir = Math.Vector3( 0,0,0 )

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )

		posStr = configData["SpaceData"].get( "enterPosition", "" )
		pos = Functions.vector3TypeConvert( posStr )
		if pos:
			self._enterPos = KBEMath.Unreal2KBEnginePosition( pos )

		dirStr = configData["SpaceData"].get( "enterDirection", "" )
		dir = Functions.vector3TypeConvert( dirStr )
		if dir:
			self._enterDir = KBEMath.Unreal2KBEngineDirection( dir )

	def getEnterPosInfo( self ):
		return ( self._enterPos, self._enterDir )
