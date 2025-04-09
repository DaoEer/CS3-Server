# -*- coding: utf-8 -*-
#
import KBEngine
import KBEDebug
import csdefine
import Trap


class SpaceDoor( Trap.Trap ):
	"""
	大地图传送门
	"""
	def __init__(self):
		Trap.Trap.__init__(self)
		self.setTrapType( csdefine.TRAP_TYPE_SPACEDOOR )