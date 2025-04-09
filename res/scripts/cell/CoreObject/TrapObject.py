# -*- coding: utf-8 -*-

"""
用于陷阱类型的基本类型
"""


import KBEngine
import KST
import CoreObject.NPCBaseObject as NPCBaseObject
import csdefine
from ObjectScript.Trap.TrapFactory import g_trapFactory


class TrapObject(NPCBaseObject.NPCBaseObject):
	"""
	陷阱对象基类
	"""
	def __init__(self):
		NPCBaseObject.NPCBaseObject.__init__(self)
		self.__scriptObject = None
		self.getScript().initEntity( self )

	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_TRAP )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_TRAP)

	def getScript( self ):
		if not self._scriptObject:
			self._scriptObject = KST.g_objFactory.getTrapBoxObject( self.scriptID )
		
		return self._scriptObject 

	def setTrapType( self, traptype ):
		"""
		设置陷阱类型
		"""
		self.trapType  =  traptype

	def getTrapType( self ):
		"""
		获取陷阱类型
		"""
		return self.trapType
	