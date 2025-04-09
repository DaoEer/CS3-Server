# -*- coding: utf-8 -*-
import KBEDebug
from SpaceCopy import SpaceCopy


class SpaceCopyCampFiveYCJMD( SpaceCopy ):
	"""
	阵营战场“勇闯绝命岛”（5人） JIRA CST-10463
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )

	def activityEnd( self ):
		"""
		活动结束
		""" 
		self.cell.closeSpace()
