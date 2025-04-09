# -*- coding: utf-8 -*-

"""
用于宠物的基本类型
"""

import KBEngine
import KST
from CoreObject.HasCellOjbect import HasCellOjbect

import csdefine

class VehiclePetObject( KBEngine.Entity, HasCellOjbect ):
	def __init__( self ):
		HasCellOjbect.__init__( self )
	
	def initEntityFlag( self ):
		self.entityFlag = csdefine.ENTITY_FLAG_VEHICLEPET

#-----------------引擎回调------------------------------------------
	def onLoseCell( self ):
		"""
		CELL丢失
		"""
		HasCellOjbect.onLoseCell( self )
	
	def onGetCell( self ):
		"""
		CELL创建完成
		"""
		HasCellOjbect.onGetCell( self )