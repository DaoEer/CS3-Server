# -*- coding: utf-8 -*-

"""
用于所有entity的基本类型
"""

import KBEngine

import csdefine

class EntityObject:
	def __init__( self ):
		self.initEntityFlag()

	#----------------------entity flag--------------------------------------------------------------
	def initEntityFlag( self ):
		self.entityFlag = csdefine.ENTITY_FLAG_UNKNOWN

	def setEntityFlag( self, entityFlag ):
		"""
		设置entity的类型
		"""
		self.entityFlag = entityFlag

	def getEntityFlag( self ):
		return self.entityFlag

	def isEntityFlag( self, entityFlag ):
		return self.entityFlag == entityFlag

	def getClient( self ):
		"""
		获取client
		"""
		if hasattr(self, "client") and self.client:
			return self.client
		return None