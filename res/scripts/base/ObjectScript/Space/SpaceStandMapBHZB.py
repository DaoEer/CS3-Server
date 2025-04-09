# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceBase import SpaceBase

class SpaceStandMapBHZB( SpaceBase ):
	"""
	帮会争霸沙盘大地图
	"""
	def __init__( self ):
		SpaceBase.__init__( self )
		self.maxLineNumber = 0
	
	def initData( self, configData ):
		SpaceBase.initData( self, configData )
		self.maxLineNumber = configData["SpaceData"].get("maxLineNumber",0)

	def getMaxLineNumber( self ):
		"""
		获得最大分线数
		"""
		return self.maxLineNumber
