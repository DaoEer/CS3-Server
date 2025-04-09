# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
import KBEngine
from SmartImport import smartImport
from ObjectScript.SpellBox import SpellBox
import csstatus

class SpellBoxCollect( SpellBox.SpellBox ):
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )
		self.needItemList = []
		self.msgID = 0

	def initData( self, data ):
		"""
		初始化数据
		@param data: dict
		"""
		SpellBox.SpellBox.initData( self, data )
		if data["Param2"]:
			self.needItemList = [int(i) for i in data["Param2"].split("|")]
		if data["Param3"]:
			self.msgID = int( data["Param3"] )
		
	def gossipWithForwardCB( self, selfCell, playerEntity ):
		"""
		玩家交互
		"""
		if self.needItemList and self.msgID:
			if not playerEntity.getItemInstsByIDList( self.needItemList ):
				playerEntity.statusMessage( self.msgID, "" )
				return
		
		SpellBox.SpellBox.gossipWithForwardCB( self, selfCell, playerEntity )
		
	def onPlayerIntonateOver( self, selfEntity, playerCell ):
		"""
		virtual method
		玩家吟唱结束
		"""
		SpellBox.SpellBox.onPlayerIntonateOver( self, selfEntity, playerCell )
		selfEntity.getCurrentSpace().onSpellBoxDie( selfEntity.id )