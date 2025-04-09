# -*- coding: utf-8 -*-
import random, time
import Const
import csconst
import csdefine
import KBEDebug
import KBEngine
import Functions
import csstatus
from CoreObject import MgrPersistentObject
from ConfigObject.AuctionCfgLoader import g_AuctionCfgLoader
from RemainItemMailInfo import Datas as MailInfos
import MysqlUtility

#插入SQL
SQL_INSERT = "INSERT INTO tbl_AuctionOrders (sm_roleDBID, sm_auction_uid, sm_auction_orderId, sm_money, sm_pickup_status) VALUES ({}, {}, '{}', {}, {});"
#更新SQL
SQL_UPDATE = "UPDATE tbl_AuctionOrders SET sm_pickup_status = {} WHERE sm_auction_orderId = '{}' AND sm_pickup_status = {};"
#插入SQL
SQL_INSERT_AUCTION_RESULT = "INSERT INTO tbl_AuctionResultData (sm_itemUID, sm_itemID, sm_auction_roleName, sm_auction_roleDBID, sm_auction_money) VALUES ({}, {}, %s, {}, {});"

def getMailInfo(remianType, titleKey):
	"""
	根据不同类型的奖励获取方式和内容关键字获取邮件的信息
	"""
	sender = MailInfos[remianType]["sender"]
	if remianType == csdefine.REMAIN_ITEM_GIFT or remianType == csdefine.REMAIN_ITEM_DROPBOX:
		title = MailInfos[remianType]["title"]
		content = MailInfos[remianType]["content"]
	else:
		title = MailInfos[remianType]["title"].replace("{0}", titleKey)
		content = MailInfos[remianType]["content"].replace("{0}", titleKey)
	return sender, title, content

class CItemBase:
	"""
	"""
	def __init__(self, uid, roleAmount):
		"""
		"""
		self.uid = uid
		self.ownerDBID = 0
		self.max_roleDBID = 0		#当前出价/掷点数最大的玩家dbid
		self.hasPickUp = False
		self.roleAmount = roleAmount
		
	def isPickUp(self):
		"""
		是否已被拾取(掷点/竞拍)
		"""
		return self.hasPickUp
		
	def isMaxRole(self, roleDBID):
		"""
		是否是当前出价/掷点数最大的玩家
		"""
		return self.max_roleDBID == roleDBID
		
class CAuctionData(CItemBase):
	"""
	竞拍数据
	"""
	def __init__(self, uid, roleAmount):
		CItemBase.__init__(self, uid, roleAmount)
		self.round = 1				#竞拍轮数（有效报价才算一轮）
		self.lastAuctionDBID = 0	#最近一次出价的玩家dbid（包括放弃竞拍的情况）
		self.maxAuction_orderID = ""
		self.auctionData = {}
		
	def hasAuction(self, roleDBID):
		"""
		当前是否竞价
		"""
		return self.auctionData.get(roleDBID, -1) >= 0
		
	def auction(self, dropBox, money, auction_orderID, roleDBID, roleCellMB):
		"""
		竞拍
		"""
		if money <= 0:
			return False, 0, self.round
		
		#如果最近的一次竞价是自己，直接返回
		if self.max_roleDBID == roleDBID:
			roleCellMB.client.statusMessage(csstatus.DROPBOX_AUCTION_MAX_ROLE, "")
			return False, 0, self.round
		
		basePrice = self.auctionData.get(self.max_roleDBID, Const.AUCTION_BASE_PRICE)
		data = g_AuctionCfgLoader.getCfByIndex(self.round)
		if data: basePrice += int(basePrice * data["price"] / 100)
		if money < basePrice:	#出价低了
			roleCellMB.client.statusMessage(csstatus.DROPBOX_AUCTION_LOW_MONEY, "")
			return False, 0, self.round
		
		self.round += 1
		oldRoleDBID = self.max_roleDBID
		oldAuction_orderID = self.maxAuction_orderID
		oldMoney = self.auctionData.get(self.max_roleDBID, 0)
		self.max_roleDBID = roleDBID
		self.lastAuctionDBID = roleDBID
		self.auctionData[roleDBID] = money
		self.maxAuction_orderID = auction_orderID
		
		#出价成功的话，在下次倒计时走完之前，是不会结束竞价的
		#根据竞拍的轮数，重新进行倒计时
		data = g_AuctionCfgLoader.getCfByIndex(self.round)
		dropBox.countDown = data["time"] if data else 30
		
		#需要返还上家的竞拍押金
		dropBox.onTurnBackLastAuctionRoleMoney(str(self.uid), oldMoney, oldRoleDBID, oldAuction_orderID)
		self.checkAuction()
		
		return True, self.getNoAbandomRoleAmount(), self.round
		
	def abandomAuction(self, roleDBID, roleCellMB):	
		"""
		放弃竞拍
		"""
		#如果为0，意味着之前已经放弃
		money = self.auctionData.get(roleDBID, -1)
		if money == 0:
			return False
		
		#当前最高价是自己，不能放弃
		if self.max_roleDBID == roleDBID:
			return False
		
		#设置最近一次出价是谁
		self.lastAuctionDBID = roleDBID
		self.auctionData[roleDBID] = 0
		
		self.checkAuction()
		return True
		
	def getNoAbandomRoleAmount(self):
		"""
		获取当前竞拍/还未出价的玩家数目
		"""
		#统计已出价且未放弃竞拍的玩家数目
		amount = 0
		for _, money in self.auctionData.items():
			if money == 0:
				continue
			amount += 1
		
		#加上还未出价的玩家数目
		amount += self.roleAmount - len(self.auctionData)
		return amount
		
	def checkAuction(self):
		"""
		"""
		#如果还有人没有出价
		if len(self.auctionData) < self.roleAmount:
			return
		
		if self.getNoAbandomRoleAmount() <= 1:
			self.hasPickUp = True
		
	def getDict(self, roleDBID):
		"""
		"""
		return {
			"UID"					: str(self.uid),
			"round"					: self.round,
			"isPickUp"				: self.isPickUp(),
			"ownerDBID"				: str(self.ownerDBID),
			"maxAuctionDBID"		: str(self.max_roleDBID),
			"lastAuctionDBID"		: str(self.lastAuctionDBID),
			"selfMoney"				: self.auctionData.get(roleDBID, -1),
			"curAuctionRoleAmount"	: self.getNoAbandomRoleAmount(),
			"maxAuctionMoney"		: self.auctionData.get(self.max_roleDBID, Const.AUCTION_BASE_PRICE),
		}
		

class CRollDomData(CItemBase):
	"""
	掷点数据
	"""
	def __init__(self, uid, roleAmount):
		CItemBase.__init__(self, uid, roleAmount)
		self.randomData = {}
		
	def getMaxRoll(self):
		"""
		"""
		return self.randomData.get(self.max_roleDBID, -1)
		
	def rolldom(self, roleDBID, isGiveUp = False):
		"""
		掷点
		"""
		if roleDBID in self.randomData:
			return self.randomData[roleDBID]
		
		if not isGiveUp:
			times = 0
			temp = list(self.randomData.values())
			while True and times < 50:
				times += 1
				r = random.randint(1, 100)
				if r in temp: continue
				self.randomData[roleDBID] = r
				break
		
		#roll为0，放弃掷点
		if roleDBID not in self.randomData:
			self.randomData[roleDBID] = 0	
		
		self.checkRolldom(roleDBID)
		return self.randomData[roleDBID]
		
	def checkRolldom(self, roleDBID):
		"""
		"""
		if self.max_roleDBID <= 0:
			self.max_roleDBID = roleDBID
		elif roleDBID:
			if self.randomData[self.max_roleDBID] < self.randomData[roleDBID]:
				self.max_roleDBID = roleDBID
		
		if len(self.randomData) >= self.roleAmount:
			#标记已被拾取
			self.hasPickUp = True
			
			maxRoll = -1
			for dbid, roll in self.randomData.items():
				#roll为0，放弃掷点
				if roll > 0 and roll > maxRoll:
					maxRoll = roll
					self.ownerDBID = dbid
					#重新赋值，防止出错
					self.max_roleDBID = dbid
	
	def getDict(self, roleDBID):
		"""
		"""
		return {
			"UID"			: str(self.uid),
			"ownerDBID"		: str(self.ownerDBID),
			"isPickUp"		: self.isPickUp(),
			"maxRollDBID"	: str(self.max_roleDBID),
			"maxRoll"		: self.getMaxRoll(),
			"selfRoll"		: self.randomData.get(roleDBID, -1),	#，-1:还未掷点 0：已放弃掷点
		}

class CDropBox:
	"""
	宝箱数据
	"""
	def __init__(self, dropBoxMB, entityExtFlag, allocation, ownerDBIDs, items, key, mgr):
		"""
		"""
		self.id = dropBoxMB.id
		self.dropBoxMB = dropBoxMB
		self.entityExtFlag = entityExtFlag
		self.allocation = allocation
		self.ownerDBIDs = ownerDBIDs
		self.dropBoxItems = items
		self.roles = {}
		self.allocationItems = {}
		self.hasAllPickUp = False
		self.pickupList = list(self.dropBoxItems.keys())
		self.countDown = self.getDefaultCountDown()
		self.hasStartAuction = False
		
		self.key = key
		self.mgr = mgr
		
	def getDefaultCountDown(self):
		"""
		"""
		if self.isRolldomPickUp():
			return Const.ROLLDOM_COUNTDOWN_TIME
		if self.isAuctionPickUp():
			return Const.AUCTION_COUNTDOWN_TIME
		else:
			return 60
		
	def isAllPickUp(self):
		"""
		物品是否都已被拾取
		"""
		return self.hasAllPickUp
		
	def isRolldomPickUp(self):
		"""
		是否是掷点拾取
		"""
		if self.entityExtFlag == csdefine.ENTITY_FLAG_EXT_TONG_DROPBOX:
			return self.allocation == csdefine.TONG_PICKUP_TYPE_RALLDOM
		elif self.entityExtFlag == csdefine.ENTITY_FLAG_EXT_TEAM_DROPBOX:
			return self.allocation == csdefine.TEAM_PICKUP_TYPE_TEAM
		return False
		
	def isAuctionPickUp(self):
		"""
		是否是竞拍拾取
		"""
		if self.entityExtFlag == csdefine.ENTITY_FLAG_EXT_TONG_DROPBOX:
			return self.allocation == csdefine.TONG_PICKUP_TYPE_AUCTION
		elif self.entityExtFlag == csdefine.ENTITY_FLAG_EXT_TEAM_DROPBOX:
			return self.allocation == csdefine.TEAM_PICKUP_TYPE_AUCTION
		return False
		
	def checkPickUpItem(self, uid, roleDBID):
		"""
		"""
		if roleDBID not in self.ownerDBIDs:
			return False
		
		if uid not in self.dropBoxItems:
			return False
		
		#掷点
		if self.isRolldomPickUp():
			if uid not in self.allocationItems:
				self.allocationItems[uid] = CRollDomData(uid, len(self.ownerDBIDs))
				return True
			if self.allocationItems[uid].isPickUp():
				return False
			if roleDBID in self.allocationItems[uid].randomData:
				return False
			return True
		
		#竞拍
		if self.isAuctionPickUp():
			if uid not in self.allocationItems:
				self.allocationItems[uid] = CAuctionData(uid, len(self.ownerDBIDs))
				return True
			if self.allocationItems[uid].isPickUp():
				return False
			return True
		
		return False
		
	def onDropBoxDestroy(self):
		"""
		"""
		self.dropBoxMB = None
		
	def onDropBoxRegisterRole(self, roleDBID, roleName, roleBaseMB):
		"""
		"""
		if roleDBID not in self.ownerDBIDs: 
			return
		
		self.roles[roleDBID] = {"name" : roleName, "mb" : roleBaseMB}
		
	def onRoleDestroy(self, roleDBID):
		"""
		"""
		if roleDBID not in self.roles: return
		self.roles[roleDBID]["mb"] = None
		
	def onReqDropBoxData(self, roleDBID, roleCellMB):
		"""
		"""
		#客户端收不到数据，没必要继续下去
		if roleCellMB.client is None:
			return
		
		if roleDBID not in self.ownerDBIDs:
			return
		
		if self.isAllPickUp():
			return
		
		#里面的物品不能是礼包类型的物品，否则无法进行数据打包
		itemList = []
		for item in list(self.dropBoxItems.values()):
			itemList.append(item.getDictForClient(roleCellMB))
		ownersInfo = {"dictData" : []}
		for dbid, info in self.roles.items():
			data = {"key" : str(dbid), "value" : info["name"]}
			ownersInfo["dictData"].append(data)
		
		#打包一些基础数据，ID、分配方式、宝箱类型、拥有分配权限的玩家信息、宝箱中的物品
		roleCellMB.client.recvDropBoxData(self.id, self.entityExtFlag, self.allocation, ownersInfo, itemList)
		
		if self.isRolldomPickUp():
			self.onReqDropBoxRalldomData(roleDBID, roleCellMB)
		elif self.isAuctionPickUp():
			self.onReqDropBoxAuctionData(roleDBID, roleCellMB)
			
	def pickupItemToRole(self, uid, roleDBID):
		"""
		"""
		#通知箱子物品分配情况
		if self.dropBoxMB:
			self.dropBoxMB.onPickUpToRoleByMgr(str(uid), roleDBID)
		
		msg = ""
		roleID = 0
		roleName = ""
		itemInst = self.dropBoxItems[uid]
		if roleDBID > 0:
			roleID = self.roles[roleDBID]["mb"].id if self.roles[roleDBID]["mb"] else 0
			roleName = self.roles[roleDBID]["name"]
			msg = "{}|{}".format(self.getItemMsg(roleName, itemInst), str(itemInst.amount))
		
		msgID = csstatus.DROPBOX_TONG_GET_ITEM
		if self.entityExtFlag == csdefine.ENTITY_FLAG_EXT_TEAM_DROPBOX:
			msgID = csstatus.PICK_UP_ITEM_ROLE_GET_ITEM
		
		flag = False
		for dbid, role in self.roles.items():
			if role["mb"] and role["mb"].client:
				role["mb"].client.onPickupItemToRole(self.id, str(uid), str(roleDBID), roleID)
				
				if roleDBID > 0:
					role["mb"].client.statusMessage( msgID, msg )
			
			#如果是竞拍的话，加竞拍记录
			if self.isAuctionPickUp():
				if self.allocationItems[uid].hasAuction(dbid):
					if role["mb"] and role["mb"].cell:
						role["mb"].cell.onRecvAuctionData(str(uid), str(itemInst.id), roleName, roleDBID, self.allocationItems[uid].auctionData.get(roleDBID, 0))
					else:
						if self.mgr is None or flag: continue
						self.mgr.onRecvAuctionResultData(str(uid), str(itemInst.id), roleName, roleDBID, self.allocationItems[uid].auctionData.get(roleDBID, 0))
						flag = True
			
			#给物品
			if roleDBID == dbid:
				if role["mb"] and role["mb"].cell:
					role["mb"].cell.onPickupItemToRole(self.id, itemInst)
					continue
				
				#这里需要通过发送邮件的方式给到玩家
				sender, title, content = getMailInfo(csdefine.REMAIN_ITEM_DROPBOX, "")
				KBEngine.globalData["MailManager"].send( None, roleName, csdefine.MAIL_SENDER_TYPE_SYS, sender, title, content, 0, 0, [itemInst], 0, 0 )
			
	def onPickUpDropBoxEnd(self):
		"""
		"""
		#通知箱子物品分配完毕
		if self.dropBoxMB:
			self.dropBoxMB.onPickUpDropBoxEnd()
		
		#通知玩家移除箱子
		for _, role in self.roles.items():
			if role["mb"] and role["mb"].cell:
				role["mb"].cell.onPickUpDropBoxEnd(self.id)
		
	def getItemMsg(self, roleName, itemInst):
		"""
		"""
		colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(itemInst.getQuality(), "(255, 255, 255, 255)")
		tempStr = Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%itemInst.getItemDir("ItemName"))
		return roleName + "|" + tempStr
		
	def onTimeCallBack(self):
		"""
		"""
		if self.isRolldomPickUp():
			self.onAllRolldomEnd()
			return
		
		if self.isAuctionPickUp():
			self.onAuctionTimeEnd()
			return
	
	#--------------------------- 掷点 ---------------------------------------------
	
	def onReqDropBoxRalldomData(self, roleDBID, roleCellMB):
		"""
		打包掷点数据
		"""
		itemList = []
		for item in list(self.allocationItems.values()):
			itemList.append(item.getDict(roleDBID))
		
		#倒计时
		countDown = Functions.getTime(self.countDown)
		roleCellMB.client.recvDropBoxRalldomData(self.id, itemList, str(countDown))
		
	def onReqRollRandomDropBox(self, uid, roleDBID, roleCellMB):
		"""
		掷点
		"""
		uid = int(uid)
		if not self.isRolldomPickUp():
			return
		
		if not self.checkPickUpItem(uid, roleDBID):
			return
		
		roll = self.allocationItems[uid].rolldom(roleDBID, False)
		if roleCellMB and roleCellMB.client:
			roleCellMB.client.onRollRandomDropBox(self.id, str(uid), str(roleDBID), roll)
		
		#如果当前自己掷点数最大，发给所有玩家
		if self.allocationItems[uid].isMaxRole(roleDBID):
			for _, role in self.roles.items():
				if role["mb"] and role["mb"].client:
					role["mb"].client.onRollRandomMaxDropBox(self.id, str(uid), str(roleDBID), roll)
		
		#队伍宝箱的话，还需要有一些提示信息
		if self.entityExtFlag == csdefine.ENTITY_FLAG_EXT_TEAM_DROPBOX:
			msg = self.getItemMsg(self.roles[roleDBID]["name"], self.dropBoxItems[uid]) + "|" + str( roll )
			for _, role in self.roles.items():
				if role["mb"] and role["mb"].client:
					role["mb"].client.statusMessage(csstatus.PICK_UP_ITEM_ROLL_POINT, msg)
		
		#所有人都已掷点/放弃
		if not self.allocationItems[uid].isPickUp():
			return
		
		self.onNotifyRollMsg(uid)
		self.pickupItemToRole(uid, self.allocationItems[uid].ownerDBID)
		self.checkRolldomEnd()
		
	def onReqAbandomRollRandomDropBox(self, uid, roleDBID, roleCellMB, isSelfMake = True):
		"""
		放弃掷点
		"""
		uid = int(uid)
		if not self.isRolldomPickUp():
			return
		
		if not self.checkPickUpItem(uid, roleDBID):
			return
		
		roll = self.allocationItems[uid].rolldom(roleDBID, True)
		if roleCellMB and roleCellMB.client:
			roleCellMB.client.onRollRandomDropBox(self.id, str(uid), str(roleDBID), roll)
		
		#队伍宝箱的话，还需要有一些提示信息
		if isSelfMake and self.entityExtFlag == csdefine.ENTITY_FLAG_EXT_TEAM_DROPBOX:
			msg = self.getItemMsg(self.roles[roleDBID]["name"], self.dropBoxItems[uid])
			for _, role in self.roles.items():
				if role["mb"] and role["mb"].client:
					role["mb"].client.statusMessage(csstatus.PICK_UP_ITEM_ROLL_ABANDON, msg)
		
		#所有人都已掷点/放弃
		if not self.allocationItems[uid].isPickUp():
			return
		
		self.onNotifyRollMsg(uid)
		self.pickupItemToRole(uid, self.allocationItems[uid].ownerDBID)
		self.checkRolldomEnd()
		
	def onNotifyRollMsg(self, uid):
		"""
		"""
		if self.entityExtFlag == csdefine.ENTITY_FLAG_EXT_TEAM_DROPBOX:
			if self.allocationItems[uid].getMaxRoll() > 0:
				colorStr = Const.ITEM_NAME_QUALITY_COLORS.get(self.dropBoxItems[uid].getQuality(), "(255, 255, 255, 255)")
				tempStr = Const.MSG_FORMAT_COLOR_STRING%(colorStr, "[%s]"%self.dropBoxItems[uid].getItemDir("ItemName"))
				msg = self.roles[self.allocationItems[uid].max_roleDBID]["name"] + "|" + str( self.allocationItems[uid].getMaxRoll() ) + "|" + tempStr + "|" + str( self.dropBoxItems[uid].amount )
				
				for _, role in self.roles.items():
					if role["mb"] and role["mb"].client:
						role["mb"].client.statusMessage(csstatus.PICK_UP_ITEM_ROLL_MAX_POINT, msg)
		
	def checkRolldomEnd(self):
		"""
		检查是否需要结束掷点
		"""
		#倒计时还未结束，
		if self.countDown > 0:
			#还有物品没人开始掷点
			if len(self.dropBoxItems) > len(self.allocationItems):
				return
			
			#还有物品没有确定归属（某些物品只有部分人掷点了）
			for _, item in self.allocationItems.items():
				if not item.isPickUp():
					return
				
			self.hasAllPickUp = True
			return
		
		#等所有物品中未掷点的玩家设置为放弃,再设置全部被拾取的标识
		if len(self.dropBoxItems) > len(self.allocationItems):
			return
		
		self.hasAllPickUp = True
		
	def onAllRolldomEnd(self):
		"""
		"""
		self.countDown -= 1
		if self.countDown > 0: 
			return
		
		#所有物品中未掷点的玩家设置为放弃
		for uid, item in self.dropBoxItems.items():
			for dbid in self.ownerDBIDs:
				self.onReqAbandomRollRandomDropBox(uid, dbid, None, False)
		
	#----------------------------- 竞拍 ----------------------------------------------
	
	def startAuction(self):
		"""
		开启竞拍
		"""
		if self.hasStartAuction:
			return
		
		pickupList = []
		for uid in self.pickupList:
			pickupList.append(str(uid))
		
		#设置标记，并通知客户端开拍
		self.hasStartAuction = True
		countDown = Functions.getTime(self.countDown)
		for _, role in self.roles.items():
			if role["mb"] and role["mb"].client:
				role["mb"].client.onStartAuction(self.id, pickupList, str(countDown))
		
	def onReqDropBoxAuctionData(self, roleDBID, roleCellMB):
		"""
		打包竞拍数据
		"""
		for uid in list(self.dropBoxItems.keys()):
			if uid in self.allocationItems: continue
			self.allocationItems[uid] = CAuctionData(uid, len(self.ownerDBIDs))
		
		itemList = []
		for item in list(self.allocationItems.values()):
			itemList.append(item.getDict(roleDBID))
		pickupList = []
		for uid in self.pickupList:
			pickupList.append(str(uid))
		
		#倒计时
		countDown = Functions.getTime(self.countDown)
		roleCellMB.client.recvDropBoxAuctionData(self.id, itemList, pickupList, str(countDown))
		
		#如果是当前的正在拍卖，通知客户端
		if self.hasStartAuction:
			roleCellMB.client.onStartAuction(self.id, pickupList, str(countDown))
		
	def onReqAuctionDropBox(self, uid, money, roleDBID, auction_orderID, roleCellMB):
		"""
		竞拍
		"""
		uid = int(uid)
		if money < 0 or not self.hasStartAuction:
			self.onReqAuctionDropBoxResult(str(uid), money, roleDBID, auction_orderID, False, roleCellMB)
			return
		
		#需要按照顺序来进行拍卖
		if len(self.pickupList) <= 0 or self.pickupList[0] != uid:
			self.onReqAuctionDropBoxResult(str(uid), money, roleDBID, auction_orderID, False, roleCellMB)
			return
		
		if not self.isAuctionPickUp():
			self.onReqAuctionDropBoxResult(str(uid), money, roleDBID, auction_orderID, False, roleCellMB)
			return
		
		if not self.checkPickUpItem(uid, roleDBID):
			self.onReqAuctionDropBoxResult(str(uid), money, roleDBID, auction_orderID, False, roleCellMB)
			return
		
		#竞价失败的话，需要返还玩家竞价押金
		result, amount, round = self.allocationItems[uid].auction(self, money, auction_orderID, roleDBID, roleCellMB)
		if not result:
			self.onReqAuctionDropBoxResult(str(uid), money, roleDBID, auction_orderID, False, roleCellMB)
			return
		
		self.onReqAuctionDropBoxResult(str(uid), money, roleDBID, auction_orderID, True, roleCellMB)
		countDown = Functions.getTime(self.countDown)
		
		#通知所有玩家，某人的竞价结果
		for _, role in self.roles.items():
			if role["mb"] and role["mb"].client:
				role["mb"].client.onAuctionDropBox(self.id, str(uid), money, str(roleDBID), amount, round,  str(countDown))
				
		self.checkAuctionEnd(uid)
		
	def onReqAbandomAuctionDropBox(self, uid, roleDBID, roleCellMB):
		"""
		放弃竞拍
		"""
		uid = int(uid)
		#需要按照顺序来进行拍卖
		if len(self.pickupList) <= 0 or self.pickupList[0] != uid:
			roleCellMB.onReqAbandomAuctionDropBoxResult(self.id, str(uid), False)
			return
			
		self._onReqAbandomAuctionDropBox(uid, roleDBID, roleCellMB)
		
	def _onReqAbandomAuctionDropBox(self, uid, roleDBID, roleCellMB):
		"""
		"""
		if not self.isAuctionPickUp():
			roleCellMB.onReqAbandomAuctionDropBoxResult(self.id, str(uid), False)
			return
		
		if not self.checkPickUpItem(uid, roleDBID):
			roleCellMB.onReqAbandomAuctionDropBoxResult(self.id, str(uid), False)
			return
		
		result = self.allocationItems[uid].abandomAuction(roleDBID, roleCellMB)
		if not result:
			roleCellMB.onReqAbandomAuctionDropBoxResult(self.id, str(uid), False)
			return
		
		roleCellMB.onReqAbandomAuctionDropBoxResult(self.id, str(uid), True)
		
		#通知所有玩家，某人放弃竞价
		for _, role in self.roles.items():
			if role["mb"] and role["mb"].client:
				role["mb"].client.onAbandomAuctionDropBox(self.id, str(uid), str(roleDBID), self.allocationItems[uid].round)
		
		self.checkAuctionEnd(uid)
		
	def onReqAbandomAuctionAllDropBox(self, roleDBID, roleCellMB):
		"""
		放弃竞拍所有
		"""
		for uid in list(self.pickupList):
			self._onReqAbandomAuctionDropBox(uid, roleDBID, roleCellMB)
		
	def onReqAuctionDropBoxResult(self, uid, money, roleDBID, auction_orderID, result, roleCellMB):
		"""
		竞拍（出价）结果
		"""
		if self.mgr is None: return
		self.mgr.onReqAuctionDropBoxResult(self.id, uid, money, result, roleDBID, auction_orderID, roleCellMB)
		
	def onTurnBackLastAuctionRoleMoney(self, uid, money, roleDBID, auction_orderID):
		"""
		"""
		if self.mgr is None: return
		roleMB = self.roles.get(roleDBID, {}).get("mb", None)
		roleCellMB = roleMB.cell if roleMB and roleMB.cell else None
		self.mgr.onTurnBackLastAuctionRoleMoney(self.id, uid, money, roleDBID, auction_orderID, roleCellMB)
		
	def checkAuctionEnd(self, uid):		
		"""
		检查竞拍是否需要结束
		"""
		if not self.allocationItems[uid].isPickUp():
			return
		
		self._onAuctionItemEnd(uid)
		
	def onAuctionTimeEnd(self):
		"""
		竞拍时间到
		"""
		if not self.hasStartAuction:
			return
		
		self.countDown -= 1
		if self.countDown > 0: 
			return
		
		if len(self.pickupList) <= 0:
			self.hasAllPickUp = True
			return
			
		#没有任何人竞拍
		uid = self.pickupList[0]
		if uid not in self.allocationItems:
			self.allocationItems[uid] = CAuctionData(uid, len(self.ownerDBIDs))
		
		self.allocationItems[uid].hasPickUp = True
		self._onAuctionItemEnd(uid)
		
	def _onAuctionItemEnd(self, uid):
		"""
		"""
		if uid != self.pickupList[0]:
			KBEDebug.ERROR_MSG("AuctionItemEnd error, %s %s" %(uid, self.pickupList))
			return
		
		self.pickupList.remove(uid)
		maxRoleDBID = self.allocationItems[uid].max_roleDBID
		maxAuctionMoney = self.allocationItems[uid].auctionData.get(maxRoleDBID, 0)
		self.pickupItemToRole(uid, maxRoleDBID)
		
		data = g_AuctionCfgLoader.getCfByIndex(1)
		self.countDown = data["time"] if data else 30
		countDown = Functions.getTime(self.countDown)
		
		pickupList = []
		for uid in self.pickupList:
			pickupList.append(str(uid))
		
		#通知所有玩家移除当前竞拍物品，更新竞拍列表
		for dbid, role in self.roles.items():
			if role["mb"] and role["mb"].client:
				role["mb"].client.onDropBoxAuctionItemEnd(self.id, str(uid), pickupList, str(countDown))
				
				#通知竞拍成功者，自己被扣了多少钱
				if maxAuctionMoney > 0:
					if dbid == maxRoleDBID:
						role["mb"].client.statusMessage(csstatus.ACCOUNT_STATE_LOSE_MONEY, str(maxAuctionMoney))
						continue
					
					#通知其他玩家竞拍结果
					msg = "{}|{}|{}".format(self.roles[maxRoleDBID]["name"], maxAuctionMoney, self.dropBoxItems[uid].getItemDir("ItemName"))
					role["mb"].client.statusMessage(csstatus.DROPBOX_AUCTION_GET_ITEM, msg)
		
		if maxAuctionMoney > 0:
			dbids = list(self.roles.keys())
			if maxRoleDBID in dbids: 
				dbids.remove(maxRoleDBID)
			if len(dbids) > 0:
				money = int(maxAuctionMoney / len(dbids))
				for dbid in dbids:
					self.mgr.onAllocationAuctionMoney(self.id, uid, money, dbid, self.roles[dbid]["mb"])
		
		if len(self.pickupList) <= 0:
			self.hasAllPickUp = True
		
	
class DropBoxManager( MgrPersistentObject.MgrPersistentObject ):
	"""
	宝箱管理
	"""
	def __init__( self ):
		"""
		"""
		MgrPersistentObject.MgrPersistentObject.__init__( self )
		
		self.dropBoxs = {}
		self.key2DropBoxIDList = {}
		self.timerID = 0
		self.onCompleteInit()

	def onAddDropBox(self, dropBoxMB, entityExtFlag, allocation, ownerDBIDs, items, keyWord):
		"""
		新增宝箱（竞拍/掷点）
		"""
		if dropBoxMB.id in self.dropBoxs:
			KBEDebug.ERROR_MSG("DropBox[%s] exists" %(dropBoxMB.id))
			return
		
		itemDct = {}
		for item in items: itemDct[item.uid] = item
		if self.timerID == 0: self.timerID = self.addTimerRepeat(1.0, "onTimeCallBack", ())
		
		#如果是竞拍拾取的话，需要进行排队
		key = "{}_{}".format(entityExtFlag, keyWord)
		box = CDropBox(dropBoxMB, entityExtFlag, allocation, ownerDBIDs, itemDct, key, self)
		if box.isAuctionPickUp():
			self.key2DropBoxIDList.setdefault(key, [])
			self.key2DropBoxIDList[key].append(dropBoxMB.id)
			if len(self.key2DropBoxIDList[key]) <= 1:
				box.startAuction()
		
		self.dropBoxs[dropBoxMB.id] = box
		
	def onDropBoxDestroy(self, dropBoxID):
		"""
		宝箱销毁
		"""
		if dropBoxID not in self.dropBoxs:
			return
			
		self.dropBoxs[dropBoxID].onDropBoxDestroy()
		
	def onRoleDestroy(self, dropBoxIDList, roleDBID):
		"""
		玩家下线
		"""
		for dropBoxID in dropBoxIDList:
			if dropBoxID in self.dropBoxs:
				self.dropBoxs[dropBoxID].onRoleDestroy(roleDBID)
	
	def onDropBoxRegisterRole(self, dropBoxID, roleDBID, roleName, roleBaseMB):
		"""
		注册个人信息
		"""
		if dropBoxID not in self.dropBoxs:
			return
		
		self.dropBoxs[dropBoxID].onDropBoxRegisterRole(roleDBID, roleName, roleBaseMB)
		
	def onReqDropBoxData(self, dropBoxID, roleDBID, roleCellMB):
		"""
		请求宝箱数据
		"""
		if dropBoxID not in self.dropBoxs:
			roleCellMB.onPickUpDropBoxEnd(dropBoxID)
			return
			
		self.dropBoxs[dropBoxID].onReqDropBoxData(roleDBID, roleCellMB)
		
	def onReqRollRandomDropBox(self, dropBoxID, uid, roleDBID, roleCellMB):
		"""
		掷点
		"""
		if dropBoxID not in self.dropBoxs:
			return
		
		self.dropBoxs[dropBoxID].onReqRollRandomDropBox(uid, roleDBID, roleCellMB)
		
	def onReqAbandomRollRandomDropBox(self, dropBoxID, uid, roleDBID, roleCellMB):
		"""
		放弃掷点
		"""
		if dropBoxID not in self.dropBoxs:
			return
		
		self.dropBoxs[dropBoxID].onReqAbandomRollRandomDropBox(uid, roleDBID, roleCellMB)
	
	def onReqAuctionDropBox(self, dropBoxID, uid, money, roleDBID, auction_orderID, roleCellMB):
		"""
		竞拍
		"""
		if dropBoxID not in self.dropBoxs:
			self.onReqAuctionDropBoxResult(dropBoxID, uid, money, False, roleDBID, auction_orderID, roleCellMB)
			return
		
		self.dropBoxs[dropBoxID].onReqAuctionDropBox(uid, money, roleDBID, auction_orderID, roleCellMB)
		
	def onReqAuctionDropBoxResult(self, dropBoxID, uid, money, result, roleDBID, auction_orderID, roleCellMB):
		"""
		出价成功/失败
		"""
		if result:
			if not auction_orderID:
				KBEDebug.ERROR_MSG("onReqAuctionDropBoxResult:[%s, %s, %s, %s] auction_orderID is None" %(dropBoxID, uid, result, roleDBID))
				return
			
			roleCellMB.onReqAuctionDropBoxResult(dropBoxID, uid, money, auction_orderID, result)
			return
		
		#将标志改为2
		sql_cmd = SQL_UPDATE.format(2, auction_orderID, 1)
		KBEngine.executeRawDatabaseCommand(sql_cmd, Functions.Functor(self.onUpdateCallBack, sql_cmd, dropBoxID, uid, money, auction_orderID, result, roleCellMB))
		
	def onUpdateCallBack( self, sql_cmd, dropBoxID, uid, money, auction_orderID, auctionResult, roleCellMB, result, rows, insertid, errstr):
		"""
		"""
		if errstr:
			KBEDebug.ERROR_MSG(sql_cmd)
			KBEDebug.ERROR_MSG(errstr)
			return
		
		roleCellMB.onReqAuctionDropBoxResult(dropBoxID, uid, money, auction_orderID, auctionResult)
		
	def onTurnBackLastAuctionRoleMoney(self, dropBoxID, uid, money, roleDBID, auction_orderID, roleCellMB):
		"""
		返还上次出价最高者的押金
		"""
		if roleDBID:
			if not auction_orderID:
				KBEDebug.ERROR_MSG("onTurnBackLastAuctionRoleMoney error, [%s, %s, %s, %s]" %(dropBoxID, uid, money, roleDBID))
				return
			
			#将标志改为1
			sql_cmd = SQL_UPDATE.format(1, auction_orderID, 2)
			KBEngine.executeRawDatabaseCommand(sql_cmd, Functions.Functor(self.onTurnBackCallBack, sql_cmd, dropBoxID, uid, money, auction_orderID, roleCellMB))
			
	def onTurnBackCallBack( self, sql_cmd, dropBoxID, uid, money, auction_orderID, roleCellMB, result, rows, insertid, errstr):
		"""
		"""
		if errstr:
			KBEDebug.ERROR_MSG(sql_cmd)
			KBEDebug.ERROR_MSG(errstr)
			return
		
		if roleCellMB:
			roleCellMB.onTurnBackLastAuctionRoleMoney(dropBoxID, uid, money, auction_orderID)
		
	def onReqAbandomAuctionDropBox(self, dropBoxID, uid, roleDBID, roleCellMB):
		"""
		放弃竞拍
		"""
		if dropBoxID not in self.dropBoxs:
			roleCellMB.onReqAbandomAuctionDropBoxResult(dropBoxID, uid, False)
			return
		
		self.dropBoxs[dropBoxID].onReqAbandomAuctionDropBox(uid, roleDBID, roleCellMB)
		
	def onReqAbandomAuctionAllDropBox(self, dropBoxIDList, roleDBID, roleCellMB):
		"""
		放弃竞拍所有
		"""
		for dropBoxID in dropBoxIDList:
			if dropBoxID not in self.dropBoxs:
				roleCellMB.onReqAbandomAuctionDropBoxResult(dropBoxID, uid, False)
				continue
			
			self.dropBoxs[dropBoxID].onReqAbandomAuctionAllDropBox(roleDBID, roleCellMB)
			
	def onAllocationAuctionMoney(self, dropBoxID, uid, money, roleDBID, roleMB):
		"""
		竞拍资金分派
		"""
		auction_orderID = "{}_{}_{}".format(KBEngine.genUUID64(), dropBoxID, roleDBID)
		sql_cmd = SQL_INSERT.format(roleDBID, str(uid), auction_orderID, money, 1)
		KBEngine.executeRawDatabaseCommand(sql_cmd, Functions.Functor(self.onInsertCallBack, sql_cmd, dropBoxID, uid, money, auction_orderID, roleMB))
		
	def onInsertCallBack( self, sql_cmd, dropBoxID, uid, money, auction_orderID, roleMB, result, rows, insertid, errstr):
		"""
		"""
		if self.isDestroyed:
			return
		
		if errstr:
			KBEDebug.ERROR_MSG(sql_cmd)
			KBEDebug.ERROR_MSG(errstr)
			return
		
		if roleMB is None:
			return
		
		if hasattr(roleMB, "isDestroyed") and roleMB.isDestroyed:
			return
			
		if roleMB.cell:
			roleMB.cell.onTurnBackLastAuctionRoleMoney(dropBoxID, str(uid), money, auction_orderID)
		
		if hasattr(roleMB, "client") and roleMB.client:
			roleMB.client.statusMessage(csstatus.ACCOUNT_STATE_GAIN_MONEY, str(money))
		
	def onRecvAuctionResultData(self, uid, itemID, roleName, roleDBID, auctionMoney):
		"""
		"""
		sql_cmd = SQL_INSERT_AUCTION_RESULT.format(uid, itemID, roleDBID, auctionMoney)
		sql_cmd = MysqlUtility.makeSafeSql(sql_cmd, (roleName,))
		KBEngine.executeRawDatabaseCommand(sql_cmd, Functions.Functor(self.onInsertAuctionResultCallBack, sql_cmd))
		
	def onInsertAuctionResultCallBack( self, sql_cmd, result, rows, insertid, errstr):
		"""
		"""
		if self.isDestroyed:
			return
		
		if errstr:
			KBEDebug.ERROR_MSG(sql_cmd)
			KBEDebug.ERROR_MSG(errstr)
			return
		
	def onTimeCallBack(self):
		"""
		"""
		tempLst = list(self.dropBoxs.keys())
		for dropBoxID in tempLst:
			if not self.dropBoxs[dropBoxID].isAllPickUp():
				self.dropBoxs[dropBoxID].onTimeCallBack()
				continue
			
			key = self.dropBoxs[dropBoxID].key
			self.dropBoxs[dropBoxID].onPickUpDropBoxEnd()
			self.dropBoxs.pop(dropBoxID)
			
			if key in self.key2DropBoxIDList:
				if dropBoxID in self.key2DropBoxIDList[key]:
					self.key2DropBoxIDList[key].remove(dropBoxID)
				
				if len(self.key2DropBoxIDList[key]) <= 0:
					self.key2DropBoxIDList.pop(key)
					continue
				
				#开启下一个宝箱竞拍倒计时
				id = self.key2DropBoxIDList[key][0]
				self.dropBoxs[id].startAuction()
			
		if len(self.dropBoxs) <= 0:
			self.popTimer(self.timerID)
			self.timerID = 0
			return
			
		
	