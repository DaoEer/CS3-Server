# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy
import csdefine
import time

class SpaceCopyShiFangCheng( SpaceCopy ):
	"""
	十方城
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )
		self.readyDestroyTimer = 0
		
	def activityStart( self,useStageIndex ):
		"""
		define method
		活动开始
		"""
		self.getScript().activityStart( self,useStageIndex )

	def activityEnd( self ):
		"""
		活动结束
		"""
		self.getScript().activityEnd( self )

	def passFailure( self ):
		"""
		通关失败
		"""
		self.getScript().passFailure( self )

	def passSuccess( self ):
		"""
		通关成功
		"""
		self.getScript().passSuccess( self )

	def destroyWall( self ):
		"""
		销毁光墙
		"""
		entityList = self.getEntityMailBoxRecord( self.getScript().getWallID() )
		for entity in entityList:
			entity.destroySelf()

	def onReady( self ):
		"""
		"""
		if len(self._spaceRoles) <= 0:
			self.closeSpace()