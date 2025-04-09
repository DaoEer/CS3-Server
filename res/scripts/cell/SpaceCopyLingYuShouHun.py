# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopy import SpaceCopy
import Math
import KBEngine
import csdefine
import csstatus

class SpaceCopyLingYuShouHun( SpaceCopy ):
	"""
	灵域狩魂副本
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )

		#玩家当前所附身的怪物ScriptID
		self.score = 0         #当前积分


