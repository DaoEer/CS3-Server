# -*- coding: utf-8 -*-

import KBEngine
from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug
import Math


class SpaceCopySanYuanJingZhu( SpaceCopy ):
	"""
	三源镜柱副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
		self.monsterData = configData["SpaceData"]["monsterData"]

	def initEntity(self, selfEntity):
		""""""
		SpaceCopy.initEntity(self, selfEntity)
		selfEntity.initSpaceData( self.monsterData )

		 	 
