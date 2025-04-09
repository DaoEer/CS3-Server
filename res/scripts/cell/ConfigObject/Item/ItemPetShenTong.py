# -*- coding: utf-8 -*-
import csdefine
import ConfigObject.Item.ItemUse as ItemUse
import Functions
import csstatus
import random
import csconst

class ItemPetShenTong( ItemUse.ItemUse ):
	"""
	学习幻兽神通技能道具
	"""
	def __init__(self, srcData):
		ItemUse.ItemUse.__init__(self, srcData)
		self._shenTongSkillID = 0
		self._times = []
		self._weightList = []
		self._maxTimes = self._maxTimes = csconst.SHENTONG_SKILL_MAX_TIMES
		self._profession = 0
		if srcData["Param1"]:
			self._shenTongSkillID = int(srcData["Param1"])

		Param2 = srcData["Param2"].split("|")
		for i in Param2:
			k = i.split(":")
			self._times.append(int(k[0]))
			self._weightList.append(float(k[1]))

		if srcData["Param3"]:
			self._profession = int(srcData["Param3"])

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

	def checkUse(self, owner):
		"""
		使用物品检测
		"""		
		return csstatus.PET_SHEN_TONG_CANT_USE

