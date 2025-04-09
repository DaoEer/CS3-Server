# -*- coding: utf-8 -*-

"""
用于管理器的基本类型
"""

import KBEngine
from CoreObject.GameObject import GameObject

import csdefine

class MgrObject( KBEngine.Entity, GameObject ):
	def __init__( self ):
		KBEngine.Entity.__init__( self )
		GameObject.__init__( self )
		self.registerInGlobalData()
	
	#----------------------entity flag--------------------------------------------------------------
	def initEntityFlag( self ):
		self.entityFlag = csdefine.ENTITY_FLAG_MGR

	def registerInGlobalData(self):
		"""
		"""
		#如果是全服唯一的系统(不然就是每个baseapp都创建)，将自身注册
		if self.isGlobalOnly:
			KBEngine.globalData[ self.__class__.__name__ ] = self