# -*- coding: utf-8 -*-

#common
import KBEDebug
#cell
import ConfigObject.Item.ItemSpellAssist as ItemSpellAssist
#data
import csstatus


class ItemSpellBatterAssist(ItemSpellAssist.ItemSpellAssist):
	"""
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemSpellAssist.ItemSpellAssist.__init__(self, srcData)

	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		return ItemSpellAssist.ItemSpellAssist.checkUse( self, owner )

	def useToPos( self, owner, Pos ):
		"""
		对位置使用物品
		"""
		statusID = owner.useSkillToEntityForItemPos( self.getSkillID(), Pos, self.getUid() )
		if statusID != csstatus.SKILL_GO_ON:
			return statusID
		
		return csstatus.ITEM_USE_GO_ON_MSG

