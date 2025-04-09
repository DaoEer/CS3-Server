# -*- coding: utf-8 -*-

#common
import KBEDebug
import csdefine
#cell
import ConfigObject.Item.ItemUse as ItemUse
#data
import csstatus


class ItemUsePet(ItemUse.ItemUse):
	"""
	幻兽专用物品
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemUse.ItemUse.__init__(self, srcData)

	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		petObject= owner.geActivePetCell()
		if not petObject:
			return csstatus.PET_NO_CONJURED_CANNOT_USE_ITEM
			
		return ItemUse.ItemUse.checkUse( self, owner )

	def use(self, owner, target):
		"""
		使用物品
		"""
		skill = owner.getSkill( self.skillID )
		petObject= owner.geActivePetCell()
		if skill.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_NONE:
			statusID = owner.useSkillToEntityForItem( self.skillID, owner.id, self.getUid() )
		elif skill.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_ENTITY:
			statusID = owner.useSkillToEntityForItem( self.skillID, petObject.id, self.getUid() )
		elif skill.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_POSITION:
			statusID = owner.useSkillToEntityForItemPos( self.skillID, petObject.position, self.getUid() )
			
		if statusID != csstatus.SKILL_GO_ON:
			return statusID
		
		return csstatus.ITEM_USE_GO_ON_MSG

