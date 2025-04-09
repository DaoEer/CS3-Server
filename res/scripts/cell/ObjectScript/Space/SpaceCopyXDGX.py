# -*- coding: utf-8 -*-


from ObjectScript.Space.SpaceCopyRingTaskChild import SpaceCopyRingTaskChild
import json
import Functions
import KBEMath
import Math
import KBEDebug
import csdefine
import Define

class SpaceCopyXDGX( SpaceCopyRingTaskChild ):
	"""
	环任务【仙岛归墟】
	"""
	def __init__( self ):
		SpaceCopyRingTaskChild.__init__( self )
		self.gridLenNumber = 0
		self.gridWidNumber = 0
		self.destroyGrideNum = 0
		self.delyTime = 0.0
	
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyRingTaskChild.initData( self, configData )
		self.gridLenNumber = configData["SpaceData"].get("gridLenNumber",0)
		self.gridWidNumber = configData["SpaceData"].get("gridWidNumber",0)
		self.destroyGrideNum = configData["SpaceData"].get("destroyGrideNum",0)
		self.delyTime = configData["SpaceData"].get("delyTime",0.0)

	def getGridLenNumber( self ):
		"""
		"""
		return self.gridLenNumber

	def getGridWidNumber( self ):
		"""
		"""
		return self.gridWidNumber

	def getDestroyGrideNum( self ):
		"""
		"""
		return self.destroyGrideNum

	def getDelyTime( self ):
		"""
		"""
		return self.delyTime