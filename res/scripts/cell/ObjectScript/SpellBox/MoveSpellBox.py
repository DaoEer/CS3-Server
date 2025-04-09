# -*- coding: utf-8 -*-

import Const
from ObjectScript.SpellBox import SpellBox

class MoveSpellBox( SpellBox.SpellBox ):
	"""
	可移动场景物件
	"""
	def __init__( self ):
		SpellBox.SpellBox.__init__( self )

	def onCooldownTimeOverCB( self, selfEntity, srcEntityID ):
		"""
		冷却结束，恢复可交互状态
		"""
		selfEntity.isCoolDowning = False
		selfEntity.allClients.CLIENT_RefreshBoxStatus()
		spaceEntity = selfEntity.getCurrentSpace()
		if spaceEntity:
			if selfEntity.id in spaceEntity.sceneObjectCoordList:
				spaceEntity.sceneObjectCoordList.remove(selfEntity.id)