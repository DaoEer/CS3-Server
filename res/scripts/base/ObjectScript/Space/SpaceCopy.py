# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceBase import SpaceBase
from ImpInterface.SpaceBunchInterface import SpaceBunchInterface

class SpaceCopy( SpaceBase, SpaceBunchInterface ):
	def __init__( self ):
		SpaceBase.__init__( self )
		SpaceBunchInterface.__init__( self )
		self._spaceMaxLevel = 99999		# 地图的最大等级
	
	def initData( self, configData ):
		SpaceBase.initData( self, configData )
		SpaceBunchInterface.initData( self, configData )
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