# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy

class SpaceCopyShiFangCheng( SpaceCopy ):
	"""
	十方城
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )

	def activityStart( self, useStageIndex ):
		"""
		define method
		活动开始
		"""
		self.cell.activityStart(useStageIndex)

	def activityEnd( self ):
		"""
		活动结束
		"""
		self.cell.activityEnd()


