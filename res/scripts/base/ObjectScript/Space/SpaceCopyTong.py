# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine


class SpaceCopyTong( SpaceCopy ):
	"""
	帮会副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
