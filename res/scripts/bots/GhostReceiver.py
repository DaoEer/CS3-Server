# -*- coding: utf-8 -*-
import KBEngine
from Interface.GhostReceiverObject import GhostReceiverObject
class GhostReceiver( KBEngine.Entity, GhostReceiverObject ):
	
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GhostReceiverObject.__init__( self )
