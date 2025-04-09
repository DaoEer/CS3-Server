# -*- coding: utf-8 -*-

import KBEDebug
import Const
import csstatus
import random
import ItemTypeEnum
import ConfigObject.Item.ItemSpell as ItemSpell
from Reward.RewardBasicValueData import datas

class ItemSpar(ItemSpell.ItemSpell):
	"""
	晶核物品
	"""
	def __init__(self, srcData):
		ItemSpell.ItemSpell.__init__(self, srcData)
		self.skillID = 1												# 覆盖skillID
		self._xiuweiRate = float( srcData.get( "Param1", 1.0 ) )		# 倍率
		self._immortalRateCommon, self._immortalRateSpecial = list(float(x) for x in srcData.get("Param2").split("|"))		# 触发仙化概率  普通区域|静心台区域
		
		sparSkillID1, sparSkillID2 = srcData.get("Param3").split(";")
		self._sparSkillIDsCommon = list(int(x) for x in sparSkillID1.split("|")) #普通区域 普通炼化技能|普通仙化技能
		self._sparSkillIDsSpecial = list(int(x) for x in sparSkillID2.split("|")) #静心台区域 高级炼化技能|高级仙化技能
		self._sparItemIDs = srcData.get("Param4", "").split("|")		# 炼化|仙化 失败给的物品ID

	def isSparItem(self):
		"""
		是否是晶石，放在晶石背包中的物品
		"""
		return True

	def use(self, owner, target):
		"""
		使用物品
		"""
		if owner.isMountOnPet():
			owner.statusMessage( csstatus.ITEM_IS_MOUNT_NOT_USE )
			return

		if not target:
			target = owner
		
		roll = random.random()
		if owner.findBuffsByBuffID(Const.BUFF_REFINE_AREA):
			immortalRate = self._immortalRateSpecial
			skillID = self._sparSkillIDsSpecial[1] if roll<= immortalRate else self._sparSkillIDsSpecial[0]
		else:
			immortalRate = self._immortalRateCommon
			skillID = self._sparSkillIDsCommon[1] if roll<= immortalRate else self._sparSkillIDsCommon[0]

		statusID = owner.useSkillToEntityForItem( skillID, target.id, self.getUid() )
		if statusID != csstatus.SKILL_GO_ON:
			return statusID
		
		return csstatus.ITEM_USE_GO_ON_MSG
		
	def checkUse(self, owner):
		"""
		使用物品检测
		"""
		return ItemSpell.ItemSpell.checkUse( self, owner )
		
	def getXiuweiValue( self, isImmortal ):
		"""
		获得修为
		"""
		if self.level in datas:
			value = datas[self.level]["xiuwei"] * self._xiuweiRate
			if isImmortal:
				value *= Const.SPAR_ITEM_RATE
			return int( value )
		else:
			KBEDebug.ERROR_MSG("config(Reward/RewardBasicValueData) level(%d) is empty!"%self.level)
			return 0
		
	def getAddItemID( self, isImmortal ):
		"""
		获得固定物品ID
		"""
		if len(self._sparItemIDs) >= 2:
			if isImmortal:
				return self._sparItemIDs[1]
		return self._sparItemIDs[0]
