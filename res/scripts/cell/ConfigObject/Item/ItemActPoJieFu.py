# -*- coding: utf-8 -*-
import csstatus
import csdefine
import ConfigObject.Item.ItemSpell as ItemSpell
import KBEngine

class ItemActPoJieFu( ItemSpell.ItemSpell ):
	"""
	破界符
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)
		self.useSpace = srcData.get("Param1", "")
		self.dist_ = 5
		if srcData["Param2"]:
			self.dist_ = int(srcData["Param2"])
	
	def checkUseBySpace( self, owner ):
		"""
		检查地图是否可以使用
		"""
		if self.useSpace:
			if owner.getCurrentSpaceScriptID() != self.useSpace:
				return False
		return ItemSpell.ItemSpell.checkUseBySpace(self, owner)
	
	def checkUse(self, owner):
		"""
		使用前检测
		"""
		result = ItemSpell.ItemSpell.checkUse( self, owner )
		if result == csstatus.ITEM_USE_GO_ON_MSG:
			for pos in owner.groundPosDict.values():
				if owner.position.distTo( pos ) > self.dist_:
					return csstatus.SKILL_TOO_FAR
		return result
		
	def onUseResult(self, owner, useResult ):
		"""
		使用物品结果
		"""
		if not useResult:return
		owner.removeItemByAmount(self, 1, csdefine.ITEM_REMOVE_BY_USE)