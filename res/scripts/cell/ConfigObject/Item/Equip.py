# -*- coding: utf-8 -*-

import KBEDebug
import ItemTypeEnum
import ConfigObject.Item.ItemUse as ItemUse
from ItemSystemExp import g_equipIntensify
import Functions
import csdefine
import time
import csstatus
from EquipPropertyParse import g_EquipPropertyLoadInst
from ItemSystemExp import g_EquipPropertyTypeExp
from ItemSystemExp import g_EquipPropertyValueExp
import ItemSystemExp

class Equip(ItemUse.ItemUse):
	"""
	装备基类
	"""
	def __init__(self, srcData):
		"""
		"""
		ItemUse.ItemUse.__init__(self, srcData)
		self.modelSources = {}
		Param1 = srcData["Param1"].split(";")	#装备模型编号
		self.modelSources[1] = Param1[0]
		if len(Param1) == 1:
			self.modelSources[2] = Param1[0]
		elif len(Param1) > 1:
			self.modelSources[2] = Param1[1]

		param2 = srcData.get("Param2")
		if param2 != "":
			param2 = int(param2)
		attackProperties = g_EquipPropertyLoadInst.getDataByID(param2)		#基础属性（不随机）
		param3 = srcData.get("Param3")
		if param3 != "":
			param3 = int(param3)
		bornProperties = g_EquipPropertyLoadInst.getDataByID(param3)					#附加属性（可配置或随机）
		self.dynamicData["hardiness"] = self.getHardinessMax()
		self.goldStar = 0
		self.silverStar = 0
		self.copperStar = 0
		self.ironStar = 0
		if srcData.get("Param4"):
			param4 = srcData.get("Param4").split("|")
			self.goldStar = int(param4[0])
			self.silverStar = int(param4[1])
			self.copperStar = int(param4[2])
			self.ironStar = int(param4[3])
		#在属性更新时也需要更新self.dynamicData字典
		self.dynamicData.update({
						   "attackPropertiesStr": self.dictToStr(self.getEffectProperties(attackProperties)),
						   "attachPropertiesStr": self.dictToStr(bornProperties),
						   "intensifyDataStr": "",#强化数据
			})
		
	def loadDynamicData( self, params ):
		"""加载动态数据"""
		ItemUse.ItemUse.loadDynamicData( self, params )
		self.createCustomIntensifyEquip()
		if self.isCreateAttachProperties():
			self.createAttachProperties()
		else:
			self.calculateCombatPower()

	def checkUse(self, owner):
		"""
		使用前检测
		"""
		if not self.checkUseBySpace( owner ):
			return csstatus.EQUIP_WIELD_FORBID_BY_SPACE
		if owner.isState(csdefine.ENTITY_STATE_FIGHT):
			return csstatus.CAN_NOT_EQUIP_IN_COMBAT
		return csstatus.ITEM_USE_GO_ON_MSG

	def use(self, owner, target):
		"""
		使用
		"""
		dstorder = self.getWieldOrder(owner)
		owner.CELL_swapItem(owner.id, self.order, dstorder)
		return csstatus.ITEM_USE_GO_ON_MSG

	def onWield(self, owner):
		"""
		装备完成
		"""
		pass

	def onUnWield(self, owner):
		"""
		卸下道具完成
		"""
		pass

	def calculateCombatPower( self ):
		"""计算装备战斗力"""
		attachStrDict = self.getAttachPropertyDict()
		combatPower = 0
		for attachDict in attachStrDict.values():
			for propertyID, property in attachDict.items():
				if propertyID in ItemTypeEnum.PROPERTYIDTOPOWNER:
					combatPower += property * ItemTypeEnum.PROPERTYIDTOPOWNER[propertyID]
		self.dynamicData["combatPower"] = round( combatPower / 50 )
		
	def getHoldEffectIDList( self ):
		"""
		获得持有效果列表
		"""
		holdEffectIDStr = self.getItemDir("HoldEffectID","")
		temp =[]
		if holdEffectIDStr:
			temp = [int(i) for i in holdEffectIDStr.split("|")] #持有效果的ID列表
		return temp
		
	def parseIntensifyDatas(self, datastr):
		"""
		强化数据解析
		"""
		result = {}
		if (datastr == ""): 	return result
		if "||" in datastr:
			items = datastr.split("||")
			for item in items:
				left, right = item.split("$")
				uid = int(left.split("*")[0])
				starlv = int(left.split("*")[1])
				propertystr = right
				result.update({uid : (starlv, propertystr)})
		else:
			left, right = datastr.split("$")
			uid = int(left.split("*")[0])
			starlv = int(left.split("*")[1])
			propertystr = right
			result.update({uid : (starlv, propertystr)})
		return result

	def getIntensifyDict(self):
		"""
		获取强化属性字典
		"""
		tempdic = self.parseIntensifyDatas(self.dynamicData["intensifyDataStr"])
		mainproperties = {}
		attachproperties = {}
		result = {"_extra":{}, "_base":{}, "_percent":{}, "_value":{}}
		base = self.strToDict(self.dynamicData[ "attackPropertiesStr" ])
		for key, value in tempdic.items():
			propertyStr = value[1].split(":")
			main = propertyStr[0]
			attach = ""
			if len( propertyStr ) >= 2:
				attach = propertyStr[1]
			maindict = self.strToDict(main)
			maincalcdict = {}
			for mainID, mainPer in maindict.items():
				mainValue = int( (mainPer / 100 ) * base[mainID] )
				maincalcdict.update( { mainID : mainValue } )
			mainproperties = ItemSystemExp.combineDict(mainproperties, maincalcdict)
			attachdict = self.strToDict(attach)
			attachproperties = ItemSystemExp.combineDict(attachproperties, attachdict)	
		# result["_percent"].update(mainproperties)
		attachproperties = ItemSystemExp.combineDict(attachproperties, mainproperties)
		result["_extra"].update(attachproperties)
		return result

	def getAttachPropertyDict(self):
		"""
		获取装备属性
		"""
		base = self.strToDict(self.dynamicData[ "attackPropertiesStr" ])
		extra = self.strToDict(self.dynamicData[ "attachPropertiesStr" ])
		#附加属性
		combine = ItemSystemExp.combineDict(base, extra)
		#强化属性
		intensifydict = self.getIntensifyDict()["_extra"]
		combine = ItemSystemExp.combineDict(combine, intensifydict)
		# 解析复合属性
		compositionDic = {}
		for propertytype in list(combine.keys()):
			if propertytype in ItemTypeEnum.COMPOSITIONPROPERTIES:		
				for element in ItemTypeEnum.COMPOSITIONPROPERTIES[propertytype]:
					compositionDic.update({element: combine[propertytype]})
				combine.pop(propertytype, None)
		combine = ItemSystemExp.combineDict(combine, compositionDic)
		result = {"_extra":{}, "_base":{}, "_percent":{}, "_value":{}}
		result["_extra"].update(combine)
		return result

	def strToPropertyDict(self, dictstr):
		"""
		把保存的属性（包括复合属性）字符串转换为dict
		"""
		result = {}
		compositionDic = {}
		if dictstr == "": return result
		for item in dictstr.split("|"):
			propertytype = int(item.split("#")[0])
			value = int(item.split("#")[1])
			if propertytype in ItemTypeEnum.COMPOSITIONPROPERTIES:			
				for element in ItemTypeEnum.COMPOSITIONPROPERTIES[propertytype]:
					compositionDic.update({element: value})				
				continue
			result.update({propertytype: value})
		return ItemSystemExp.combineDict(result, compositionDic)

	def intensifyDictToStr(self, dic):
		"""
		强化数据转换为字符串
		{uid:(starlv, PropertyStr)}, propertystr = 30001#10|20001#20|40001#30
		"""
		temp = ""
		for uid, value in dic.items():
			temp += (str(uid) + "*" + str(value[0]) + "$" + str(value[1]) + "||")
		if temp.endswith("||"):
			temp = temp[:-2]
		return temp

	def getEquipProperty(self, strdict, propertyID):
		"""
		获取装备的天生属性或附加属性
		dict:装备属性来源，只处只能是attackProperties或attachProperties
		propertyID: 属性配置的ID，在common/ItemTypeEnum.py#属性编号定义
		"""
		dic = self.strToDict(strdict)
		return dic.get(propertyID, 0)

	def createCustomIntensifyEquip( self ):
		"""配置的强化属性"""
		if self.goldStar or self.silverStar or self.copperStar or self.ironStar:
			if self.dynamicData["intensifyDataStr"] == "":
				intensifyLevel = self.goldStar + self.silverStar + self.copperStar + self.ironStar
				if intensifyLevel > g_equipIntensify.getMaxIntensifyLv( self.getLevel() ):
					KBEDebug.ERROR_MSG("Equip(%d) Param4(%s) is err!!"%( self.id, self.getItemDir("Param4") ))
					return
				
				intensifyResults = g_equipIntensify.getCustomIntensifResult( self, self.goldStar, self.silverStar, self.copperStar, self.ironStar )
				self.addIntensifyLevels( None, intensifyResults )

	def isCreateAttachProperties(self):
		"""
		装备是否要创建随机属性
		"""
		return not self.isWhite() and (self.dynamicData["attachPropertiesStr"] == "")
	
	def createAttachProperties(self):
		"""
		创建非白装的随机属性
		"""
		if self.dynamicData["attachPropertiesStr"] != "":	# 已经计算过了
			self.calculateCombatPower()
			return
		num = min(self.getQuality() , 5)	#最多5条属性
		level = self.getLevel()
		professsion = self.getReqClass()
		modelpart = self.getEquipPart()
		TypeList = g_EquipPropertyTypeExp.getNPropertyTypes(level, professsion, modelpart, num)
		temp = {}
		for propertyID in TypeList:
			value = g_EquipPropertyValueExp.getPropertyValue(level, professsion, modelpart, propertyID)
			temp.update({propertyID: value})
		
		self.dynamicData.update({"attachPropertiesStr": self.dictToStr(temp)})
		self.calculateCombatPower()

	def getClientTipDynamicProperty( self ):
		"""获取客户端显示的动态数据"""
		property = {}
		propertyName = ["combatPower", "attachPropertiesStr", "attackPropertiesStr", "intensifyDataStr","hardiness"]
		for name in propertyName:
			property[name] = self.dynamicData[name]
		if "Quality" in self.dynamicData:
			property["Quality"] = self.dynamicData["Quality"]
		return property
	
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
				
	def strToDict(self, dictstr):
		"""
		把保存的属性字符串转换为dict
		"""
		result = {}
		if dictstr == "": return result
		for item in dictstr.split("|"):
			propertytype = int(item.split("#")[0])
			value = int(item.split("#")[1])
			result.update({propertytype: value})
		return result

	def getReqClass( self ):
		"""获取相关职业"""
		# 如果配置了多个职业，则计算装备属性的生成用0计算
		reqClass = [int(item) for item in self.getItemDir("ReqClasses").split("|")]
		if reqClass[0] and len(reqClass) == 1:
			return reqClass[0]
		return 0

	def checkReqClasses(self, owner):
		"""
		检测装备职业
		"""
		reqClass = self.getItemDir("ReqClasses")
		if reqClass:
			return str(owner.getProfession()) in reqClass.split("|")
		# 如果没有配置，说明多个职业匹配
		return True

	def checkReqGender(self, owner):
		"""
		检测装备性别
		"""
		return True

	def canWield(self, owner):
		"""
		能否装备
		"""
		if owner.actionForbidSign( csdefine.ACTION_FORBID_USE_ITEM ):
			return False
		if owner.actionForbidSign( csdefine.ACTION_FORBID_WIELD ):
			return False
		if not self.checkReqLevel(owner):	return False
		if not self.checkReqClasses(owner): return False
		if not self.checkReqGender(owner):	return False
		if not self.checkHardiness():
			owner.statusMessage( csstatus.ITEM_USE_HARDINESS_ZERO, "" )
			return False
		return True

	def wield(self, owner):
		"""
		装备道具
		@param update:卸载模型是否生效
		@type update: bool
		"""
		if not self.canWield(owner):	
			return False
			
		if self.getItemDir("BindType")  == ItemTypeEnum.EQUIP_BIND:
			self.setBindType(owner, ItemTypeEnum.BINDED_STATE)
		
		owner.onEquipWieldCb(self)
		return True

	def unWield( self, owner ):
		"""
		卸下道具
		@param update:卸载模型是否生效
		@type update: bool
		"""
		owner.onEquipUnWieldCb(self)

	def getEquipPart(self):
		"""
		获取装备部位
		"""
		return 0
	
	def isEquip( self ):
		"""
		判断是否是装备
		"""
		return True

	def getWieldOrder(self, player):
		"""
		获取装备的ItemOrder
		"""
		#非戒指部位
		if self.getEquipPart() != ItemTypeEnum.EQUIP_RING:	
			return self.getEquipPart()
		#戒指部位
		return player.getFreeRingWieldOrder()

	def getHardiness( self ):
		"""
		获得装备当前耐久度
		"""
		return self.dynamicData.get("hardiness",0)

	def getHardinessMax( self ):
		"""
		获得装备最大耐久度
		"""
		if self.getEquipPart() in ItemTypeEnum.EQUIP_ALL_WEAPON:
			return int((self.getLevel() ** 1.2 * 20 + 20000) * 100 )
		elif self.getEquipPart() in ItemTypeEnum.EQUIP_ARMOR:
			return int((600000 * 1.5 ** (0.1 * self.getLevel() - 1)))
		else:
			return -1

	def addHardiness( self, hardiness, owner ):
		"""
		增加耐久度
		"""
		self.setHardiness( self.getHardiness() + hardiness,owner )

	def setHardiness( self, hardiness, owner):
		"""
		设置当前耐久度
		"""
		oldHardiness = self.getHardiness()
		hardiness = max( min( self.getHardinessMax(), hardiness ), 0 )
		if oldHardiness == hardiness:
			return
		self.dynamicData["hardiness"] = hardiness
		owner.updateOneDataToClient( "hardiness",self.getHardiness(),self )
		
		owner.onEquipHardinessChange( self, oldHardiness, hardiness )

	def checkHardiness( self ):
		"""
		检查当前耐久度
		"""
		hardinessMax = self.getHardinessMax()
		if hardinessMax is None or hardinessMax <= 0:
			return True
		return self.getHardiness() > 0

	def setReturnBackTime( self, time, owner ):
		"""
		设置可以退货时间
		"""
		self.dynamicData["returnBackTime"] = time
		owner.updateOneDataToClient( "returnBackTime",self.dynamicData["returnBackTime"],self )

	def checkCanReturnBack( self ):
		"""
		检查是否可以退货
		"""
		time = self.dynamicData.get("returnBackTime",0)
		if time > 0:
			if time.time() -time >= 0:
				self.dynamicData.pop( "returnBackTime" )
				return True
		return False
	
	#----------------------装备强化----------------------------
	def canIntensify( self ):
		"""
		判断装备是否能被强化
		"""
		maxIntensifyLv = g_equipIntensify.getMaxIntensifyLv(self.getLevel())
		if(self.getIntensifyLevel() >= maxIntensifyLv):	return False
		return True

	def getIntensifyLevel( self ):
		"""
		获取装备强化等级
		"""
		return len(self.parseIntensifyDatas(self.dynamicData["intensifyDataStr"]))

	def addIntensifyLevels( self, owner, intensifyResults ):
		"""
		增加强化等级（中括号表示可能有，也可能无）
		index * starlv $ mainID # mainPercent [|mainID # mainPercent ] : intensifyID # intensifyValue [| intensifyID # intensifyValue]
		"""
		temp = self.parseIntensifyDatas(self.dynamicData["intensifyDataStr"])
		index = 0
		for i in intensifyResults:
			if temp:
				index = max(temp) + 1
			temp[index] = i
		self.dynamicData["intensifyDataStr"] = self.intensifyDictToStr(temp)
		self.calculateCombatPower()
		if owner:
			owner.updateOneDataToClient("intensifyDataStr", self.dynamicData["intensifyDataStr"], self)
			owner.updateOneDataToClient("combatPower", self.dynamicData["combatPower"], self)

	def decIntensifyLevel( self, owner, saveUIDs ):
		"""
		减少强化等级（回火）
		"""
		temp = self.parseIntensifyDatas(self.dynamicData["intensifyDataStr"])
		for uid in list(temp.keys()):
			if str(uid) not in saveUIDs:
				temp.pop(uid)
		self.dynamicData["intensifyDataStr"] = self.intensifyDictToStr(temp)
		self.calculateCombatPower()
		owner.updateOneDataToClient("intensifyDataStr", self.dynamicData["intensifyDataStr"], self)
		owner.updateOneDataToClient("combatPower", self.dynamicData["combatPower"], self)

	def intensifyRestore( self, owner, intensifyResults ):
		"""
		强化属性还原
		"""
		self.dynamicData["intensifyDataStr"] = intensifyResults["intensifyDataStr"]
		self.calculateCombatPower()
		owner.updateOneDataToClient("intensifyDataStr", self.dynamicData["intensifyDataStr"], self)
		owner.updateOneDataToClient("combatPower", self.dynamicData["combatPower"], self)

	def replaceAttachPro( self, owner, newPro ):
		"""替换附加属性"""
		self.dynamicData["attachPropertiesStr"] = newPro
		self.calculateCombatPower()
		owner.updateOneDataToClient("attachPropertiesStr", self.dynamicData["attachPropertiesStr"], self )
		owner.updateOneDataToClient("combatPower", self.dynamicData["combatPower"], self )

	def onTransferIntensifyEquip( self, owner, newProDict, isBinded ):
		"""装备传星"""
		if isBinded and not self.isBinded(): self.setBindType(owner)
		self.dynamicData["intensifyDataStr"] = self.intensifyDictToStr( newProDict )
		self.calculateCombatPower()
		owner.updateOneDataToClient("intensifyDataStr", self.dynamicData["intensifyDataStr"], self )
		owner.updateOneDataToClient("combatPower", self.dynamicData["combatPower"], self )

	def getDynamicDataForClient(self, entity ):
		temp = {
			"hardiness": str(self.dynamicData["hardiness"]),
			"combatPower": str(self.dynamicData["combatPower"]),
			"attackProperties": self.dynamicData["attackPropertiesStr"],
			"attachProperties": self.dynamicData["attachPropertiesStr"],
			"intensifyData": self.dynamicData["intensifyDataStr"]
		}
		if "Quality" in self.dynamicData:
			temp["Quality"] = self.dynamicData["Quality"]
		return Functions.toJsonString( temp )
		
	def getQuality( self ):
		"""获取装备品质"""
		if "Quality" in self.dynamicData:
			return self.dynamicData["Quality"]
		return ItemUse.ItemUse.getQuality( self )
		
	def isKingEquip( self ):
		"""是否是 王道神兵"""
		return self.getQuality() == ItemTypeEnum.QUALITY_GREEN_SHEN
		
	def canBeKingCraft( self ):
		"""能否变为 王道神兵"""
		return g_equipIntensify.canBeKingcraft( self )
		
	def changeKingCraft( self, owner ):
		"""变成 王道神兵"""
		self.dynamicData["Quality"] = ItemTypeEnum.QUALITY_GREEN_SHEN
		# 修改附加属性
		attachDict = self.strToDict( self.dynamicData["attachPropertiesStr"] )
		level = self.getLevel()
		professsion = self.getReqClass()
		modelpart = self.getEquipPart()
		for pID in list( attachDict.keys() ):
			attachDict[pID] = g_EquipPropertyValueExp.getMaxPropertyValue(level, professsion, modelpart, pID)
		self.dynamicData["attachPropertiesStr"] = self.dictToStr( attachDict )
		# 修改强化属性
		intensifydict = self.parseIntensifyDatas(self.dynamicData["intensifyDataStr"])
		for index, intDatas in intensifydict.items():
			starLv, proDataStr = intDatas
			mainProStr = self.dictToStr( g_equipIntensify.getMainPropertyIDAndMaxValue( self, starLv))
			proDataStrList = proDataStr.split(":")
			if len( proDataStrList ) >= 2:
				intProStr = proDataStrList[1]
				intPro = self.strToDict( intProStr )
				for pID in list(intPro):
					intPro[pID] = g_EquipPropertyValueExp.getMaxIntensifyPropertyValue(level, professsion, modelpart, pID)
				intProStr = self.dictToStr( intPro )
				intensifydict[index] = ( starLv, mainProStr + ":" + intProStr )
			else:
				intensifydict[index] = ( starLv, mainProStr )
		self.dynamicData["intensifyDataStr"] = self.intensifyDictToStr( intensifydict )
		self.calculateCombatPower()
		owner.updateOneDataToClient("Quality", self.dynamicData["Quality"], self)
		owner.updateOneDataToClient("combatPower", self.dynamicData["combatPower"], self)
		owner.updateOneDataToClient("attachPropertiesStr", self.dynamicData["attachPropertiesStr"], self)
		owner.updateOneDataToClient("intensifyDataStr", self.dynamicData["intensifyDataStr"], self)