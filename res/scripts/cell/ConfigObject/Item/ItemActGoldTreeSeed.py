# -*- coding: utf-8 -*-
import csstatus
import csdefine
import ConfigObject.Item.ItemUse as ItemUse

class ItemActGoldTreeSeed( ItemUse.ItemUse ):
	"""
	玲珑宝珠
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._scriptID = srcData["Param1"]

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)	
		entity = owner.createEntityByScriptID(self._scriptID, owner.position, owner.direction,{ "spawnPos":owner.position ,"spawnDir":owner.position,"creatorDBID":owner.playerDBID})
		owner.removeItemByAmount( self, 1, csdefine.ITEM_REMOVE_BY_USE )
		return csstatus.ITEM_USE_GO_ON_MSG
