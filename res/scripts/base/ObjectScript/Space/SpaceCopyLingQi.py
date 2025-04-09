# -*- coding: utf-8 -*-


import KBEDebug
import Math
import csdefine
import Functions
import random
import KBEMath
from ObjectScript.Space.SpaceCopy import SpaceCopy

class SpaceCopyLingQi( SpaceCopy ):
	"""
	收集灵气
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
		self._reviveData = []
	
	def initData( self, configData ):
		"""
		"""
		SpaceCopy.initData( self, configData )
