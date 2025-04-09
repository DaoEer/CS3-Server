# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy

class SpaceCopyFirstTongStarcraft( SpaceCopy ):
	"""
	帮会争霸 第一场
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
	
	def activeStart( self ):
		"""
		"""
		self.cell.activeStart()