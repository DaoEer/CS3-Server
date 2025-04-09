# -*- coding: utf-8 -*-

from SpaceMultiLine import SpaceMultiLine

class SpaceLunHuiMiJinMultiLine( SpaceMultiLine ):
	def __init__( self ):
		SpaceMultiLine.__init__( self )

	def activityStart( self ):
		"""
		define method
		活动开始(开始刷怪)
		"""
		self.cell.activityStart()

	def activityEnd( self ):
		"""
		活动结束(停止刷怪)
		"""
		self.cell.activityEnd()