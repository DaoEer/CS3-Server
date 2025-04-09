# -*- coding: utf-8 -*-

from ObjectScript.Space.SpaceCopy import SpaceCopy


class SpaceCopyStory( SpaceCopy ):
	"""
	剧情副本
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )
	
	def onLastPlayerLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		最后一个玩家离开副本
		"""
		selfEntity.leaveCloseTimer = selfEntity.addTimerCallBack( 0.5, "closeSpace", () )