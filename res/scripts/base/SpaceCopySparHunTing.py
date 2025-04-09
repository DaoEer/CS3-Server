# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import KBEngine
import csdefine

class SpaceCopySparHunTing( SpaceCopy ):
	"""
	晶石狩猎场副本
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
	
	def activeStart( self ):
		"""
		活动开始
		"""
		self.cell.activeStart()

	def activeEnd( self ):
		"""
		活动结束
		"""
		self.cell.activeEnd()
