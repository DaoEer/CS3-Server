
import ConfigObject.Item.ItemBase as ItemBase
import random
import ItemFactory
import csdefine
import Functions
from EquipPropertyParse import g_EquipPropertyLoadInst
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
		self.addMaxRate = int(srcData["Param3"])
		self.composeEquipID = int(srcData["Param4"])
		self.generateAttchPro()
		# 更新 绿装打造成功率
		self.dynamicData.update( {"successRate" : random.randint(self.successRateMin, self.successRateMax),
								  "addRate" : 0.0,
								  "suitIndex" : random.choice(suitList)})
				
	def generateAttchPro( self ):
		"""生成装备的攻击属性"""
		itemData = ItemFactory.ItemFactoryInst.getItemData(self.composeEquipID)
		if itemData["Param2"]:
			attackProperties = g_EquipPropertyLoadInst.getDataByID(int(itemData["Param2"]))
			self.dynamicData.update({"attackPropertiesStr": self.dictToStr(self.getEffectProperties(attackProperties))})
				
	def getSuccessRate( self ):
		"""获得绿装打造成功率"""
		return (self.dynamicData["successRate"]  + self.dynamicData["addRate"]) / 100
		
	def addSuccessRate( self, player, addRate ):
		"""增加成功率"""
		oldRate = self.dynamicData["addRate"]
		rate = min( self.dynamicData["addRate"] + addRate, self.addMaxRate)
		if rate + self.dynamicData["successRate"] > 100:
			rate = 100 - self.dynamicData["successRate"]
		self.dynamicData["addRate"] = float( rate )
		player.updateOneDataToClient( "addRate",self.dynamicData["addRate"],self )
		return oldRate - rate
	
	def getSuitIndex( self ):
		"""获取元素属性"""
		return self.dynamicData["suitIndex"]
		
	def getComposeEquipID( self ):
		"""打造装备ID"""
		return self.composeEquipID
		
	def getEffectProperties(self, dict):
		"""
		获取非零属性
		"""
		if not dict:
			return {}
		temp = {}
		for key, value in dict.items():
			if value != 0:
				temp.update({key: value})
		return temp

	def dictToStr(self, dict):
		"""
		把字典数据转换为字符串，可用于传输到客户端
		格式为：propertytype#value|propertytype#value|propertytype#value
		"""
		tempstr = ""
		if not dict:
			return tempstr
		for key, value in dict.items():
			tempstr += (str(key) + "#" + str(value) + "|")
		tempstr = tempstr[:-1]		#去掉最后一个的|
		return tempstr
		
	def getDynamicDataForClient(self, entity ):
		return Functions.toJsonString( self.dynamicData )
		
	def hasRandomAttrAtInit(self):
		"""
		创建时候有随机属性
		"""
		return True