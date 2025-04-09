# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
from ObjectScript.Space.SpacePlane import SpacePlane

class SpacePlaneJSZZ( SpacePlane ):
	"""
	CST-7419 金树种子
	"""
	def __init__( self ):
		SpacePlane.__init__( self )
		

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpacePlane.initData( self, configData )
		
