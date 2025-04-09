# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine
import Const

class SpaceCopyHQLZ( SpaceCopy ):
	"""
	环任务:获取龙珠
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		
	def isPointHasEntity( self, point ):
		"""
		判断该点是否有Entity
		"""
		if point in self.pointHasEntity:
			return True
		return False

	def addPointHasEntity( self, point ):
		"""
		增加该点存在Entity
		"""
		self.pointHasEntity.append(point)

