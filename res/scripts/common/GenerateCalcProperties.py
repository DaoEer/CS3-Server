#-*-coding:utf-8-*-

import sys
import os
import codecs
import copy
import ItemTypeEnum

#-----------------未出战幻兽数据备份-------------------------------------------------
# 一级属性
BAK_VPET_ONE_PROPERTY = [ "corporeity", "strength", "intellect", "discern", "dexterity", ]
# 二级属性
BAK_VPET_TWO_PROPERTY = [ "HP_Max", "MP_Max", "damage", "magic_damage", "armor", "magic_armor", "criticalstrike",\
						"parry", "speed", "hitrate", "dodgerate", "gangQiValue_Max", "gangQi_damagePoint", "gangQi_armorPoint",\
						"combatPower","cure", "ice_damage", "fire_damage", "thunder_damage", "xuan_damage", "ice_armor",\
						"fire_armor", "thunder_armor", "xuan_armor", "damage_ignore", "magic_damage_ignore", "armor_ignore",\
						"magic_armor_ignore", "criticalstrike_ignore", "parry_ignore", "hitrate_ignore", "dodgerate_ignore",\
						"ice_damage_ignore", "fire_damage_ignore", "thunder_damage_ignore", "xuan_damage_ignore", "ice_armor_ignore",\
						"fire_armor_ignore", "thunder_armor_ignore", "xuan_armor_ignore", "depress_resist", "hitback_resist",\
						"control_resist", "insane_resist" ]

# 幻兽客户端数据
BAK_VPET_SENT_TO_CLIENT_DATAS = ["uid", "scriptID", "step", "exp", "quality", "name", "ability", "ability_Max", "attrSkillBox",\
			 					"HP", "MP", "sleepTime", "noLearnedSkillBox", "passiveSkillBox", "gangQiValue" ]
BAK_VPET_SENT_TO_CLIENT_DATAS.extend( BAK_VPET_ONE_PROPERTY )
BAK_VPET_SENT_TO_CLIENT_DATAS.extend( BAK_VPET_TWO_PROPERTY )

# 幻兽Cell数据
BAK_VPET_SENT_TO_CLELL_DATAS = ["uid", "scriptID", "step", "exp", "quality", "sleepTime", "name"]
#-------------------------------------------------------------------------------------

# 用来生成CalcProperties文件

PATH = sys.path[0]+ "/CalcProperties.py"

data = \
"# -*- coding: utf-8 -*-\n\n\
import ItemSystemExp\n\
import ItemTypeEnum\n\n\n\n\
def calcProperty( baseVal, extraVal, percentVal, value ):\n\
\treturn ( baseVal + extraVal ) * ( 1 + percentVal/ItemTypeEnum.PRECENTRATIO ) + value\n\n\
class CalcProperties:\n\
\tdef __init__( self ):\n\
\t\tpass\n\n"

def setRoleBaseProperties():
	#重新设置基础属性值, xxx_base
	global data
	data += "\n\tdef setRoleBaseProperties(self):\n"
	template = \
	"\t\tself.xxx_base = int(self.getBaseProperties().get(yyy, 0))\n"
	for key, value in ItemTypeEnum.PROPERTYIDTOSTR.items():
		temp = template.replace("yyy", str(key)).replace("xxx", value)
		data += temp

def setMonsterBaseProperties():
	#重新设置基础属性值, xxx_base
	global data
	data += "\n\tdef setMonsterBaseProperties(self):\n"
	template = \
	"\t\tvv = int(self.getBaseProperties().get(yyy, 0))\n\
		self.xxx_base = self.getBasicValue(yyy,vv)\n\n"
	for key, value in ItemTypeEnum.PROPERTYIDTOSTR.items():
		temp = template.replace("yyy", str(key)).replace("xxx", value)
		data += temp

def setVehiclePetBaseProperties():
	#重新设置基础属性值, xxx_base
	global data
	data += "\n\tdef setVehiclePetBaseProperties(self):\n"
	template = "\t\tself.xxx_base = int(self.getBaseProperties().get(yyy, 0))\n"
	for key, value in ItemTypeEnum.PROPERTYIDTOSTR.items():
		temp = template.replace("yyy", str(key)).replace("xxx", value)
		data += temp

def setRoleExtraProperties():
	#计算属性的成长值，xxx_extra
	global data
	data += "\n\tdef setRoleExtraProperties(self, dic):\n"
	template = \
	"\t\tvv = int( dic.get(yyy, 0) )\n\
		self.xxx_extra = vv + self.getXiuweiExtraProperties(yyy)\n"
	for key, value in ItemTypeEnum.PROPERTYIDTOSTR.items():
		temp = template.replace("yyy", str(key)).replace("xxx", value)
		data += temp

def setMonsterExtraProperties():
	#计算属性的成长值，xxx_extra
	global data
	data += "\n\tdef setMonsterExtraProperties(self, dic):\n"
	template = "\t\tself.xxx_extra = int( dic.get(yyy, 0) )\n"
	for key, value in ItemTypeEnum.PROPERTYIDTOSTR.items():
		temp = template.replace("yyy", str(key)).replace("xxx", value)
		data += temp

def setVehiclePetExtraProperties():
	#计算属性的成长值，xxx_extra
	global data
	data += "\n\tdef setVehiclePetExtraProperties(self, dic):\n"
	template = "\t\tself.xxx_extra = int( dic.get(yyy, 0) )\n"
	for key, value in ItemTypeEnum.PROPERTYIDTOSTR.items():
		temp = template.replace("yyy", str(key)).replace("xxx", value)
		data += temp

def setPrecentProperties():
	#计算属性的增长百分比， xxx_precent
	global data
	data += "\n\tdef setPrecentProperties(self, dic):\n"
	template = "\t\tself.xxx_percent = dic.get(yyy, 0)\n"
	for key, value in ItemTypeEnum.PROPERTYIDTOSTR.items():
		temp = template.replace("yyy", str(key)).replace("xxx", value)
		data += temp

def setValueProperties():
	#计算属性附加值， xxx_value
	global data
	data += "\n\tdef setValueProperties(self, dic):\n"
	template = "\t\tself.xxx_value = dic.get(yyy, 0)\n"
	for key, value in ItemTypeEnum.PROPERTYIDTOSTR.items():
		temp = template.replace("yyy", str(key)).replace("xxx", value)
		data += temp

def setLVOneProperties():
	#重新计算一级属性
	global data
	data += "\n\tdef setLVOneProperties(self):\n"
	template = \
	"\t\tbasevalue =  self.getBaseResultPropertyValue( self.xxx_base)\n\
		extravalue = self.getExtraResultPropertyValue( self.xxx_extra )\n\
		precentvalue = self.getPrecentResultPropertyValue( self.xxx_percent )\n\
		vvalue = self.getValueResultPropertyValue( self.xxx_value)\n\
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)\n\
		result = int(self.getResultPropertyValue( result ))\n\
		if self.xxx != int(result):\n\
			self.xxx = int(result)\n\n"
	List = [ItemTypeEnum.PROPERTYIDTOSTR[i] for i in ItemTypeEnum.ONEPROPERTIES]
	for value in List:
		temp = template.replace("xxx", value)
		data += temp

def setLVTwoProperties():
	# 重新计算二级属性
	global data
	data += "\n\tdef setLVTwoProperties(self ):\n"
	data += '\t\tList = ["HP_Max", "MP_Max", "gangQiValue_Max", "damage", "magic_damage", "cure"]\n'
	template = \
	'\t\tbasevalue =  self.getBaseResultPropertyValue( self.xxx_base )\n\
		extravalue = self.getExtraResultPropertyValue( self.xxx_extra )\n\
		precentvalue = self.getPrecentResultPropertyValue( self.xxx_percent )\n\
		vvalue = self.getValueResultPropertyValue( self.xxx_value )\n\
		extravalue += self.getExchangeTwoPropertyValue(yyy)	#把兑换值加在成长值中\n\
		self.xxx_extra = int(extravalue)\n\
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)\n\
		if ItemTypeEnum.PROPERTYIDTOSTR[yyy] in List:\n\
			result = max(result, 1)\n\
		result = int(self.getResultPropertyValue( result ))\n\
		if self.xxx != int( result ):\n\
			self.xxx = int( result )\n\n'
	List = [ItemTypeEnum.PROPERTYIDTOSTR[i] for i in ItemTypeEnum.TWOPROPETYTIES]
	k = 0
	for value in List:
		temp = template.replace("yyy", str(ItemTypeEnum.TWOPROPETYTIES[k])).replace("xxx", value)
		k += 1
		data += temp

def getExchangeTwoProperty():
	#获取一级属性兑换的二级属性property的值
	global data
	data += "\n\tdef getExchangeTwoProperty(self, propertyID):\n"
	data +="\t\tresult = 0\n"
	template = \
	"\t\texchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, yyy).get(propertyID, 0)\n\
		result += (self.xxx * exchangeratio)\n\n"
	List = [ItemTypeEnum.PROPERTYIDTOSTR[i] for i in ItemTypeEnum.ONEPROPERTIES]
	k = 0
	for value in List:	
		temp = template.replace("yyy", str(ItemTypeEnum.ONEPROPERTIES[k])).replace("xxx", value)
		k += 1
		data += temp
	data += "\n\t\treturn result\n\n"

def getRoleExchangeTwoProperty():
	#获取玩家一级属性兑换的二级属性property的值
	global data
	data += "\n\tdef getRoleExchangeTwoProperty(self, propertyID):\n"
	data +="\t\tresult = 0\n"
	template = \
	"\t\texchangeratio = ItemSystemExp.g_PropertyExchangeCfg.getData(self.profession, yyy).get(propertyID, 0)\n\
		exchangeratio += ItemSystemExp.g_SkillPostureExchangeCfg.getData(self.skillPosture, yyy).get(propertyID, 0)\n\
		result += (self.xxx * exchangeratio)\n\n"
	List = [ItemTypeEnum.PROPERTYIDTOSTR[i] for i in ItemTypeEnum.ONEPROPERTIES]
	k = 0
	for value in List:	
		temp = template.replace("yyy", str(ItemTypeEnum.ONEPROPERTIES[k])).replace("xxx", value)
		k += 1
		data += temp
	data += "\n\t\treturn result\n\n"

def getRolePropertyFactor():
	#计算玩家战斗力价值
	global data
	data += "\n\tdef getRolePropertyFactor(self):\n"
	data +="\t\tM1 = 0.0\n"
	template = "\t\tM1 += self.xxx * yyy\n"
	Dict = {}
	for key, value in ItemTypeEnum.PROPERTY_FACTOR.items():
		Dict[ItemTypeEnum.PROPERTYIDTOSTR[key]] = value
	for key, value in Dict.items():
		temp = template.replace("yyy", str(value)).replace("xxx", key )
		data += temp
	data += "\n\t\treturn M1\n"

def getProfessionCorrectoin():
	#计算战斗力修正
	global data
	data += "\n\tdef getProfessionCorrectoin(self):\n"
	
	template = "\t\tMzzz += self.xxx * yyy\n"
	Dict = "\t\treturn {\n"
	for key, value in ItemTypeEnum.PROFESSION_CORRECTION_FACTOR.items():
		data +="\t\tM" +str(key)+ "= 0.0\n"
		for k, v in value.items():
			temp = template.replace("yyy", str(v)).replace("zzz", str(key) ).replace("xxx", k )
			data += temp
		a = str(key)
		b = "M" +str(key)
		Dict += "\t\t\t" + a + " : " + b + ",\n"
	Dict += "\t\t\t}\n\n"
	data += Dict

def getVehiclePetPropertyFactor():
	#计算幻兽战斗力价值
	global data
	data += "\n\tdef getVehiclePetPropertyFactor(self, correct):\n"
	data +=\
	"\t\tM1 = 0.0\n\
	\tabilityList = ['corporeity', 'strength', 'intellect', 'discern', 'dexterity']\n"
	template = \
	"\t\tability = 1\n\
	\tif 'xxx' in abilityList:\n\
	\t\tability = correct\n\
	\tM1 += self.xxx * yyy * ability\n\n"
	Dict = {}
	for key, value in ItemTypeEnum.PROPERTY_FACTOR.items():
		Dict[ItemTypeEnum.PROPERTYIDTOSTR[key]] = value
	for key, value in Dict.items():
		temp = template.replace("yyy", str(value)).replace("xxx", key )
		data += temp
	data += "\t\treturn M1\n"

def setPetBaseLVOneProperties():
	#重新计算幻兽base一级属性
	global data
	data += "\n\tdef setPetBaseLVOneProperties(self, propertiesDict):\n"
	template = \
	'\t\tbasevalue =  propertiesDict[ "xxx_base" ]\n\
		extravalue = propertiesDict[ "xxx_extra" ]\n\
		precentvalue = propertiesDict[ "xxx_percent" ]\n\
		vvalue = propertiesDict[ "xxx_value" ]\n\
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)\n\
		result = int(self.getResultPropertyValue( result ))\n\
		propertiesDict.update( { "xxx" : result } )\n\
		if "xxx" in BAK_VPET_ONE_PROPERTY:\n\
			self.xxx = result\n\n'
	List = [ItemTypeEnum.PROPERTYIDTOSTR[i] for i in ItemTypeEnum.ONEPROPERTIES]
	for value in List:
		temp = template.replace("xxx", value).replace("BAK_VPET_ONE_PROPERTY", str(BAK_VPET_ONE_PROPERTY))
		data += temp
	data += "\t\treturn propertiesDict\n"

def setPetBaseLVTwoProperties():
	# 重新计算幻兽Base二级属性
	global data
	data += "\n\tdef setPetBaseLVTwoProperties(self, propertiesDict):\n"
	template = \
	'\t\tbasevalue =  propertiesDict[ "xxx_base" ]\n\
		extravalue = propertiesDict[ "xxx_extra" ]\n\
		precentvalue = propertiesDict[ "xxx_percent" ]\n\
		vvalue = propertiesDict[ "xxx_value" ]\n\
		extravalue += self.getExchangeTwoPropertyValue(yyy) #把兑换值加在成长值中\n\
		propertiesDict[ "xxx_extra" ] = int(extravalue)\n\
		result = calcProperty(basevalue, extravalue, precentvalue, vvalue)\n\
		if "xxx" == "HP_Max":\n\
			result = max(result, 1)\n\
		result = int(self.getResultPropertyValue( result ))\n\
		propertiesDict["xxx"] = result\n\
		if "xxx" in BAK_VPET_TWO_PROPERTY:\n\
			self.xxx = result\n\n'
	List = [ItemTypeEnum.PROPERTYIDTOSTR[i] for i in ItemTypeEnum.TWOPROPETYTIES]
	k = 0
	for value in List:
		temp = template.replace("yyy", str(ItemTypeEnum.TWOPROPETYTIES[k])).replace("xxx", value).replace("BAK_VPET_TWO_PROPERTY",str(BAK_VPET_TWO_PROPERTY))
		k += 1
		data += temp
	data += "\t\treturn propertiesDict\n"

def onPetStepChangeSetProperties():
	#幻兽升阶时更新属性
	global data
	data += "\n\tdef onPetStepChangeSetProperties(self):\n"
	template = '\t\tself.updatePetEpitomeDatas( "xxx", self.xxx )\n'
	List = []
	List.extend( BAK_VPET_ONE_PROPERTY )
	List.extend( BAK_VPET_TWO_PROPERTY )
	for value in List:
		temp = template.replace("xxx", value)
		data += temp

def onOriginPetStepChangeSetProperties():
	#幻兽原兽升阶时更新属性
	global data
	data += "\n\tdef onOriginPetStepChangeSetProperties(self, playerMB):\n"
	template = '\t\tself.updateOriginPetEpitomeDatas( playerMB, "xxx", self.xxx )\n'
	List = []
	List.extend( BAK_VPET_ONE_PROPERTY )
	List.extend( BAK_VPET_TWO_PROPERTY )
	for value in List:
		temp = template.replace("xxx", value)
		data += temp

def pickPetDataForClient():
	#打包幻兽发给客户端数据
	global data
	data += "\n\tdef pickPetDataForClient(self, data):\n"
	template = '\t\tdata["xxx"] = self.xxx\n'
	List = copy.deepcopy(BAK_VPET_SENT_TO_CLIENT_DATAS)
	for i in ["uid", "attrSkillBox", "passiveSkillBox", "noLearnedSkillBox"]:
		List.remove(i)	
	for value in List:
		temp = template.replace("xxx", value)
		data += temp
	data += "\t\treturn data\n"

def pickPetDataForCell():
	#打包幻兽发给cell数据
	global data
	data += "\n\tdef pickPetDataForCell(self, pet ):\n"
	template = '\t\tpet.xxx = self.xxx\n'
	for value in BAK_VPET_SENT_TO_CLELL_DATAS:
		temp = template.replace("xxx", value)
		data += temp
	data += "\t\treturn pet\n"

def getEffectProperty():
	#打包幻兽发给cell数据
	global data
	data += "\ndef getEffectProperty(receiver):\n"
	data += "\tdata={}\n"
	template = \
	'\tdata.update({"xxx": receiver.xxx})\n\
	data.update({"xxx_base": receiver.xxx_base})\n\
	data.update({"xxx_extra": receiver.xxx_extra})\n\
	data.update({"xxx_percent": receiver.xxx_percent})\n\
	data.update({"xxx_value": receiver.xxx_value})\n\n'
	for key, value in ItemTypeEnum.PROPERTYIDTOSTR.items():
		temp = template.replace("xxx", value)
		data += temp
	data += "\treturn data\n"

setRoleBaseProperties()
setMonsterBaseProperties()
setVehiclePetBaseProperties()
setRoleExtraProperties()
setMonsterExtraProperties()
setVehiclePetExtraProperties()
setPrecentProperties()
setValueProperties()
setLVOneProperties()
setLVTwoProperties()
getExchangeTwoProperty()
getRoleExchangeTwoProperty()
getRolePropertyFactor()
getProfessionCorrectoin()
getVehiclePetPropertyFactor()
setPetBaseLVOneProperties()
setPetBaseLVTwoProperties()
onPetStepChangeSetProperties()
onOriginPetStepChangeSetProperties()
pickPetDataForClient()
pickPetDataForCell()
getEffectProperty()

fp = codecs.open(PATH, "w", "utf-8")

fp.write(data)
fp.close()