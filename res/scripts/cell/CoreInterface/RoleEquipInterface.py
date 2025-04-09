#-*-coding:utf-8-*-

import KBEngine
import csdefine
import random
import ItemFactory
from KBEDebug import *
import ItemTypeEnum
import Const
import csconst
import csstatus
import cschannel_msgs
from ItemSystemExp import g_equipIntensify
from ItemSystemExp import g_EquipReSet
from ItemSystemExp import g_EquipPropertyTypeExp
from ItemSystemExp import g_EquipPropertyValueExp
from ItemSystemExp import g_EquipCompose
from MsgLogger import g_logger

class RoleEquipInterface:
	"""
	description of class
	"""
	def __init__(self):
		equipItemList = self.getItemListByKBType( ItemTypeEnum.BAG_EQUIP)
		for equipItem in equipItemList:
			self.addEquipHoldEffects(equipItem)
			self.addKingEquipEffect(equipItem)

	def onEquipWieldCb(self, itemInst):
		"""
		装备物品装备后回调
		"""
		self.oldCombatPower = self.combatPower
		self.addEquipHoldEffects(itemInst)
		self.addKingEquipEffect(itemInst)
		self.calcAttachProperties(csdefine.CALC_COMBAT_POWER_REASON_EQUIP)
		self.onCombatPowerChange(self.oldCombatPower, csdefine.CALC_COMBAT_POWER_REASON_EQUIP)
		itemInst.onWield( self )
		self.client.CLIENT_onEquipWieldCb( str( itemInst.uid ) )

	def onEquipUnWieldCb(self, itemInst):
		"""
		装备卸载后回调
		"""
		self.oldCombatPower = self.combatPower
		self.removeEquipHoldEffects(itemInst)
		self.removeKingEquipEffect( itemInst )
		self.calcAttachProperties(csdefine.CALC_COMBAT_POWER_REASON_EQUIP)
		self.onCombatPowerChange(self.oldCombatPower, csdefine.CALC_COMBAT_POWER_REASON_EQUIP)
		itemInst.onUnWield( self )
		self.client.CLIENT_onEquipUnWieldCb( str( itemInst.uid ) )
		
	def onEquipHardinessChange( self, itemInst, oldHard, newHard):
		"""
		装备的耐久度改变
		"""
		if newHard == 0:			# 装备耐久度用完
			self.removeEquipHoldEffects(itemInst)
			self.removeKingEquipEffect( itemInst )
			self.calcAttachProperties()
		if oldHard == 0:			# 装备耐久度维修
			self.addEquipHoldEffects(itemInst)
			self.addKingEquipEffect(itemInst)
			self.calcAttachProperties()

	#------------------装备持有效果 CST-3057------------------

	def addEquipHoldEffects( self, itemInst ):
		"""
		增加装备的持有效果
		"""
		holdEffectIDList = itemInst.getHoldEffectIDList()
		effectIndexList = []
		for holdEffectID in holdEffectIDList:
			index = self.addFixIDHoldEffect( holdEffectID, self )
			if index != -1:
				effectIndexList.append(index)

		self.itemHoldEffectIndexDict[str(itemInst.uid)] = effectIndexList

	def removeEquipHoldEffects( self, itemInst ):
		"""
		移除装备的持有效果
		"""
		if str(itemInst.uid) not in self.itemHoldEffectIndexDict:
			return
		effectIndexList = self.itemHoldEffectIndexDict.get(str(itemInst.uid))
		for index in effectIndexList:
			self.removeFixIDHoldEffect( index )
		self.itemHoldEffectIndexDict.pop(str(itemInst.uid))

	def addKingEquipEffect( self, itemInst ):
		"""添加神兵武器 效果"""
		if itemInst.isKingEquip():
			effectData = g_equipIntensify.getKingCraftEffect( itemInst.id )
			holdEffectID = effectData.get("HoldEffect", 0)
			effectID = effectData.get("EnterEffect", 0)
			if holdEffectID:
				self.addFixIDHoldEffect( holdEffectID, self )
			if effectID:
				self.addFixIDEffect( self, effectID )
		
	def removeKingEquipEffect( self, itemInst ):
		"""移除神兵武器 效果"""
		if itemInst.isKingEquip():
			effectData = g_equipIntensify.getKingCraftEffect( itemInst.id )
			holdEffectID = effectData.get("HoldEffect", 0)
			effectID = effectData.get("LeaveEffect", 0)
			if holdEffectID:
				self.removeFixIDHoldEffectByID( holdEffectID )
			if effectID:
				self.addFixIDEffect( self, effectID )
	# ---------------------------查看装备------------------------------
	def CELL_queryTargetEquipInfo( self, srcEntityID, targetID ):
		"""
		Exposed Method
		查询目标玩家装备
		"""
		target = KBEngine.entities.get(targetID)
		if target is None:
			ERROR_MSG("player( id:%d, name:%s ) can not find targetID(%d)"%( self.id, self.playerName, targetID ))
			return
		target.onQueryEquipInfo( self )
		
	def onQueryEquipInfo( self, playerMB ):
		"""
		define Method
		查询玩家装备
		"""
		playerMB.client.CLIENT_OnQueryTargetEquipInfo( self._getEquipInfo(), self._getPropertyDict() )
		
	def _getPropertyDict( self ):
		"""获取玩家属性值"""
		info = {}
		info["name"] = self.playerName
		info["camp"] = self.camp
		info["gender"] = self.gender
		info["profession"] = self.profession
		info["level"] = self.level
		info["xiuwei"] = self.xiuwei
		info["jingjieLevel"] = self.jingjieLevel
		info["killingValue"] = self.killingValue
		info["feats"] = self.feats
		info["potential"] = self.potential
		info["combatPower"] = self.combatPower
		
		info["strength"] = self.strength
		info["dexterity"] = self.dexterity
		info["intellect"] = self.intellect
		info["corporeity"] = self.corporeity
		info["discern"] = self.discern
		info["speed"] = self.speed
		
		info["HP"] = self.HP
		info["HP_Max"] = self.HP_Max
		info["MP"] = self.MP
		info["MP_Max"] = self.MP_Max
		info["gangQiValue"] = self.gangQiValue
		info["gangQiValue_Max"] = self.gangQiValue_Max
		
		info["damage"] = self.damage
		info["magic_damage"] = self.magic_damage
		info["armor"] = self.armor
		info["magic_armor"] = self.magic_armor
		info["gangQi_damagePoint"] = self.gangQi_damagePoint
		info["gangQi_armorPoint"] = self.gangQi_armorPoint
		
		info["parry"] = self.parry
		info["hitrate"] = self.hitrate
		info["dodgerate"] = self.dodgerate
		info["criticalstrike"] = self.criticalstrike
		info["healingrate"] = self.healingrate
		info["cure"] = self.cure

		info["ice_damage"] = self.ice_damage
		info["fire_damage"] = self.fire_damage
		info["thunder_damage"] = self.thunder_damage
		info["xuan_damage"] = self.xuan_damage
		info["ice_armor"] = self.ice_armor
		info["fire_armor"] = self.fire_armor
		info["thunder_armor"] = self.thunder_armor
		info["xuan_armor"] = self.xuan_armor

		info["damage_ignore"] = self.damage_ignore
		info["magic_damage_ignore"] = self.magic_damage_ignore
		info["armor_ignore"] = self.armor_ignore
		info["magic_armor_ignore"] = self.magic_armor_ignore
		info["criticalstrike_ignore"] = self.criticalstrike_ignore
		info["parry_ignore"] = self.parry_ignore
		info["hitrate_ignore"] = self.hitrate_ignore
		info["dodgerate_ignore"] = self.dodgerate_ignore

		info["ice_damage_ignore"] = self.ice_damage_ignore
		info["fire_damage_ignore"] = self.fire_damage_ignore
		info["thunder_damage_ignore"] = self.thunder_damage_ignore
		info["xuan_damage_ignore"] = self.xuan_damage_ignore
		info["ice_armor_ignore"] = self.ice_armor_ignore
		info["fire_armor_ignore"] = self.fire_armor_ignore
		info["thunder_armor_ignore"] = self.thunder_armor_ignore
		info["xuan_armor_ignore"] = self.xuan_armor_ignore
		info["depress_resist"] = self.depress_resist
		info["hitback_resist"] = self.hitback_resist
		info["control_resist"] = self.control_resist
		info["insane_resist"] = self.insane_resist

		return info
		
	def _getEquipInfo( self ):
		"""获取装备信息"""
		equipList = []
		itemList = self.getItemListByKBType(ItemTypeEnum.BAG_EQUIP)
		for equip in itemList:
			info = {}
			info["itemID"] = equip.id
			info["combatPower"] = equip.dynamicData["combatPower"]
			info["hardiness"] = equip.dynamicData["hardiness"]
			info["attackPropertiesStr"] = equip.dynamicData["attackPropertiesStr"]
			info["attachPropertiesStr"] = equip.dynamicData["attachPropertiesStr"]
			info["intensifyDataStr"] = equip.dynamicData["intensifyDataStr"]
			equipList.append( info )
		return {"Datas" : equipList }

	# ----------------------------------------------------------------
	# 装备强化
	# ----------------------------------------------------------------
	def checkIntensifyEquip( self, equip, dstIntensifyLv, attachItemID):
		"""
		检查装备强化要求
		@return bool
		"""
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return False

		if equip.getLevel() < Const.EQUIP_INTENSIFY_NEED_LEVEL:
			self.statusMessage( csstatus.EQUIP_INTENSIFY_NEED_LEVEL, "" )
			return False

		if equip.getQuality() < Const.EQUIP_INTENSIFY_NEED_QUALITY:
			self.statusMessage( csstatus.EQUIP_INTENSIFY_QUALITY_BLUE, "" )
			return False

		if not equip.canIntensify():
			self.statusMessage( csstatus.EQUIP_INTENSIFY_NO_SUPPORT, "" )
			return False

		if equip.getIntensifyLevel() >= dstIntensifyLv:
			return False
		
		if equip.getIntensifyLevel() >= g_equipIntensify.getMaxIntensifyLv(equip.getLevel()):
			self.statusMessage( csstatus.EQUIP_INTENSIFY_MAX_LEVEL, "" )
			return False
		return True

	def doEquipIntensify( self, srcEntityID, equipuid, dstIntensifyLv, attachItemID):
		"""
		<Exposed Method>
		装备普通强化
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		equip = self.getItemInstByUid(int(equipuid))
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		if not self.checkIntensifyEquip(equip, dstIntensifyLv, attachItemID): return
		
		curIntensifyLv = equip.getIntensifyLevel()
		costmoney, XJCount, FXJCount, SXJCount = g_equipIntensify.getSumIntensifyCost(equip.getLevel(), curIntensifyLv, dstIntensifyLv)
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY] = costmoney
		payItems[csdefine.TRADE_PAY_ITEM_NORMAL_CRYTAL] = XJCount
		if FXJCount:
			payItems[csdefine.TRADE_PAY_ITEM_MCOLOR_CRYTAL] = FXJCount
		if SXJCount:
			payItems[csdefine.TRADE_PAY_ITEM_SUPPER_CRYTAL] = SXJCount
		attachItemCost = dstIntensifyLv - curIntensifyLv
		if attachItemID:
			hasAmount = 0
			for item in self.getItemInstsByID(attachItemID):
				hasAmount += item.getAmount()
			if hasAmount < ( dstIntensifyLv - curIntensifyLv ):
				attachItemCost = hasAmount
			payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = {attachItemID : attachItemCost}
		if equip.isBinded():
			self.requestPay(csdefine.TRADE_TYPE_INTENSIFY_EQUIP, 0, payItems, equipuid, dstIntensifyLv, attachItemID, attachItemCost)
		else:
			self.inquireMessage(csstatus.EQUIP_INTENSIFY_BIND_CONFIRM, [], "requestPayIntensify", payItems, equipuid, dstIntensifyLv, attachItemID, attachItemCost)

	def requestPayIntensify(self, reply, payItems, equipuid, dstIntensifyLv, attachItemID, attachItemCost):
		if reply:
			self.requestPay(csdefine.TRADE_TYPE_INTENSIFY_EQUIP, 0, payItems, equipuid, dstIntensifyLv, attachItemID, attachItemCost)

	def onIntensify( self, order, equipuid, dstIntensifyLv, attachItemID, attachItemCost ):
		"""
		装备强化成功
		"""
		equip = self.getItemInstByUid(int(equipuid))
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		
		attachItem = None
		if attachItemID:
			attachItem = ItemFactory.ItemFactoryInst.createDynamicItem( attachItemID )			# 有可能被删除了，只能重新创建
		#处理强化属性
		oldIntensifyData = equip.getIntensifyDict()["_extra"]
		oldInstLevel = equip.getIntensifyLevel()
		intensifyResult = g_equipIntensify.getIntensifResult(equip, dstIntensifyLv, attachItem, attachItemCost)
		equip.addIntensifyLevels(self, intensifyResult)
		self.client.OnIntensifySuccess( str( equip.uid ) )
		if not equip.isBinded(): equip.setBindType(self)
		
		self.tryToBeKingEquip( equip )
		newIntensifyData = equip.getIntensifyDict()["_extra"]
		#添加日志
		g_logger.equipIntensifyLog(self.playerDBID, self.getName(), equip.id, equip.uid, equip.getItemDir("ItemName"), equip.amount, oldInstLevel,
			equip.getIntensifyLevel(), oldIntensifyData, newIntensifyData, order, equip)

	# ----------------------------------------------------------------
	# 装备回火
	# ----------------------------------------------------------------
	def checkBackfireEquip( self, equip, saveIndexs ):
		"""
		检查装备回火要求
		@return bool
		"""
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return False
		if equip.getIntensifyLevel() == 0:
			self.statusMessage( csstatus.EQUIP_BACKFIRE_NEED_LEVEL, "" )
			return False
			
		return True

	def doEquipBackfire( self, srcEntityID, equipuid, saveIndexs ):
		"""
		<Exposed Method>
		装备回火
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		equip = self.getItemInstByUid(int(equipuid))
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		if not self.checkBackfireEquip( equip, saveIndexs): return
		
		costmoney, lowMaterialCost, mediumMaterialCost, highMaterialCost = g_equipIntensify.getBackFireCost(equip.getLevel(), len(saveIndexs))
		payItems = {}
		#payItems[csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY] = costmoney
		payItems[csdefine.TRADE_PAY_ITEM_HH_SYMBOL] = lowMaterialCost
		if mediumMaterialCost:
			payItems[csdefine.TRADE_PAY_ITEM_ZY_SYMBOL] = mediumMaterialCost
		if highMaterialCost:
			payItems[csdefine.TRADE_PAY_ITEM_BD_SYMBOL] = highMaterialCost
		
		self.requestPay( csdefine.TRADE_TYPE_RESET_EQUIP, 0, payItems, equipuid, saveIndexs )
		
	def onBackfire( self, order, equipuid, saveIndexs ):
		"""
		装备回火成功
		"""
		equip = self.getItemInstByUid(int(equipuid))
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		
		oldInstLevel = equip.getIntensifyLevel()
		oldIntensifyData = equip.getIntensifyDict()["_extra"]
		equip.decIntensifyLevel( self, saveIndexs )
		self.statusMessage( csstatus.EQUIP_BACKFIRE_SUCCEED, "" )
		self.client.OnBackfireSuccess( str( equip.uid ) )
		newIntensifyData = equip.getIntensifyDict()["_extra"]
		
		#添加日志
		g_logger.equipBackFrieLog(self.playerDBID, self.getName(), equip.id, equip.uid, equip.getItemDir("ItemName"), equip.amount, oldInstLevel,
			equip.getIntensifyLevel(), oldIntensifyData, newIntensifyData, order, equip)

	# ----------------------------------------------------------------
	# 装备强化保存与还原
	# ----------------------------------------------------------------
	def requestIntensifySaveSlotInfo( self, srcEntityID ):
		"""
		Exposed Method
		请求 装备备份数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.client.CLIENT_OnRequestIntensifySaveSlotInfo( self.intensifySaveSlotNum, self.intensifySaveSlot)
		
	def openIntensifySaveSlot( self, srcEntityID ):
		"""
		Exposed Method
		开启 装备备份栏位
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.intensifySaveSlotNum >= Const.INTENSIFY_SAVE_SLOT_MAX_NUM:return
		
		payItems = {}
		if self.intensifySaveSlotNum == 3:
			payItems[csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY] = Const.INTENSIFY_SAVE_ONE_SLOT_COST
		else:
			payItems[csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY]  = Const.INTENSIFY_SAVE_TWO_SLOT_COST
		
		self.requestPay(csdefine.TRADE_TYPE_OPEN_INTENSIFY_SAVE_SLOT, 0, payItems )
		
	def openIntensifySaveSlotSuccess( self, order ):
		"""
		开启 新备份栏位 成功
		"""
		self.intensifySaveSlotNum += 1
		self.client.OpenIntensifySaveSlotSuccess()
		
		#添加日志
		g_logger.equipOpenSaveSlotLog(self.playerDBID, self.getName(), self.intensifySaveSlotNum, order)
	
	def checkIntensifySaveEquip( self, equip ):
		"""
		检查装备保存要求
		@return bool
		"""
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return False
			
		maxLv = g_equipIntensify.getIntensifyMaxLevel( equip )
		if maxLv == 0:return
		
		if equip.getIntensifyLevel() != maxLv:
			self.statusMessage( csstatus.EQUIP_INTENSIFY_SAVE_NEED_LEVEL, "" )
			return False

		return True

	def doEquipIntensifySave( self, srcEntityID, index, equipuid ):
		"""
		<Exposed Method>
		装备保存
		"""
		if not self.validateClientCall( srcEntityID ):
			return

		equip = self.getItemInstByUid( int( equipuid ) )
		if equip is None:
			ERROR_MSG("Can not find equip by uid(%s)"%equipuid)
			return
		
		if not self.checkIntensifySaveEquip( equip ): return
		saveMoneyCost, saveBDFuCost = g_equipIntensify.getIntensifySaveCost( equip )
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY] = saveMoneyCost
		payItems[csdefine.TRADE_PAY_ITEM_BD_SYMBOL] = saveBDFuCost
		self.requestPay(csdefine.TRADE_TYPE_SAVE_INTENSIFY_EQUIP, 0, payItems, index, equipuid )
		
	def onIntensifySave( self, order, index, equipuid ):
		"""
		装备保存成功
		"""
		equip = self.getItemInstByUid( int( equipuid ) )
		if equip is None:
			ERROR_MSG("Can not find equip by uid(%s)"%equipuid)
			return
		# 如果重复保存，顶替原有的保存
		for saveIndex, saveSlot in self.intensifySaveSlot.items():
			if saveSlot["EquipUID"] == equip.uid:
				index = saveIndex
				break
		# 设置栏位
		self.intensifySaveSlot[index] = {}
		self.intensifySaveSlot[index]["index"] = index
		self.intensifySaveSlot[index]["EquipUID"] = equip.uid
		self.intensifySaveSlot[index]["EquipID"] = equip.id
		self.intensifySaveSlot[index]["intensifyDataStr"] = equip.dynamicData["intensifyDataStr"]
		
		self.statusMessage( csstatus.EQUIP_INTENSIFY_SAVE_SUCCEED, "" )
		self.client.OnIntensifySaveSuccess( index, str( equip.uid ) )
		#添加日志
		g_logger.equipSaveLog(self.playerDBID, self.getName(), equip.id, equip.uid, equip.getItemDir("ItemName"), 1, equip.getIntensifyLevel(),
			equip.parseIntensifyDatas(equip.dynamicData["intensifyDataStr"]), index, order, equip)

	def doEquipIntensifyRestore( self, srcEntityID, uid ):
		"""
		<Exposed Method>
		装备还原
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		uid = int(uid)
		equip = self.getItemInstByUid( uid )
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		key = -1
		for index, item in self.intensifySaveSlot.items():
			if item["EquipUID"] == uid:
				key = index
		if key == -1:
			self.statusMessage( csstatus.EQUIP_INTENSIFY_RESTORE_EQUIP_WRONG, "" )
			return

		restoreMoneyCost, restoreDBFuCost = g_equipIntensify.getIntensifyRestore( equip )
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY] = restoreMoneyCost
		payItems[csdefine.TRADE_PAY_ITEM_BD_SYMBOL] = restoreDBFuCost
		self.requestPay(csdefine.TRADE_TYPE_RESET_INTENSIFY_EQUIP, 0, payItems, key, uid )
		
	def onReStoreIntensify(self, order, key, equipuid):
		"""装备还原"""
		equip = self.getItemInstByUid( int(equipuid ))
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		oldIntensifyData = equip.getIntensifyDict()["_extra"]
		intensifyResult = self.intensifySaveSlot.pop( key )
		equip.intensifyRestore( self, intensifyResult )
		self.statusMessage( csstatus.EQUIP_INTENSIFY_RESTORE_SUCCEED, "" )
		self.client.OnIntensifyRestoreSuccess( str( equip.uid ) )
		newIntensifyData = equip.getIntensifyDict()["_extra"]
		#添加日志
		g_logger.equipRestoreLog(self.playerDBID, self.getName(), equip.id, equip.uid, equip.getItemDir("ItemName"), equip.amount, equip.getIntensifyLevel(),
			oldIntensifyData, newIntensifyData, key, order, equip)

	# ----------------------------------------------------------------
	# 装备洗练
	# ----------------------------------------------------------------
	def _getMaterialByTypeItemClass( self, itemClass, type ):
		"""获取相关材料的数据"""
		num = 0
		itemList= []
		stoneList = self.getItemInstsByItemClass( itemClass )
		for s in stoneList:
			if s.intensifyType == type:
				num += s.amount
				itemList.append( s )
		return num, itemList
	
	def shuffleEquip( self, srcEntityID, equipuid, lockProps, useYBToPearl, useYBToFu ):
		"""
		Exposed Method
		装备洗练
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		equip = self.getItemInstByUid( int(equipuid) )
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		if equip.getLevel() < Const.EQUIP_SHUFFLE_NEED_LEVEL:
			#self.statusMessage( csstatus.EQUIP_SHUFFLE_NEED_LEVEL, "" )
			return
		if equip.isWhite():
			self.statusMessage( csstatus.EQUIP_SHUFFLE_QUALITY_BLUE, "" )
			return
		if equip.isKingEquip():
			ERROR_MSG("player(%d) Can not shuffle kingEquip(%s)!!"%( self.id, equipuid))
			return
		
		payItems = {}
		stone = 0
		money, wastStone, bloodFu = g_EquipReSet.getShuffleCost( equip, len( lockProps ) )
		YBS, YBF = g_EquipReSet.getShuffleYBCost( equip, len( lockProps ) )
		
		payItems[csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY] = money
		if useYBToPearl:
			stone += YBS
		else:
			payItems[csdefine.TRADE_PAY_ITEM_WASH_STONE] = wastStone
		if useYBToFu:
			stone += YBF
		else:
			payItems[csdefine.TRADE_PAY_ITEM_BLOOD_SYMBOL] = bloodFu
		if stone:
			payItems[csdefine.TRADE_PAY_ITEM_STONE] = str(stone)
		if equip.isBinded():
			self.requestPay(csdefine.TRADE_TYPE_SHUFFLE_EQUIP, 0, payItems, equipuid, lockProps )
		else:
			self.inquireMessage(csstatus.EQUIP_SHUFFLE_BIND_CONFIRM, [], "requestShuffle", payItems, equipuid, lockProps)

	def requestShuffle(self, reply, payItems, equipuid, lockProps):
		if reply:
			self.requestPay(csdefine.TRADE_TYPE_SHUFFLE_EQUIP, 0, payItems, equipuid, lockProps )
	
	def doShuffleEquip( self, order, equipuid, lockProps ):
		"""开始洗练"""
		equip = self.getItemInstByUid( int(equipuid) )
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		if not equip.isBinded(): equip.setBindType(self)
		extra = equip.strToDict(equip.dynamicData[ "attachPropertiesStr" ])
		num = len( extra ) - len( lockProps )
		proList = []
		level = equip.getLevel()
		professsion = equip.getReqClass()
		modelpart = equip.getEquipPart()
		while( num > 0 ):
			TypeList = g_EquipPropertyTypeExp.getNPropertyTypes(level, professsion, modelpart, 1 )
			if (not TypeList[0] in lockProps) and (not TypeList[0] in proList):			# 随机出来的属性不会与锁定属性相同
				num -= 1
				proList.extend( TypeList )
		temp = {}
		for propertyID in proList:
			value = g_EquipPropertyValueExp.getPropertyValue(level, professsion, modelpart, propertyID)
			temp.update({propertyID: value})
		for propertyID in lockProps:
			temp[propertyID] = extra[propertyID]
			
		makeStr = equip.dictToStr(temp)
		self.client.OnShuffleEquip( str(equip.uid), makeStr )
		
		self.shuffleEquipProDict.clear()
		self.shuffleEquipProDict[str(equip.uid)] = makeStr
		#添加日志
		g_logger.equipShuffleLog(self.playerDBID, self.getName(), equip.id, equip.uid, equip.getItemDir("ItemName"), equip.amount, extra, temp, order, equip)
		
	def replaceShufflePro( self, srcEntityID, equipuid ):
		"""
		Exposed Method
		替换 洗练属性
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		equip = self.getItemInstByUid( int(equipuid) )
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		if equipuid in self.shuffleEquipProDict:
			oldAttchPro = equip.strToDict(equip.dynamicData["attachPropertiesStr"])
			equip.replaceAttachPro( self, self.shuffleEquipProDict[equipuid] )
			self.client.OnShuffleEquipSuccess( equipuid )
			newAttchPro = equip.strToDict(equip.dynamicData["attachPropertiesStr"])
			
			self.tryToBeKingEquip( equip )
			g_logger.equipShuffleReplaceLog(self.playerDBID, self.getName(), equip.id, equip.uid, equip.getItemDir("ItemName"), equip.amount, oldAttchPro,
				newAttchPro, equip)
		else:
			ERROR_MSG("Role(%s) replace equip(%s) propertyID err!"%( self.getName(), equipuid ))

	# ----------------------------------------------------------------
	# 装备重铸
	# ----------------------------------------------------------------
	def recastEquip( self, srcEntityID, equipuid, protectList, useYBToPearl, useYBToFu ):
		"""
		Exposed Method
		装备重铸
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		equipuid = int(equipuid)
		equip = self.getItemInstByUid( equipuid )
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		if equip.getLevel() < Const.EQUIP_RECAST_NEED_LEVEL:
			#self.statusMessage( csstatus.EQUIP_RECAST_NEED_LEVEL, "" )
			return
		if equip.isWhite():
			self.statusMessage( csstatus.EQUIP_RECAST_QUALITY_BLUE, "" )
			return
		if equip.isKingEquip():
			ERROR_MSG("player(%d) Can not recast kingEquip(%s)!!"%( self.id, equipuid))
			return
			
		payItems = {}
		YB = 0
		protectNum = len( protectList )
		payItems[csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY] = g_EquipReSet.getRecastCostByProtect( equip, protectNum, "MoneyCost" )
		if useYBToPearl:
			YB += g_EquipReSet.getRecastCostByProtect( equip, protectNum, "YBReplaceStone" )
		else:
			payItems[csdefine.TRADE_PAY_ITEM_RECAST_STONE] = g_EquipReSet.getRecastCostByProtect( equip, protectNum, "RecastStone" )
		if useYBToFu:
			YB += g_EquipReSet.getRecastCostByProtect( equip, protectNum, "YBReplaceFu" )
		else:
			payItems[csdefine.TRADE_PAY_ITEM_RECAST_SYMBOL] = g_EquipReSet.getRecastCostByProtect( equip, protectNum, "RecastFu" )
		if YB:
			payItems[csdefine.TRADE_PAY_ITEM_STONE] = str(YB)
			
		if equip.isBinded():
			self.requestPay(csdefine.TRADE_TYPE_RECOST_EQUIP, 0, payItems, equipuid, protectList)
		else:
			self.inquireMessage(csstatus.EQUIP_RECAST_BIND_CONFIRM, [], "requestPayRecast", payItems, equipuid, protectList)

	def requestPayRecast(self, reply, payItems, equipuid, protectList):
		if reply:
			self.requestPay( csdefine.TRADE_TYPE_RECOST_EQUIP, 0, payItems, equipuid, protectList )
	
	def doRecastEquip( self, order, equipuid, protectList ):
		"""重铸流程"""
		equip = self.getItemInstByUid( equipuid )
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		extra = equip.strToDict(equip.dynamicData[ "attachPropertiesStr" ])
		level = equip.getLevel()
		professsion = equip.getReqClass()
		modelpart = equip.getEquipPart()
		temp = {}
		for propertyID, value in extra.items():
			recastValue = g_EquipPropertyValueExp.getReCastPropertyValue(level, professsion, modelpart, propertyID)
			if propertyID in protectList and recastValue < value:
				recastValue = value
			temp[propertyID] = recastValue
		if not equip.isBinded(): equip.setBindType(self)
		equip.replaceAttachPro( self, equip.dictToStr( temp ))
		self.client.OnRecastEquipSuccess( str(equip.uid) )
		
		self.tryToBeKingEquip( equip )
		g_logger.equipRecastLog(self.playerDBID, self.getName(), equip.id, equip.uid, equip.getItemDir("ItemName"), equip.amount, temp, order, equip)
	# ----------------------------------------------------------------
	# 装备传星
	# ----------------------------------------------------------------
	def transferIntensifyEquip( self, srcEntityID, srcEquipUID, dstEquipUID, useNewPro, transferList ):
		"""
		装备传星
		Exposed Method
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		srcEquip = self.getItemInstByUid( int(srcEquipUID) )
		dstEquip = self.getItemInstByUid( int(dstEquipUID) )
		if srcEquip is None or dstEquip is None:
			ERROR_MSG("Equip is None!!srcEquip is None(%r),dstEquip is None(%r)"%(srcEquip is None, dstEquip is None))
			return
		
		if not self.canTransferIntensifyEquip( srcEquip, dstEquip, len( transferList ) ):return
		
		Money, WSparCount, FSparCount, SSparCount = g_EquipReSet.getTransferIntensifyCost( dstEquip, len( transferList ) )
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY] = Money
		payItems[csdefine.TRADE_PAY_ITEM_HH_SYMBOL] = WSparCount
		if FSparCount:
			payItems[csdefine.TRADE_PAY_ITEM_ZY_SYMBOL] = FSparCount
		if SSparCount:
			payItems[csdefine.TRADE_PAY_ITEM_BD_SYMBOL] = SSparCount
		if dstEquip.isBinded():
			self.requestPay(csdefine.TRADE_TYPE_TRANSFER_EQUIP, 0, payItems, srcEquipUID, dstEquipUID, useNewPro,transferList)
		else:
			self.inquireMessage(csstatus.EQUIP_BIOGRAPHY_BIND_CONFIRM, [], "requestPayTransfer", payItems, srcEquipUID, dstEquipUID, useNewPro,transferList)


	def requestPayTransfer(self, reply, payItems, srcEquipUID, dstEquipUID, useNewPro, transferList):
		if reply:
			self.requestPay(csdefine.TRADE_TYPE_TRANSFER_EQUIP, 0, payItems, srcEquipUID, dstEquipUID, useNewPro,transferList)
			
	def onTransferIntensifyEquip( self, order, srcEquipUID, dstEquipUID, useNewPro, transferList ):
		"""开始装备传星"""
		srcEquip = self.getItemInstByUid( int(srcEquipUID) )
		dstEquip = self.getItemInstByUid( int(dstEquipUID) )
		if srcEquip is None or dstEquip is None:
			ERROR_MSG("Equip is None!!srcEquip is None(%r),dstEquip is None(%r)"%(srcEquip is None, dstEquip is None))
			return
		
		if not useNewPro:							# 不是使用dst装备的附加属性
			dstEquip.replaceAttachPro( self, srcEquip.dynamicData["attachPropertiesStr"] )
		temp = {}
		srcIntenSify = srcEquip.parseIntensifyDatas(srcEquip.dynamicData["intensifyDataStr"])
		for intensifyID in transferList:
			intensifyID = int(intensifyID)
			if intensifyID in srcIntenSify:
				temp[intensifyID] = srcIntenSify[intensifyID]
			else:
				ERROR_MSG("Transfer intensify equip(%d) err!!can not find intensifyID(%d)"%(srcEquip.uid, intensifyID))
		isBind = srcEquip.isBinded() or srcEquip.isBinded()	#有一件是绑定装备，最后传星之后也是绑定装备
		dstEquip.onTransferIntensifyEquip( self, temp, isBind )
		self.removeItemByAmount( srcEquip, 1, csdefine.ITEM_REMOVE_BY_BIOGRAPHY )
		self.client.OnBiographyEquipSuccess()
		
		self.tryToBeKingEquip( dstEquip )
		#添加日志
		g_logger.equipTranStarLog(self.playerDBID, self.getName(), srcEquip.id, srcEquip.uid, srcEquip.getItemDir("ItemName"), srcEquip.amount, dstEquip.id,
			dstEquip.uid, dstEquip.getItemDir("ItemName"), dstEquip.amount, temp, order, srcEquip )
		
	def canTransferIntensifyEquip( self, srcEquip, dstEquip, lockNum ):
		"""能够传星"""
		if srcEquip.isKingEquip():
			ERROR_MSG("player(%d) Can not transfer intensify to kingEquip(%s)!!"%( self.id, srcEquip))
			return
		if dstEquip.isKingEquip():
			ERROR_MSG("player(%d) Can not transfer intensify to kingEquip(%s)!!"%( self.id, dstEquip))
			return
		if srcEquip is None or dstEquip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return False
		if srcEquip.getEquipPart() != dstEquip.getEquipPart():
			self.statusMessage( csstatus.EQUIP_BIOGRAPHY_NO_SAMPLE_PART, "" )
			return False
		if srcEquip.getQuality() != dstEquip.getQuality():
			self.statusMessage( csstatus.EQUIP_BIOGRAPHY_NO_SAMPLE_QUALITY, "" )
			return False
		if dstEquip.getLevel() < srcEquip.getLevel():
			self.statusMessage( csstatus.EQUIP_BIOGRAPHY_LEVEL_NOT_MATCH, "" )
			return False
		if dstEquip.getLevel() - srcEquip.getLevel() > Const.EQUIP_DIOGRAPHY_BW_LEVEL:
			self.statusMessage( csstatus.EQUIP_BIOGRAPHY_LEVEL_NOT_MATCH, "" )
			return False
		for index, item in self.intensifySaveSlot.items():
			if item["EquipUID"] == srcEquip.uid:
				self.statusMessage(csstatus.EQUIP_BIOGRAPHY_HAS_INTENSIFY_SAVED, "")
				return False
		return True
		
	def tryToBeKingEquip( self, equip ):
		""" 王道神兵 接口"""
		if equip.isEquip() and equip.canBeKingCraft():
			equip.changeKingCraft( self )
			
			equipName = cschannel_msgs.KING_CRAFT_EQUIP + equip.getItemDir("ItemName")
			self.statusMessage( csstatus.PLAYER_GET_KIND_EQUIP, equipName )
			spaceEntity = self.getCurrentSpace()
			if spaceEntity:
				messageArg = "{}|{}".format(self.getName(), equipName)
				spaceEntity.globalWorld(csstatus.GLOBAL_PLAYER_GET_KIND_EQUIP, messageArg)
		
	# ----------------------------------------------------------------
	# 装备打造
	# ----------------------------------------------------------------
	def studyEquipCompose( self, equipID ):
		"""
		学习装备打造
		"""
		if equipID in self.equipBPrint:
			return

		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(equipID)
		self.equipBPrint.append(equipID)
		self.statusMessage(csstatus.EQUIP_COMPOSE_PRINT_HAS_LEARNED, itemInst.getItemDir("ItemName"))
		self.client.CLIENT_onStudyEquipCompose( equipID )
		
	def CELL_requestEquipCompose( self, srcEntityID ):
		"""
		请求装备打造卷轴
		Exposed Method
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		self.client.CLIENT_onRequestEquipCompose( self.equipBPrint )
			
	def CELL_composeEquip( self, srcEntityID, equipID, useUnBind ):
		"""
		打造装备
		Exposed Method
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if not equipID in self.equipBPrint:
			ERROR_MSG("Cannot find equipID(%d)"%equipID)
			return
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
		freeOrderList = self.getAllFreeOrder(ItemTypeEnum.BAG_COMMON)
		if not freeOrderList:
			self.statusMessage( csstatus.NPCSHOP_BAG_ENOUGH )
			return
		composeCost = g_EquipCompose.getEquipComposeCost( equipID )
		if composeCost is None:
			ERROR_MSG("Equip compose config is err!no equipID(%d)"%equipID)
			return
			
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_MONEY_AND_BINDMONEY] = composeCost["money"]
		if useUnBind:
			payType = csdefine.TRADE_PAY_ITEM_UNBIND_GOODS_BY_ID
			isBinded = 0
		else:
			payType = csdefine.TRADE_PAY_ITEM_GOODS_BY_ID
			isBinded = self.isBindedEquip( composeCost )
		payItems[payType] = composeCost["material"]
			
		self.requestPay( csdefine.TRADE_TYPE_COMPOSE_EQUIP, 0, payItems, equipID, isBinded )
			
	def isBindedEquip(self, composeCost):
		"""打造装备是否绑定"""
		materialDict = {}
		for materialID, num in composeCost["material"].items():
			mList = self.getItemInstsByID( materialID )
			for mItem in list(mList):
				if mItem.isBinded():return 1
		return 0
			
	def doComposeEquit( self, order, equipID, isBinded ):
		"""
		打造装备
		"""
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(equipID, 1, {"bindType":isBinded})
		if itemInst is None:
			ERROR_MSG("Compose equip err!!equip(%d) is None"%equipID)
			return
		self.addItem( itemInst, csdefine.ITEM_ADD_BY_COMPOSE )
		self.client.CLIENT_onSuccessComposeEquip(equipID)
		
		if itemInst.getQuality() >= ItemTypeEnum.QUALITY_GREEN_SHENG:
			spaceEntity = self.getCurrentSpace()
			if spaceEntity:
				messageArg = "{}|{}".format(self.getName(), itemInst.getItemDir("ItemName"))
				spaceEntity.globalWorld(csstatus.ITEM_ADD_DAZAO, messageArg)
			
			#if self.getClient():
			#	self.client.CLIENT_PlaySound(Const.SHENGJIE_ITEM_GET_SOUND)
			#	self.client.CLIENT_PlayEffect(Const.SHENGJIE_ITEM_GET_EFFECTID)
		
		#添加日志
		g_logger.equipComposeLog( self.playerDBID, self.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"), itemInst.amount, order, itemInst )

	# ----------------------------------------------------------------
	# 手写装备
	# ----------------------------------------------------------------
	def customIntensifyEquip(self, equipID, posture, goldStar, silverStar, copperStar, ironStar, mainValueRange ):
		"""
		手写装备自定义强化星级
		"""
		equip = ItemFactory.ItemFactoryInst.createDynamicItem(equipID)
		if equip is None:
			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG, "" )
			return
		if not equip.isEquip():
			return
		level = equip.getLevel()
		profession = equip.getReqClass()
		modelpart = equip.getEquipPart()
		dstIntensifyLv = goldStar + silverStar + copperStar + ironStar
		if g_equipIntensify.getMaxIntensifyLv(level) < dstIntensifyLv:
			return
		if dstIntensifyLv != 0 and not self.checkIntensifyEquip(equip, dstIntensifyLv, 0): return
		temp = {}
		propertyList = csconst.CUSTOM_EQUIP_POSTURE_PROPERTY[profession][posture]
		for propertyID in propertyList:
			maxValue = g_EquipPropertyValueExp.getMaxPropertyValue(level, profession, modelpart, propertyID)
			temp[propertyID] =  maxValue
		equip.replaceAttachPro( self, equip.dictToStr( temp ))
		intensifyResult = g_equipIntensify.getCustomIntensifResult(equip, goldStar, silverStar, copperStar, ironStar, mainValueRange)
		equip.addIntensifyLevels(self, intensifyResult)
		reason = self.addItem( equip, csdefine.ITEM_ADD_BY_GM_COMMAND )
		if reason != csstatus.ITEM_GO_ON:
			self.statusMessage( reason,"" )