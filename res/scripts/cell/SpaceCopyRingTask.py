# -*- coding: utf-8 -*-

import random
from KBEDebug import *
from SpaceCopy import SpaceCopy
import math
import KBEMath
import Math
import KBEngine
import csdefine
import csstatus
import Const
import Define

class SpaceCopyRingTask( SpaceCopy ):
	"""
	环任务秘境
	"""
	def __init__( self ) :
		SpaceCopy.__init__( self )

	def closeSpace( self ):
		"""
		<define method>
		关闭副本唯一入口，所有关闭副本操作（base或cell）都应该走此接口
		"""
		DEBUG_MSG("Close space(%s)! scriptID:%s."%( self.id, self.scriptID ))
		self.clearCellAppDataBeforeClose()
		
		if len( self._spaceRoles ):
			self.getScript().onCloseSpace( self )
			self.addTimerCallBack( 5, "closeSpace", () )	#5秒后再次关闭
			DEBUG_MSG("Delay close space(%s) reason 1! scriptID:%s."%( self.id, self.scriptID ))
		
		elif len( self._readyEnterRoles ):
			self.getScript().onCloseSpace( self )
			self._readyEnterRoles = []
			self.addTimerCallBack( 5, "closeSpace", () )	#5秒后再次关闭
			DEBUG_MSG("Delay close space(%s) reason 2! scriptID:%s."%( self.id, self.scriptID ))
		else:
			self.destroySelf()