# -*- coding: utf-8 -*-
import csdefine
import csstatus
import ConfigObject.Item.ItemSpell as ItemSpell
import KBEDebug
class ItemTianJiMiTu( ItemSpell.ItemSpell ):
	"""
	天机秘图 CST-12052
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)

	def use(self, owner, target):
		"""
		"""
		status = ItemSpell.ItemSpell.use(self, owner, target)
		if status != csstatus.ITEM_USE_GO_ON_MSG:
			return status

		owner.setTemp("JIYUANDATA", {"TianJiMiID" : self.id})
		return csstatus.ITEM_USE_GO_ON_MSG

	def checkUse(self, owner):
		space = owner.getCurrentSpace()
		spacetype = space.getScript().getSpaceType()
		if spacetype == csdefine.SPACE_TYPE_COPY or spacetype == csdefine.SPACE_TYPE_PLANE:
			return csstatus.ITEM_CANNOT_USED
		return ItemSpell.ItemSpell.checkUse(self, owner)
