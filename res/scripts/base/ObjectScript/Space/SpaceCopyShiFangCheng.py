# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine


class SpaceCopyShiFangCheng( SpaceCopy ):
	"""
	十方城
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self.stageListStr = []

	def initData( self, configData ):
		SpaceCopy.initData( self, configData )
		self.stageListStr = configData["SpaceData"].get("stageListStr","").split("|") #["1 2 3","4 5 6"]

	def getStageListStr( self ):
		"""
		获得阶段
		"""
		return self.stageListStr

