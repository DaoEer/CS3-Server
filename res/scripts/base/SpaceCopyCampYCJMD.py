# -*- coding: utf-8 -*-
import KBEDebug
from SpaceCopy import SpaceCopy


class SpaceCopyCampYCJMD( SpaceCopy ):
	"""
	阵营战场“勇闯绝命岛” JIRA CST-9960
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )

	def activityEnd( self ):
		"""
		活动结束
		""" 
		self.cell.closeSpace()
