# -*- coding: utf-8 -*-

import KBEngine
import Functions
import KBEMath
from ObjectScript.Space.SpaceBase import SpaceBase

class SpaceTong( SpaceBase ):
	def __init__( self ):
		SpaceBase.__init__( self )
		self.nagualPosition = (0.0, 0.0, 0.0)
		self.nagualDirection = (0.0, 0.0, 0.0)

	def initData( self, configData ):
		SpaceBase.initData( self, configData )
		spaceData = configData["SpaceData"]
		nagualPosition = Functions.vector3TypeConvert(spaceData["nagualPosition"])
		if nagualPosition:
			self.nagualPosition = KBEMath.Unreal2KBEnginePosition(nagualPosition)
		nagualDirection = Functions.vector3TypeConvert(spaceData["nagualDirection"])
		if nagualPosition:
			self.nagualDirection = KBEMath.Unreal2KBEnginePosition(nagualDirection)
		

	def createAnywhereEntity( self, params = None, callbackFunc = None ):
		"""
		为了减少帮会远程 通信，
		将帮会领地 创建 在帮会同一个base
		"""
		params["tongDBID"] = int( params["spaceKey"] )
		space = SpaceBase.createLocalEntity( self, self.getEntityProperties( params ) )
		if space and callbackFunc:
			callbackFunc( space )