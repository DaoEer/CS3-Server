# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopyTong import SpaceCopyTong
import KBEngine


class SpaceCopyTongJiuZiZhenYan( SpaceCopyTong ):
	"""
	帮会副本(九字真言)
	"""
	def __init__( self ):
		SpaceCopyTong.__init__( self )

	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyTong.initData( self, configData )
