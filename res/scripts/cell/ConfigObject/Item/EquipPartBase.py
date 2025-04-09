# -*- coding: utf-8 -*-
import KBEDebug
import ItemTypeEnum
import csconst
import copy
import random
import Functions
from EquipPropertyParse import g_EquipPropertyLoadInst
import ConfigObject.Item.Equip as Equip

class EquipPartBase(Equip.Equip):
	"""
	装备 半成品基类
	"""
	def __init__(self, srcData):
		Equip.Equip.__init__(self, srcData)
		self.equipPropertyID = 0
		if srcData["Param2"]:				# 基础属性不随机
			self.equipPropertyID = int(srcData.get("Param2"))
			attackProperties = self.getBasePropertyByRate(csconst.PART_EQUIP_BASE_PROPERTY_RATE / 100)
			self.dynamicData["attackPropertiesStr"] = self.dictToStr(self.getEffectProperties(attackProperties))
		self.dynamicData["quenchingNum"] = 0			# 淬炼次数
		
	def getBasePropertyByRate( self, rate ):
		"""获得基础属性的倍率"""
		attackProperties = copy.deepcopy( g_EquipPropertyLoadInst.getDataByID(self.equipPropertyID) )
		for _id, value in attackProperties.items():
			attackProperties[_id] = round( value * rate )
		return attackProperties

	def checkUse(self, owner):
		"""
		使用前检测
		"""
		if self.canQuenching():
			return 
		
		return Equip.Equip.checkUse(self, owner)
		
	def canQuenching( self ):
		"""是否可淬炼"""
		return self.dynamicData["quenchingNum"] < csconst.QUENCHING_EQUIP_MAX_NUM
		
	def Quenching( self, owner ):
		"""淬炼"""
		self.dynamicData["quenchingNum"] += 1
		rate = random.randint(csconst.PART_EQUIP_QUENCHING_MIN_RATE, csconst.PART_EQUIP_QUENCHING_MAX_RATE) / 1000
		property = self.getBasePropertyByRate(rate)
		base = self.strToDict(self.dynamicData[ "attackPropertiesStr" ])
		for id, value in property.items():
			base[id] += value
		self.dynamicData["attackPropertiesStr"] = self.dictToStr(base)
		self.calculateCombatPower()
		owner.updateOneDataToClient("attackPropertiesStr", self.dynamicData["attackPropertiesStr"], self )
		owner.updateOneDataToClient("quenchingNum", self.dynamicData["quenchingNum"], self )
		
	def getDynamicDataForClient(self, entity ):
		#打包动态属性发送给客户端(注意，这里有3个属性的名字改了，所以要特殊处理)
		return Functions.toJsonString( {
			"hardiness": str(self.dynamicData["hardiness"]),
			"combatPower": str(self.dynamicData["combatPower"]),
			"attackProperties": self.dynamicData["attackPropertiesStr"],
			"attachProperties": self.dynamicData["attachPropertiesStr"],
			"intensifyData": self.dynamicData["intensifyDataStr"],
			"quenchingNum":self.dynamicData["quenchingNum"]
		} )