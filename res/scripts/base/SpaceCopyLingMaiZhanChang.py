# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import KBEngine
import csdefine

class SpaceCopyLingMaiZhanChang( SpaceCopy ):
	"""
	灵脉战场
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
	
	def activityEnd( self ):
		"""
		define method
		活动结束
		"""
		self.cell.activityEnd()
