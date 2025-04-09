import datetime
import json
import math
import random
import time

import Const
import Functions
import ItemFactory
import ItemSystemExp
import ItemTypeEnum
import KBEDebug
import KBEMath
import KBEngine
import QuestEventDefine
import csconst
import csdefine
import csstatus
from ItemSystemExp import g_equipIntensify
from KitBag import KitBagGridCost
from KitBag import StoreGridCost
from MsgLogger import g_logger
from RemainItemMailInfo import Datas as MailInfos


class RoleKitBagInterface:
	"""
	"""

	def __init__(self):
		# 普通背包格子容量（默认是可用的）
		self.commonCapacity = ItemTypeEnum.COMMONCAPACITY
		# 任务背包格子容量（默认是可用的）
		self.questCapacity = ItemTypeEnum.QUESTCAPACIRY
		# 晶石背包格子容量（默认是可用的）
		self.crystalCapacity = ItemTypeEnum.CRYSTALCAPACIRY
		# 普通背包可以解锁格子容量（默认是不可以用的）
		self.canUnLockCapacity = ItemTypeEnum.LOCKCAPACITY
		# 副本特殊专用背包已解锁的的格子数
		self.unLockSpaceCopyGridNum = 0
		self.itemLimitTimer = 0
		KBEDebug.INFO_MSG("kitbagPassword[%s], kbLockStatus[%d]" % (self.kitbagPassword, self.kbLockStatus))
		if self.kitbagPassword != "":
			self.setPWKitBagLock(csdefine.LOCK_KB_WITH_PW)

		if self.resetKBPWStatus != csdefine.RESET_KBPW_NONE:
			lefttime = self.requestresetKBPWTime + csdefine.RESET_KB_PW_TIMELIMIT - int(time.time())
			if lefttime <= 0:
				self.resetKBPWCB()
				return
			self.resetKBPWTimerID = self.addTimerCallBack(lefttime, "resetKBPWCB", ())
			d = 24 * 60 * 60  # 一天多少秒
			h = 60 * 60  # 一小时多少秒
			m = 60  # 一分钟多少秒
			day = int(lefttime) // d
			hour = (int(lefttime) // h) % 24
			minute = (int(lefttime) % h) // m
			second = int(lefttime) % m
			self.statusMessage(csstatus.CIB_MSG_RESET_KBPW_LEFTTIME, day, hour, minute, second)

	def initKitBagItems(self, roleState):
		"""
		初始化背包物品
		"""
		KBEDebug.DEBUG_MSG("initKitBagItem when role logonin!")
		self.initItemUseAmount()
		if roleState != csdefine.ROLE_STATE_CREATE:
			initList = []
			self.itemLimitTimes = {}
			for itemInst in self.itemsBag.values():
				# self.client.addItem(itemInst.getDictForClient(self), 0)
				if itemInst.isLimitTimeItem() and itemInst.getItemDir("Script") != "ItemStoreAppearance":
					self.itemLimitTimes[itemInst.uid] = int(itemInst.getItemEndTime())
				initList.append(itemInst.getDictForClient(self))

			self.client.kitbagInit(initList)

		self.destoryLimitTimeItems()

	def isPWKitBagLock(self):
		"""
		判断是背包是否处理于密码锁定
		True表示背包已经使用了安全锁加锁了
		False表示已经解开安全锁或未使用安全锁
		"""
		return self.kbLockStatus == csdefine.LOCK_KB_WITH_PW

	def setPWKitBagLock(self, status):
		"""
		设置背包锁的状态
		"""
		if status == self.kbLockStatus:
			KBEDebug.DEBUG_MSG("want to set same LockStatus[%d]!" % status)
			return
		self.kbLockStatus = status
		KBEDebug.DEBUG_MSG("setPWKitBagLock to set LockStatus[%d], old kbLockStatus[%d]!" % (status, self.kbLockStatus))
		# 设置Base上的kbLockStatus状态
		self.base.setPWKitBagLock(status)

	def isKitBagLock(self):
		"""
		判断背包是否锁定
		"""
		return self.isPWKitBagLock() or self.isSystemKitBagLock()

	def doKBOpratorCheck(self, item=None):
		"""
		背包中通用性操作的通用性检测
		只有蓝色品质以上的物品才会触发安全锁
		"""
		if self.isPWKitBagLock():
			if item:
				if item.getQuality() >= ItemTypeEnum.QUALITY_BLUE:
					KBEDebug.DEBUG_MSG("KitBag is Password Lock ,can't do someting!")
					# 通知客户端打开输入密码的对话框
					self.client.CLIENT_openInputKBPW()
					return csdefine.KB_OPRATOR_PW_LOCK
			else:
				KBEDebug.DEBUG_MSG("KitBag is Password Lock ,can't do someting!")
				# 通知客户端打开输入密码的对话框
				self.client.CLIENT_openInputKBPW()
				return csdefine.KB_OPRATOR_PW_LOCK
		if self.isSystemKitBagLock():
			KBEDebug.DEBUG_MSG("KitBag is System Lock ,can't do someting!")
			return csdefine.KB_OPRATOR_SYSTEM_LOCK
		return csdefine.KB_OPRATOR_CAN_GO

	def isSystemKitBagLock(self):
		"""
		判断系统是否锁定背包
		"""
		return self.systemKitBagLock

	def systemLockKitBag(self):
		"""
		系统锁定背包
		防止玩家进行背包操作
		"""
		self.systemKitBagLock = True

	def systemUnlockKitBag(self):
		"""
		系统解锁背包
		玩家可以进行背包操作
		"""
		self.systemKitBagLock = False

	def getItemInstByOrder(self, order):
		""""""
		return self.itemsBag[order]

	def getItemInstByUid(self, uid):
		"""
		根据物品uid获取物品实例
		"""
		order = self.itemsBag.getOrderID(uid)
		return self.itemsBag[order]

	def setItemLockState(self, uid, isLock):
		"""设置物品锁定状态"""
		itemInst = self.getItemInstByUid(uid)
		if itemInst:
			itemInst.setLock(isLock)

	def isItemLock(self, uid):
		"""物品是否被锁定"""
		itemInst = self.getItemInstByUid(uid)
		return itemInst.isLocking()

	def hasEnoughItem(self, itemID, amount):
		"""背包是否有足够物品"""
		itemList = self.getItemInstsByID(itemID)
		hasAmount = 0
		for item in itemList:
			hasAmount += item.getAmount()
		return hasAmount >= amount

	def addItemCheck(self, itemInst):
		"""
		添加物品检测
		返回csstatus.ITEM_GO_ON，表示可能添加
		"""
		gridNum = math.ceil(itemInst.getAmount() / itemInst.getMaxAmount())  # 需要的格子数量
		unlockItemList, lockItemList = self.itemsBag.getRelationItem(itemInst)
		# 数量限制
		if itemInst.hasLimitTaskAmount():
			tempList = []
			tempList.extend(unlockItemList)
			tempList.extend(lockItemList)
			amount = 0
			for item in tempList:
				amount += item.getAmount()
			if itemInst.getAmount() + amount > itemInst.getMaxTakeAmount():
				return csstatus.ITEM_IS_REACH_MAX_TAKE_LIMIT

		allOrder = self.getAllFreeOrder(itemInst.getKitBagType())
		if len(allOrder) >= gridNum:
			return csstatus.ITEM_GO_ON
		amount = itemInst.getAmount()
		if itemInst.isBinded():
			num = len(lockItemList)
			for item in lockItemList:
				amount += item.getAmount()
		else:
			num = len(unlockItemList)
			for item in unlockItemList:
				amount += item.getAmount()
		if math.ceil(amount / itemInst.overlyingMax) > num + len(allOrder):
			return csstatus.ITEM_SPACE_LESS
		return csstatus.ITEM_GO_ON

	def addItemListCheck(self, itemList):
		"""
		添加一组物品检测
		返回csstatus.ITEM_GO_ON，表示可能添加
		"""
		if not self.checkItemsLimit(itemList):
			return csstatus.ITEM_IS_REACH_MAX_TAKE_LIMIT
		if not self.checkItemsOrder(itemList):
			return csstatus.ITEM_SPACE_LESS
		return csstatus.ITEM_GO_ON

	def checkItemsLimit(self, itemList):
		"""检查一组物品的数量限制"""
		itemData = {}
		for item in itemList:
			if item.hasLimitTaskAmount():
				if not item.id in itemData:
					itemData[item.id] = 0
				itemData[item.id] += item.getAmount()
		if itemData:
			for item in self.itemsBag.values():
				if item.id in itemData:
					itemData[item.id] += item.getAmount()
					if itemData[item.id] > item.getMaxTakeAmount():
						return False
		return True

	def checkItemsOrder(self, itemList):
		"""检查背包位置"""
		_commonItems = []
		_questItems = []
		_sparItems = []
		_spaceCopyItems = []
		for itemInst in itemList:
			if itemInst.isQuestItem():
				_questItems.append(itemInst)
			elif itemInst.isSparItem():
				_sparItems.append(itemInst)
			elif itemInst.isSpaceCopyItem():
				_spaceCopyItems.append(itemInst)
			else:
				_commonItems.append(itemInst)
		canEnterCommon = self._allotBagOrder(_commonItems, ItemTypeEnum.BAG_COMMON)
		canEnterQuest = self._allotBagOrder(_questItems, ItemTypeEnum.BAG_QUEST)
		canEnterSpar = self._allotBagOrder(_sparItems, ItemTypeEnum.BAG_SPAR)
		canEnterSpace = self._allotBagOrder(_spaceCopyItems, ItemTypeEnum.BAG_SPACE_COPY)
		return canEnterCommon and canEnterQuest and canEnterSpar and canEnterSpace

	def _allotBagOrder(self, itemList, bagType):
		"""背包能否分配足够order"""
		if not itemList: return True
		freeNum = self.getAllFreeOrder(bagType)
		if len(freeNum) >= len(itemList):  # 如果有足够格子
			return True

		unStack = []  # 不可叠加
		isBindDict = {}  # 预添加的物品数据{itemID:amount}
		unBindDict = {}
		grid = 0  # 参与计算的格子数
		itemData = {}
		for item in itemList:
			if not item.canStack():
				unStack.append(item)
				continue
			itemData[item.id] = item
			if item.isBinded():
				if not item.id in isBindDict:
					isBindDict[item.id] = 0
				isBindDict[item.id] += item.getAmount()
			else:
				if not item.id in unBindDict:
					unBindDict[item.id] = 0
				unBindDict[item.id] += item.getAmount()
		if len(unStack) > len(freeNum):  # 不可叠加的物品大于可分配格子
			return False

		for item in self.itemsBag.values():
			if item.isBinded() and item.id in isBindDict:
				isBindDict[item.id] += item.getAmount()
				grid += 1
			elif not item.isBinded() and item.id in unBindDict:
				unBindDict[item.id] += item.getAmount()
				grid += 1
		needGrid = 0
		for id, num in isBindDict.items():
			needGrid += math.ceil(num / itemData[id].getMaxAmount())
		for id, num in unBindDict.items():
			needGrid += math.ceil(num / itemData[id].getMaxAmount())
		return needGrid + len(unStack) <= grid + len(freeNum)

	def addItemByID(self, itemID, amount=1, reason=csdefine.ITEM_ADD_BY_SYS):
		"""
		添加物品
		根据物品ID和数量添加物品
		"""
		itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amount, {})
		if itemInst is None:
			return csstatus.ITEM_NOT_EXIST_MSG, None
		itemList = self.splitItemByItemStackAmount(itemInst)
		if len(itemList) == 1:
			return self.addItem(itemInst, reason), itemInst
		else:  # 添加多个物品
			return self.addItemList(itemList, reason), itemInst

	def addItemByIDList(self, itemIDList, amountList, reason=csdefine.ITEM_ADD_BY_SYS):
		"""
		添加物品
		根据物品ID和数量列表添加物品
		"""
		index = 0
		List = []
		itemInsts = []
		for itemID in itemIDList:
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(itemID, amountList[index], {})
			if itemInst is None:
				return csstatus.ITEM_NOT_EXIST_MSG, None
			itemList = self.splitItemByItemStackAmount(itemInst)
			if len(itemList) == 1:
				result = self.addItemCheck(itemList[0])
			else:
				result = self.addItemListCheck(itemList)
			if result != csstatus.ITEM_GO_ON:
				return result, None
			index += 1
			List.append(itemList)
			itemInsts.append(itemInst)
		for i in List:
			if len(i) == 1:
				self.addItem(i[0], reason)
			else:
				self.addItemList(i, reason)
		return csstatus.ITEM_GO_ON, itemInsts

	def addItemList(self, itemList, reason):
		"""
		添加一组物品
		"""
		tempList = []
		for item in itemList:
			tempList.extend(self.splitItemByItemStackAmount(item))
		result = self.addItemListCheck(tempList)
		if result == csstatus.ITEM_GO_ON:
			for item in tempList:
				self.addItem(item, reason)
		return result

	def splitItemByItemStackAmount(self, itemInst):
		"""
		根据叠加数量上限来拆分物品
		"""
		itemInstList = []
		if itemInst.getAmount() <= itemInst.getMaxAmount():
			itemInstList.append(itemInst)
			return itemInstList
		tempAmount = itemInst.amount
		while tempAmount > 0:
			if tempAmount > itemInst.overlyingMax:
				amount = itemInst.overlyingMax
				tempAmount -= itemInst.overlyingMax
			else:
				amount = tempAmount
				tempAmount = 0
			item = ItemFactory.ItemFactoryInst.createDynamicItem(itemInst.id, amount)

			itemInstList.append(item)
		return itemInstList

	def addItem(self, itemInst, reason, order=""):
		"""
		添加物品,并给出提示信息
		"""
		# 为简化流程，此流程不会将超过堆叠上限的物品分割（如需要此功能，请使用addItemByID方法）
		assert itemInst.getAmount() <= itemInst.getMaxAmount(), "Please use addItemByID method!!"
		if itemInst is None:
			return csstatus.ITEM_NOT_EXIST_MSG

		unlockItemList, lockItemList = self.itemsBag.getRelationItem(itemInst)
		# 数量限制
		if itemInst.hasLimitTaskAmount():
			tempList = []
			tempList.extend(unlockItemList)
			tempList.extend(lockItemList)
			amount = 0
			for item in tempList:
				amount += item.getAmount()
			if itemInst.getAmount() + amount > itemInst.getMaxTakeAmount():
				return csstatus.ITEM_IS_REACH_MAX_TAKE_LIMIT
		if itemInst.isLimitTimeItem() and itemInst.getItemDir("Script") != "ItemStoreAppearance":
			itemInst.setLimitTimeData()
		if not itemInst.isLimitTimeItem():
			if itemInst.isBinded() and lockItemList:
				return self._addItemByStack(lockItemList, itemInst, reason)
			elif not itemInst.isBinded() and unlockItemList:
				return self._addItemByStack(unlockItemList, itemInst, reason)
		return self._addItemWithNewGrid(itemInst, itemInst.getAmount(), reason)

	def _addItemByStack(self, itemList, itemInst, reason):
		"""叠加方式添加物品"""
		amount = itemInst.amount
		for item in itemList:
			if not item.canStack(): continue
			if item.amount + amount <= item.overlyingMax:
				item.setAmount(self, item.amount + amount)
				amount = 0
			else:
				amount = item.amount + amount - item.overlyingMax
				item.setAmount(self, item.overlyingMax)
		if amount:  # 如果还没有叠加完
			srcAmount = itemInst.getAmount()
			itemInst.setAmount(None, amount)
			return self._addItemWithNewGrid(itemInst, srcAmount, reason)
		else:
			self.onAddItem(itemInst, itemInst.getAmount(), reason)
			return csstatus.ITEM_GO_ON

	def _addItemWithNewGrid(self, itemInst, amount, reason):
		"""
		采用新格子来放物品
		"""
		itemOrder = self.getFreeOrderByItemInst(itemInst.getKitBagType())
		if itemOrder is None:
			return csstatus.ITEM_SPACE_LESS
		itemInst.setOrder(itemOrder)
		itemInst.setOwner(self)
		self.itemsBag.addItem(itemInst)
		self.client.addItem(itemInst.getDictForClient(self), reason)
		self.onAddItem(itemInst, amount, reason)
		return csstatus.ITEM_GO_ON

	def onAddItem(self, itemInst, amount, reason):
		"""添加物品回调"""
		self.addItemUseAmount(itemInst)
		KBEDebug.DEBUG_MSG("player[%d] add Item[%s] success" % (itemInst.ownerID, itemInst.id))
		ItemName = itemInst.getItemDir("ItemName")
		tempStr = ""
		colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
		# 事件ID没有单物品添加
		# 多个物品添加事件与单个物品添加事件 复用
		tempStr += "[@L{t='%s';m=chat_item:%s;cfc=%s}]" % (ItemName, self.packItemDynamicData(itemInst), colorStr)
		self.statusMessage(csstatus.CIB_MSG_GAIN_ITEMS, amount, tempStr)

		self.triggerQuestEvent(QuestEventDefine.EVENT_GET_ITEM, (itemInst.id, amount))  # 触发获取物品任务事件
		self.client.RefreshAroundBoxStatus(csdefine.SPELL_BOX_LISTEN_EVENT_ADD_ITEM)  # 刷新箱子的状态
		self.spaceEvent_roleADDItem(itemInst.id)  # 触发副本事件
		self.triggerSkillEvent(csdefine.SKILL_EVENT_ADDITEM, self.id, {"itemID": itemInst.id})
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onPlayerGetItem(spaceEntity, self, itemInst.id, amount)  # 触发获取物品副本阶段目标
		if itemInst.isLimitTimeItem() and itemInst.getItemDir("Script") != "ItemStoreAppearance":
			self.onAddLimitTimeItem(itemInst)

		# 从商城买的外观商品购买时自动帮其穿上
		if reason == csdefine.ITEM_ADD_BY_SHOPMALLTRADE and itemInst.getItemDir("Script") == "ItemStoreAppearance":
			useResult = itemInst.checkUse(self)
			if useResult == csstatus.ITEM_USE_GO_ON_MSG:
				itemInst.use(self, self)
			if useResult != csstatus.ITEM_USE_GO_ON_MSG and useResult != None:
				self.statusMessage(useResult)

		# 添加日志
		g_logger.itemAddLog(self.playerDBID, self.getName(), itemInst.id, itemInst.uid, itemInst.getItemDir("ItemName"),
							amount, self.grade, reason, itemInst)

	def packItemDynamicData(self, itemInst):
		"""打包物品动态数据用于客户端超链接tips显示"""
		if itemInst.isEquip():
			data = {
				"id": str(itemInst.id),
				"uid": str(itemInst.uid),
				"amount": str(itemInst.amount),
				"bindType": str(itemInst.bindType),
				"hardiness": str(itemInst.dynamicData["hardiness"]),
				"combatPower": str(itemInst.dynamicData["combatPower"]),
				"attackProperties": itemInst.dynamicData["attackPropertiesStr"].replace("|", "_"),
				"attachProperties": itemInst.dynamicData["attachPropertiesStr"].replace("|", "_"),
				"intensifyData": itemInst.dynamicData["intensifyDataStr"].replace("|", "_")
			}
		else:
			data = {
				"id": str(itemInst.id),
				"uid": str(itemInst.uid),
				"amount": str(itemInst.amount),
				"bindType": str(itemInst.bindType)
			}
		return json.dumps({"ROOT": data}).replace('"', "/")

	def CELL_unWieldEquip(self, srcEntityID, srcorder):
		"""
		<Exposed method>
		客户端卸载装备
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if self.isSystemKitBagLock():
			self.statusMessage(csstatus.ITEMBAG_LOCKED, "")
			return
		srcorder = int(srcorder)
		
		#临时装备卸载到副本背包
		bagType = self.getBagTypeByOrder(srcorder)
		if bagType == ItemTypeEnum.BAG_TEMP_EQUIP:
			dstorder = self.getFreeOrderByItemInst(ItemTypeEnum.BAG_SPACE_COPY)
		else:
			dstorder = self.getFreeOrderByItemInst(ItemTypeEnum.BAG_COMMON)

		itemInst = self.itemsBag[srcorder]
		if not (itemInst and itemInst.isEquip() or bagType==ItemTypeEnum.BAG_TEMP_EQUIP):
			return

		if self.isState(csdefine.ENTITY_STATE_FIGHT):
			self.statusMessage(csstatus.CAN_NOT_EQUIP_IN_COMBAT)
			return

		if dstorder == None:
			self.statusMessage(csstatus.BAG_NOT_ENOUGHSPACE, "")
			return
		self.CELL_swapItem(self.id, srcorder, dstorder)

	def updateOneDataToClient(self, propertyname, propertyvalue, itemInst):
		"""
		更新一条属性到客户端
		"""
		uid = str(itemInst.uid)
		type_ = type(propertyvalue)
		if type_ == type(1):  # 整形
			type_ = "INT"
		elif type_ == type(1.0):  # 浮点数
			type_ = "FLOAT"
		elif type_ == type(""):  # 字符串
			type_ = "STRING"
		elif type_ == type(True):  # 字符串
			type_ = "BOOL"
		else:  # 其它
			type_ = "STRING"
		value = type_ + "|#|" + uid + "|#|" + propertyname[0].upper() + propertyname[1:] + "|#|" + str(propertyvalue)
		self.client.CLIENT_SetFStringPropertyByKey("DynamicProperty", value)

	def removeItemByAmount(self, itemInst, amount, reason, isSendMessage=True, order=""):
		"""
		使用，删除物品都会走到这里。
		"""
		if itemInst is None:
			KBEDebug.ERROR_MSG("Remove item err!as item is None!")
			return False
		if amount > itemInst.getAmount():
			KBEDebug.ERROR_MSG("Remove Item err!as not enought amount(%d > %d)" % (amount, itemInst.getAmount()))
			return False
		if amount == itemInst.getAmount():
			self.itemsBag.removeByOrder(itemInst.order)
			if self.getClient():
				self.client.CLIENT_removeItem(itemInst.order)
		else:
			itemInst.setAmount(self, itemInst.amount - amount)
		if isSendMessage:
			tempStr = ""
			ItemName = itemInst.getItemDir("ItemName")
			colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
			tempStr += "[@L{t='%s';m=chat_item:%s;cfc=%s}]" % (
				ItemName, self.packItemDynamicData(itemInst), colorStr)
			if amount == 1 or itemInst.getAmount() == 1:
				self.statusMessage(csstatus.CIB_MSG_ITEM_LOST, tempStr)
			else:
				self.statusMessage(csstatus.CIB_MSG_ITEM_LOST_AMOUNT, amount, tempStr)
		self.onRemoveItem(itemInst, amount, reason)
		# 添加日志
		g_logger.itemDelLog(self.playerDBID, self.getName(), itemInst.id, itemInst.uid,
							itemInst.getItemDir("ItemName"), amount, self.grade, reason, order, itemInst)
		
		if reason in csdefine.PROP_USE_TYPE_DICT:
			rAmount = 0
			if itemInst.getAmount() > amount:
				rAmount = itemInst.getAmount() - amount
			g_logger.propLog(1, self.accountDBID, self.playerDBID, self.getLevel(), itemInst.id, itemInst.getItemDir("ItemName"), rAmount)
		
		return True

	def removeItemListByAmount(self, itemInstList, amount, reason, bindType=csdefine.ITEM_REMOVE_BY_IS_BIND, order=""):
		"""
		删除列表中物品的总数量为amount,使用之前需要自己判定是否有足够数量去扣除
		"""
		if amount <= 0: return
		if bindType == csdefine.ITEM_REMOVE_BY_IS_BIND:  # 优先消耗绑定物品，再消耗无绑定物品
			itemInstList.sort(key=lambda x: x.isBinded())
		elif bindType == csdefine.ITEM_REMOVE_BY_NOT_BIND:  # 优先消耗无绑定物品，再消耗绑定物品
			itemInstList.sort(key=lambda x: x.isBinded(), reverse=True)
		elif bindType in [csdefine.ITEM_REMOVE_BY_ONLY_IS_BIND,
						  csdefine.ITEM_REMOVE_BY_ONLY_NOT_BIND]:  # 只消耗绑定物品(无绑定物品)
			isBind = (bindType == csdefine.ITEM_REMOVE_BY_ONLY_IS_BIND)
			temp = itemInstList
			itemInstList = []
			for item in temp:
				if item.isBinded() == isBind:
					itemInstList.append(item)

		totalAmount = 0
		for item in itemInstList:
			totalAmount += item.getAmount()
		if totalAmount < amount: return False

		tempAmount = amount
		while len(itemInstList) > 0:
			item = itemInstList.pop()
			if amount <= item.getAmount():
				self.removeItemByAmount(item, amount, reason, False, order)
				tempStr = ""
				colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(item.getQuality(), "(255, 255, 255, 255)")
				tempStr += Const.MSG_FORMAT_COLOR_STRING % (colorStr, "[%s]" % item.getItemDir("ItemName"))
				self.statusMessage(csstatus.CIB_MSG_ITEM_LOST_AMOUNT, tempAmount, tempStr)
				return True
			else:
				self.removeItemByAmount(item, item.getAmount(), reason, False, order)
				amount -= item.getAmount()
		return False

	def removeItemsByItemID(self, itemID, amount, reason, bindType=csdefine.ITEM_REMOVE_BY_IS_BIND, order=""):
		"""
		删除指定
		"""
		itemList = self.getItemInstsByID(itemID)
		return self.removeItemListByAmount(itemList, amount, reason, bindType, order)

	def onRemoveItem(self, itemInst, amount, reason):
		"""
		移除物品回调
		"""
		self.triggerQuestEvent(QuestEventDefine.EVENT_REMOVE_ITEM, (itemInst.id, amount))
		if reason == csdefine.ITEM_REMOVE_BY_USE:
			self.triggerQuestEvent(QuestEventDefine.EVENT_REMOVE_ITEM_ON_USE, itemInst.id)
		self.triggerSkillEvent(csdefine.SKILL_EVENT_REMOVEITEM, self.id, {"itemID": itemInst.id})
		self.spaceEvent_roleRemoveItem(itemInst.id)  # 触发副本事件
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onPlayerRemoveItem(spaceEntity, self, itemInst.id, - amount)  # 触发获取物品副本阶段目标

	def CELL_requestRemoveItemByUID(self, srcEntityID, uid):
		"""
		<Exposed method>
		请求删除物品
		uid定义的是string 类型
		"""
		if not self.validateClientCall(srcEntityID):
			return
		uid = int(uid)
		item = self.getItemInstByUid(uid)
		if not item:
			KBEDebug.INFO_MSG("player[%d] want to remove item by uid[%d]" % (self.playerDBID, uid))
			return
		item.setLock(True)
		self.inquireMessage(csstatus.ITEM_DESTROY, [item.getItemDir("ItemName")], "replyRemoveItemByUID", uid)
		if self.getClient():
			self.client.CLIENT_OnSetGridEnabledByOrderID(item.order, False)

	def replyRemoveItemByUID(self, reply, uid):
		"""
		"""
		item = self.getItemInstByUid(uid)
		if not item:
			KBEDebug.INFO_MSG("player[%d] want to remove item by uid[%d]" % (self.playerDBID, uid))
			return
		item.setLock(False)
		if self.getClient():
			self.client.CLIENT_OnSetGridEnabledByOrderID(item.order, True)
		if reply:
			if self.getClient():
				self.client.OnBeforeRemoveItemBP(str(uid))

			if self.doKBOpratorCheck(item) != csdefine.KB_OPRATOR_CAN_GO:
				return
			if not item.isCanDestory():
				self.statusMessage(csstatus.ITEM_LIMITDESTORY)
				return

			if uid == self.getUsingItem():
				self.statusMessage(csstatus.CIB_MSG_CAN_REMOVE_ITEM_AS_USING)
				return
			self.removeItemByAmount(item, item.getAmount(), csdefine.ITEM_REMOVE_BY_DROP)

	def CELL_swapItem(self, srcEntityID, srcorder, dstorder):
		"""
		<Exposed method>
		srcorder和dstorder定义的是string 类型
		交换两个物品位置
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if srcorder == dstorder:  # 移动之后再放回
			return
		srcorder = int(srcorder)
		dstorder = int(dstorder)
		if not self.isValidKitBagIndex(dstorder):
			return
		srcitem = self.itemsBag[srcorder]
		if srcitem is None or srcitem.isLocking():  # 无原始位置物品时
			return
		if self.doKBOpratorCheck(srcitem) != csdefine.KB_OPRATOR_CAN_GO:
			return
		dstItem = self.itemsBag[dstorder]
		if dstItem and dstItem.isLocking():
			return
		if self.doKBOpratorCheck(dstItem) != csdefine.KB_OPRATOR_CAN_GO:
			return
		# 从装备拖曳到 背包
		if self.getBagTypeByOrder(srcorder) == ItemTypeEnum.BAG_EQUIP and dstItem:
			if dstItem.getEquipPart() != srcitem.getEquipPart() \
					or dstItem.checkUse(self) != csstatus.ITEM_USE_GO_ON_MSG:
				dstorder = self.getFreeOrderByItemInst(ItemTypeEnum.BAG_COMMON)

		#从副本临时装备到副本背包
		if self.getBagTypeByOrder(srcorder) == ItemTypeEnum.BAG_TEMP_EQUIP and dstItem:
			if dstItem.getEquipPart() != srcitem.getEquipPart() \
				or dstItem.checkUse(self) != csstatus.ITEM_USE_GO_ON_MSG:
				dstorder = self.getFreeOrderByItemInst(ItemTypeEnum.BAG_SPACE_COPY)

		if srcitem.isLimitTimeItem() and dstItem and dstItem.isLimitTimeItem():
			self.inquireMessage(csstatus.CIB_MSG_IS_STACK_LIMITTIME_ITEM, [], "synItemEndTime", srcorder, dstorder)
			return
		self.itemsBag.swapOrder(self, srcorder, dstorder)

	def synItemEndTime(self, isSyn, srcorder, dstorder):
		if isSyn:
			self.itemsBag.swapOrder(self, srcorder, dstorder)

	def CELL_splitItem(self, srcEntityID, uid, amount):
		"""
		<Exposed method>
		分开一个可叠加的道具。
		"""
		if not self.validateClientCall(srcEntityID):
			return
		amount = int(amount)
		srcitem = self.getItemInstByUid(int(uid))
		if srcitem is None or srcitem.isLocking():
			return
		if amount < 1 or srcitem.getAmount() - amount < 1:
			return
		if self.doKBOpratorCheck(srcitem) != csdefine.KB_OPRATOR_CAN_GO:
			return

		bagType = srcitem.getKitBagType()
		if bagType in [ItemTypeEnum.BAG_QUEST, ItemTypeEnum.BAG_SPAR]:
			self.statusMessage(csstatus.CIB_MSG_CANNOT_SPLIT_ITEM)
			return

		dstItem = ItemFactory.ItemFactoryInst.createDynamicItem(srcitem.id, amount)
		dstItem.setBindType(None, srcitem.bindType)
		result = self._addItemWithNewGrid(dstItem, amount, csdefine.ITEM_ADD_BY_SPLIT)
		if result != csstatus.ITEM_GO_ON:
			self.statusMessage(csstatus.CIB_MSG_FULL)
			return

		srcitem.setAmount(self, srcitem.amount - amount)

	def getItemInstsByItemClass(self, itemClass):
		"""
		根据物品脚本获取物品实例
		"""
		itemList = []
		for item in self.itemsBag.values():
			if item.__class__.__name__ == itemClass:
				itemList.append(item)
		return itemList

	def getBagTypeByOrder(self, itemorder):
		"""
		根据位置获取背包的类型
		"""
		if itemorder < ItemTypeEnum.BAG_COMMONSTART:
			return ItemTypeEnum.BAG_EQUIP
		elif itemorder < ItemTypeEnum.BAG_QUESTSTART:
			return ItemTypeEnum.BAG_COMMON
		elif itemorder < ItemTypeEnum.BAG_SPARSTART:
			return ItemTypeEnum.BAG_QUEST
		elif itemorder < ItemTypeEnum.BAG_STORESTART:
			return ItemTypeEnum.BAG_SPAR
		elif itemorder <= ItemTypeEnum.BAG_STOREEND:
			return ItemTypeEnum.BAG_STORE
		elif itemorder <= ItemTypeEnum.BAG_TONG_STORE_END:
			return ItemTypeEnum.BAG_TONG_STORE
		elif itemorder <= ItemTypeEnum.BAG_SPACECOPY_END:
			return ItemTypeEnum.BAG_SPACE_COPY  # 副本专用背包
		elif itemorder <= ItemTypeEnum.BAG_APPEARANCES_END:
			return ItemTypeEnum.BAG_APPEARANCE  # 外观隐藏背包
		elif itemorder <= ItemTypeEnum.BAG_TEMP_EQUIP_END:
			return ItemTypeEnum.BAG_TEMP_EQUIP  # 吃鸡副本临时装备背包
		return None

	def getItemInstsByID(self, itemID):
		"""
		根据itemID获取玩家身上的物品实例
		"""
		return self.itemsBag.getItemByID(itemID)

	def getItemInstsByIDList(self, idList):
		"""
		根据itemID获取玩家身上的物品实例
		"""
		return self.itemsBag.getItemByIDList(idList)

	def getEquipAttachProperties(self):
		"""
		获取装备的附加属性统计
		"""
		itemList = self.getItemListByKBType(ItemTypeEnum.BAG_EQUIP)
		result = {"_extra": {}, "_base": {}, "_percent": {}, "_value": {}}
		for item in itemList:
			if item.getHardiness() == 0: continue

			tempdict = item.getAttachPropertyDict()
			result = ItemSystemExp.combineEquipAttachProperties(tempdict, result)
		return result

	def calcItemListAmount(self, itemList):
		"""
		计算列表中物品的总数量
		"""
		amount = 0
		for item in itemList:
			amount += item.getAmount()
		return amount

	def getAllFreeOrder(self, kitbagType):
		"""获取某个背包的所有空闲位置"""
		start = 0
		end = 0
		freeOrder = []
		if kitbagType == ItemTypeEnum.BAG_COMMON:
			start = ItemTypeEnum.BAG_COMMONSTART
			end = ItemTypeEnum.BAG_COMMONSTART + ItemTypeEnum.COMMONCAPACITY + self.unLockGridNum - 1
		if kitbagType == ItemTypeEnum.BAG_QUEST:
			start = ItemTypeEnum.BAG_QUESTSTART
			end = ItemTypeEnum.BAG_QUESTEND
		if kitbagType == ItemTypeEnum.BAG_SPAR:
			start = ItemTypeEnum.BAG_SPARSTART
			end = ItemTypeEnum.BAG_SPAREND
		if kitbagType == ItemTypeEnum.BAG_SPACE_COPY:
			start = ItemTypeEnum.BAG_SPACECOPY_START
			end = ItemTypeEnum.BAG_SPACECOPY_START + self.unLockSpaceCopyGridNum - 1
		orderList = self.itemsBag.keys()
		for i in range(start, end + 1):
			if i not in orderList:
				freeOrder.append(i)
		return freeOrder

	def getFreeOrderByItemInst(self, kitbagType):
		"""
		根据物品实例获取物品空闲背包位置
		"""
		if kitbagType == ItemTypeEnum.BAG_COMMON:
			return self.getFreeOrder(ItemTypeEnum.BAG_COMMONSTART,
									 ItemTypeEnum.BAG_COMMONSTART + ItemTypeEnum.COMMONCAPACITY + self.unLockGridNum - 1)
		if kitbagType == ItemTypeEnum.BAG_QUEST:
			return self.getFreeOrder(ItemTypeEnum.BAG_QUESTSTART, ItemTypeEnum.BAG_QUESTEND)
		if kitbagType == ItemTypeEnum.BAG_SPAR:
			return self.getFreeOrder(ItemTypeEnum.BAG_SPARSTART, ItemTypeEnum.BAG_SPAREND)
		if kitbagType == ItemTypeEnum.BAG_SPACE_COPY:
			return self.getFreeOrder(ItemTypeEnum.BAG_SPACECOPY_START,
									 ItemTypeEnum.BAG_SPACECOPY_START + self.unLockSpaceCopyGridNum - 1)
		if kitbagType == ItemTypeEnum.BAG_SPACE_COPY_YXLM1:
			return self.getFreeOrder(ItemTypeEnum.BAG_SPACECOPY_YXLM1_START, ItemTypeEnum.BAG_SPACECOPY_YXLM1_END)
		if kitbagType == ItemTypeEnum.BAG_SPACE_COPY_YXLM2:
			return self.getFreeOrder(ItemTypeEnum.BAG_SPACECOPY_YXLM2_START, ItemTypeEnum.BAG_SPACECOPY_YXLM2_END)
		if kitbagType == ItemTypeEnum.BAG_SPACE_COPY_YXLM3:
			return self.getFreeOrder(ItemTypeEnum.BAG_SPACECOPY_YXLM3_START, ItemTypeEnum.BAG_SPACECOPY_YXLM3_END)
		if kitbagType == ItemTypeEnum.BAG_SPACE_COPY_YXLM4:
			return self.getFreeOrder(ItemTypeEnum.BAG_SPACECOPY_YXLM4_START, ItemTypeEnum.BAG_SPACECOPY_YXLM4_END)
		if kitbagType == ItemTypeEnum.BAG_APPEARANCE:
			return self.getFreeOrder(ItemTypeEnum.BAG_APPEARANCES_START, ItemTypeEnum.BAG_APPEARANCES_END)
		if kitbagType == ItemTypeEnum.BAG_TEMP_EQUIP:
			return self.getFreeOrder(ItemTypeEnum.BAG_TEMP_EQUIP_START, ItemTypeEnum.BAG_TEMP_EQUIP_END)

	def getFreeOrder(self, startIndex, endIndex):
		"""
		获取指定区间内的空闲格子
		"""
		if startIndex > endIndex:
			raise IndexError("startIndex[%d] less then endIndex[%d]" % (startIndex, endIndex))
		orderList = self.itemsBag.keys()
		for i in range(startIndex, endIndex + 1):
			if i not in orderList:
				return i
		return None

	def isValidKitBagIndex(self, index):
		"""是否合法的index"""
		if self.getBagTypeByOrder(index) == ItemTypeEnum.BAG_COMMON:
			# 背包需要验证格子的有效性
			if index < ItemTypeEnum.BAG_COMMONSTART or index > ItemTypeEnum.BAG_COMMONSTART + ItemTypeEnum.COMMONCAPACITY + self.unLockGridNum - 1:
				return False
		return True

	# -----------------------------------------------使用物品-------------------------------------------------------------
	def CELL_useItem(self, srcEntityID, uid, targetObjID):
		"""
		<Exposed method>
		使用物品
		uid: string
		targetObjID: string
		"""
		if not self.validateClientCall(srcEntityID):
			return

		if self.getCurrTradeState() > csdefine.TRADE_STATE_WAIT:
			self.statusMessage(csstatus.ITEM_IS_TRADING)
			return
		uid = int(uid)
		itemInst = self.getItemInstByUid(uid)
		if not itemInst:
			self.statusMessage(csstatus.ITEM_NOT_EXIST_MSG)
			return
		if self.doKBOpratorCheck(itemInst) != csdefine.KB_OPRATOR_CAN_GO:
			return
		if itemInst.isLocking():
			KBEDebug.ERROR_MSG("Use item fail!as item(%d) is locking!" % uid)
			return

		useResult = itemInst.checkUse(self)
		if useResult == csstatus.ITEM_USE_GO_ON_MSG:
			targetObj = None
			if targetObjID != "":
				targetObjID = int(targetObjID)
				targetObj = KBEngine.entities.get(targetObjID, None)
			useResult = itemInst.use(self, targetObj)
		if useResult != csstatus.ITEM_USE_GO_ON_MSG and useResult != None:
			self.statusMessage(useResult)

	def onUseItem(self, itemInst):
		"""在使用物品"""
		actForbid = self.getSkill(itemInst.skillID).getActForbid() if self.getSkill(itemInst.skillID) else None
		self.triggerSkillEvent(csdefine.SKILL_EVENT_REQUEST_ACTION, self.id,
							   {"requestType": csdefine.SKILL_EVENT_ACTION_TYPE_ITEM, "id": itemInst.id,
								"actForbid": actForbid})
		self.triggerQuestEvent(QuestEventDefine.EVENT_USE_ITEM, itemInst.id)
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onPlayerUseItem(spaceEntity, self, itemInst.id, 1)

	def onUseItemResult(self, itemInst, useResult):
		"""使用物品结果"""
		itemInst.onUseResult(self, useResult)

	def CELL_uesItemByShortcutBar(self, srcEntityID, itemID, targetObjID):
		"""
		<Exposed method>
		快捷栏使用物品规则
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if self.getCurrTradeState() > csdefine.TRADE_STATE_WAIT:
			self.statusMessage(csstatus.ITEM_IS_TRADING)
			return
		itemList = self.getItemInstsByID(itemID)
		itemList.sort(key=lambda x: x.isBinded())
		if not itemList:
			self.statusMessage(csstatus.ITEM_NOT_EXIST_MSG)
			return

		itemInst = None
		for item in itemList:
			if item.isLocking(): continue
			if self.doKBOpratorCheck(item) != csdefine.KB_OPRATOR_CAN_GO: continue
			itemInst = item
			break
		if itemInst is None: return

		useResult = itemInst.checkUse(self)
		if useResult == csstatus.ITEM_USE_GO_ON_MSG:
			targetObj = None
			if targetObjID:
				targetObj = KBEngine.entities.get(int(targetObjID), None)
			useResult = itemInst.use(self, targetObj)
		if useResult != csstatus.ITEM_USE_GO_ON_MSG and useResult != None:
			self.statusMessage(useResult)

	def CELL_useItemByPos(self, srcEntityID, uid, pos):
		"""
		<Exposed method>
		对位置使用物品
		"""
		if not self.validateClientCall(srcEntityID):
			return
		uid = int(uid)
		itemInst = self.getItemInstByUid(uid)
		if not itemInst:
			self.statusMessage(csstatus.ITEM_NOT_EXIST_MSG)
			return
		if self.doKBOpratorCheck(itemInst) != csdefine.KB_OPRATOR_CAN_GO:
			return
		if itemInst.isLocking():
			KBEDebug.ERROR_MSG("Use item fail!as item(%d) is locking!" % uid)
			return
		pos = KBEMath.Unreal2KBEnginePosition(pos)
		useResult = itemInst.checkUse(self)
		if useResult == csstatus.ITEM_USE_GO_ON_MSG:
			useResult = itemInst.useToPos(self, pos)
		if useResult != csstatus.ITEM_USE_GO_ON_MSG and useResult != None:
			self.statusMessage(useResult)

	def CELL_useItemByPosAndDir(self, srcEntityID, uid, pos, dir):
		"""
		<Exposed method>
		对位置 和朝向 使用物品
		"""
		if not self.validateClientCall(srcEntityID):
			return
		uid = int(uid)
		itemInst = self.getItemInstByUid(uid)
		if not itemInst:
			self.statusMessage(csstatus.ITEM_NOT_EXIST_MSG)
			return
		if self.doKBOpratorCheck(itemInst) != csdefine.KB_OPRATOR_CAN_GO:
			return
		if itemInst.isLocking():
			KBEDebug.ERROR_MSG("Use item fail!as item(%d) is locking!" % uid)
			return

		useResult = itemInst.checkUse(self)
		if useResult == csstatus.ITEM_USE_GO_ON_MSG:
			pos = KBEMath.Unreal2KBEnginePosition(pos)
			dir = KBEMath.Unreal2KBEngineDirection(dir)
			useResult = itemInst.useToPosAndDir(self, pos, dir)
		if useResult != csstatus.ITEM_USE_GO_ON_MSG and useResult != None:
			self.statusMessage(useResult)

	def CELL_useLevelGiftItem(self, srcEntityID, uid):
		"""
		<Exposed method>
		领取等级礼包
		"""
		if not self.validateClientCall(srcEntityID):
			return
		uid = int(uid)
		itemInst = self.getItemInstByUid(uid)
		if not itemInst:
			self.statusMessage(csstatus.ITEM_NOT_EXIST_MSG)
			return
		if itemInst.__class__.__name__ == "ItemLevelGift":
			useResult = itemInst.use(self, None)
			if useResult != csstatus.ITEM_USE_GO_ON_MSG and useResult != None:
				self.statusMessage(useResult)

	def showNextLevelGiftItem(self, reqLevel, itemIDs, amountList):
		self.client.CLIENT_ShowNextLevelGift(reqLevel, itemIDs, amountList)

	# ------------------------------解锁背包格子------------------------------
	def getItemNameByID(self, ItemID):
		"""
		通过物品ID获得物品名字
		"""
		itemInstList = self.getItemInstsByID(ItemID)
		tempStr = ""
		itemInst = None
		if len(itemInstList) >= 1:
			itemInst = itemInstList[0]
		else:
			itemInst = ItemFactory.ItemFactoryInst.createDynamicItem(ItemID)
		if itemInst:
			ItemName = itemInst.getItemDir("ItemName")
			colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
			tempStr += "[@L{t='%s';m=chat_item:%s;cfc=%s}]" % (ItemName, self.packItemDynamicData(itemInst), colorStr)
		return tempStr

	def CELL_unLockGrid(self, srcEntityID, index):
		"""
		<Exposed method>
		index:格子序号
		"""
		if not self.validateClientCall(srcEntityID):
			return

		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO:
			return

		index = int(index)
		self.unLockGrid(index)

	def unLockGrid(self, index):
		"""
		解锁背包格子
		"""
		Moneycost, ItemID, Itemcost, unLockNum, unLockIndex = self.calcSumUnLockGridCost(index)
		if Moneycost <= 0 and Itemcost <= 0:
			return
		if ItemID and Itemcost > 0:
			ItemName = self.getItemNameByID(ItemID)
			self.inquireMessage(csstatus.UNLOCK_GRID_ITEM_MONEY_COST,
								[Functions.moneyToStr(Moneycost), Itemcost, ItemName, unLockNum], "replyUnLockGrid",
								Moneycost, ItemID, Itemcost, unLockIndex)
		else:
			self.inquireMessage(csstatus.UNLOCK_MULTI_GRID_COST, [Functions.moneyToStr(Moneycost), unLockNum],
								"replyUnLockGrid", Moneycost, ItemID, Itemcost, unLockIndex)

	def replyUnLockGrid(self, reply, Moneycost, ItemID, Itemcost, index):
		if reply:
			if Itemcost > 0:
				itemInstList = self.getItemInstsByID(ItemID)
				totalAmount = 0
				for itemInst in itemInstList:
					totalAmount += itemInst.amount  # 需要物品来解锁时检测一下物品是否足够
				if totalAmount < Itemcost:
					ItemName = self.getItemNameByID(ItemID)
					self.statusMessage(csstatus.NOT_ITEM_UNLOCK_GRID, ItemName)
					return
			# 之前是消耗仙石，现在已修改为消耗金币，所以不需要调用base方法
			if self.subBindMoneyAndMoney(Moneycost, csdefine.MONEY_SUB_REASON_UNLOCK_GRID):
				self.unLockGridRemoveItem(Itemcost,ItemID)
				self.unLockGridCB(index, True)
				self.unLockGrid(index)
			else:
				self.unLockGridCB(index, False)

	def calcSumUnLockGridCost(self, index):
		"""
		计算解锁到第index个格子的总花费
		花费单位是仙石
		"""
		startindex = ItemTypeEnum.BAG_COMMONSTART + ItemTypeEnum.COMMONCAPACITY + self.unLockGridNum
		startLock = ItemTypeEnum.BAG_COMMONSTART + ItemTypeEnum.COMMONCAPACITY - 1
		Moneycost = 0
		ItemID = 0
		Itemcost = 0
		lockIndex = startindex - startLock
		gridCost = KitBagGridCost.Datas.get(int(lockIndex), {})
		Moneycost = gridCost["MoneyCost"]
		if gridCost["ItemID"] and gridCost["ItemCost"]:
			ItemID = gridCost["ItemID"]
			Itemcost = gridCost["ItemCost"]
		return Moneycost, ItemID, Itemcost, 1, startindex

	def unLockGridRemoveItem(self, itemcost, itemID=None):
		"""
		<define method>
		消耗完金钱后消耗物品
		之前已经检测过物品足够
		"""
		if itemcost > 0:
			if itemID:
				itemInstList = self.getItemInstsByID(itemID)  # CST-12384 北京测试提出--背包扩充问题 三种储物袋解锁
			# itemInstList = self.getItemInstsByID(Const.UnlockGrid_ITEMID) # 使用乾坤囊解锁
			self.removeItemListByAmount(itemInstList, itemcost, csdefine.ITEM_REMOVE_BY_UNLOCK_GRID)

	def unLockGridCB(self, index, isSuccess):
		"""
		<define method>
		base解锁格子的回调
		"""
		kbType = self.getBagTypeByOrder(index)
		start = 0
		if isSuccess:
			if kbType == ItemTypeEnum.BAG_COMMON:
				start = ItemTypeEnum.BAG_COMMONSTART + ItemTypeEnum.COMMONCAPACITY - 1
				self.unLockGridNum = index - start
			self.statusMessage(csstatus.UNLOCK_GRID_OR_STORE_SUCCESS, "背包", index - ItemTypeEnum.BAG_COMMONSTART + 1)
		else:  # 金钱不够，解锁失败
			self.statusMessage(csstatus.NOT_ENOUGH_MONEY_UNLOCK_GRID)

	def CELL_unLockStoreGrid(self, index, unLockGridNum):
		"""
		Define method
		解锁仓库格子
		"""
		kbType = self.getBagTypeByOrder(index)
		if kbType == ItemTypeEnum.BAG_STORE:
			moneyCost, itemID, itemCost, unLockNum, unLockIndex = self.calcSumUnLockStoreCost(index, unLockGridNum)
			if moneyCost <= 0: return
			if itemID and itemCost > 0:
				itemName = self.getItemNameByID(itemID)
				self.inquireMessage(csstatus.UNLOCK_GRID_ITEM_MONEY_COST,
									[Functions.moneyToStr(moneyCost), itemCost, itemName, unLockNum],
									"replyUnLockStore", moneyCost, itemID, itemCost, unLockGridNum, unLockIndex)
			else:
				self.inquireMessage(csstatus.UNLOCK_MULTI_GRID_COST, [Functions.moneyToStr(moneyCost), unLockNum],
									"replyUnLockStore", moneyCost, itemID, itemCost, unLockGridNum, unLockIndex)

	def replyUnLockStore(self, reply, moneyCost, itemID, itemCost, unLockGridNum, index):
		"""
		确认是否解锁仓库格子
		"""
		if reply:
			moneyCost_, itemID_, itemCost_, unLockNum, unLockIndex = self.calcSumUnLockStoreCost(index, unLockGridNum)
			if moneyCost_ != moneyCost or itemCost_ != itemCost: return
			if itemCost > 0:
				itemInstList = self.getItemInstsByID(itemID)
				totalAmount = 0
				for itemInst in itemInstList:
					totalAmount += itemInst.amount  # 需要物品来解锁时检测一下物品是否足够
				if totalAmount < itemCost:
					self.statusMessage(csstatus.NOT_ITEM_UNLOCK_GRID)
					return

			if self.subBindMoneyAndMoney(moneyCost, csdefine.MONEY_SUB_REASON_UNLOCK_GRID):
				self.unLockGridRemoveItem(itemCost,itemID)
				self.statusMessage(csstatus.UNLOCK_GRID_OR_STORE_SUCCESS, "仓库", unLockIndex)
				self.base.unLockStoreGridCB(unLockGridNum + unLockNum)
			else:
				self.statusMessage(csstatus.NOT_ENOUGH_MONEY_UNLOCK_GRID)

	def calcSumUnLockStoreCost(self, index, unLockGridNum):
		"""
		计算解锁到第index个格子的总花费
		花费单位是仙石
		"""
		startindex = ItemTypeEnum.BAG_STORESTART + ItemTypeEnum.STORE_CAPACITY + unLockGridNum
		startLock = ItemTypeEnum.BAG_STORESTART + ItemTypeEnum.STORE_CAPACITY - 1
		Moneycost = 0
		ItemID = 0
		Itemcost = 0
		lockIndex = startindex - startLock
		gridCost = StoreGridCost.Datas.get(int(lockIndex), {})
		Moneycost = gridCost["MoneyCost"]
		if gridCost["ItemID"] and gridCost["ItemCost"]:
			ItemID = gridCost["ItemID"]
			Itemcost = gridCost["ItemCost"]
		return Moneycost, ItemID, Itemcost, 1, startindex

	def getFreeRingWieldOrder(self):
		"""
		获取戒指的装备的ItemOrder
		"""
		left = self.itemsBag[ItemTypeEnum.EQUIP_RING]
		right = self.itemsBag[ItemTypeEnum.EQUIP_RING + 1]
		if not left:
			return ItemTypeEnum.EQUIP_RING
		if not right:
			return ItemTypeEnum.EQUIP_RING + 1
		# 戒指槽位已满，则按战斗力的大小进行替换，优先替换战斗力小的，战斗力相等，随机替换。
		if left.dynamicData["combatPower"] < right.dynamicData["combatPower"]:
			return ItemTypeEnum.EQUIP_RING
		elif left.dynamicData["combatPower"] > right.dynamicData["combatPower"]:
			return ItemTypeEnum.EQUIP_RING + 1
		else:
			return random.randint(ItemTypeEnum.EQUIP_RING, ItemTypeEnum.EQUIP_RING + 1)

	def getItemListByOrderRange(self, start, end):
		"""
		获取区间内的物品列表,注意结尾，这里会自动在end后面加1
		实际range的区间是range(start, end+1)
		"""
		result = []
		orderList = self.itemsBag.keys()
		for order in range(start, end + 1):
			if order in orderList:
				result.append(self.itemsBag[order])
		return result

	def getItemListByKBType(self, kbType):
		"""
		获取各类型背包的所有物品
		"""
		if kbType == ItemTypeEnum.BAG_EQUIP:
			return self.getItemListByOrderRange(ItemTypeEnum.BAG_EQUIPSTART, ItemTypeEnum.BAG_EQUIPEND)
		elif kbType == ItemTypeEnum.BAG_COMMON:
			return self.getItemListByOrderRange(ItemTypeEnum.BAG_COMMONSTART, ItemTypeEnum.BAG_COMMONEND)
		elif kbType == ItemTypeEnum.BAG_QUEST:
			return self.getItemListByOrderRange(ItemTypeEnum.BAG_QUESTSTART, ItemTypeEnum.BAG_QUESTEND)
		elif kbType == ItemTypeEnum.BAG_SPAR:
			return self.getItemListByOrderRange(ItemTypeEnum.BAG_SPARSTART, ItemTypeEnum.BAG_SPAREND)
		elif kbType == ItemTypeEnum.BAG_SPACE_COPY:
			return self.getItemListByOrderRange(ItemTypeEnum.BAG_SPACECOPY_START, ItemTypeEnum.BAG_SPACECOPY_END)
		elif kbType == ItemTypeEnum.ITEM_TYPE_COPY_YXWZ1:
			return self.getItemListByOrderRange(ItemTypeEnum.BAG_SPACECOPY_YXLM1_START,
												ItemTypeEnum.BAG_SPACECOPY_YXLM1_END)
		elif kbType == ItemTypeEnum.BAG_APPEARANCE:
			return self.getItemListByOrderRange(ItemTypeEnum.BAG_APPEARANCES_START, ItemTypeEnum.BAG_APPEARANCES_END)
		elif kbType == ItemTypeEnum.BAG_TEMP_EQUIP:
			return self.getItemListByOrderRange(ItemTypeEnum.BAG_TEMP_EQUIP_START, ItemTypeEnum.BAG_TEMP_EQUIP_END)
		else:
			return []

	def doStackItems(self, items):
		"""
		根据叠加上限，自动叠加可以叠加的物品
		策略：找出可以叠加的物品
			根据最高叠加物品，直接设置几个为最大叠加数量，剩余的全给另外一个物品，多余的物品就删除
		"""
		result = {True: {}, False: {}}  # True的value表示是绑定的物品数据，False表示的是未绑定的物品数据
		if not items:    return
		# 找出可以叠加的物品
		for item in items:
			if item.canStack() and not item.isLocking():
				isbind = item.isBinded()
				if item.id not in result[isbind]:
					result[isbind].update({item.id: [item]})
				else:
					result[isbind][item.id].append(item)
		# 去掉只有绑定和不绑定的字典中，同一id的列表中只有一个物品的（因为一个物品不能进行叠加操作）
		for isbind, value in result.items():
			for itemid, itemlist in value.items():
				if len(itemlist) != 1:
					# 进行叠加操作
					self.stackItemList(itemlist)
				else:
					pass

	# 只有一组物品的不能进行叠加处理
	# result[isbind].pop(itemid)

	def stackItemList(self, itemlist):
		"""
		叠加一个物品列表,目前仅用于整理
		"""
		itemGrids = len(itemlist)  # 物品格子数
		curListAmount = self.calcItemListAmount(itemlist)
		maxStackGrid = curListAmount // itemlist[0].getMaxAmount()  # 可以放满的格子数
		liftAmount = curListAmount % itemlist[0].getMaxAmount()  # 剩余的数量（不足放满一个格子的）
		KBEDebug.DEBUG_MSG("itemGrids[%d], curListAmount[%d], maxStackGrid[%d], liftAmount[%d], stackAmount[%d]" % (
			itemGrids, curListAmount, maxStackGrid, liftAmount, itemlist[0].getMaxAmount()))
		for index in range(0, itemGrids):
			if index < maxStackGrid:
				itemlist[index].setAmount(self, itemlist[index].getMaxAmount())  # 更新数量
			elif index == maxStackGrid:
				if liftAmount != 0:
					itemlist[index].setAmount(self, liftAmount)  # 更新数量
				else:
					self.itemsBag.removeByOrder(itemlist[index].order)
					self.client.CLIENT_removeItem(itemlist[index].order)
			else:
				self.itemsBag.removeByOrder(itemlist[index].order)
				self.client.CLIENT_removeItem(itemlist[index].order)

	def CELL_requestSortKitBag(self, srcEntityID, kbType):
		"""
		<exposed method>
		参数是背包类型，表示要排序那个背包
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if kbType == ItemTypeEnum.BAG_STORE:
			self.base.requestSortStoreBag()
			return

		items = self.getItemListByKBType(kbType)
		if not items:  # 空的背包不需要排序
			self.client.CLIENT_endSort()
			return
		# 只有在普通背包时，才需要处理叠加
		if kbType == ItemTypeEnum.BAG_COMMON:
			self.doStackItems(items)
			# 重新赋值，避免由于普通背包物品叠加导致删除物品的情况
			items = self.getItemListByKBType(kbType)
		oldorders = []
		neworders = []
		start = 0
		# 按获取的index从大到小排序
		items = sorted(items, key=lambda item: item.getSortIndex(), reverse=True)
		tempItem = []
		for item in items:
			if item.isLocking(): continue
			oldorders.append(item.order)
			tempItem.append(item)
			self.itemsBag.removeByOrder(item.order)

		allFreeOrder = self.getAllFreeOrder(kbType)
		for index, item in enumerate(tempItem):
			item.setOrder(allFreeOrder[index])
			neworders.append(allFreeOrder[index])
			self.itemsBag.addItem(item)

		# 通知客户端更新，把新旧orders列表发到客户端，让客户端处理表示的更新
		self.client.CLIENT_requestSortKitBagCB(kbType, oldorders, neworders)
		KBEDebug.DEBUG_MSG("kbType[%d], oldorders[%s], neworders[%s]" % (kbType, str(oldorders), str(neworders)))

	def CELL_requsetSetPW(self, srcEntityID, oldpassword, newpassword):
		"""
		<exposed method>
		设置密码
		"""
		if not self.validateClientCall(srcEntityID):
			return
		# 设置密码，并上锁
		if self.kitbagPassword == "":
			if newpassword == "":  # 新密码输入为空弹出提示“请输入新密码”
				self.statusMessage(csstatus.CIB_MSG_ENTER_NEW_KBPW)
			else:  # 新密码输入成功，设置背包锁密码为新密码，状态为“有密码未锁定”，并自动上锁关闭界面
				self.kitbagPassword = newpassword
				self.setPWKitBagLock(csdefine.UNLICK_KB_WITH_PW)
				self.CELL_LockKB(self.id)
		# 修改密码
		else:
			if oldpassword == self.kitbagPassword:
				self.kitbagPassword = newpassword
				# 如果背包原有密码再修改密码，新密码不输入则视为取消密码保护，状态设为“无密码未锁定”
				if newpassword == "":
					self.setPWKitBagLock(csdefine.UNLOCK_KB_WITHOUT_PW)
				else:
					self.statusMessage(csstatus.CIB_MSG_REFIX_PASSWORLD)
				self.client.CLIENT_hideKBLockWin()
				if self.resetKBPWStatus != csdefine.RESET_KBPW_NONE:
					self.CELL_cancelResetKBPW(self.id)  # 取消密码重置
			else:
				self.statusMessage(csstatus.CIB_MSG_UNLOCK_WRONGPW)

	def CELL_unLockKB(self, srcEntityID, password):
		"""
		<exposed method>
		解锁背包
		"""
		if not self.validateClientCall(srcEntityID):
			return
		# 上线两分钟内不能解锁
		if int(time.time()) - self.loginTime <= csdefine.UNLOCK_TIMELIMIT_LOGIN:
			self.statusMessage(csstatus.CIB_MSG_UNLOCK_LOGIN)
			return
		if self.kitbagPassword == "":
			self.setPWKitBagLock(csdefine.UNLOCK_KB_WITHOUT_PW)
			return
		if password == self.kitbagPassword:
			self.setPWKitBagLock(csdefine.UNLICK_KB_WITH_PW)
			if self.requestresetKBPWTime > 0:
				self.CELL_cancelResetKBPW(self.id)
			self.client.CLIENT_hideKBLockWin()
		else:
			self.statusMessage(csstatus.CIB_MSG_KBPW_WRONG)

	def CELL_LockKB(self, srcEntityID):
		"""
		<exposed method>
		背包上锁
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if self.kitbagPassword == "":    return
		if self.kbLockStatus == csdefine.LOCK_KB_WITH_PW:    return

		self.setPWKitBagLock(csdefine.LOCK_KB_WITH_PW)
		self.client.CLIENT_hideKBLockWin()

	def CELL_cancelPW(self, srcEntityID, password):
		"""
		<exposed method>
		取消密码
		"""
		if not self.validateClientCall(srcEntityID):
			return
		# 取消密码，并解锁
		if password == self.kitbagPassword:
			self.resetKBPWCB()
			self.client.CLIENT_hideKBLockWin()
		else:
			self.statusMessage(csstatus.CIB_MSG_KBPW_WRONG)

	def CELL_resetKBPW(self, srcEntityID):
		"""
		<exposed method>
		重置密码
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if self.resetKBPWStatus != csdefine.RESET_KBPW_NONE:
			self.statusMessage(csstatus.CIB_MSG_IN_RESET_KBPW)
			return
		self.requestresetKBPWTime = int(time.time())
		self.resetKBPWStatus = csdefine.RESET_KBPW_NOW
		self.resetKBPWTimerID = self.addTimerCallBack(csdefine.RESET_KB_PW_TIMELIMIT, "resetKBPWCB", ())
		self.statusMessage(csstatus.CIB_MSG_REQUEST_RESET_KBPW)
		self.client.CLIENT_hideKBLockWin()

	def resetKBPWCB(self):
		"""
		重置密码请求回调
		"""
		self.requestresetKBPWTime = 0
		self.resetKBPWTimerID = 0
		self.kitbagPassword = ""
		self.resetKBPWStatus = csdefine.RESET_KBPW_NONE
		self.setPWKitBagLock(csdefine.UNLOCK_KB_WITHOUT_PW)
		self.statusMessage(csstatus.CIB_MSG_RESET_KBPW_SUCCESS)

	def CELL_cancelResetKBPW(self, srcEntityID):
		"""
		Exposed method
		取消重置
		"""
		if not self.validateClientCall(srcEntityID):
			return
		self.requestresetKBPWTime = 0
		self.popTimer(self.resetKBPWTimerID)
		self.resetKBPWStatus = csdefine.RESET_KBPW_NONE
		self.resetKBPWTimerID = 0
		self.statusMessage(csstatus.CIB_MSG_RESET_KBPW_CANCEL)

	def getItemAmountByIDAndBindType(self, itemID, isBinded):
		"""
		获取同绑定类型物品的总数
		"""
		itemList = []
		for item in self.getItemInstsByID(itemID):
			if item.isBinded() == isBinded:
				itemList.append(item)
		return self.calcItemListAmount(itemList)

	def sortItemListByOrder(self, itemList):
		"""
		根据order进行排序
		"""
		orderList = []
		result = []
		for itemInst in itemList:
			orderList.append(self.itemsBag.getOrderID(itemInst.uid))
		if len(orderList) <= 0:
			return result
		orderList.sort()
		for order in orderList:
			result.append(self.itemsBag[order])
		return result

	def addItemUseAmount(self, itemInst):
		"""
		物品的使用限量
		useAmount[0] 代表刷新时间
		useAmount[1] 代表使用限量
		"""
		tempValue = []
		value = self.itemUseAmount.get(itemInst.id, None)
		if value == None and itemInst.useAmount != "":
			tempValue.append(int(time.mktime(datetime.date.today().timetuple()) * csconst.TIME_ENLARGE_MULTIPLE))
			tempValue.append(itemInst.useAmount[1])
			self.itemUseAmount[itemInst.id] = tempValue
			self.client.CLIENT_AddToItemUseAmountArray(itemInst.id, tempValue[1], str(tempValue[0]))

	def getItemUseAmount(self, itemID):
		"""
		获得物品的剩余使用限量
		"""
		value = self.itemUseAmount.get(itemID, None)
		if value != None:
			return value
		return None

	def initItemUseAmount(self):
		"""
		初始化背包物品的使用限量
		"""
		for itemID, itemUseAmountData in self.itemUseAmount.items():
			self.client.CLIENT_AddToItemUseAmountArray(itemID, itemUseAmountData[1], str(itemUseAmountData[0]))

	def reduceItemUseAmount(self, itemInst, amount=1):
		"""
		减少物品使用限量
		"""
		value = self.getItemUseAmount(itemInst.id)
		if value != None and value[1] >= amount:
			value[1] = value[1] - amount
			self.updateItemUseAmount(itemInst.id, value[1], value[0])

	def updateItemUseAmount(self, itemID, value, newRefreshTime):
		"""
		更新物品使用限量
		"""
		data = []
		data.append(int(newRefreshTime))
		data.append(value)
		self.itemUseAmount[itemID] = data
		self.client.CLIENT_UpdateItemUseAmount(itemID, value, str(int(newRefreshTime)))

	def setUnLockSpaceCopyGridNum(self, number):
		"""
		设置副本专用背包解锁的格子数
		"""
		self.unLockSpaceCopyGridNum = number
		if number == 0:  # 清除格子，对应的物品也要清除
			itemList = self.getItemListByKBType(ItemTypeEnum.BAG_SPACE_COPY)
			for item in itemList:
				self.itemsBag.removeByOrder(item.order)
				self.client.CLIENT_removeItem(item.order)

	# -----------------------------------------仓库----------------------------------------------------
	def CELL_requestSaveMoney(self, srcEntityID, money):
		"""
		<Exposed method>
		存入金币到仓库
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO: return
		money = int(money)
		if self.money < money:
			self.statusMessage(csstatus.STORE_NO_ENOUGHMONEY)
			return
		self.base.requestSaveMoney(money)

	def onRequestSaveMoney(self, money):
		"""
		define method
		存钱回调
		"""
		if money > 0:
			self.money -= money
			self.statusMessage(csstatus.STORE_MONEY, Functions.moneyToStr(money))

	def CELL_requestTakeMoney(self, srcEntityID, money):
		"""
		<Exposed method>
		从仓库里取钱
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO: return
		money = int(money)
		if self.money >= csconst.MONEY_MAX_AMOUNT:
			self.statusMessage(csstatus.ACCOUNT_CANT_GAIN_MONEY, "")
			return False
		if self.money + money >= csconst.MONEY_MAX_AMOUNT:
			self.statusMessage(csstatus.ACCOUNT_CANT_GAIN_MONEY, "")
			money = csconst.MONEY_MAX_AMOUNT - self.money
		self.base.requestTakeMoney(money)

	def onRequestTakeMoney(self, money):
		"""
		define method
		取钱回调
		"""
		if money > 0:
			self.addMoney(money, csdefine.MONEY_ADD_REASON_FROM_STORE)

	def CELL_requestSaveItem(self, srcEntityID, srcorder):
		"""
		<Exposed method>
		请求存物品到仓库
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO: return
		srcorder = int(srcorder)
		srcitem = self.itemsBag[srcorder]
		if not srcitem:  # 可能由于手速太快导致
			#			self.statusMessage( csstatus.ITEM_NOT_EXIST_MSG )
			return
		if srcitem.isLocking(): return
		if srcitem.isLimitTimeItem(): return
		if srcitem.isQuestItem() or srcitem.isSparItem() or srcitem.isSpaceCopyItem():
			self.statusMessage(csstatus.ITEM_CAN_NOT_STORE)
			return
		srcitem.setLock(True)
		self.base.requestSaveItem(srcorder, srcitem)

	def onRequestSaveItem(self, srcorder, dstorder, isSuccess):
		"""
		define method
		保存物品到仓库回调
		"""
		if isSuccess:
			itemInst = self.itemsBag[srcorder]
			self.itemsBag.removeByOrder(srcorder)
			if dstorder:
				# 交换物品
				self.client.CLIENT_swapItemFromBagToStore(srcorder, dstorder)
			else:
				# 处理仓库堆叠
				self.client.CLIENT_removeItem(srcorder)
			# 添加日志
			g_logger.itemTranStoreLog(self.playerDBID, self.getName(), itemInst.id, itemInst.uid,
									  itemInst.getItemDir("ItemName"), itemInst.amount, itemInst)
		else:
			itemInst = self.itemsBag[srcorder]
			if itemInst:
				itemInst.setLock(False)

	def CELL_requestTakeItem(self, srcEntityID, srcorder):
		"""
		<Exposed method>
		请求从仓库取出物品
		"""
		if not self.validateClientCall(srcEntityID):
			return
		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO: return
		srcorder = int(srcorder)
		self.base.requestTakeItem(srcorder)

	def onRequestTakeItem(self, srcorder, srcitem, isSuccess):
		"""
		define method
		从仓库取出物品回调
		"""
		if isSuccess and srcitem:
			if self._doStackItem(srcitem):
				self.client.CLIENT_removeStoreItem(srcitem.order)  # 如果是叠加效果，需要通知客户端删除仓库物品
				# 添加日志
				g_logger.itemTalkStoreLog(self.playerDBID, self.getName(), srcitem.id, srcitem.uid,
										  srcitem.getItemDir("ItemName"), srcitem.getAmount(), srcitem)
				return

			freeOrder = self.getFreeOrderByItemInst(srcitem.getKitBagType())
			if freeOrder:
				srcitem.setOrder(freeOrder)
				srcitem.setOwner(self)
				self.itemsBag.addItem(srcitem)
				self.client.CLIENT_swapItemFromBagToStore(freeOrder, srcorder)
				# 添加日志
				g_logger.itemTalkStoreLog(self.playerDBID, self.getName(), srcitem.id, srcitem.uid,
										  srcitem.getItemDir("ItemName"), srcitem.getAmount(), srcitem)
			else:
				self.statusMessage(csstatus.NPCSHOP_BAG_ENOUGH)
				self.base.onRequestTakeItemFail(srcorder, srcitem)

	def _doStackItem(self, itemInst):
		"""叠加单个物品到仓库"""
		if itemInst.canStack():
			itemList = []
			amount = itemInst.getAmount()
			for order, item in self.itemsBag.items():
				if item.id == itemInst.id and item.isBinded() == itemInst.isBinded() and item.canStack():
					itemList.append(item)
					amount += item.getAmount()
					if amount <= itemInst.getMaxAmount() * len(itemList):
						for item in itemList:
							if amount <= item.getMaxAmount():
								item.setAmount(self, amount)
							else:
								amount -= item.getMaxAmount()
								item.setAmount(self, item.getMaxAmount())
						return True
		return False

	def addItemToStoreClient(self, itemInst):
		"""
		define method
		添加物品到客户端仓库
		"""
		self.client.addStoreItem(itemInst.getDictForClient(self))

	def CELL_swapStoreItem(self, srcEntityID, srcorder, dstorder):
		"""
		Exposed method
		交换仓库物品位置
		"""
		if not self.validateClientCall(srcEntityID):
			return
		srcorder = int(srcorder)
		dstorder = int(dstorder)
		if srcorder == dstorder: return
		srcBagType = self.getBagTypeByOrder(srcorder)
		dstBagType = self.getBagTypeByOrder(dstorder)
		# 不支持，帮会仓库(任务背包)的物品放入玩家仓库
		if srcBagType == ItemTypeEnum.BAG_TONG_STORE or dstBagType == ItemTypeEnum.BAG_TONG_STORE:
			return
		if srcBagType == ItemTypeEnum.BAG_QUEST or dstBagType == ItemTypeEnum.BAG_QUEST:
			return

		if srcBagType == dstBagType:  # 仓库物品位置互换
			if srcBagType == ItemTypeEnum.BAG_STORE:
				self.base.swapItemAC(srcorder, dstorder)
				return

		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO: return
		if srcBagType == ItemTypeEnum.BAG_STORE:
			dstitem = self.itemsBag[dstorder]
			if dstitem:
				dstitem.setLock(True)
			self.base.swapItemFromStoreToBag(srcorder, dstorder, dstitem)
		elif dstBagType == ItemTypeEnum.BAG_STORE:
			srcitem = self.itemsBag[srcorder]
			if srcitem:
				srcitem.setLock(True)
			self.base.swapItemFromBagToStore(srcorder, dstorder, srcitem)

	def onStackItemToStore(self, bagOrder, bagItem):
		"""
		Define method
		仓库堆叠回调
		"""
		if bagItem:
			srcItem = self.itemsBag[bagOrder]
			srcItem.setLock(False)
			srcItem.setAmount(None, bagItem.amount)
		else:
			self.itemsBag.removeByOrder(bagOrder)
			self.client.CLIENT_removeItem(bagOrder)

	def onSwapItemToStore(self, srcorder, dstorder, dstitem):
		"""
		define method
		仓库与其他包括交换物品回调
		@param srcorder 背包order
		@param dstorder 仓库order
		@param dstitem  拖入背包的item
		"""
		srcitem = self.itemsBag[srcorder]
		if srcitem:
			self.itemsBag.removeByOrder(srcorder)
		if dstitem:
			dstitem.setLock(False)
			dstitem.setOrder(srcorder)
			dstitem.setOwner(self)
			self.itemsBag.addItem(dstitem)
		self.client.CLIENT_swapItemFromBagToStore(srcorder, dstorder)

	# -----------------------------------------------------------------------------------------------------
	def teleportByItem(self, point):
		"""
		玩家通过神行石来进行传送到指定的地点
		"""
		if self.getCurrTradeState() > csdefine.TRADE_STATE_WAIT:
			self.statusMessage(csstatus.ITEM_IS_TRADING)
			return

		if self.doKBOpratorCheck() != csdefine.KB_OPRATOR_CAN_GO:
			return

		itemInst = self.getItemInstsByID(Const.TELEPORTSTONE_ITEMID)
		if not itemInst:
			self.statusMessage(csstatus.CANNOT_TELEPORT_WITHOUT_STONE)
			return

		item = itemInst[0]
		useResult = item.checkUse(self)
		if useResult == csstatus.ITEM_USE_GO_ON_MSG:
			useResult = item.useToTeleport(self, point)

		if useResult != csstatus.ITEM_USE_GO_ON_MSG and useResult != None:
			self.statusMessage(useResult)

	# -----------------------------------------------------------------------------------------------------

	def getAllTypeBagFreeGridNum(self):
		"""获取各个背包的剩余格子数"""
		common_free = self.getAllFreeOrder(ItemTypeEnum.BAG_COMMON)
		quest_free = self.getAllFreeOrder(ItemTypeEnum.BAG_QUEST)
		spar_free = self.getAllFreeOrder(ItemTypeEnum.BAG_SPAR)
		copy_free = self.getAllFreeOrder(ItemTypeEnum.BAG_SPACE_COPY)
		return len(common_free), len(quest_free), len(spar_free), len(copy_free)

	def spiltRemainItemDatas(self, itemDatas):
		"""将剩余物品数量以4为单位进行分割，参见CST-7200"""
		if len(itemDatas) <= 4:
			return [itemDatas]
		else:
			return [itemDatas[i:i + 4] for i in range(0, len(itemDatas), 4)]

	def getMailInfo(self, remianType, titleKey):
		"""根据不同类型的奖励获取方式和内容关键字获取邮件的信息"""
		sender = MailInfos[remianType]["sender"]
		if remianType == csdefine.REMAIN_ITEM_GIFT or remianType == csdefine.REMAIN_ITEM_DROPBOX:
			title = MailInfos[remianType]["title"]
			content = MailInfos[remianType]["content"]
		else:
			title = MailInfos[remianType]["title"].replace("{0}", titleKey)
			content = MailInfos[remianType]["content"].replace("{0}", titleKey)
		return sender, title, content

	def sendRemainItemWithMail(self, itemList, remianType, reason, titleKey=""):
		"""向背包添加一组奖励物品，当背包已满时将剩余的未添加的物品用邮件发送给玩家"""
		common_num, quest_num, spar_num, copy_num = self.getAllTypeBagFreeGridNum()
		remianList = []

		for itemInst in itemList:
			if common_num > 0 and itemInst.getKitBagType() == ItemTypeEnum.BAG_COMMON:
				self.addItem(itemInst, reason)
				common_num -= 1
				continue
			elif quest_num > 0 and itemInst.getKitBagType() == ItemTypeEnum.BAG_QUEST:
				self.addItem(itemInst, reason)
				quest_num -= 1
				continue
			elif spar_num > 0 and itemInst.getKitBagType() == ItemTypeEnum.BAG_SPAR:
				self.addItem(itemInst, reason)
				spar_num -= 1
				continue
			elif copy_num > 0 and itemInst.getKitBagType() == ItemTypeEnum.BAG_SPACE_COPY:
				self.addItem(itemInst, reason)
				copy_num -= 1
				continue
			else:
				remianList.append(itemInst)

		sender, title, content = self.getMailInfo(remianType, titleKey)
		itemDatasList = self.spiltRemainItemDatas(remianList)
		for ItemDatas in itemDatasList:
			KBEngine.globalData["MailManager"].sendWithMailbox(None, self.base, self.getName(),
															   csdefine.MAIL_SENDER_TYPE_SYS, sender, title, content, 0,
															   0, ItemDatas, 0, 0)

	# ------------------------------------------------处理限时物品------------------------------------------------
	def onAddLimitTimeItem(self, itemInst):
		"""
		获得限时物品后
		"""
		self.itemLimitTimes[itemInst.uid] = int(itemInst.getItemEndTime())
		self.destoryLimitTimeItems()

	def destoryLimitTimeItems(self):
		"""
		定时销毁定时物品
		"""
		if len(self.itemLimitTimes) == 0:
			return
		dictList = sorted(self.itemLimitTimes.items(), key=lambda i: i[1], reverse=True)
		for i in dictList:
			if Functions.convertTime(i[1] - Functions.getTime(0.1)) <= 0:
				itemInst = self.getItemInstByUid(i[0])
				if itemInst and itemInst.isLimitTimeDestory():
					self.removeItemByAmount(itemInst, itemInst.amount, csdefine.ITEM_REMOVE_BY_LIMIT_TIME)
				self.itemLimitTimes.pop(i[0], None)
			else:
				if self.itemLimitTimer:
					self.popTimer(self.itemLimitTimer)
					self.itemLimitTime = 0
				self.itemLimitTimer = self.addTimerCallBack(Functions.convertTime(i[1] - Functions.getTime()),
															"destoryLimitTimeItems", ())
