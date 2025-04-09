# -*- coding: utf-8 -*-

import KBEDebug
import Const
import csstatus
import random
import csdefine
import ItemTypeEnum
from ConfigObject.ConfigLoader import g_XiuweiMgr
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

	def use(self, owner, target):
		"""
		使用物品
		"""
		if owner.isMountOnPet():
			owner.statusMessage( csstatus.ITEM_IS_MOUNT_NOT_USE )
			return

		owner.onUseItem( self )
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
		roleNextLevelXiuWeiData = g_XiuweiMgr.getRoleXiuWeiData(g_XiuweiMgr.getRoleXiuweiLevel(owner) + 1)
		if owner.getLevel() < roleNextLevelXiuWeiData["playerLevel"] or owner.getXiuwei() > roleNextLevelXiuWeiData["xiuwei"]:
			return csstatus.ACCOUNT_STATE_CAN_NOT_GAIN_XIUWEI
		return ItemSpell.ItemSpell.checkUse( self, owner )
		
	def getXiuweiValue( self, isImmortal ):
		"""
		获得修为
		"""
		level = self.getLevel()
		if level in datas:
			value = datas[level]["xiuwei"] * self._xiuweiRate
			if isImmortal:
				value *= Const.SPAR_ITEM_RATE
			return int( value )
		else:
			KBEDebug.ERROR_MSG("config(Reward/RewardBasicValueData) level(%d) is empty!"%level)
			return 0
		
	def getAddItemID( self, isImmortal ):
		"""
		获得固定物品ID
		"""
		if len(self._sparItemIDs) >= 2:
			if isImmortal:
				return self._sparItemIDs[1]
		return self._sparItemIDs[0]

	def onUseResult(self, owner, useResult ):
		"""
		使用物品结果
		"""
		if not useResult:
			return
		# 充能物品,只消耗次数！不销毁
		if self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_EMPOWER:
			self.setAmount( owner, self.amount - 1 )
		# 次数物品，使用完！就销毁
		elif self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_TIME:
			if self.overlyingMax == -1:return		# 使用无限次数
			if self.amount > 1:
				self.setAmount( owner, self.amount - 1 )
			else:
				owner.removeItemByAmount(self, 1, csdefine.ITEM_REMOVE_BY_USE)
		# 无叠加物品，不消耗
		elif self.overlyingType == csdefine.ITEM_OVERLYING_TYPE_NONE:
			return
		else:
			# 使用次数的物品，用完就销毁
			owner.removeItemByAmount(self, 1, csdefine.ITEM_REMOVE_BY_USE)
			return