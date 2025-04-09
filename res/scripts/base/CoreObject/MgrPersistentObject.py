# -*- coding: utf-8 -*-

"""
用于需要存档管理器的基本类型
"""

import KST
import KBEngine
from CoreObject import MgrObject

class MgrPersistentObject( MgrObject.MgrObject ):
	def __init__( self ):
		MgrObject.MgrObject.__init__( self )
		self._isInitSelf = False
		
	def onCompleteInit(self):
		"""
		"""
		if not self._isInitSelf:
			self._isInitSelf = True
			KST.g_serverInfosMgr.registerReadySysEntity(  self.__class__.__name__ )
			
	def GMCommand( self, funStr ):
		"""
		"""
		func = getattr(self, funStr)
		if func: func("")