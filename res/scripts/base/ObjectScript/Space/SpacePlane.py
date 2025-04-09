# -*- coding: utf-8 -*-

import KBEMath
import Math
from ObjectScript.Space.SpaceBase import SpaceBase

class SpacePlane( SpaceBase ):
	def __init__( self ):
		SpaceBase.__init__( self )
		self._reviveScriptID = ""
		self._revivePosition = Math.Vector3(0.0, 0.0, 0.0)
		self._reviveDirection = Math.Vector3(0.0, 0.0, 0.0)
		self._spaceMaxLevel = 99999		# 地图的最大等级
		
	def initData( self, configData ):
		SpaceBase.initData( self, configData )
		self._reviveScriptID = configData["SpaceData"].get( "reviveScriptID", "")
		self._revivePosition = KBEMath.Unreal2KBEnginePosition( Math.Vector3( configData["SpaceData"].get( "revivePosition", (0.0,0.0,0.0)) ) )
		self._reviveDirection = KBEMath.Unreal2KBEngineDirection( Math.Vector3( configData["SpaceData"].get( "reviveDirection", (0.0,0.0,0.0)) ))
		self._spaceMaxLevel = configData["SpaceData"].get("spaceMaxLevel",99999)

	def getEntityProperties( self, params ):
		entityDict = SpaceBase.getEntityProperties( self, params )
		if "packSpaceLevel" in params["createArgs"]:	# 如果打包了参数packSpaceLevel，将会以此赋值副本等级spaceLvel
			level = params["createArgs"].pop( "packSpaceLevel" )
			if level > self._spaceMaxLevel:
				level = self._spaceMaxLevel
			entityDict[ "spaceLevel" ] = level
		entityDict.update( params )
		return entityDict