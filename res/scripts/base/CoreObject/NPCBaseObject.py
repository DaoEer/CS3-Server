# -*- coding: utf-8 -*-

"""
用于非PC只有base的基本类型

包括只有base的NPC、怪物、陷阱等各种类型
"""

import KBEngine
import KST
from CoreObject.HasCellOjbect import HasCellOjbect

import csdefine

class NPCBaseObject( KBEngine.Entity, HasCellOjbect ):
	def __init__( self ):
		KBEngine.Entity.__init__( self )
		HasCellOjbect.__init__( self )
		self.createMonsterCell()
	
	def initEntityFlag( self ):
		self.entityFlag = csdefine.ENTITY_FLAG_NPC

	def createMonsterCell( self ):
		self.createCellEntity( self.spaceCell )
		
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