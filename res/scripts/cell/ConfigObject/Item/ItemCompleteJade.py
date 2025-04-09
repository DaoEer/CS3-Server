# -*- coding: utf-8 -*-

import KBEDebug
import Const
import csstatus
import random
import csdefine
import ConfigObject.Item.ItemSpell as ItemSpell

class ItemCompleteJade(ItemSpell.ItemSpell):
	"""
	完整的玉玦
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)
		self._chuanChengSkillID = 0
		if srcData["Param1"]:
			self._chuanChengSkillID = int(srcData["Param1"])

	def onUseResult(self, owner, useResult ):
		"""
		使用物品结果
		"""
		if not useResult:
			return

		ItemSpell.ItemSpell.onUseResult( self, owner, useResult )

	def checkUse(self, owner):
		"""
		使用物品检测
		"""		
		if self._chuanChengSkillID == 0:
			KBEDebug.ERROR_MSG("ItemID : %s Param1 is ERROR!!!!!!!!!"%self.id)
			return csstatus.SKILL_NOT_EXIST

		if owner.hasSkill(self._chuanChengSkillID):
			return csstatus.ADD_SKILL_FAIL_AS_HAS_LEAR

		return ItemSpell.ItemSpell.checkUse( self, owner )


	def use(self, owner, target):
		ItemSpell.ItemSpell.use(self, owner, target)
		if not target:
			target = owner

		owner.learnChuanChengSkill( self._chuanChengSkillID )
		owner.removeItemByAmount( self, 1, csdefine.ITEM_REMOVE_BY_USE )