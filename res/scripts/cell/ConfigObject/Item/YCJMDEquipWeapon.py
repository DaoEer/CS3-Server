# -*- coding: utf-8 -*-

import KBEDebug
import ConfigObject.Item.YCJMDEquip as YCJMDEquip
import ItemTypeEnum

class YCJMDEquipWeapon(YCJMDEquip.YCJMDEquip):
	"""
	CST-12212 大荒战场50人PVP 武器
	"""
	def __init__(self, srcData):
		"""
		"""
		YCJMDEquip.YCJMDEquip.__init__(self, srcData)

	def getDictFromObj(self):
		"""
		转化为字典打包传输或保存到数据库
		"""
		return YCJMDEquip.YCJMDEquip.getDictFromObj(self)


	def getEquipPart(self):
		"""
		获取装备部位,武器
		"""
		return ItemTypeEnum.EQUIP_WEAPON_YCJMD