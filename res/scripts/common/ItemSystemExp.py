#-*-coding:utf-8-*-

import KBEDebug
import Singleton
import LoadModule
import random
import csdefine
import copy
import ItemTypeEnum
import KBEngine

#datas/Item
import Item.PropertyType
import Item.PropertyValue
import Item.ValueProbability
import EntityProperty.RoleBaseProperty
import EntityProperty.PetBaseProperty
import EntityProperty.MonsterBaseProperty
import EntityProperty.PropertyExchangeCfg
import EntityProperty.SkillPostureExchangeCfg
import EntityProperty.CombatDamager
import EntityProperty.YXLMMonsterBaseProperty_1
import EntityProperty.YXLMMonsterBaseProperty_2
import EntityProperty.YXLMMonsterBaseProperty_3


#通过输入等级，获取所在等级区间范围
def getMatchLv(LvSectionList, InputLv):
	for item in LvSectionList:
		min = int(item.split("-")[0])
		max = int(item.split("-")[1])
		if (InputLv >= min) and (InputLv <= max):
			return item
	return None


def combineDict(dict1, dict2):
	"""
	合并两个属性值字典
	"""
	if not dict1:	return dict2
	if not dict2:	return dict1
	result = {}
	keylist = []
	keylist.extend(dict1.keys())
	for item in dict2.keys():
		if item not in keylist:
			keylist.append(item)

	for key in keylist:
		v1 = dict1.get(key, 0)
		v2 = dict2.get(key, 0)
		result.update({key: v1 + v2})
	return result

def combineEquipAttachProperties(dict1, dict2):
	"""
	合并附加属性
	"""
	result = {"_extra":{}, "_base":{}, "_percent":{}, "_value":{}}
	keylist = ["_extra", "_base", "_percent", "_value"]
	for key in keylist:
		result[key] = combineDict(dict1.get(key, {}), dict2.get(key, {}))
	return result


def getMatchProbability(propertyList, randomProperty):
	"""
	大部分应用
	propertyList是一个近似0到1的概率区间（已经排序了）
	randomProperty是一个0到1的概率
	也可以应用到值超过1的情况，只要是求一个正数在一个区间内的取值算法
	"""
	if randomProperty <= propertyList[0]:
		return propertyList[0]
	if randomProperty >= propertyList[-1]:
		return propertyList[-1]
	index = 0
	for item in propertyList:
		index += 1
		if (item < randomProperty) and (randomProperty <= propertyList[index]):		#概率落在此区间
			return propertyList[index]

def getSectionProbability( propertyDist ):
	"""
	获取区间概率
	propertyDist字典{section : probability}
	"""
	totalP = 0
	sectPro = 0
	for p in propertyDist.values():
		totalP += p
	randP = random.uniform( 0, totalP )
	for section, probability in propertyDist.items():
		sectPro += probability
		if sectPro >= randP:
			return section
	return 1
# -------------------------------------------------------------
# 装备强化公式
# -------------------------------------------------------------
class EquipIntensifyExp( Singleton.Singleton ):
	"""
	装备强化、装备回火、装备保存和还原
	"""
	def __init__( self ):
		self._intensifyDatas = {}	# 强化数据
		self._backfireDatas = {}	# 回火数据
		self._intensifyLv = {}		# 强化等级
		self._intensifyLvPercents = {}	#强化星级概率
		self._saveRestoreDatas = {}	# 保存还原数据
		self._kingCraftEquip = {}	# 升级王道神兵条件
		self._kingCraftEffect = {}	# 王道神兵效果
		self.initDatas()

	def initDatas( self ):
		#读取强化等级配置
		intensifyLv = LoadModule.openJsonCfg("Item/IntensifyLv.json")
		for item in intensifyLv:
			if item["MinMaxLv"] not in self._intensifyLv:
				self._intensifyLv.update({item["MinMaxLv"]: item})

		#读取强化消耗配置 
		intensifycost = LoadModule.openJsonCfg("Item/IntensifyCost.json")
		for item in intensifycost:
			if item["MinMaxLv"] not in self._intensifyDatas:
				self._intensifyDatas.update({item["MinMaxLv"] : { item["IntensifyLv"] : item}})
			else:
				self._intensifyDatas[item["MinMaxLv"]].update({item["IntensifyLv"] : item})

		#读取回火消耗配置
		backfirecost = LoadModule.openJsonCfg("Item/BackFireCost.json")
		for item in backfirecost:
			if item["MinMaxLv"] not in self._backfireDatas:
				self._backfireDatas.update({item["MinMaxLv"] : { item["BackFireLockCount"] : item}})
			else:
				self._backfireDatas[item["MinMaxLv"]].update({item["BackFireLockCount"] : item})

		#读取强化星级概率配置
		intensifyLvPercent = LoadModule.openJsonCfg("Item/IntensifyLvPercent.json")
		for item in intensifyLvPercent:
			self._intensifyLvPercents[item["StartLevel"]] = item
			
		# 读取保存、备份数据
		restorecost = LoadModule.openJsonCfg("Item/IntensifyRestoreCost.json")
		for item in restorecost:
			self._saveRestoreDatas[item["MinMaxLv"]] = item
			
		# 王道神兵 条件配置
		kingCraft = LoadModule.openJsonCfg("Item/KingCraftEquip.json")
		for item in kingCraft:
			if not item["MinMaxLv"] in self._kingCraftEquip:
				self._kingCraftEquip[item["MinMaxLv"]] = []
			self._kingCraftEquip[item["MinMaxLv"]].append( item )
			
		# 王道神兵 效果配置
		kingCraft = LoadModule.openJsonCfg("Item/KingCraftEffect.json")
		for item in kingCraft:
			self._kingCraftEffect[item["Name"]] = item

	def getMaxIntensifyLv(self, equiplv):
		"""
		获取最高强化等级
		"""
		lvsection = getMatchLv(self._intensifyLv.keys(), equiplv)
		if lvsection in self._intensifyLv:
			return self._intensifyLv[lvsection]["MaxIntensifyLv"]
		KBEDebug.ERROR_MSG("Can not find intensify levelsection as level(%d)"%equiplv)
		return 0

	def getMaxBackFireCount(self, equiplv):
		"""
		获取最高锁星数量
		"""
		lvsection = getMatchLv(self._intensifyLv.keys(), equiplv)
		if lvsection in self._intensifyLv:
			return self._intensifyLv[lvsection]["MaxLockStar"]
		KBEDebug.ERROR_MSG("Can not find backFire levelsection as level(%d)"%equiplv)
		return 0

	def getIntensifyCost(self, equiplv, intensifylv):
		"""
		获取单次强化消耗
		"""
		costmoney = 0
		lowMaterialCost = 0
		mediumMaterialCost = 0
		highMaterialCost = 0
		lvsections = self._intensifyDatas.keys();
		findsection = getMatchLv(lvsections, equiplv)
		if(findsection):
			if intensifylv in self._intensifyDatas[findsection]:
				costmoney = self._intensifyDatas[findsection][intensifylv]["MoneyCost"]
				lowMaterialCost = self._intensifyDatas[findsection][intensifylv]["LowMaterialCost"]
				mediumMaterialCost = self._intensifyDatas[findsection][intensifylv]["MediumMaterialCost"]
				highMaterialCost = self._intensifyDatas[findsection][intensifylv]["HighMaterialCost"]
				return (costmoney, lowMaterialCost, mediumMaterialCost, highMaterialCost)
		KBEDebug.ERROR_MSG("Can not find intensify levelsection as level(%d), intensifylv(%d)"%(equiplv,intensifylv))
		return (costmoney, lowMaterialCost, mediumMaterialCost, highMaterialCost)
	
	def getSumIntensifyCost(self, equiplv, currIntensifyLv, dstIntensifylv, ):
		"""
		获取多次强化消耗
		"""
		costmoney = 0
		lowMaterialCost = 0
		mediumMaterialCost = 0
		highMaterialCost = 0
		if currIntensifyLv <= dstIntensifylv:	
			tempcostmoney = 0
			tempwhiteBeadCount = 0
			tempfiveBeadCount = 0
			tempsuperBeadCount = 0
			for lv in range(currIntensifyLv+1, dstIntensifylv+1):
				tempcostmoney, tempwhiteBeadCount, tempfiveBeadCount, tempsuperBeadCount = self.getIntensifyCost(equiplv, lv)
				costmoney += tempcostmoney
				lowMaterialCost += tempwhiteBeadCount
				mediumMaterialCost += tempfiveBeadCount
				highMaterialCost += tempsuperBeadCount
		return (costmoney, lowMaterialCost, mediumMaterialCost, highMaterialCost)

	def getBackFireCost(self, equiplv, SaveCount):
		"""
		获取回火的消耗
		"""	
		costmoney, lowMaterialCost, mediumMaterialCost, highMaterialCost = (0,0,0,0)
		lvsections = self._backfireDatas.keys();
		findsection = getMatchLv(lvsections, equiplv)
		if findsection:
			if SaveCount in self._backfireDatas[findsection]:
				costmoney = self._backfireDatas[findsection][SaveCount]["MoneyCost"]
				lowMaterialCost = self._backfireDatas[findsection][SaveCount]["LowMaterialCost"]
				mediumMaterialCost = self._backfireDatas[findsection][SaveCount]["MediumMaterialCost"]
				highMaterialCost = self._backfireDatas[findsection][SaveCount]["HighMaterialCost"]
				return (costmoney, lowMaterialCost, mediumMaterialCost, highMaterialCost)
		KBEDebug.ERROR_MSG("Can not find backFire config levelsection as level(%d)"%equiplv)
		return (costmoney, lowMaterialCost, mediumMaterialCost, highMaterialCost)

	def getStar(self, dstIntensifyLv, attachItem):
		"""
		获取装备强化星级
		"""
		iron = self._intensifyLvPercents[dstIntensifyLv]["IronPercent"]
		copper = self._intensifyLvPercents[dstIntensifyLv]["CopperPercent"]
		silver = self._intensifyLvPercents[dstIntensifyLv]["SilverPercent"]
		gold = self._intensifyLvPercents[dstIntensifyLv]["GoldPercent"]
		total = iron + copper + silver + gold
		ironPercent = iron / total
		copperPercent = copper / total
		silverPercent = silver / total
		goldPercent = gold / total 
		
		if attachItem:			# 如果有附加材料
			goldPercent += attachItem.goldProbability
			silverPercent += attachItem.silberProbability
			remainPercent = 1 - goldPercent - silverPercent
			if copperPercent:
				copperPercent = remainPercent / ( copperPercent + ironPercent ) * copperPercent
			if ironPercent:
				ironPercent = remainPercent / ( copperPercent + ironPercent ) * ironPercent
		randomfloat = random.random()
		if ironPercent >= randomfloat:
			return ItemTypeEnum.IRONSTAR
		elif ironPercent + copperPercent >= randomfloat:
			return ItemTypeEnum.COPPERSTAR
		elif ironPercent + copperPercent + silverPercent >= randomfloat:
			return ItemTypeEnum.SILVERSTAR
		else:
			return ItemTypeEnum.GOLDSTAR

	def getMainPropertyIDAndValue(self, equip, starLv):
		"""
		获取主属性ID及值，一般是两个，
		"""
		valueRange = ItemTypeEnum.INTENSIFY_MAINVALUE[starLv]
		value = random.uniform(valueRange[0],valueRange[1])
		mainProperty = []
		for proerptyID, properptyValue in equip.strToDict(equip.dynamicData[ "attackPropertiesStr" ]).items():
#			mainProperty.append( (proerptyID, properptyValue * value) )
			mainProperty.append( (proerptyID, int(value * ItemTypeEnum.PRECENTRATIO / 100) ))
		return mainProperty

	def getMainPropertyIDAndMaxValue(self, equip, starLv):
		"""
		获取主属性ID及最大值，一般是两个，
		"""
		valueRange = ItemTypeEnum.INTENSIFY_MAINVALUE[starLv]
		maxValue = valueRange[1]
		mainProperty = {}
		for proerptyID, properptyValue in equip.strToDict(equip.dynamicData[ "attackPropertiesStr" ]).items():
			mainProperty[proerptyID] = int(maxValue * ItemTypeEnum.PRECENTRATIO / 100 )
		return mainProperty

	def getMaxMainPropertyIDAndValue(self, equip, starLv):
		"""
		获取主属性ID及最大值，一般是两个，
		"""
		valueRange = ItemTypeEnum.INTENSIFY_MAINVALUE[starLv]
		maxValue = valueRange[1]
		mainProperty = []
		for proerptyID, properptyValue in equip.strToDict(equip.dynamicData[ "attackPropertiesStr" ]).items():
#			mainProperty.append( (proerptyID, properptyValue * maxValue) )
			mainProperty.append( (proerptyID, int(maxValue * ItemTypeEnum.PRECENTRATIO / 100) ))
		return mainProperty
	def getMinMainPropertyIDAndValue(self, equip, starLv):
		"""
		获取主属性ID及最小值，一般是两个，
		"""
		valueRange = ItemTypeEnum.INTENSIFY_MAINVALUE[starLv]
		minValue = valueRange[0]
		mainProperty = []
		for proerptyID, properptyValue in equip.strToDict(equip.dynamicData[ "attackPropertiesStr" ]).items():
			mainProperty.append( (proerptyID, int(minValue * ItemTypeEnum.PRECENTRATIO / 100) ))
		return mainProperty

	def getAveMainPropertyIDAndValue(self, equip, starLv):
		"""
		获取主属性ID及平均值，一般是两个，
		"""
		valueRange = ItemTypeEnum.INTENSIFY_MAINVALUE[starLv]
		aveValue = (valueRange[0] + valueRange[1])/2
		mainProperty = []
		for proerptyID, properptyValue in equip.strToDict(equip.dynamicData[ "attackPropertiesStr" ]).items():
			mainProperty.append( (proerptyID, int(aveValue * ItemTypeEnum.PRECENTRATIO / 100) ))
		return mainProperty

	def getAttachPropertyAndValues(self, equip, starLv):
		"""
		获取附加属性和值，可能为空，或一条或两条
		"""
		result = []
		propertyIDs = self.getPropertyIDs(starLv, equip)
		for propertyID in propertyIDs:
			propertyvalue = g_EquipPropertyValueExp.getIntensifyPropertyValue(equip.getLevel(), equip.getReqClass(), equip.getEquipPart(), propertyID)
			result.append((propertyID, propertyvalue))
		return result
		
	def getMaxAttachPropertyAndValues(self, equip, starLv):
		"""
		获取附加属性和最大值，可能为空，或一条或两条
		"""
		result = []
		propertyIDs = self.getPropertyIDs(starLv, equip)
		for propertyID in propertyIDs:
			propertyvalue = g_EquipPropertyValueExp.getMaxIntensifyPropertyValue(equip.getLevel(), equip.getReqClass(), equip.getEquipPart(), propertyID)
			result.append((propertyID, propertyvalue))
		return result

	def getPropertyID(self, starLv, equip):
		"""
		获取一条属性ID
		"""
		return g_EquipPropertyTypeExp.getNPropertyTypes(equip.getLevel(), equip.getReqClass(), equip.getEquipPart(), 1)

	def getPropertyIDs(self, starLv, equip):
		"""
		获取属性ID列表
		铁星	0%	0%
		铜星	50%	0%
		银星	100%	30%
		金星	100%	80%
		"""
		result = []
		randomfirst = random.uniform(0.0, 1.0)
		randomsecond = random.uniform(0.0, 1.0)
		if starLv == ItemTypeEnum.IRONSTAR:	#铁星
			return result
		elif starLv == ItemTypeEnum.COPPERSTAR:	#铜星
			if randomfirst <= 0.5:
				result.extend(self.getPropertyID(starLv, equip))
			return result
		elif starLv == ItemTypeEnum.SILVERSTAR:	#银星
			result.extend(self.getPropertyID(starLv, equip))
			if randomsecond <= 0.3:
				result.extend(self.getPropertyID(starLv, equip))
			return result
		elif starLv == ItemTypeEnum.GOLDSTAR:	#金星
			result.extend(self.getPropertyID(starLv, equip))
			if randomsecond <= 0.8:
				result.extend(self.getPropertyID(starLv, equip))
			return result
		else:
			return result

	def getOnceIntensifyResult(self, equip, intensifyLv, attachItem):
		"""
		获取单次强化结果
		"""
		starLv = self.getStar(intensifyLv, attachItem)
		mainPV = self.getMainPropertyIDAndValue(equip, starLv)
		attachPVs = self.getAttachPropertyAndValues(equip, starLv)
		
		propertystr = ""
		for (id, value) in mainPV:
			propertystr += str(id) + "#" + str(value) + "|"
		propertystr = propertystr[:-1]
		
		propertystr += ":"
		for (id, value) in attachPVs:
			propertystr += str(id) + "#" + str(value) + "|"
		propertystr = propertystr[:-1]
#		uid = KBEngine.genUUID64()
		return ( starLv, propertystr )


	def getIntensifResult(self, equip, dstIntensifyLv, attachItem, attachItemNum = 0):
		"""
		获取强化结果,可能是多条强化结果
		(starlv, PropertyStr), propertystr = 30001#10:20001#20|40001#30
		"""
		result = []
		currIntensifyLv = equip.getIntensifyLevel()
		intensifyLvList = [lv for lv in range(currIntensifyLv+1, dstIntensifyLv+1)]
		isKingEquip = equip.isKingEquip()
		hasStar = 0
		if isKingEquip:			
			hasStar = self.getKingCraftStart( equip )
		for lv in intensifyLvList:
			attachItemNum -= 1
			if attachItemNum <= 0:
				attachItem = 0
			
			if isKingEquip:
				if hasStar >= lv:			# 王道神兵 保护最基本的金星（hasStar）
					result.append( self.getCustomOnceIntensifyResult(equip, ItemTypeEnum.GOLDSTAR) )
				else:						# 王道神兵生成其他星的规则
					starLv = self.getStar(lv, attachItem)
					result.append( self.getCustomOnceIntensifyResult(equip, starLv) )
			else:				
				result.append(self.getOnceIntensifyResult(equip, lv, attachItem))
		return result
		
	def getIntensifySaveCost( self, equip ):
		"""获取保存强化消耗"""
		section = getMatchLv( self._saveRestoreDatas, equip.getLevel() )
		if section:
			return self._saveRestoreDatas[section]["SaveMoneyCost"], self._saveRestoreDatas[section]["SaveBeidouFuCost"]
		else:
			KBEDebug.ERROR_MSG("Save intensify err!!can not find equip(%d) levelsection"%equip.getLevel())
			return 0,0
		
	def getIntensifyRestore( self, equip ):
		"""获取还原强化消耗"""
		section = getMatchLv( self._saveRestoreDatas, equip.getLevel() )
		if section:
			return self._saveRestoreDatas[section]["RestoreMoneyCost"], self._saveRestoreDatas[section]["RestoreBeidouFuCost"]
		else:
			KBEDebug.ERROR_MSG("Restore intensify err!!can not find equip(%d) levelsection"%equip.getLevel())
			return 0,0
			
	def getIntensifyMaxLevel( self, equip ):
		"""获取装备强化的最大等级"""
		section = getMatchLv( self._intensifyDatas, equip.getLevel() )
		if section:
			return max(self._intensifyDatas[section])
		KBEDebug.ERROR_MSG("Can not find intensify config levelsection as level(%d)"%equip.getLevel())
		return 0

	def getCustomIntensifResult(self, equip, goldStar, silverStar, copperStar, ironStar, mainValueRange = 2):
		"""根据自定义星级获取装备强化数据"""
		result = []
		for i in range(goldStar):
			result.append(self.getCustomOnceIntensifyResult(equip, ItemTypeEnum.GOLDSTAR, mainValueRange))
		for i in range(silverStar):
			result.append(self.getCustomOnceIntensifyResult(equip, ItemTypeEnum.SILVERSTAR, mainValueRange))
		for i in range(copperStar):
			result.append(self.getCustomOnceIntensifyResult(equip, ItemTypeEnum.COPPERSTAR, mainValueRange))
		for i in range(ironStar):
			result.append(self.getCustomOnceIntensifyResult(equip, ItemTypeEnum.IRONSTAR, mainValueRange))
		return result

	def getCustomOnceIntensifyResult(self, equip, starLv, mainValueRange = 2):
		"""
		获取自定义单次强化结果
		"""
		mainPV = []
		if mainValueRange == 0:
			mainPV = self.getMainPropertyIDAndValue(equip, starLv)
		elif mainValueRange == 1:
			mainPV = self.getMinMainPropertyIDAndValue(equip, starLv)
		elif mainValueRange == 2:
			mainPV = self.getMaxMainPropertyIDAndValue(equip, starLv)
		elif mainValueRange == 3:
			mainPV = self.getAveMainPropertyIDAndValue(equip, starLv)
		attachPVs = self.getMaxAttachPropertyAndValues(equip, starLv)
		
		propertystr = ""
		for (id, value) in mainPV:
			propertystr += str(id) + "#" + str(value) + "|"
		propertystr = propertystr[:-1]
		
		propertystr += ":"
		for (id, value) in attachPVs:
			propertystr += str(id) + "#" + str(value) + "|"
		propertystr = propertystr[:-1]
#		uid = KBEngine.genUUID64()
		return ( starLv, propertystr )
		
	def getKingCraftStart( self, equip ):
		"""王道神兵 有金星个数"""
		if equip.isKingEquip():
			level = equip.getLevel()
			section = getMatchLv( self._kingCraftEquip.keys(), level )
			if section:
				reqClass = equip.getReqClass()
				equipPart = equip.getEquipPart()
				intensifyDatas = equip.parseIntensifyDatas( equip.dynamicData["intensifyDataStr"])
				attachDatas = equip.strToDict(equip.dynamicData[ "attachPropertiesStr" ])
				for data in self._kingCraftEquip[section]:
					if data["Class"] == reqClass and data["ModelPart"] == equipPart:
						return data["NeedStar"]
		return 0
		
	def canBeKingcraft( self, equip ):
		"""获取 变成王道神兵条件"""
		if equip.isGreenSheng():
			level = equip.getLevel()
			section = getMatchLv( self._kingCraftEquip.keys(), level )
			if section:
				reqClass = equip.getReqClass()
				equipPart = equip.getEquipPart()
				intensifyDatas = equip.parseIntensifyDatas( equip.dynamicData["intensifyDataStr"])
				attachDatas = equip.strToDict(equip.dynamicData[ "attachPropertiesStr" ])
				for data in self._kingCraftEquip[section]:
					if data["Class"] == reqClass and data["ModelPart"] == equipPart:
						# 金星数量检查
						starNum = 0
						for datas in intensifyDatas.values():
							if datas[0] == ItemTypeEnum.GOLDSTAR:
								starNum += 1
						if starNum < data["NeedStar"]:
							return False
						# 对应属性和属性值检查
						for name in ["NeedPropertys1", "NeedPropertys2"]:
							isPass = True
							for pID in data[name]:
								if not pID in attachDatas:
									isPass = False
									break
								maxValue = g_EquipPropertyValueExp.getMaxPropertyValue(level, reqClass,equipPart, pID)
								if attachDatas[pID] / maxValue < data["UpperPercent"] / 100:
									isPass = False
									break
							if isPass:
								return True
		return False
		
	def getKingCraftEffect( self, equipID ):
		"""王道神兵效果"""
		return self._kingCraftEffect.get( equipID, {} )

def getListSum(srcList):
	"""
	计算出列表
	"""
	sum = 0
	for item in srcList:
		sum += item
	return sum


#装备随机属性类型的抽取
class EquipPropertyTypeExp(Singleton.Singleton ):
	def __init__(self):
		"""
		PropertyType字典结构Datas[levelsection][profession][modelpart] = {propertyprobability: propertytype}
		"""
		self._datas = Item.PropertyType.Datas

	def getPropertyTypeData(self, level, profession, modelpart):
		"""
		profession 用0来表示所有职业通用
		返回一个字典的数据
		"""
		levelsection = getMatchLv(list(self._datas), level)
		try:
			return list(self._datas[levelsection][profession][modelpart])
		except:
			KBEDebug.ERROR_MSG("Can not find PropertyType.py config!level(%d), profession(%d), modelpart(%d)"%(level,profession,modelpart))
			return []

	def getOnePropertyType(self, data):
		"""
		data = [(propertyprobability: propertytype)]
		"""
		randomvalue = random.random()
		newdic = self.getNewDict(data)
		matchvalue = getMatchProbability(sorted(newdic.keys()), randomvalue)
		return newdic[matchvalue]

	def getNewDict(self, data):
		"""
		把[(propertyprobability: propertytype)]，转换为字典
		"""
		temp = {}
		index = 0
		if not data:
			KBEDebug.ERROR_MSG("getNewDict datas[%s] is None"%str(data))
			return temp
		sumprobability = getListSum([item[0] for item in data])
		for i in range(0, len(data)):
			probability = getListSum([item[0] for item in data[:i+1]]) / sumprobability
			propertytype = data[i][1]
			temp.update({probability: propertytype})	
		return temp

	def updateList(self, data, propertytype):
		"""
		通过值找以key
		"""
		for item in data:
			if item[1] == propertytype:
				data.remove(item)
				return data

	def getNPropertyTypes(self, level, profession, modelpart, n):
		"""
		抽取n条属性类型
		"""
		result = []
		data = self.getPropertyTypeData(level, profession, modelpart)
		for i in range(0, n):
			propertyID = self.getOnePropertyType(data)
			result.append(propertyID)
			self.updateList(data, propertyID)

		return result


#装备随机属性值的抽取
class EquipPropertyValueExp(Singleton.Singleton ):
	"""
	PropertyValue字典结构Datas[levelsection][profession][modelpart] = {propertyID: (min, max)}
	ValueProbability字典结构 {probability: session}
	"""
	def __init__(self):
		self._datas = Item.PropertyValue.Datas
		self._valueprobability = Item.ValueProbability.Datas["attach"]	#附加属性的
		self._intensifyvalueprobability = Item.ValueProbability.Datas["intensify"]	#强化属性的概率
		self._recastvalueprobability = Item.ValueProbability.Datas["recast"]	#重铸属性的概率

	def getLevelSection(self, level, profession, modelpart, propertyID):
		"""
		获取所在属性值范围
		profession 用0来表示所有职业通用
		"""
		levelsection = getMatchLv(list(self._datas), level)		#所属等级段
		try:
			return list(self._datas[levelsection][profession][modelpart][propertyID])
		except:
			KBEDebug.ERROR_MSG("Can not find PropertyValue.py config!level(%d), profession(%d), modelpart(%d)"%(level,profession,modelpart))
			return []

	def getPropertyValue(self, level, profession, modelpart, propertyID):
		"""
		抽取属性值
		"""
		result = self.getLevelSection(level, profession, modelpart, propertyID)
		KBEDebug.DEBUG_MSG("type[%s], result[%s]"%(str(type(result)), str(result)))
		min, max, intensifymin, intensifymax = result
		session = getSectionProbability(self._valueprobability)
		newmin = int( min + ((max-min) * (session - 1))/10.0 )
		newmax = int( min + ((max-min) * session)/10.0 )
		return random.randint(newmin, newmax)
	
	def getIntensifyPropertyValue(self, level, profession, modelpart, propertyID):
		"""
		抽取强化属性
		"""
		result = self.getLevelSection(level, profession, modelpart, propertyID)
		KBEDebug.DEBUG_MSG("type[%s], result[%s]"%(str(type(result)), str(result)))
		_min, _max, intensifymin, intensifymax = result
		session = getSectionProbability(self._intensifyvalueprobability)
		newmin = int( intensifymin + ((intensifymax-intensifymin) * (session - 1))/10.0 )
		newmax = int( intensifymin + ((intensifymax-intensifymin) * session)/10.0 )
		return max( random.randint(newmin, newmax), 1 )
		
	def getReCastPropertyValue(self, level, profession, modelpart, propertyID):
		"""
		抽取重铸属性值
		"""
		result = self.getLevelSection(level, profession, modelpart, propertyID)
		KBEDebug.DEBUG_MSG("type[%s], result[%s]"%(str(type(result)), str(result)))
		min, max, intensifymin, intensifymax = result
		session = getSectionProbability(self._recastvalueprobability)
		newmin = int( min + ((max-min) * (session - 1))/10.0 )
		newmax = int( min + ((max-min) * session)/10.0 )
		return random.randint(newmin, newmax)

	def getMaxPropertyValue(self, level, profession, modelpart, propertyID):
		"""
		抽取最大值
		"""
		result = self.getLevelSection(level, profession, modelpart, propertyID)
		KBEDebug.DEBUG_MSG("type[%s], result[%s]"%(str(type(result)), str(result)))
		min, max, intensifymin, intensifymax = result
		return max
		
	def getMaxIntensifyPropertyValue(self, level, profession, modelpart, propertyID):
		"""
		抽取强化属性最大值
		"""
		result = self.getLevelSection(level, profession, modelpart, propertyID)
		KBEDebug.DEBUG_MSG("type[%s], result[%s]"%(str(type(result)), str(result)))
		_min, _max, intensifymin, intensifymax = result
		return intensifymax

# 装备洗练(附加属性)
# 装备重铸（附加属性）
# 装备传星
class EquipPropertyReSet( Singleton.Singleton ):
	def __init__( self ):
		self._shuffleCost = {}			# 装备洗练消耗
		self._recastCost = {}			# 装备重铸消耗
		self._transferIntensifyCost = {}		# 装备传星消耗
		self.initDatas()

	def initDatas( self ):
		#读取强化等级配置
		shuffleCost = LoadModule.openJsonCfg("Item/ShuffleCost.json")
		for item in shuffleCost:
			lv = item.pop( "MinMaxLv" )
			if not lv in self._shuffleCost:
				self._shuffleCost[lv] = []
			self._shuffleCost[lv].append( item )
			
		recastCost = LoadModule.openJsonCfg("Item/RecastCost.json")
		for item in recastCost:
			lv = item.pop( "MinMaxLv" )
			if not lv in self._recastCost:
				self._recastCost[lv] = []
			self._recastCost[lv].append( item )
		
		transferIntensifyCost = LoadModule.openJsonCfg("Item/TransferIntensifyCost.json")
		for item in transferIntensifyCost:
			lv = item.pop( "MinMaxLv" )
			if not lv in self._transferIntensifyCost:
				self._transferIntensifyCost[lv] = []
			self._transferIntensifyCost[lv].append( item )
			
	def getShuffleCost( self, equip, lockNum ):
		"""装备洗练消耗"""
		costConfigs = getMatchLv( self._shuffleCost, equip.getLevel() )
		if costConfigs:
			for config in self._shuffleCost[costConfigs]:
				if config["LockProNum"] == lockNum:
					return config["MoneyCost"], config["WashStone"], config["BloodFu"]
		KBEDebug.ERROR_MSG("Item/ShuffleCost.json config err!!equip(level:%d) can not match key(LockProNum:%d)"%(equip.getLevel(),lockNum))
		return 0, 0, 0
		
	def getShuffleYBCost( self, equip, lockNum ):
		"""装备洗练元宝消耗"""
		costConfigs = getMatchLv( self._shuffleCost, equip.getLevel() )
		if costConfigs:
			for config in self._shuffleCost[costConfigs]:
				if config["LockProNum"] == lockNum:
					return config["YBReplaceStone"], config["YBReplaceFu"]
		KBEDebug.ERROR_MSG("Item/ShuffleCost.json config err!!equip(level:%d) can not match key(LockProNum:%d)"%(equip.getLevel(),lockNum))
		return 0, 0
		
	def getRecastCostByProtect( self, equip, protectProNum, protectKey ):
		"""装备重铸消耗 """
		costConfigs = getMatchLv( self._recastCost, equip.getLevel() )
		if costConfigs:
			for config in self._recastCost[costConfigs]:
				if config["ProtectProNum"] == protectProNum:
					return config[protectKey]
		KBEDebug.ERROR_MSG("Item/RecastCost.json config err!!equip(level:%d) can not match key(ProtectProNum:%d)"%(equip.getLevel(),protectProNum))
		return 0

	def getTransferIntensifyCost( self, equip, proNum ):
		"""装备传星消耗"""
		costConfigs = getMatchLv( self._transferIntensifyCost, equip.getLevel() )
		if costConfigs:
			for config in self._transferIntensifyCost[costConfigs]:
				if config["LockCount"] == proNum:
					return config["MoneyCost"], config["LowMaterialCost"],config["MediumMaterialCost"],config["HighMaterialCost"]
		KBEDebug.ERROR_MSG("Item/transferIntensifyCost.json config err!!equip(level:%d) can not match key(ProtectProNum:%d)"%(equip.getLevel(),proNum))
		return 0, 0, 0, 0

# 装备打造
class EquipComposeCfg( Singleton.Singleton ):
	def __init__( self ):
		self._datas = {}			# 装备洗练消耗
		self.initDatas()

	def initDatas( self ):
		#读取强化等级配置
		composeDatas = LoadModule.openJsonCfg("Item/EquipComposeCost.json")
		for data in composeDatas:
			tmp = {}
			tmp["money"] = data["money"]
			tmp["equipID"] = int(data["Name"])
			tmp["material"] = {}
			tmp["material"][data["srcEquip"]] = 1
			tmp["material"][data["material_1"]] = data["mNum_1"]
			tmp["material"][data["material_2"]] = data["mNum_2"]
			tmp["material"][data["material_3"]] = data["mNum_3"]
			tmp["material"][data["material_4"]] = data["mNum_4"]
			self._datas[int(data["Name"])] = tmp
			
	def getEquipComposeCost( self, equipID ):
		"""获得装备打造消耗"""
		return self._datas.get( equipID, None )
		
# 轮回秘籍（工具打造）
class ToolComposeCfg( Singleton.Singleton ):
	def __init__( self ):
		self._toolComposeCost = {}			# 工具打造消耗
		self._greenComposeCost = {}			# 绿装打造消耗
		self._tripodComposeCost = {}		# 乾坤鼎打造消耗
		self._meltingEquipCfg = []			# 熔炼配置
		self._prayPoolCfg = {}				# 祈福 时间池
		self._jadeCommonedCfg = {}			# 玲珑玉令升级消耗
		self._forgeRateCfg = {}				# 打造倍率消耗表
		self.initDatas()

	def initDatas( self ):
		composeDatas = LoadModule.openJsonCfg("LunHuiMiJin/ToolComposeCost.json")
		for data in composeDatas:
			for strKey in list(data["material"].keys()):
				data["material"][int(strKey)] = data["material"].pop(strKey)
			self._toolComposeCost[int(data["Name"])] = data
			
		composeDatas = LoadModule.openJsonCfg("LunHuiMiJin/GreenEquipComposeCost.json")
		for data in composeDatas:
			for strKey in list(data["material"].keys()):
				data["material"][int(strKey)] = data["material"].pop(strKey)
			for strKey in list(data["mainMaterial"].keys()):
				data["mainMaterial"][int(strKey)] = data["mainMaterial"].pop(strKey)
			self._greenComposeCost[int(data["Name"])] = data
			
		composeDatas = LoadModule.openJsonCfg("LunHuiMiJin/TripodComposeCost.json")
		for data in composeDatas:
			for strKey in list(data["material"].keys()):
				data["material"][int(strKey)] = data["material"].pop(strKey)
			self._tripodComposeCost[int(data["Name"])] = data
			
		self._meltingEquipCfg = LoadModule.openJsonCfg("LunHuiMiJin/MeltingEquipCfg.json")
		
		dataDict = LoadModule.openJsonCfg("LunHuiMiJin/PrayPoolCfg.json")
		for key in list(dataDict):
			for _key in list(dataDict[key].keys()):
				dataDict[key][int(_key)] = dataDict[key].pop(_key)
		self._prayPoolCfg = dataDict
		
		self._jadeCommonedCfg = LoadModule.openJsonCfg("LunHuiMiJin/JadeCommonedCfg.json")
		for key in list(self._jadeCommonedCfg.keys()):
			self._jadeCommonedCfg[int(key)] = self._jadeCommonedCfg.pop(key)
			
		rateCfg = LoadModule.openJsonCfg("LunHuiMiJin/ForgeConsumeCfg.json")
		for rateData in rateCfg:
			self._forgeRateCfg[rateData["level"]] = rateData
			
	def getToolComposeCost( self, equipID, composeType, type, buildLevel ):
		"""获得工具打造消耗"""
		if composeType == csdefine.COMPOSE_TOOL_NORMAL:
			cost = copy.deepcopy( self._toolComposeCost.get( equipID, None ))
		elif composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			cost = copy.deepcopy(self._tripodComposeCost.get( equipID, None ))
		
		rate = None
		if type == csdefine.SPACE_TYPE_PUBLIC:
			rate = self._forgeRateCfg[buildLevel]["publicConsumeRate"] / 100
		elif type == csdefine.SPACE_TYPE_HIGH_DF:
			rate = self._forgeRateCfg[buildLevel]["highConsumeRate"] / 100
			
		if rate and cost:
			cost["money"] = round(cost["money"] * rate)
			cost["psionic"] = round(cost["psionic"] * rate)
			for id, num in cost["material"].items():
				cost["material"][id] = round( num * rate )
		return cost
		
	def getToolComposeEndTime( self, equipID, composeType ):
		"""获取打造结束时间"""
		if composeType == csdefine.COMPOSE_TOOL_NORMAL:
			cost = self._toolComposeCost[equipID]
		elif composeType == csdefine.COMPOSE_TOOL_GREEN_EQUIP:
			cost = self._greenComposeCost[equipID]
		elif composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			cost = self._tripodComposeCost[equipID]
		return cost["useTime"] * 60
		
	def getToolComposeNeedLevel( self, equipID, composeType ):
		"""获取打造 需要等级"""
		level = 0
		if composeType == csdefine.COMPOSE_TOOL_NORMAL:
			level = self._toolComposeCost[equipID]["needLevel"]
		elif composeType == csdefine.COMPOSE_TOOL_GREEN_EQUIP:
			level = self._greenComposeCost[equipID]["needLevel"]
		elif composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			level = self._tripodComposeCost[equipID]["needLevel"]
		return level
		
	def getGreenComposeCost( self, equipID, suitIndex, type, buildLevel ):
		"""获得绿装打造消耗"""
		cost = copy.deepcopy(self._greenComposeCost.get( equipID, {} ))
		cost["material"].update({cost["mainMaterial"][suitIndex] : cost["mainMaterialNum"]})
		
		rate = None
		if type == csdefine.SPACE_TYPE_PUBLIC:
			rate = self._forgeRateCfg[buildLevel]["publicConsumeRate"] / 100
		elif type == csdefine.SPACE_TYPE_HIGH_DF:
			rate = self._forgeRateCfg[buildLevel]["highConsumeRate"] / 100
			
		if rate and cost:
			cost["money"] = round(cost["money"] * rate)
			for id, num in cost["material"].items():
				cost["material"][id] = round( num * rate )
		return cost
		
	def getGreenComposeEquipPart(self, equipID):
		"""获得半成品ID"""
		return self._greenComposeCost[equipID]["partEquipID"]
		
	def getSuccessRate( self, level, quality, meltingLevel, meltingQuality ):
		"""获得增加的成功率"""
		for data in self._meltingEquipCfg:
			if data["level"] == level and data["quality"] == quality and \
			data["meltingLevel"] == meltingLevel and data["meltingQuality"] == meltingQuality:
				return data["successRate"] / 100				# 配置乘以10000了
		return 0
		
	def getPrayCost( self ):
		"""祈福消耗"""
		return self._prayPoolCfg["costItem"]
		
	def getTimeItemsFromPool( self ):
		"""从时间池中，随机时间"""
		itemTime = []
		total = sum(self._prayPoolCfg["prayTime"].values())
		poolData = copy.deepcopy(self._prayPoolCfg["prayTime"])
		for i in range(0,7):
			randNum = random.randrange(0, total)
			for time in sorted(poolData):
				weight = poolData[time]
				if randNum <= weight:
					itemTime.append( time )
					poolData.pop(time)
					total -= weight
					break
				randNum -= weight
		return itemTime
		
	def getRandomTime( self, timeList ):
		"""再次随机"""
		temp = {}
		for time in timeList:
			temp[time] = self._prayPoolCfg["prayTime"][time]
		total = sum(temp.values())
		randNum = random.randrange(0, total)
		for time in sorted(timeList):
			if temp[time] >= randNum:
				return time
			randNum -= temp[time]
		
	def getJadeMaxLevel( self ):
		"""玲珑玉令最大等级"""
		return max( self._jadeCommonedCfg )
		
	def getJadeCfg( self, level ):
		"""玲珑玉令升级消耗"""
		return self._jadeCommonedCfg.get(level, None)
		
	def getComposeSuccessRate( self, level ):
		"""获取额外成功率"""
		if level in self._forgeRateCfg:
			return self._forgeRateCfg[level]["successRate"] / 100
		return 0
		
	def getComposeGreenEquipSuccessRate( self, type, buildLevel ):
		"""获取打造绿装叠加的成功率"""
		if buildLevel in self._forgeRateCfg:
			if type == csdefine.SPACE_TYPE_PRIVATE:
				return self._forgeRateCfg[buildLevel]["df_SumSuccessRate"] / 100
			elif type == csdefine.SPACE_TYPE_PUBLIC:
				return self._forgeRateCfg[buildLevel]["xf_SumSuccessRate"] / 100
			elif type == csdefine.SPACE_TYPE_HIGH_DF:
				return self._forgeRateCfg[buildLevel]["gjdf_SumSuccessRate"] / 100
		return 0
		
	def getSalaryInterval(self, level):
		"""获取领取俸禄间隔"""
		if level in self._jadeCommonedCfg:
			return self._jadeCommonedCfg[level]["salaryInterval"] * 24 * 3600			# 单位是天
		return 0
		
	def getSalary(self, level):
		"""获取俸禄"""
		if level in self._jadeCommonedCfg:
			return self._jadeCommonedCfg[level]["salary"]
		return 0

#玩家的基础属性值
class RolePropertyValueCfg(Singleton.Singleton ):
	def __init__(self):
		"""
		字典的key为{profession: {level:{propertyID: value}}}
		"""
		self._datas = EntityProperty.RoleBaseProperty.Datas

	def getData(self, profession, level):
		"""
		获取职业所在等级的基础属性值
		"""
		return self._datas[profession][level]

#幻兽的基础属性值
class PetPropertyValueCfg(Singleton.Singleton ):
	def __init__(self):
		"""
		字典的key为{profession: {level:{propertyID: value}}}
		"""
		self._datas = EntityProperty.PetBaseProperty.Datas

	def getData(self, profession, level):
		"""
		获取职业所在等级的基础属性值
		"""
		return self._datas[profession][level]

#怪物的基础属性
class MonsterPropertyValueCfg(Singleton.Singleton ):
	def __init__(self):
		"""
		字典的key为{profession: {level:{propertyID: value}}}
		"""
		self._datas = EntityProperty.MonsterBaseProperty.Datas

	def getData(self, profession, attrlevel, level):
		"""
		获取职业所在等级强度所在等级的基础属性值
		"""
		return self._datas[profession][attrlevel][level]


#属性兑换配置
class PropertyExchangeCfg( Singleton.Singleton ):
	def __init__(self):
		self._datas = EntityProperty.PropertyExchangeCfg.Datas

	def getData(self, profession, propertyID):
		"""
		获取属性的兑换配置
		"""
		if propertyID not in self._datas[profession]:
			return {}
		return self._datas[profession][propertyID]

#心法影响属性兑换配置
class SkillPostureExchangeCfg( Singleton.Singleton ):
	def __init__(self):
		self._datas = EntityProperty.SkillPostureExchangeCfg.Datas

	def getData(self, skillPosture, propertyID):
		"""
		获取属性的兑换配置
		"""
		if skillPosture not in self._datas:
			return {}
		if propertyID not in self._datas[skillPosture]:
			return {}
		return self._datas[skillPosture][propertyID]

#标准伤害计算
class CombatNormalDamager( Singleton.Singleton ):
	def __init__( self ):
		self._datas = EntityProperty.CombatDamager.Datas
		
	def getBaseCombatData( self, level, profession ):
		"""
		获取基准伤害值
		"""
		if level in self._datas and profession in self._datas[level]:
			return self._datas[level][profession]
		return {}

#副本英雄联盟怪物的1阶基础属性
class SpaceCopyYXLMMonsterPropertyValueCfg_1( Singleton.Singleton ):
	def __init__(self):
		"""
		字典的key为{profession: {level:{propertyID: value}}}
		"""
		self._datas = EntityProperty.YXLMMonsterBaseProperty_1.Datas

	def getData(self, profession, attrlevel, level):
		"""
		获取职业所在等级强度所在等级的基础属性值
		"""
		return self._datas[profession][attrlevel][level]

#副本英雄联盟怪物的2阶基础属性
class SpaceCopyYXLMMonsterPropertyValueCfg_2( Singleton.Singleton ):
	def __init__(self):
		"""
		字典的key为{profession: {level:{propertyID: value}}}
		"""
		self._datas = EntityProperty.YXLMMonsterBaseProperty_2.Datas

	def getData(self, profession, attrlevel, level):
		"""
		获取职业所在等级强度所在等级的基础属性值
		"""
		return self._datas[profession][attrlevel][level]

#副本英雄联盟怪物的3阶基础属性
class SpaceCopyYXLMMonsterPropertyValueCfg_3( Singleton.Singleton ):
	def __init__(self):
		"""
		字典的key为{profession: {level:{propertyID: value}}}
		"""
		self._datas = EntityProperty.YXLMMonsterBaseProperty_3.Datas

	def getData(self, profession, attrlevel, level):
		"""
		获取职业所在等级强度所在等级的基础属性值
		"""
		return self._datas[profession][attrlevel][level]

g_EquipPropertyTypeExp = EquipPropertyTypeExp()
g_EquipPropertyValueExp = EquipPropertyValueExp()
g_equipIntensify = EquipIntensifyExp()
g_EquipReSet = EquipPropertyReSet()
g_EquipCompose = EquipComposeCfg()

g_ToolCompose = ToolComposeCfg()

g_RolePropertyValueCfg = RolePropertyValueCfg()
g_PetPropertyValueCfg = PetPropertyValueCfg()
g_MonsterPropertyValueCfg = MonsterPropertyValueCfg()
g_PropertyExchangeCfg = PropertyExchangeCfg()
g_SkillPostureExchangeCfg = SkillPostureExchangeCfg()
g_CombatNormalDamager = CombatNormalDamager()
g_SpaceCopyYXLMMonsterPropertyValueCfg_1 = SpaceCopyYXLMMonsterPropertyValueCfg_1()
g_SpaceCopyYXLMMonsterPropertyValueCfg_2 = SpaceCopyYXLMMonsterPropertyValueCfg_2()
g_SpaceCopyYXLMMonsterPropertyValueCfg_3 = SpaceCopyYXLMMonsterPropertyValueCfg_3()

