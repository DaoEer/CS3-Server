# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyShiFangCheng( SpaceDomainCopy ):
	"""
	十方成活动 副本空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )


	def activityStart( self,useStageIndex ):
		"""
		活动开始
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.activityStart(useStageIndex)

	def activityEnd( self ):
		"""
		活动结束
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.activityEnd()
