# -*- coding: utf-8 -*-

import KBEDebug
import KBEngine
import csstatus

from ObjectScript.SpellBox import SpellBox

class SpellBoxPet( SpellBox.SpellBox ):
	"""
	幻兽掉落 专属SpellBox
	"""
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )



	def gossipWith( self, selfEntity, srcEntityID ):
		"""
		玩家点击交互
		"""
		if selfEntity.id == srcEntityID:
			return
		
		playerCell = KBEngine.entities.get( srcEntityID, None )
		if playerCell is None:
			KBEDebug.ERROR_MSG( "SpellBox::gossipWith:Can't found gossip with player entity %i!" % srcEntityID )
			return
		
		#不在同一个space
		if playerCell.spaceID != selfEntity.spaceID:
			return
		
		if selfEntity.isCoolDowning or selfEntity.isDestroyHide:
			return

		if 0 != selfEntity.keeperDBID  and playerCell.playerDBID != selfEntity.keeperDBID:
			playerCell.statusMessage(csstatus.PET_CANT_CATCH)
			return

		self.gossipWithForwardCB( selfEntity, playerCell )
