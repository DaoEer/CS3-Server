# -*- coding: utf-8 -*-

"""
用于门类型怪物的基类
"""

from CoreObject import NPCBaseObject
import csdefine

class DoorObject( NPCBaseObject.NPCBaseObject ):
	def __init__( self ):
		NPCBaseObject.NPCBaseObject.__init__( self )
		

	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_DOOR )\


	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt( csdefine.ENTITY_FLAG_EXT_DOOR )	