# -*- coding: utf-8 -*-
#
import csdefine
import KBEngine
from KBEDebug import *
import NPC as NPC
import CoreInterface.TeleportStoneInterface as TeleportStoneInterface


class TeleportStone(NPC.NPC, TeleportStoneInterface.TeleportStoneInterface):
	"""
	"""
	def __init__(self):
		NPC.NPC.__init__(self)
		TeleportStoneInterface.TeleportStoneInterface.__init__( self )
		
	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_TELEPORTSTONE )
		
	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_TELEPORTSTONE)