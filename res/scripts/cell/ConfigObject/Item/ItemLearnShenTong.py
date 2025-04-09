# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
import Functions
import csstatus
import random
import KBEDebug
import csconst

class ItemLearnShenTong( ItemUse.ItemUse ):
	"""
	学习神通技能道具
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._shenTongSkillID = 0
		self._times = []
		self._weightList = []
		self._maxTimes = csconst.SHENTONG_SKILL_MAX_TIMES
		if srcData["Param1"]:
			self._shenTongSkillID = int(srcData["Param1"])

		Param2 = srcData["Param2"].split("|")
		for i in Param2:
			k = i.split(":")
			self._times.append(int(k[0]))
			self._weightList.append(float(k[1]))

	def loadDynamicData( self, params ):
		"""加载动态数据"""
		ItemUse.ItemUse.loadDynamicData( self, params )
		
		# 该动态数据只在第一次创建生成
		if "shentongUseTimes" in self.dynamicData:
			return
		times = self.getUseTimesForWeight()
		self.dynamicData.update({"shentongUseTimes": times })

	def getDynamicDataForClient(self, entity ):
		"""
		将物品动态数据发送到客户端
		"""
		return Functions.toJsonString( {"shentongUseTimes":self.dynamicData["shentongUseTimes"]} )

	def getUseTimesForWeight(self):
		"""
		根据权重获得神通技能使用次数
		"""
		weightValue = 0
		sumWeight = 0
		for value in self._weightList:
			sumWeight += value
		x = random.uniform( 0, sumWeight )
		for times, weight in zip( self._times, self._weightList ):
			weightValue += weight
			if x <= weightValue:
				return times
		return 0

	def getSkillID( self ):
		"""
		获取物品触发的技能ID
		"""
		return self.skillID

	def checkReqClasses(self, owner):
		"""
		检测职业
		"""
		reqClass = self.getItemDir("ReqClasses")
		if reqClass:
			return str(owner.getProfession()) in reqClass.split("|")
		# 如果没有配置，说明多个职业匹配
		return True

	def checkUse(self, owner):
		"""
		使用物品检测
		"""		
		if self._shenTongSkillID == 0:
			KBEDebug.ERROR_MSG("ItemID : %s Param1 is ERROR!!!!!!!!!"%self.id)
			return csstatus.SKILL_NOT_EXIST

		if not self.checkReqLevel(owner):
			return csstatus.ITEM_USE_LV_LESS_MSG
		if not self.checkReqClasses(owner):
			return csstatus.ITEM_USE_CLASS_NOTMATCH
			
		isHas = False
		for element in owner.shentongSkills:
			if element["skillID"] == self._shenTongSkillID:
				isHas = True
				if element["times"] >= self._maxTimes:
					return csstatus.SHEN_TONG_TIMES_FULL
				break

		if not isHas and len(owner.shentongSkills) >= 30:
			return csstatus.SHEN_TONG_MAX

		return ItemUse.ItemUse.checkUse( self, owner )

	def use(self, owner, target):
		ItemUse.ItemUse.use(self, owner, target)
		if not target:
			target = owner
		addTimes = self.dynamicData.get("shentongUseTimes", 0)
		owner.useItemLearnShenTong( self._shenTongSkillID, addTimes, self._maxTimes, self.getUid())