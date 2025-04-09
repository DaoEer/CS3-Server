# -*- coding: utf-8 -*-

import KBEngine
from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug

class SpaceCopyAndySnatch( SpaceCopy ):
	"""
	送宝任务(烈阳果送予莫何)
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.coordinates = []

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		coordinates = configData["SpaceData"].get( "coordinates", "" )
		if coordinates:
			self.coordinates = coordinates.split("|")
		self.moHeScriptID = configData["SpaceData"].get("moHeScriptID", "" )

	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopy.initEntity( self, selfEntity )
		selfEntity.initSpaceData( self.coordinates, self.moHeScriptID )