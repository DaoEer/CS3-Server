# -*- coding: utf-8 -*-

import KBEngine
import csdefine
from ObjectScript.SpaceDomain.SpaceDomainCopy import SpaceDomainCopy
import KBEDebug

class SpaceDomainCopyActivity( SpaceDomainCopy ):
	"""
	活动 副本空间领域
	"""
	def __init__( self ):
		SpaceDomainCopy.__init__( self )


	def activityStart( self ):
		"""
		活动开始
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.activityStart()

	def activityEnd( self ):
		"""
		活动结束
		"""
		for spaceItem in self.spaceItems.values():
			if spaceItem.spaceMailBox:
				spaceItem.spaceMailBox.activityEnd()
