# -*- coding: utf-8 -*-

import KBEngine
from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug

class SpaceCopyLindenSnatch( SpaceCopy ):
	"""
	送宝任务(菩提子送予燃灯道人)
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.coordinates = []
		self.XTDLScriptIDList = []

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		coordinates = configData["SpaceData"].get( "coordinates", "" )
		if coordinates:
			self.coordinates = coordinates.split("|")
		XTDLScriptIDList = configData["SpaceData"].get("XTDLScriptIDList", "" )
		if XTDLScriptIDList:
			self.XTDLScriptIDList = XTDLScriptIDList.split("|")

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.coordinates, self.XTDLScriptIDList )