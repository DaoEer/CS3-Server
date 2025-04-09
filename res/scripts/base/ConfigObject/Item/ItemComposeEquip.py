# -*- coding: utf-8 -*-

#common
import KBEDebug
#cell
import ConfigObject.Item.ItemUse as ItemUse
#data
import csstatus


class ItemComposeEquip(ItemUse.ItemUse):
	"""
	打造装备卷轴
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemUse.ItemUse.__init__(self, srcData)
		self._equipID = int( srcData.get( "Param1", 0 ) )		# 卷轴ID

	def use(self, owner, target):
		"""
		使用物品
		"""
		ItemUse.ItemUse.use(self, owner, target)
		if self._equipID:
			owner.studyEquipCompose( self._equipID )
		self.onUseResult( owner, True )
		return csstatus.ITEM_USE_GO_ON_MSG

