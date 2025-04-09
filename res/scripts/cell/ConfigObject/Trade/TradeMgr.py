# -*- coding: utf-8 -*-
import KBEngine
import csdefine
import KBEDebug
from LoadModule import *
from Singleton import Singleton

from ConfigObject.Trade.Condition.TradeConditionLevel import TradeConditionLevel
from ConfigObject.Trade.Condition.TradeConditionJingjieLevel import TradeConditionJingjieLevel
from ConfigObject.Trade.Condition.TradeConditionTongShopLevel import TradeConditionTongShopLevel
from ConfigObject.Trade.Condition.TradeConditionTongTitle import TradeConditionTongTitle
from ConfigObject.Trade.Condition.TradeConditionTongResearchSkill import TradeConditionTongResearchSkill
from ConfigObject.Trade.Condition.TradeConditionTongSmithyLevel import TradeConditionTongSmithyLevel
from ConfigObject.Trade.Condition.TradeConditionMilitaryRankLevel import TradeConditionMilitaryRankLevel
from ConfigObject.Trade.Condition.TradeConditionJadeItemLevel import TradeConditionJadeItemLevel

from ConfigObject.Trade.RoleTradeState.RoleTradeStateNull import RoleTradeStateNull
from ConfigObject.Trade.RoleTradeState.RoleTradeStateInvite import RoleTradeStateInvite
from ConfigObject.Trade.RoleTradeState.RoleTradeStateBegin import RoleTradeStateBegin
from ConfigObject.Trade.RoleTradeState.RoleTradeStateLock import RoleTradeStateLock
from ConfigObject.Trade.RoleTradeState.RoleTradeStateSure import RoleTradeStateSure
from ConfigObject.Trade.RoleTradeState.RoleTradeStateWait import RoleTradeStateWait
import csstatus


class TradeMgr( Singleton ):
	"""
	交易处理类
	"""
	def __init__( self ):
		self.conditionMap = {
			"level"				:	TradeConditionLevel(),
			"jingjieLevel"		:	TradeConditionJingjieLevel(),
			"tongShopLevel"		:	TradeConditionTongShopLevel(),
			"tongTitle"			:	TradeConditionTongTitle(),
			"researchSkillID"	:	TradeConditionTongResearchSkill(),
			"tongSmithyLevel"	:	TradeConditionTongSmithyLevel(),
			"militaryRankLevel" :	TradeConditionMilitaryRankLevel(),
			"jadeItemLevel"		:	TradeConditionJadeItemLevel(),
		}

		self.roleTradeStateMap = {
			csdefine.TRADE_STATE_NULL		:	RoleTradeStateNull( self ),
			csdefine.TRADE_STATE_INVITE		:	RoleTradeStateInvite( self ),
			csdefine.TRADE_STATE_WAIT       :	RoleTradeStateWait( self ),
			csdefine.TRADE_STATE_BEGIN		:	RoleTradeStateBegin( self ),
			csdefine.TRADE_STATE_LOCK		:	RoleTradeStateLock( self ),
			csdefine.TRADE_STATE_SURE		:	RoleTradeStateSure( self ),
		}
		self.shopTypeMapping = {}						# 商店类型数据
		self.shopItems = {}								# 商店物品数据
		self.skillLearnConfig = {}						# 学习技能数据
		self.passiveSkillLearnConfig = {}				# 被动学习技能数据
		self.randomLimitShopConfig = {}					# 随机限量商品数据
		self.mysteriousConfig = {}						# 神秘宝盒配置数据
		self.mysteriousMerchantConfig = {}				# 神秘商人配置
		
		self.combatSoulItem = {}						# 英雄王座\战魂商店
		self.guardSoulItem = {}							# 英雄王座\魂卫商店
		self.pagodaSoulItem = {}						# 英雄王座\魂塔商店
		self.drugSoulItem = {}							# 英雄王座\药品商店
		self.LMNeuralItem = {}							# 英雄王座\中立商店
		
	def init( self, shopDataConfig, randomLimitShopConfig, skillLearnConfig, passiveSkillLearnConfig, shopTypeConfig, mysteriousConfig, mysteriousMerchantConfig, tongPlunderShopConfig ):
		"""
		初始化配置
		"""
		self.initSoulShop()
		self.shopTypeMapping = shopTypeConfig
		
		self.randomLimitShopConfig = randomLimitShopConfig
		for config in [shopDataConfig, randomLimitShopConfig, tongPlunderShopConfig]:
			for shopID, shopDatas in config.items():
				for slot, shopData in shopDatas.items():
					temp = {}
					for key, value in shopData["price"].items():
						if key == "bindMoney":
							temp[csdefine.TRADE_PAY_ITEM_BIND_MONEY] = value
						elif key == "money":
							temp[csdefine.TRADE_PAY_ITEM_MONEY] = value
						elif key == "tongContribute":
							temp[csdefine.TRADE_PAY_ITEM_CONTRIBUTE] = value
						elif key == "feats":
							temp[csdefine.TRADE_PAY_ITEM_FEATS] = value
						elif key == "psionic":
							temp[csdefine.TRADE_PAY_ITEM_LING_NENG] = value
					shopData["price"] = temp
				
				self.shopItems.setdefault(shopID, {})
				self.shopItems[shopID].update( shopDatas )
				
		#这里按照slotID来进行保存，使用的时候更方便一点
		for config in mysteriousMerchantConfig:
			if config["slotID"] not in self.mysteriousMerchantConfig:
				self.mysteriousMerchantConfig[config["slotID"]] = {}
			
			temp = config["price"].split(":")
			config["price"] = {int(temp[0]) : int(temp[1])}
			self.mysteriousMerchantConfig[config["slotID"]][config["id"]] = config
			
		#神秘宝盒开出的物品
		for config in mysteriousConfig:
			self.mysteriousConfig[config["id"]] = config
			
		self.initSkillLearnData(skillLearnConfig)
		self.initPassiveSkillLearnData(passiveSkillLearnConfig)
		
	def initSkillLearnData( self, config ):
		"""初始化技能升级配置"""
		for getData in config:
			getData["material"] = {}
			if getData["material_1"]: getData["material"][getData["material_1"]] = int(getData["mNum_1"])
			if getData["material_2"]: getData["material"][getData["material_2"]] = int(getData["mNum_2"])
			if getData["material_3"]: getData["material"][getData["material_3"]] = int(getData["mNum_3"])
			self.skillLearnConfig[int(getData["ID"])] = getData

	def initPassiveSkillLearnData( self, config ):
		"""初始化被动 技能升级配置"""
		for getData in config:
			getData["material"] = {}
			if getData["Material_1"]:
				Material_1 = getData["Material_1"].split("|")
				getData["material"][int(Material_1[0])] = int(Material_1[1])
			if getData["Material_2"]:
				Material_2 = getData["Material_2"].split("|")
				getData["material"][int(Material_2[0])] = int(Material_2[1])
			if getData["Material_3"]:
				Material_3 = getData["Material_3"].split("|")
				getData["material"][int(Material_3[0])] = int(Material_3[1])
			self.passiveSkillLearnConfig[int(getData["ID"])] = getData

	#------------------------------------------------------------------
	# 英雄王座商店
	#------------------------------------------------------------------
	def initSoulShop( self ):
		"""初始化英雄王座配置"""
		self.combatSoulItem = openJsonCfg("ShopData/SoulShop/CombatSoulShop.json")
		self.guardSoulItem = openJsonCfg("ShopData/SoulShop/GuardSoulShop.json")
		self.pagodaSoulItem = openJsonCfg("ShopData/SoulShop/PagodaSoulShop.json")
		self.drugSoulItem = openJsonCfg("ShopData/SoulShop/DrugSoulShop.json")
		self.LMNeuralItem = openJsonCfg("ShopData/SoulShop/NPCNeuralShop.json")
		
	def getCombatSoulInfo( self, itemID ):
		"""获取战魂数据"""
		if itemID in self.combatSoulItem:
			return self.combatSoulItem[itemID]
		else:
			KBEDebug.ERROR_MSG("Get combatSoulItem(%s) err!!"%itemID)
			return {}
		
	def getGuardSoulInfo( self, scriptID ):
		"""获取魂卫数据"""
		if scriptID in self.guardSoulItem:
			return self.guardSoulItem[scriptID]
		else:
			KBEDebug.ERROR_MSG("Get GuardSoulItem(%s) err!!"%scriptID)
			return {}
			
	def getNeuralGuardSoulInfo( self, scriptID ):
		"""获取中立商店 魂卫数据"""
		if scriptID in self.LMNeuralItem:
			return self.LMNeuralItem[scriptID]
		else:
			KBEDebug.ERROR_MSG("Get GuardSoulItem(%s) err!!"%scriptID)
			return {}
		
	def getAllGuardLevel( self, passTime ):
		"""根据时间获取所有魂卫等级"""
		tempList = []
		for scriptID in self.guardSoulItem.keys():
			temp = {}
			level = self.getGuardLevelsByTime( scriptID, passTime )
			temp["scriptID"] = scriptID
			temp["level"] = level
			tempList.append(temp)
		return tempList

	def getAllGuardLevelByCamp( self, camp, passTime ):
		"""根据时间获取所有魂卫等级"""
		tempList = []
		for scriptID in self.guardSoulItem.keys():
			if camp!= self.guardSoulItem[scriptID]["camp"]:
				continue
			temp = {}
			level = self.getGuardLevelsByTime( scriptID, passTime )
			temp["scriptID"] = scriptID
			temp["level"] = level
			tempList.append(temp)
		return tempList
		
	def getGuardLevelsByTime( self, scriptID, passTime ):
		"""根据时间获取相应魂卫等级"""
		if scriptID in self.guardSoulItem:
			guardInfo = self.guardSoulItem[scriptID]
			levelRels = guardInfo["levelRelevant"].split("|")
			datas = {}
			for rel in levelRels:
				levelRelList = rel.split(":")
				if len(levelRelList) >= 2:
					datas[int(levelRelList[0])] = int(levelRelList[1])
			
			for time in sorted(datas):
				if passTime <= time:
					return datas[time]
		return 1
		
	def getNeuralGuardLevelsByTime( self, scriptID, passTime ):
		"""根据时间获取 中立商店 相应魂卫等级"""
		if scriptID in self.LMNeuralItem:
			guardInfo = self.LMNeuralItem[scriptID]
			levelRels = guardInfo["levelRelevant"].split("|")
			datas = {}
			for rel in levelRels:
				levelRelList = rel.split(":")
				if len(levelRelList) >= 2:
					datas[int(levelRelList[0])] = int(levelRelList[1])
			
			for time in sorted(datas):
				if passTime <= time:
					return datas[time]
		return 1
		
	def getSourcePagoda( self, camp, wayType ):
		"""获取某个阵营的初始塔"""
		paList = []
		for scriptID, pagodaInfos in self.pagodaSoulItem.items():
			for pagodaInfo in pagodaInfos:
				if pagodaInfo["camp"] == camp and int(pagodaInfo["type"]) == wayType:
					paList.append( scriptID )
					break
		return paList
		
	def getSourcePagodaByScriptID( self, camp, scriptID , wayType):
		"""获取某个阵营的某个初始塔"""
		paList = []
		for sourceScriptID, pagodaInfos in self.pagodaSoulItem.items():
			for pagodaInfo in pagodaInfos:
				if pagodaInfo["camp"] == camp and int(pagodaInfo["type"]) == wayType:
					if sourceScriptID == scriptID or pagodaInfo["lavaPagoda"] == scriptID or\
					pagodaInfo["icePagoda"] == scriptID or pagodaInfo["trapPagoda"] == scriptID or\
					pagodaInfo["spiritPagoda"] == scriptID:
						return sourceScriptID
		return 0
		
	def getPriceByPagodaID( self, scriptID, wayType ):
		for pagodaInfos in self.pagodaSoulItem.values():
			for pagodaInfo in pagodaInfos:
				if pagodaInfo["lavaPagoda"] == scriptID and int( pagodaInfo["type"] ) == wayType:
					return pagodaInfo["lavaPrice"]
				if pagodaInfo["icePagoda"] == scriptID and int( pagodaInfo["type"] ) == wayType:
					return pagodaInfo["icePrice"]
				if pagodaInfo["trapPagoda"] == scriptID and int( pagodaInfo["type"] ) == wayType:
					return pagodaInfo["trapPrice"]
				if pagodaInfo["spiritPagoda"] == scriptID and int( pagodaInfo["type"] ) == wayType:
					return pagodaInfo["spiritPrice"]
		return -1

	def getWayTypeByPagodaID( self, scriptID ):
		for pagodaInfos in self.pagodaSoulItem.values():
			for pagodaInfo in pagodaInfos:
				if pagodaInfo["lavaPagoda"] == scriptID:
					return pagodaInfo["type"]
				if pagodaInfo["icePagoda"] == scriptID:
					return pagodaInfo["type"]
				if pagodaInfo["trapPagoda"] == scriptID:
					return pagodaInfo["type"]
				if pagodaInfo["spiritPagoda"] == scriptID:
					return pagodaInfo["type"]
		return -1
		
	def getDrugInfo( self ):
		""""""
		return list(self.drugSoulItem.values())
		
	def getDrugInfoByItemID( self, itemID ):
		""""""
		return self.drugSoulItem.get(itemID, None)
	#------------------------------------------------------------------
	# NPC商店
	#------------------------------------------------------------------
	def getShopTypeConfig( self,shopType ):
		"""
		获得某商店配置
		"""
		return self.shopTypeMapping.get(shopType,None)
		
	def hasLimitItem(self, shopID):
		"""该商店是否有上限物品"""
		if shopID in self.shopItems:
			for slot, item in self.shopItems[shopID].items():
				if item["buyLimit"] > 0:
					return True
		return False
		
	def isLimitItem( self, shopID, slot ):
		"""是否是上限物品"""
		slotData = self.shopItems[shopID][slot]
		return slotData["buyLimit"] > 0
	
	def checkCondition( self, player, shopID, slot, itemID ):
		"""是否满足购买条件"""
		if shopID in self.shopItems and slot in self.shopItems[shopID]:
			shopItem = self.shopItems[shopID][slot]
			if shopItem["itemID"] != itemID:
				KBEDebug.ERROR_MSG("Buy NPC item err!slot(%s) item id is not same!(sell itemID:%d,buy itemID:%d)"%(slot,shopItem["itemID"],itemID))
				return False
			for type, value in shopItem["condition"].items():
				currency = self.conditionMap.get( type, None )
				if currency == None:
					KBEDebug.ERROR_MSG("Cannot find condition type(%s)"%type)
					return False
				if not currency.verify( player, value ):
					return False
			return True
		return False
			
	def getShopItemConfig( self, shopID, slot ):
		"""
		商店物品配置
		@param id: 商店ID
		@type  id: STRING
		@return: 返回商店物品配置
		"""
		try:
			return self.shopItems[shopID][slot]
		except:
			KBEDebug.ERROR_MSG("Find NPC item err!shopItems(%s,%s) is None"%(shopID,slot))
			return {}
			
	def getRandomLimitShopConfig( self, shopID, slot ):
		"""
		"""
		return self.randomLimitShopConfig.get(shopID, {}).get(slot, None)
		
	def getSkillLearnData( self, skillID ):
		"""获取技能学习相关条件"""
		return self.skillLearnConfig.get( skillID, None )
		
	def getMaxLevelSkillLearnDatas( self, player, skillID ):
		"""获取升级到最大技能等级数据"""
		money = 0
		potential = 0
		maxSkillID = 0
		materials = {}
		nextSkillID = 0
		skillData = self.skillLearnConfig.get( skillID )
		if skillData:
			nextSkillID = skillData["NextLevelID"]
		while nextSkillID:
			data = self.skillLearnConfig.get(nextSkillID)
			if not data:
				return maxSkillID, potential, money, materials
			if player.level < data["ReqLevel"]:
				return maxSkillID, potential, money, materials
			
			maxSkillID = nextSkillID
			money += data["money"]
			potential += data["ReqPotential"]
			nextSkillID = data["NextLevelID"]
			
			for material, amount in data["material"].items():
				if material not in materials:
					materials[material] = 0
				materials[material] += amount
			
		return maxSkillID, potential, money, materials

	def getPassiveSkillLearnData( self, skillID ):
		"""获取被动技能学习相关条件"""
		return self.passiveSkillLearnConfig.get( skillID, None )
	
	def getShopTypeConfig( self,shopType ):
		"""
		获得某商店配置
		"""
		return self.shopTypeMapping.get(shopType,None)
		
	def onEnd( self, avatar ):
		"""
		交易结束
		@param avatar: 购买对象
		@type  avatar: MAILBOX
		"""
		self.unlock( avatar )

	def getRoleTradeState( self, state ):
		"""
		给予玩家之间交易当前状态处理类
		@param state: 玩家状态
		@type  state: INT32
		"""
		return self.roleTradeStateMap.get( state, None )
		
	def getMysteriousConfig( self ):
		"""
		获取神秘宝盒配置
		"""
		return self.mysteriousConfig
		
	def getMysteriousMerchantConfig( self ):
		"""
		获取神秘商人商店配置
		"""
		return self.mysteriousMerchantConfig
		
g_tradeMgr = TradeMgr()