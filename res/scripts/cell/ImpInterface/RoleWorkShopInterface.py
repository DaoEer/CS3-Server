# -*- coding: utf-8 -*-


import csconst
import KBEDebug
import KBEngine
import csdefine
import csstatus
import ItemFactory
import time
import ItemTypeEnum
from ComposeScheme import ComposeScheme
from ItemSystemExp import g_ToolCompose

class RoleWorkShopInterface:
	"""
	轮回秘境（工坊、炼金坊）
	"""
	def __init__( self ):
		self.toolComposeType = 0				# 当前正在打造的工具类型（工具打造\绿装）
		self.toolComposeEndTime = 0.0			# 打造的工具结束时间
		self.toolComposeItemID = 0				# 正在打造的工具ID
		self.greenEquipComposeSuccess = 0.0		# 绿装打造成功率
		self.toolFreeNum = 0					# 储物柜可存储物品数量
		self.toolUnlockNum = 0					# 储物柜解锁格子数量
		self.recordToolNPCID = 0				# 工具打造NPCID 
		self.tripodComposeEndTime = 0.0			# 打造的乾坤鼎结束时间
		self.tripodComposeItemID = 0			# 正在打造的乾坤鼎ID
		self.tripodFreeNum = 0					# 储物柜可存储物品数量
		self.tripodUnlockNum = 0				# 储物柜解锁格子数量
		self.recordTripodNPCID = 0				# 乾坤鼎打造NPCID
#		self.reflashTime = 0					# 祈福时间上一个刷新时间
#		self.proyTimeList = []					# 祈福时间表
#		self.proyNum = 0						# 祈福次数

	def onNewDayLogin( self ):
		"""
		"""
		self.proyNum = 0
		
	def recordComposeTool( self, entityMB, dongfuType, composeType ):
		"""记录打造 entity"""
		if self.occupySpaceDF == dongfuType:
			if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
				self.recordTripodNPCID = entityMB.id
				if csdefine.LHMJ_BUIILD_QIAN_KU_DING in self.destroyBuilds:
					entityMB.onBuildDestroy( self )
				elif self.tripodComposeEndTime > time.time():
					entityMB.onComposeBegin( self )
			else:
				self.recordToolNPCID = entityMB.id
				if csdefine.LHMJ_BUIILD_GONG_FANG in self.destroyBuilds:
					entityMB.onBuildDestroy( self )
				if self.toolComposeEndTime > time.time():
					entityMB.onComposeBegin( self )
		
	def requestComposetDatas(self, composeType, npcTalkID ):
		"""请求打造相关数据"""
		self.ShopNPCID = npcTalkID
		if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			self.client.CLIENT_onRequestComposeData(csdefine.COMPOSE_TOOL_TRIPOD, int(self.tripodComposeEndTime), self.tripodComposeItemID, self.tripodUnlockNum, npcTalkID)
			return
		else:
			if self.toolComposeType == csdefine.COMPOSE_TOOL_NORMAL:
				self.client.CLIENT_onRequestComposeData(self.toolComposeType, int(self.toolComposeEndTime), self.toolComposeItemID, self.toolUnlockNum, npcTalkID)
			else:
				self.client.CLIENT_onRequestGEComposeData(self.toolComposeType, int(self.toolComposeEndTime), self.toolComposeItemID, self.toolUnlockNum, self.greenEquipComposeSuccess, npcTalkID)
			return
	
	def onRequestComposeData(self, composeType, endTime, itemID, freeNum, unlockNum, successRate ):
		"""
		Define Method
		请求回调
		"""
		if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			self.tripodComposeEndTime = endTime
			self.tripodComposeItemID = itemID
			self.tripodFreeNum = freeNum
			self.tripodUnlockNum = unlockNum
		else:
			self.toolComposeType = composeType
			self.toolComposeEndTime = endTime
			self.toolComposeItemID = itemID
			self.toolFreeNum = freeNum
			self.toolUnlockNum = unlockNum
		if composeType == csdefine.COMPOSE_TOOL_GREEN_EQUIP:
			self.greenEquipComposeSuccess = successRate * 100
	
	def CELL_composeTool( self, srcEntityID, composeType, toolID, useUnBind ):
		"""
		打造工具
		Exposed Method
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
			
		if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			if self.tripodComposeEndTime > time.time():			# 正在打造
				self.statusMessage( csstatus.TRIPOD_ONlY_COMPOSE_ONE_ITEM, "" )
				return
			if self.tripodFreeNum <= 0:
				self.statusMessage( csstatus.TRIPOD_IS_FULL_SHOULD_CLEAN, "" )
				return
		else:
			if self.toolComposeEndTime > time.time():
				self.statusMessage( csstatus.SHOP_ONlY_COMPOSE_ONE_ITEM, "" )
				return
			if self.toolFreeNum <= 0:
				self.statusMessage( csstatus.TRIPOD_IS_FULL_SHOULD_CLEAN, "" )
				return
		
		spaceType = self.occupySpaceDF
		buildLevel = self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_GONG_FANG )
		needLevel = g_ToolCompose.getToolComposeNeedLevel( toolID, composeType )
		if buildLevel < needLevel:
			self.statusMessage( csstatus.BUILD_LEVEL_NO_ENOUGH )
			return
		composeCost = g_ToolCompose.getToolComposeCost( toolID, composeType, spaceType, buildLevel )
		if composeCost is None:
			ERROR_MSG("Tool compose config is err!no toolID(%d)"%toolID)
			return
			
		successRate = 1.0
		if spaceType == csdefine.SPACE_TYPE_PUBLIC:
			successRate = g_ToolCompose.getComposeSuccessRate(buildLevel)		# 公用仙府，灵泉等级就是其他建筑等级
			
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_MONEY] = composeCost["money"]
		payItems[csdefine.TRADE_PAY_ITEM_LING_NENG] = composeCost["psionic"]
		if useUnBind:
			payType = csdefine.TRADE_PAY_ITEM_UNBIND_GOODS_BY_ID
			isBinded = 0
		else:
			payType = csdefine.TRADE_PAY_ITEM_GOODS_BY_ID
			isBinded = self.isBindedEquip( composeCost )
		payItems[payType] = composeCost["material"]
			
		self.requestPay( csdefine.TRADE_TYPE_COMPOSE_TOOL, 0, payItems, composeType, toolID, isBinded, successRate )
		
	def doComposeTool( self, composeType, equipID, isBinded, successRate ):
		"""开始打造工具"""
		endTime = g_ToolCompose.getToolComposeEndTime( equipID, composeType ) + time.time()
		if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			self.tripodComposeEndTime = endTime
			self.tripodComposeItemID = equipID
			self.recordTripodNPCID = self.ShopNPCID
			npc = KBEngine.entities.get( self.recordTripodNPCID )
			if npc:
				npc.onComposeBegin( self )
		else:
			self.toolComposeEndTime = endTime
			self.toolComposeItemID = equipID
			self.toolComposeType = composeType
			self.recordToolNPCID = self.ShopNPCID
			npc = KBEngine.entities.get( self.recordToolNPCID )
			if npc:
				npc.onComposeBegin( self )
			
		scheme = ComposeScheme(self.playerDBID, self.getName(), composeType, equipID, isBinded, endTime, successRate)
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].addToolComposeScheme(self.base, scheme )
		if composeType == csdefine.COMPOSE_TOOL_GREEN_EQUIP:
			self.greenEquipComposeSuccess = successRate * 100
			self.client.CLIENT_beginGEComposeTool(composeType, equipID, int(endTime), self.greenEquipComposeSuccess)
		else:
			self.client.CLIENT_beginComposeTool(composeType, equipID, int(endTime))
		
	def CELL_composeGreedEquip( self, srcEntityID, equipID, useUnBind, bPrintUID ):
		"""
		打造绿装
		Exposed Method
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.isPWKitBagLock():
			#处于背包上锁状态时，请求打开解锁界面
			self.client.CLIENT_openInputKBPW()
			return False
			
		if self.toolComposeEndTime > time.time():
			self.statusMessage( csstatus.SHOP_ONlY_COMPOSE_ONE_ITEM, "" )
			return
		if self.toolFreeNum <= 0:
			self.statusMessage( csstatus.TRIPOD_IS_FULL_SHOULD_CLEAN, "" )
			return
		bPrint = self.getItemInstByUid(int(bPrintUID))
		if not bPrint:
			KBEDebug.ERROR_MSG("Canot find item(uid:%s)"%bPrintUID)
			return
		
		spaceType = self.occupySpaceDF
		buildLevel = self.getLHMJBuildLevel( csdefine.LHMJ_BUIILD_GONG_FANG )
		needLevel = g_ToolCompose.getToolComposeNeedLevel( equipID, csdefine.COMPOSE_TOOL_GREEN_EQUIP )
		if buildLevel < needLevel:
			self.statusMessage( csstatus.BUILD_LEVEL_NO_ENOUGH )
			return
		composeCost = g_ToolCompose.getGreenComposeCost( equipID, bPrint.getSuitIndex(), spaceType, buildLevel )
		if composeCost is None:
			KBEDebug.ERROR_MSG("Tool compose config is err!no equipID(%d)"%equipID)
			return
		if composeCost["bluePrint"] != bPrint.id:
			KBEDebug.ERROR_MSG("Green equip compose err!!bprint(%d) is err bprint(%d)"%(composeCost["bluePrint"], bPrint.id))
			return
		equip = ItemFactory.ItemFactoryInst.createDynamicItem(equipID, 1, {"uid":0})
		if not equip.checkReqClasses( self ):
			self.statusMessage( csstatus.CANNOT_COMPOSE_OTHER_PROFESSION )
			return
		
		successRate = bPrint.getSuccessRate()
		successRate += g_ToolCompose.getComposeGreenEquipSuccessRate(spaceType, buildLevel)
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_MONEY] = composeCost["money"]
		payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_UID] = {int(bPrintUID):1}
		if useUnBind:
			payType = csdefine.TRADE_PAY_ITEM_UNBIND_GOODS_BY_ID
			isBinded = 0
		else:
			payType = csdefine.TRADE_PAY_ITEM_GOODS_BY_ID
			isBinded = self.isBindedEquip( composeCost ) or bPrint.isBinded()
		
		payItems[payType] = composeCost["material"]
		self.requestPay( csdefine.TRADE_TYPE_COMPOSE_TOOL, 0, payItems, csdefine.COMPOSE_TOOL_GREEN_EQUIP, equipID, isBinded, successRate )
		
	def onFinishCompose(self, composeType, bAddItem ):
		"""
		<Define method>
		完成打造回调
		"""
		if bAddItem:
			if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
				self.tripodFreeNum -= 1					# 更新储物柜的数据
			else:
				self.toolFreeNum -= 1
		if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			self.tripodComposeEndTime = 0.0
			self.tripodComposeItemID = 0
			npc = KBEngine.entities.get( self.recordTripodNPCID )
			if npc and npc.spaceID == self.spaceID:
				npc.onComposeEnd( self )
		else:
			self.toolComposeEndTime = 0.0
			self.toolComposeItemID = 0
			npc = KBEngine.entities.get( self.recordToolNPCID )
			if npc and npc.spaceID == self.spaceID:
				npc.onComposeEnd( self )
		
	def CELL_meltingEquip(self, srcEntityID, bPrintUID, equipUIDList):
		"""
		<Exposed Method>
		装备熔炼（提供图纸打造成功率）
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		bPrint = self.getItemInstByUid(int(bPrintUID))
		if not bPrint:
			KBEDebug.ERROR_MSG("Canot find item(uid:%s)"%bPrintUID)
			return
		equipID =  bPrint.getComposeEquipID()
		equip = ItemFactory.ItemFactoryInst.createDynamicItem(equipID, 1, {"uid":0})
		if not equip:
			KBEDebug.ERROR_MSG("Canot find item(id:%s)"%equipID)
			return
		
		level = int(equip.getLevelLv() * 10)
		quality = equip.getQuality()
		addRate = 0
		for uidStr in equipUIDList:
			equip = self.getItemInstByUid(int(uidStr))
			if equip:
				addRate += g_ToolCompose.getSuccessRate(level, quality, int(equip.getLevelLv() * 10), equip.getQuality() )
				self.removeItemByAmount( equip, 1, csdefine.ITEM_REMOVE_BY_SYS )
		addRate = bPrint.addSuccessRate(self, addRate)
		bPrint.setBindType( self )
		self.client.CLIENT_onMeltingtEquip( str(bPrintUID), float(addRate) )
		
	def CELL_requestPrayTimes( self, srcEntityID ):
		"""
		<exposed method>
		请求 祈福时间表
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		# 刷新祈福次数
		#if time.time() - self.reflashTime >= csconst.REFLASH_PROY_NUM:
		#	self.proyNum = 0
		# 刷新祈福时间表
		if time.time() - self.reflashTime >= csconst.REFLASH_PROY_TIME:
			self.reflashTime = time.time()
			self.proyTimeList = g_ToolCompose.getTimeItemsFromPool()
		
		self.client.CLIENT_OnRequestPrayTimes( self.proyTimeList, self.proyNum )
		
	def CELL_prayComposeTime( self, srcEntityID ):
		"""
		<Exposed method>
		祈福，减少绿装打造时间
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if self.toolComposeType != csdefine.COMPOSE_TOOL_GREEN_EQUIP:
			KBEDebug.ERROR_MSG("Canot pray compose!as compose type(%d) err!!"%self.toolComposeType)
			return
		if self.toolComposeEndTime <= time.time():			# 正在打造
			KBEDebug.ERROR_MSG("canot pray compose!!as nothing compose~")
			return
		if self.proyNum >= csconst.PROY_MAX_NUM:
			self.statusMessage( csstatus.CAN_NOT_PRAY_AGAIN, "" )
			return
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = g_ToolCompose.getPrayCost()
		self.requestPay( csdefine.TRADE_TYPE_PRAY_EQUIP, 0, payItems )
			
	def doPrayComposeTime( self ):
		"""开始祈福"""
		self.proyNum += 1
		_time = g_ToolCompose.getRandomTime( self.proyTimeList )
		self.toolComposeEndTime -= _time * 60
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].reduceComposeTime(self.playerDBID, _time * 60)
		self.client.CLIENT_OnPrayTime(_time)
		
	def CELL_quenchingEquip( self, srcEntityID, equipUID):
		"""
		<Exposed Method>
		淬炼装备
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		equipUID = int(equipUID)
		equip = self.getItemInstByUid(equipUID)
		if equip is None:
			KBEDebug.ERROR_MSG("Quenching err!!canot find item(uid=%d)!"%equipUID)
			return
		if not equip.canQuenching():
			self.statusMessage( csstatus.QUENCHING_EQUIP_FINISH, "" )
			return
			
		payItems = {}
		payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID] = {csconst.QUENCHING_EQUIP_COST_ITEM : 1}
		payItems[csdefine.TRADE_PAY_ITEM_MONEY] = csconst.QUENCHING_EQUIP_COST_MONEY
		equipType = equip.getEquipPart()
		if equipType in ItemTypeEnum.EQUIP_ARMOR:
			payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID].update({ csconst.QUENCHING_EQUIP_COST_ARMOR : 1})
		elif equipType in ItemTypeEnum.EQUIP_ALL_WEAPON:
			payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID].update( {csconst.QUENCHING_EQUIP_COST_WEAPON : 1})
		else:
			payItems[csdefine.TRADE_PAY_ITEM_GOODS_BY_ID].update( { csconst.QUENCHING_EQUIP_COST_ORNA : 1})
		self.requestPay( csdefine.TRADE_TYPE_QUENCHING_EQUIP, 0, payItems, equipUID )
		
	def beginQuenchingEquip( self, equipUID ):
		"""开始淬炼"""
		equip = self.getItemInstByUid(equipUID)
		equip.Quenching(self)
		self.client.CLIENT_OnQuenchingEquip( str(equipUID) )
		
	def CELL_requestTakeToolItem(self, srcEntityID, srcorder):
		"""
		<Exposed method>
		请求从储物柜取出物品
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		if ItemTypeEnum.BAG_WORK_SHOP_LOCKERS_START <= srcorder and srcorder <= ItemTypeEnum.BAG_WORK_SHOP_LOCKERS_END:
			composeType = csdefine.COMPOSE_TOOL_NORMAL
		elif ItemTypeEnum.BAG_ALCHEMIST_LOCKERS_START <= srcorder and srcorder <= ItemTypeEnum.BAG_ALCHEMIST_LOCKERS_END:
			composeType = csdefine.COMPOSE_TOOL_TRIPOD
		else:
			KBEDebug.ERROR_MSG("Take tool item err!err order(%d)"%srcorder)
			return
		freeOrder = self.getFreeOrderByItemInst( ItemTypeEnum.BAG_COMMON )
		if freeOrder is None:
			self.statusMessage( csstatus.NPCSHOP_BAG_ENOUGH )
			return
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO:return
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].requestTakeToolItem( self, self.playerDBID, composeType, srcorder )
		
	def onRequestTakeToolItem(self, composeType, item):
		"""
		<Define Method>
		从储物柜取物品回调
		"""
		if composeType == csdefine.COMPOSE_TOOL_TRIPOD:
			self.tripodFreeNum += 1
		else:
			self.toolFreeNum += 1
		self.addItem( item, csdefine.ITEM_ADD_BY_STORE_TOOL )
		
	def GM_finishCompose( self ):
		"""
		"""
		KBEngine.globalData["SpaceLunHuiMiJinMgr"].GM_finishCompose(self, self.playerDBID)
