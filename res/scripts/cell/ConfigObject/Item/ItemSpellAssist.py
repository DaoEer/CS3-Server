# -*- coding: utf-8 -*-

#common
import KBEDebug
#cell
import ConfigObject.Item.ItemSpell as ItemSpell
#data
import csstatus


class ItemSpellAssist(ItemSpell.ItemSpell):
	"""
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemSpell.ItemSpell.__init__(self, srcData)
		self.useSpaceList = srcData["Param2"].split("|")

	def checkUseBySpace( self, owner ):
		"""
		检查地图是否可以使用
		"""
		if self.useSpaceList:
			if not owner.getCurrentSpaceScriptID() in self.useSpaceList:
				return False
		return ItemSpell.ItemSpell.checkUseBySpace(self, owner)