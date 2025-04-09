# -*- coding: utf-8 -*-
import Math
import random
from SpaceCopy import SpaceCopy
import KBEDebug

class SpaceCopyJDCY( SpaceCopy ):
	"""
	禁地采药
	"""
	def __init__( self ):
		SpaceCopy.__init__( self )

	def randomRefreshXLC( self , amount ):
		"""
		随机刷新仙灵草
		"""
		scriptID = self.getScript().getLXCSrciptID()
		posList = self.getScript().getLXCPositionList()
		random.shuffle(posList)
		direction = Math.Vector3(0,0,0)
		createPosList = posList[:amount]
		for pos in createPosList:
			self.createEntityByScriptID( scriptID, pos, direction,  {"spawnPos":pos, "spawnDir": direction} )

	def onCollectedXLC( self ):
		"""
		仙灵草销毁
		"""
		self.XLCamount += 1
		for e in self._spaceRoles:
			e.client.CollectedXLC( self.XLCamount )
