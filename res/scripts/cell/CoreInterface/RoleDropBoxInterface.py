
# -*- coding: utf-8 -*-
import Functions
import KBEngine
import KBEDebug
import csstatus
import csdefine
import ItemTypeEnum
from DropBox import DropBox

#插入SQL
SQL_INSERT = "INSERT INTO tbl_AuctionOrders (sm_roleDBID, sm_auction_uid, sm_auction_orderId, sm_money) VALUES (%s, %s, %s, %s);"
#更新SQL
SQL_UPDATE = "UPDATE tbl_AuctionOrders set sm_pickup_status = {} WHERE sm_auction_orderId = '{}' AND sm_pickup_status = {};"
#查询SQL
SQL_SELECT = "SELECT sm_itemID, sm_auction_roleName, sm_auction_roleDBID, sm_auction_money FROM tbl_AuctionResultData WHERE sm_itemUID = {};"

class RoleDropBoxInterface:
	"""
	玩家宝箱接口
	"""
	def __init__( self ):
		"""
		初始化
		"""
		#加载上次拍卖到一半下线的竞拍结果
		for uid in self.curAuctionData:
			sql_cmd = SQL_SELECT.format(uid)
			KBEngine.executeRawDatabaseCommand(sql_cmd, Functions.Functor(self.onSelectCallBack, sql_cmd, uid))
			
	def onSelectCallBack( self, sql_cmd, uid, results, rows, insertid, errstr):
		"""
		"""
		if self.isDestroyed:
			return
		
		if errstr:
			self.curAuctionData.remove(uid)
			KBEDebug.ERROR_MSG(sql_cmd)
			KBEDebug.ERROR_MSG(errstr)
			return
		
		if uid in self.curAuctionData:
			self.curAuctionData.remove(uid)
		
		for result in results:
			if len(result) > 0:
				self.onRecvAuctionData(uid, str(result[0]), result[1].decode("utf-8"), int(result[2]), int(result[3]))
		
	def beforeDestroy( self ):
		"""
		"""
		#清理一下自身的数据
		KBEngine.globalData["DropBoxManager"].onRoleDestroy(self.dropBoxIDList, self.playerDBID)
		
	def getDropBoxByID( self, dropBoxID ):
		"""
		"""
		dropBox = KBEngine.entities.get(dropBoxID, None)
		if dropBox is None:
			KBEDebug.WARNING_MSG( "Role[%d:%d]:getDropBoxByID, not found dropBox"%( self.playerDBID, self.id ) )
			return None
			
		if not isinstance(dropBox, DropBox):
			KBEDebug.WARNING_MSG( "Role[%d:%d]:getDropBoxByID, entity(id) is not dropBox"%( self.playerDBID, self.id, dropBoxID ) )
			return None
			
		return dropBox
		
	def CELL_reqSendItemInfoListToClient( self, srcEntityID, dropBoxID ):
		"""
		<exposed method>
		发送掉落物品列表数据到客户端
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		dropBox = self.getDropBoxByID(dropBoxID)
		if dropBox is None:
			return
		
		dropBox.reqSendItemInfoListToClient(self.id)
		
	def CELL_reqPickUp( self, srcEntityID, dropBoxID, itemUIDList ):
		"""
		<Exposed method>
		拾取物品请求，进行检测处理，返回能否拾取成功，返回拾取物品的uid列表
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		dropBox = self.getDropBoxByID(dropBoxID)
		if dropBox is None:
			return
		
		dropBox.reqPickUp(self.id, itemUIDList)
		
	def CELL_pickUpToMember( self, srcEntityID, dropBoxID, uid, dstEntityID ):
		"""
		<exposed method>
		队长分配物品给队员或自己
		@param uid: STRING,物品uid
		@param dstEntityID: INT32,将得到物品的玩家的entity id
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		dropBox = self.getDropBoxByID(dropBoxID)
		if dropBox is None:
			return
		
		dropBox.pickUpToMember(self.id, uid, dstEntityID)
		
	def CELL_rollRandom( self, srcEntityID, dropBoxID, uid ):
		"""
		<exposed method>
		玩家掷骰子
		
		@param uid: STRING,物品uid
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		dropBox = self.getDropBoxByID(dropBoxID)
		if dropBox is None:
			return
		
		dropBox.rollRandom(self.id, uid)
		
	def CELL_abandonRoll( self, srcEntityID, dropBoxID, uid ):
		"""
		<exposed method>
		放弃参与掷骰子
		
		@param uid: STRING, 放弃的物品uid
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		dropBox = self.getDropBoxByID(dropBoxID)
		if dropBox is None:
			return
	
		dropBox.abandonRoll(self.id, uid)
		
	def CELL_autoPickUpDropBox( self, srcEntityID, dropBoxIDs ):
		"""
		<exposed method>
		自动拾取
		
		@param dropBoxIDs: 自动拾取的掉落箱子id
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		allPickup = True
		item2dropBox = {}			# { itemInst : dropInst }
		for id in dropBoxIDs:
			dropBox = self.getDropBoxByID(id)
			if dropBox is None:
				continue
			
			#如果背包满了，就不捡普通物品了
			allocationItems, itemList = dropBox.getPlayerDropItems(self.playerDBID)
			if self.addItemListCheck(allocationItems) != csstatus.ITEM_GO_ON:
				allPickup = False	
			else:
				itemList.extend(allocationItems)
	
			pickUpDataSort = sorted(itemList, key=lambda info : info.getPickUpShortIndex(), reverse=True)
			for item in pickUpDataSort:
				dropBox.pickUp(self.id, [item.uid])
		
		if not allPickup:
			self.statusMessage(csstatus.NPCSHOP_BAG_ENOUGH)
	
	#------------------------------------帮会宝箱拾取 -----------------------------------------
	def onTeleportCompleted(self, isFirst):
		"""
		"""
		if not isFirst: return
		for dropBoxID in self.dropBoxIDList:
			KBEngine.globalData["DropBoxManager"].onDropBoxRegisterRole(dropBoxID, self.playerDBID, self.playerName, self.base)
			KBEngine.globalData["DropBoxManager"].onReqDropBoxData(dropBoxID, self.playerDBID, self)
		
	def onDropBoxRegister(self, dropBoxID):
		"""
		记录宝箱
		"""
		if dropBoxID not in self.dropBoxIDList: self.dropBoxIDList.append(dropBoxID)
		KBEngine.globalData["DropBoxManager"].onDropBoxRegisterRole(dropBoxID, self.playerDBID, self.playerName, self.base)
		
	def onReqDropBoxData(self, dropBoxID):
		"""
		获取宝箱中掷点分配和竞拍分配的物品数据
		"""
		if dropBoxID not in self.dropBoxIDList:
			return
		
		KBEngine.globalData["DropBoxManager"].onReqDropBoxData(dropBoxID, self.playerDBID, self)
	
	def reqRollRandomDropBox(self, srcEntityID, dropBoxID, uid):
		"""
		Exposed method
		请求掷点
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if dropBoxID not in self.dropBoxIDList:
			return
		
		KBEngine.globalData["DropBoxManager"].onReqRollRandomDropBox(dropBoxID, uid, self.playerDBID, self)
		
	def reqAbandomRollRandomDropBox(self, srcEntityID, dropBoxID, uid):
		"""
		Exposed method
		放弃掷点
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if dropBoxID not in self.dropBoxIDList:
			return
			
		KBEngine.globalData["DropBoxManager"].onReqAbandomRollRandomDropBox(dropBoxID, uid, self.playerDBID, self)
		
	def reqAuctionDropBox(self, srcEntityID, dropBoxID, uid, money):
		"""
		Exposed method
		请求竞拍
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if dropBoxID not in self.dropBoxIDList:
			return
		
		if money <= 0:
			return
		
		#钱不够
		if self.money < money:
			self.statusMessage(csstatus.DROPBOX_AUCTION_NO_ENOUGH_MONEY)
			return
		
		#如果前一次的出价/放弃流程没走完不能继续出价
		if dropBoxID in self.auctionData:
			return
		
		self.money -= money
		self.auctionData.append(dropBoxID)
		self.curAuctionData.append(uid)
		#self.statusMessage(csstatus.ACCOUNT_STATE_LOSE_MONEY, money)
		
		#只能写数据库了
		auction_orderID = str(KBEngine.genUUID64())
		sql_cmd = SQL_INSERT %(self.playerDBID, uid, auction_orderID, money)
		KBEngine.executeRawDatabaseCommand(sql_cmd, Functions.Functor(self.onInsertCallBack, sql_cmd, dropBoxID, uid, money, auction_orderID))
		
	def onInsertCallBack( self, sql_cmd, dropBoxID, uid, money, auction_orderID, result, rows, insertid, errstr):
		"""
		"""
		if self.isDestroyed:
			return
		if errstr:
			KBEDebug.ERROR_MSG(sql_cmd)
			KBEDebug.ERROR_MSG(errstr)
			
			self.money += money
			self.removeAuctionTempData(dropBoxID, uid)
			#self.statusMessage(csstatus.ACCOUNT_STATE_GAIN_MONEY, money)
			return
		
		KBEngine.globalData["DropBoxManager"].onReqAuctionDropBox(dropBoxID, uid, money, self.playerDBID, auction_orderID, self)
		
	def onReqAuctionDropBoxResult(self, dropBoxID, uid, money, auction_orderID, result):
		"""
		出价成功/失败
		"""
		self.removeAuctionTempData(dropBoxID, uid)
		#如果出价失败了需要返还押金
		if not result:
			sql_cmd = SQL_UPDATE.format(1, auction_orderID, 0)
			KBEngine.executeRawDatabaseCommand(sql_cmd, Functions.Functor(self.onUpdateCallBack, sql_cmd, money, auction_orderID))
			
	def onUpdateCallBack( self, sql_cmd, money, auction_orderID, result, rows, insertid, errstr):
		"""
		"""
		if self.isDestroyed:
			return
		if errstr:
			KBEDebug.ERROR_MSG(sql_cmd)
			KBEDebug.ERROR_MSG(errstr)
			return
		
		#这这里加回来
		self.money += money
		#self.statusMessage(csstatus.ACCOUNT_STATE_GAIN_MONEY, money)
		
	def onTurnBackLastAuctionRoleMoney(self, dropBoxID, uid, money, auction_orderID):
		"""
		"""
		#如果出价失败了需要返还押金
		sql_cmd = SQL_UPDATE.format(1, auction_orderID, 0)
		KBEngine.executeRawDatabaseCommand(sql_cmd, Functions.Functor(self.onUpdateCallBack, sql_cmd, money, auction_orderID))
		
	def reqAbandomAuctionDropBox(self, srcEntityID, dropBoxID, uid):
		"""
		Exposed method
		放弃竞拍
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		if dropBoxID not in self.dropBoxIDList:
			return
		
		#如果前一次的出价/放弃流程没走完不能继续
		if dropBoxID in self.auctionData:
			return
		
		self.auctionData.append(dropBoxID)
		KBEngine.globalData["DropBoxManager"].onReqAbandomAuctionDropBox(dropBoxID, uid, self.playerDBID, self)
		
	def onReqAbandomAuctionDropBoxResult(self, dropBoxID, uid, result):
		"""
		放弃竞拍结果
		"""
		self.removeAuctionTempData(dropBoxID, uid)
		
	def reqAbandomAuctionAllDropBox(self, srcEntityID, dropBoxIDList):
		"""
		Exposed method
		放弃竞拍所有箱子
		"""
		if not self.validateClientCall( srcEntityID ):
			return
			
		for dropBoxID in dropBoxIDList:
			if dropBoxID not in self.dropBoxIDList:
				return
			
			#如果前一次的出价/放弃流程没走完不能继续
			if dropBoxID in self.auctionData:
				return
		
		for dropBoxID in dropBoxIDList:
			self.auctionData.append(dropBoxID)
		
		KBEngine.globalData["DropBoxManager"].onReqAbandomAuctionAllDropBox(dropBoxIDList, self.playerDBID, self)
		
	def onPickupItemToRole(self, dropBoxID, itemInst):
		"""
		"""
		if self.addItemCheck(itemInst):
			self.addItem(itemInst, csdefine.ITEM_ADD_BY_PICKUP)
			return
		
		#通过邮件给到玩家
		self.sendRemainItemWithMail([itemInst], csdefine.REMAIN_ITEM_DROPBOX, csdefine.ITEM_ADD_BY_PICKUP)
		
	def onPickUpDropBoxEnd(self, dropBoxID):
		"""
		define method
		移除箱子（竞拍/掷点结束）
		"""
		if dropBoxID in self.dropBoxIDList:
			self.dropBoxIDList.remove(dropBoxID)
		if dropBoxID in self.auctionData:
			self.auctionData.remove(dropBoxID)
		if self.getClient():
			self.client.onPickUpDropBoxEnd(dropBoxID)
			
	def reqAuctionHistoryData(self, srcEntityID):
		"""
		Exposed method
		请求获取竞拍历史数据
		"""
		if not self.validateClientCall( srcEntityID ):
			return
		
		self.client.recvAuctionHistoryData(self.auctionHistoryData)
		
	def onRecvAuctionData(self, uid, itemID, roleName, roleDBID, money):
		"""
		增加竞拍历史记录
		"""
		result = 0
		if roleDBID == self.playerDBID:
			result = 1
		
		dct = {"id" : itemID, "roleName": roleName, "result" : result, "money" : money}
		self.auctionHistoryData.append(dct)
		if len(self.auctionHistoryData) > 30:
			self.auctionHistoryData.pop(0)
		
		if uid in self.curAuctionData:
			self.curAuctionData.remove(uid)
			
		if self.getClient():
			self.client.updateAuctionHistoryData(dct)
		
	def removeAuctionTempData(self, dropBoxID, uid):
		"""
		"""
		if dropBoxID in self.auctionData:
			self.auctionData.remove(dropBoxID)