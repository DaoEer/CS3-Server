
import ConfigObject.Item.ItemBase as ItemBase
import random
import csdefine
import KBEDebug

class ItemComposeEquipBP(ItemBase.ItemBase):
	"""
	打造绿装图纸
	"""
	def __init__(self, srcData):
		ItemBase.ItemBase.__init__(self, srcData)
		self.successRateMin = 0
		self.successRateMax = 0
		self.addMaxRate = 0										# 可增加最大的成功率
		
		suitList = [int(i) for i in srcData["Param1"].split("|")]	# 0:没有，1:冰，2:火，3:玄，4:雷
		expStrList = srcData["Param2"].split("|")				# 配置数值0~100
		if len(expStrList) >= 2:
			self.successRateMin = int( expStrList[0] )
			self.successRateMax = int( expStrList[1] )
		self.addMaxRate = int(srcData["Param3"]) * 100
		#self.composeEquipID = int(srcData["Param4"])
		# 更新 绿装打造成功率
		self.dynamicData.update( {"successRate" : random.randint(self.successRateMin, self.successRateMax),
								  "addRate" : 0,
								  "suitIndex" : random.choice(suitList)})
				
	def getSuccessRate( self ):
		"""获得绿装打造成功率"""
		return (self.dynamicData["successRate"]  + self.dynamicData["addRate"]) / 100
		
	def addSuccessRate( self, addRate ):
		"""增加成功率"""
		oldRate = self.dynamicData["addRate"]
		rate = min( self.dynamicData["addRate"] + addRate, self.addMaxRate)
		if rate + self.dynamicData["successRate"] > 100:
			rate = 100 - self.dynamicData["successRate"]
		self.dynamicData["addRate"] = rate
		self.updateOneDataToClient( "addRate",self.dynamicData["addRate"],self )
		return oldRate - rate
	
	def getSuitIndex( self ):
		"""获取元素属性"""
		return self.dynamicData["suitIndex"]