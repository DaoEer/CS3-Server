# -*- coding: utf-8 -*-


"""
用于所有非PC类型、有base的基本类型

包括NPC、怪物、陷阱等各种类型
"""

from CoreObject import NPCObject

class NPCHasBaseObject(  NPCObject.NPCObject ):
	def __init__( self ):
		NPCObject.NPCObject.__init__( self )