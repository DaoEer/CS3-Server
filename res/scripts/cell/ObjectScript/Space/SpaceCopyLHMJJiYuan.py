# -*- coding: utf-8 -*-

import KBEngine
from ObjectScript.Space.SpaceCopy import SpaceCopy
import KBEDebug

class SpaceCopyLHMJJiYuan(SpaceCopy):
	"""
	轮回秘境机缘副本
	"""
	def __init__(self):
		SpaceCopy.__init__(self)

	def getPackDomainData(self, playerEntity, args):
		"""
		"""
		packDict = SpaceCopy.getPackDomainData( self, playerEntity, args )
		spaceName  =  self.getSpaceName()
		packDict.update({"jiyuanSpaceName":spaceName})
		return packDict
