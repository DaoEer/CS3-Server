# -*- coding: utf-8 -*-

import KBEngine
import KBEDebug
import Math
import csdefine
from MoveTrap import MoveTrap
from ConfigObject import PatrolRouteLoader

class PushTrap( MoveTrap ):
	"""
	推人陷阱类
	"""
	def __init__( self ):
		MoveTrap.__init__( self )