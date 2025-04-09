# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from ObjectScript.Space.SpaceCopy import SpaceCopy

class SpaceCopyLLBZ( SpaceCopy ):
	"""
	玲珑宝珠副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
		