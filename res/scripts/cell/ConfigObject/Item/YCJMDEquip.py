# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.ItemUse as ItemUse
import csstatus

class YCJMDEquip(ItemUse.ItemUse):
	"""
	勇闯绝命岛临时装备
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self.wieldSkillID = 0
		self.unwieldSkillID = 0
		if srcData["Param1"]:
			self.wieldSkillID, self.unwieldSkillID = [int(skillID) for skillID in srcData["Param1"].split("|")]	#装备buffID

	def isEquip( self ):
		"""
		判断是否是装备
		"""
		return False

	def isTempEquip(self):
		"""
		判断是否是临时装备
		"""
		return True

	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		if self.getEquipPart() != self.order:		# 穿装备
			skill = owner.getSkill( self.wieldSkillID )
			if skill and skill.isCasterCooldown( owner ):
				return csstatus.SKILL_NOT_READY
		return ItemUse.ItemUse.checkUse(self, owner)

	def use(self, owner, target):
		"""
		使用
		"""
		dstorder = self.getWieldOrder(owner)
		owner.CELL_swapItem(owner.id, self.order, dstorder)
		return csstatus.ITEM_USE_GO_ON_MSG

	def getWieldOrder(self, player):
		"""
		获取装备的ItemOrder
		"""
		return self.getEquipPart()


	def getEquipPart(self):
		"""
		获取装备部位
		"""
		return 0

	def wield(self, owner):
		"""
		装备道具
		"""					
		owner.useSkillToEntity(self.wieldSkillID, owner.id)
		return True

	def unWield( self, owner ):
		"""
		卸下道具
		"""
		owner.useSkillToEntity(self.unwieldSkillID, owner.id)