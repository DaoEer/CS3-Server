# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.EquipPartBase as EquipPartBase
import ItemTypeEnum

class RingPart(EquipPartBase.EquipPartBase):
	"""
	戒指 半成品
	"""
	def __init__(self, srcData):
		EquipPartBase.EquipPartBase.__init__(self, srcData)
		
	def getWieldOrder(self, player):
		"""
		获取装备的ItemOrder
		"""
		#戒指部位
		return player.getFreeRingWieldOrder()

	def getEquipPart(self):
		"""
		获取装备部位,戒指
		"""
		return ItemTypeEnum.EQUIP_RING

	def onWield(self, owner):
		"""
		装备完成
		"""
		EquipPartBase.EquipPartBase.onWield(self, owner)
		owner.onRingWield(self)

	def onRingUnWield(self, owner):
		"""
		卸下道具完成
		"""
		EquipPartBase.EquipPartBase.onUnWield(self, owner)
		owner.onHatUnWield(self)
