# -*- coding: utf-8 -*-

#common
import KBEDebug
#cell
import ConfigObject.Item.ItemUse as ItemUse
#data
import csstatus


class ItemSpell(ItemUse.ItemUse):
	"""
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemUse.ItemUse.__init__(self, srcData)

	def getSkillID( self ):
		"""
		获取物品触发的技能ID
		"""
		return self.skillID

	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		#判断是否正在使用其它物品
		if owner.getUsingItem():
			return csstatus.ITEM_USING_NOW
		
		if not self.getSkillID():
			return csstatus.ITEM_CANNOT_USED
		
		return ItemUse.ItemUse.checkUse( self, owner )

	def use(self, owner, target):
		"""
		使用物品
		"""
		ItemUse.ItemUse.use(self, owner, target)
		if not target:
			target = owner
		statusID = owner.useSkillToEntityForItem( self.getSkillID(), target.id, self.getUid() )
		if statusID != csstatus.SKILL_GO_ON:
			return statusID
		
		return csstatus.ITEM_USE_GO_ON_MSG

	def useToPos( self, owner, Pos ):
		"""
		对位置使用物品
		"""
		statusID = owner.useSkillToEntityForItemPos( self.getSkillID(), Pos, self.getUid() )
		if statusID != csstatus.SKILL_GO_ON:
			return statusID
		
		return csstatus.ITEM_USE_GO_ON_MSG

