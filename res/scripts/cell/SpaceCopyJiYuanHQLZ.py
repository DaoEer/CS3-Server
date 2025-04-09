# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopyJiYuan import SpaceCopyJiYuan
import csdefine
import Const

class SpaceCopyJiYuanHQLZ( SpaceCopyJiYuan ):
	"""
	CST-12052
	机缘玩法:获取龙珠
	"""
	def __init__( self ) :
		SpaceCopyJiYuan.__init__( self )
		
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

