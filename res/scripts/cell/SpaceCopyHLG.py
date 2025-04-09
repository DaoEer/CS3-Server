# -*- coding: utf-8 -*-

import KBEDebug
from SpaceCopy import SpaceCopy

class SpaceCopyHLG( SpaceCopy ):
	"""
	副本浩灵谷
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )

	def onCompleteQTENotyfy( self, playerID, isSucceed ):
		"""
		QTE结束执行行为
		"""
		if playerID not in self.completeQTENum:
			self.completeQTENum[playerID] = isSucceed
		else:
			self.completeQTENum[playerID] += isSucceed