# -*- coding: utf-8 -*-

"""
用于所有非PC类型、有cell的基本类型

包括NPC、怪物、陷阱等各种类型
"""

import KBEngine
import KST
from CoreObject.NPCBaseObject import NPCBaseObject

class NPCHasBaseObject( NPCBaseObject ):
	def __init__( self ):
		NPCBaseObject.__init__( self )
	
	def getScript( self ):
		return KST.g_objFactory.getNPCObject( self.scriptID )