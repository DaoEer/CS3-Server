# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
import Functions
import csstatus
import random
import KBEDebug

class ItemLearnPassiveSkill( ItemUse.ItemUse ):
	"""
	学习被动技能道具
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._passiveSkillID = 0
		if srcData["Param1"]:
			self._passiveSkillID = int(srcData["Param1"])

	def getSkillID( self ):
		"""
		获取物品触发的技能ID
		"""
		return self.skillID

	def checkReqClasses(self, owner):
		"""
		检测职业
		"""
		reqClass = self.getItemDir("ReqClasses")
		if reqClass:
			return str(owner.getProfession()) in reqClass.split("|")
		# 如果没有配置，说明多个职业匹配
		return True

	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		if self._passiveSkillID == 0:
			KBEDebug.ERROR_MSG("ItemID : %s Param1 is ERROR!!!!!!!!!"%self.id)
			return csstatus.SKILL_NOT_EXIST

		if not self.checkReqLevel(owner):
			return csstatus.ITEM_USE_LV_LESS_MSG
		if not self.checkReqClasses(owner):
			return csstatus.ITEM_USE_CLASS_NOTMATCH

		if owner.hasSkill(self._passiveSkillID):
			return csstatus.ADD_SKILL_FAIL_AS_HAS_LEAR

		return ItemUse.ItemUse.checkUse( self, owner )

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		if not target:
			target = owner
		owner.learnPassiveSkill( self._passiveSkillID )
		owner.removeItemByAmount( self, 1, csdefine.ITEM_REMOVE_BY_USE )