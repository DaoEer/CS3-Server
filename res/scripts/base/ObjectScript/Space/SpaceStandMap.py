# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceBase import SpaceBase

class SpaceStandMap( SpaceBase ):
	"""
	沙盘大地图
	"""
	def __init__( self ):
		SpaceBase.__init__( self )
		self.triggerLinePlayerAmount = 0
	
	def initData( self, configData ):
		SpaceBase.initData( self, configData )
		self.triggerLinePlayerAmount = configData["SpaceData"].get("triggerLinePlayerAmount",0)

	def getTriggerLinePlayerAmount( self ):
		"""
		获得触发分线的人数
		"""
		return self.triggerLinePlayerAmount
