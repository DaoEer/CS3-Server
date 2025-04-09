# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine

class SpaceCopyFirstTongStarcraft( SpaceCopy ):
	"""
	帮会争霸 第一场
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.tongDBID = self.createArgs["tongDBID"]
		self.camp = self.createArgs["camp"]

	def activeStart( self ):
		"""
		活动开始
		"""
		self.getScript().activeStart( self )
