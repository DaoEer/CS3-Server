# -*- coding: utf-8 -*-
import csstatus
import csdefine
import ConfigObject.Item.ItemUse as ItemUse

class ItemActCompass( ItemUse.ItemUse ):
	"""
	灵气罗盘
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self.useSpace = srcData.get("Param1")

	def checkUseBySpace( self, owner ):
		"""
		检查地图是否可以使用
		"""
		if self.useSpace:
			if owner.getCurrentSpaceScriptID() != self.useSpace:
				return False
		if owner.hasDongFu():
			return False
		return True

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		owner.client.OnShowCompassUI()
	