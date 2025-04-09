# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
import Functions
import csstatus
import random
import KBEDebug
import ItemTypeEnum
import ItemFactory

class ItemActBaleRope( ItemUse.ItemUse ):
	"""
	捆兽绳
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self.probability = [ float(i) for i in srcData["Param1"].split("|") ] #凡兽的捕捉概率|灵兽的捕捉概率|圣兽的捕捉概率

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		#检测目标是否满足使用条件
		if not target:
			return csstatus.CATCH_TARGET_NOT_ORIGINPET
		if target.getEntityFlagExt() != csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_ORIGIN_PET:
			return csstatus.CATCH_TARGET_NOT_ORIGINPET
		if owner.id not in target.ownerIDList:
			return csstatus.CATCH_TARGET_NOT_BELONG_TO_PLAYER
			
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(target.getScript().itemPetEgg)
		result = owner.addItemCheck(itemInst)
		if result != csstatus.ITEM_GO_ON:
			if result == csstatus.ITEM_SPACE_LESS:
				return csstatus.STORE_BAG_HAS_ENOUGH
			else:
				return result
		
		#移除定时器
		if target.destroyTimeID != 0:
			target.popTimer( target.destroyTimeID )
			target.destroyTimeID = 0
		target.probability = self.probability[target.getScript().quality -1]
		statusID = owner.useSkillToEntityForItem( self.skillID, target.id, self.getUid() )
		if statusID != csstatus.SKILL_GO_ON:
			return statusID
		
		return csstatus.ITEM_USE_GO_ON_MSG