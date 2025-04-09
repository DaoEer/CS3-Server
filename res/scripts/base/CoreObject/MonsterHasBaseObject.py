# -*- coding: utf-8 -*-

"""
用于有base的怪物类型的基类
"""

import KBEngine
import KST
from CoreObject.NPCBaseObject import NPCBaseObject

import csdefine

class MonsterHasBaseObject( NPCBaseObject ):
	def __init__( self ):
		NPCBaseObject.__init__( self )
	
	def getScript( self ):
		return KST.g_objFactory.getMonsterObject( self.scriptID )
	
	#----------------------entity flag--------------------------------------------------------------
	def initEntityFlag( self ):
		self.entityFlag = csdefine.ENTITY_FLAG_MONSTER