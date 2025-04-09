# -*- coding: utf-8 -*-

from ObjectScript.SpellBox import SpellBox

class SpellBoxXTBL( SpellBox.SpellBox ):
	"""
	玄天宝录副本 专属SpellBox
	"""
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )

	def onPlayerIntonateOver( self, selfEntity, playerCell ):
		"""
		virtual method
		玩家吟唱结束
		"""
		SpellBox.SpellBox.onPlayerIntonateOver( self, selfEntity, playerCell )
		spaceEntity = playerCell.getCurrentSpace()
		if spaceEntity:
			spaceEntity.onStartTurnMirror()