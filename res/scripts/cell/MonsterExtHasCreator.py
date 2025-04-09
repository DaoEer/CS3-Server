# -*- coding: utf-8 -*-

import Monster

class MonsterExtHasCreator( Monster.Monster ):
	"""
	专属怪
	"""

	def __init__( self ):
		Monster.Monster.__init__( self )
		daleyTime = 10*60
		if self.getScript().getDestroyTime():
			daleyTime = self.getScript().getDestroyTime()
		self.addTimerCallBack( daleyTime, "destroySelf", () )
