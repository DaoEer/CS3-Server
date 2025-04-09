# -*- coding: utf-8 -*-

"""
用于NPC对象的基类
"""

import KBEngine
#script
import CoreObject.NPCBaseObject as NPCBaseObject
import KST
import csdefine


class NPCObject(NPCBaseObject.NPCBaseObject):
	"""
	NPC对象基类
	"""
	def __init__(self):
		NPCBaseObject.NPCBaseObject.__init__(self)
		
	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_NPC )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_NPC)

	def getScript( self ):
		if not self._scriptObject:
			self._scriptObject =  KST.g_objFactory.getNPCObject( self.scriptID )
		
		return self._scriptObject
		