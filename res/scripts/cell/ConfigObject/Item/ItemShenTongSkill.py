# -*- coding: utf-8 -*-
import csstatus
import csdefine
import random
from ItemFactory import ItemFactoryInst as g_itemFactory
import ConfigObject.Item.ItemUse as ItemUse

class ItemShenTongSkill( ItemUse.ItemUse ):
	"""
	神通技能
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemUse.ItemUse.__init__(self, srcData)
		self.comminutionExp = srcData["Param1"] if srcData["Param1"] else 0		
		self.reduceUseSkillLevel = 0  # 随机降低使用等级
		rNum = random.randint(0, 10000)
		if rNum >= 0 and rNum < 4000:
			self.reduceUseSkillLevel = 5
		self.isComminution = False  	# 随机是否可以精研
		rNum = random.randint(0, 10000)
		if rNum >= 0 and rNum < 1000:
			self.isComminution = True


		self.dynamicData.update({"shenTongSkillID": self.skillID, "shenTongLevel":1,"preExp" : 0, "reduceUseSkillLevel":self.reduceUseSkillLevel, "isComminution":self.isComminution })

	def getItemDir( self, attrStr, default = "" ):
		"""获取物品的静态属性"""
		itemData = g_itemFactory.getItemData(self.id)
		if attrStr == "ReqLevel":
			return itemData[attrStr] - self.reduceUseSkillLevel
		if itemData:
			try:
				return itemData[attrStr]
			except:
				return default
		return default

	def checkReqClasses(self, owner):
		"""
		检测装备职业
		"""
		itemData = g_itemFactory.getItemData(self.id)
		reqClass = itemData["ReqClasses"]
		if reqClass:
			return str(owner.getProfession()) in reqClass.split("|")
		# 如果没有配置，说明多个职业匹配
		return True

	def checkUse(self, owner):
		"""
		使用前检测
		"""
		if not self.checkReqLevel(owner):
			return csstatus.ITEM_USE_LV_LESS_MSG
		if not self.checkReqClasses(owner):
			return csstatus.ITEM_USE_CLASS_NOTMATCH
		return csstatus.ITEM_USE_GO_ON_MSG

	def use(self, owner, target):
		"""
		使用物品
		"""
		ItemUse.ItemUse.use(self, owner, target)
		skillID = self.dynamicData["shenTongSkillID"]
		skill = owner.getSkill(skillID)
		if skill.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_NONE:
			statusID = owner.useSkillToEntityForItem( skillID, owner.id, self.getUid() )
		elif skill.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_ENTITY:
			statusID = owner.useSkillToEntityForItem( skillID, target.id, self.getUid() )
		elif skill.getTargetType() == csdefine.SKILL_CAST_OBJECT_TYPE_POSITION:
			statusID = owner.useSkillToEntityForItemPos( skillID, target.position, self.getUid() )
			
		if statusID != csstatus.SKILL_GO_ON:
			return statusID
		
		return csstatus.ITEM_USE_GO_ON_MSG

	def updateDynamicData(self, owner, prama):
		"""
		更新动态数据
		"""
		self.dynamicData.update(prama)
		skillID = self.dynamicData["shenTongSkillID"]
		level = self.dynamicData["shenTongLevel"]
		preExp = self.dynamicData["preExp"]
		reduceUseLevel = self.dynamicData["reduceUseSkillLevel"]
		isComminution = self.dynamicData["isComminution"]
		owner.client.CLIENT_UpdateShenTongDynamic(str(self.uid), skillID, level, preExp, reduceUseLevel, isComminution)

	def isHighQuality(self):
		"""
		是否为高品质
		"""
		return self.reduceUseSkillLevel and self.isComminution

	def hasRandomAttrAtInit(self):
		"""
		创建时候有随机属性
		"""
		return True