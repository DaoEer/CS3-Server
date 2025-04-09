# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from ObjectScript.Space.SpaceCopyTong import SpaceCopyTong

class SpaceCopySLZD( SpaceCopyTong ):
	"""
	试炼之地
	"""
	def __init__( self ):
		SpaceCopyTong.__init__( self )

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyTong.initData( self, configData )
		