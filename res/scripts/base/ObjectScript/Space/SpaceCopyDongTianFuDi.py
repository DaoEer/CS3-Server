# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEngine


class SpaceCopyDongTianFuDi( SpaceCopy ):
	"""
	洞天福地副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopy.initData( self, configData )
