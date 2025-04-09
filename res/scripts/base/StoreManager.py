# -*- coding: utf-8 -*-

import KBEDebug
import json
import KBEngine
import Functions
import csdefine
import csstatus
import csconst
import copy
from CoreObject import MgrPersistentObject
from ConfigObject.Store.StoreMgr import g_storeMgr
from Functions import Functor
from ConfigObject.MailContentDataLoader import g_mailContentDataLoader

STORE_GIFT_STATE = {	
	csdefine.STORE_GIFT_STATE_SELF_ACCEPT 	: 	csdefine.STORE_GIFT_STATE_ACCEPT,
	csdefine.STORE_GIFT_STATE_SELF_REFUSE 	: 	csdefine.STORE_GIFT_STATE_REFUSE,
}

class StoreManager(MgrPersistentObject.MgrPersistentObject):
	"""
	商城管理器(新)
	"""
	def __init__(self):
		MgrPersistentObject.MgrPersistentObject.__init__(self)
		self.tradeTimeID = 0	
		self.start()
		self.onCompleteInit()

	def start(self):
		"""
		初始化数据
		"""
		self.serverLimits.initConfig()			# {goodID: {goodID, "amount":amount, "startTime":time}}
		self.playerLimits.initConfig()			# {playerDbid:{{goodID: goodID, "amount":amount, "startTime":time}}}
		self.configTime = Functions.getTime()   # 配置时间

	def reload(self):
		"""
		<Define method>
		"""
		self.serverLimits.initConfig()
		self.playerLimits.initConfig()
		self.configTime = Functions.getTime()

	def initClientData(self, player, playerDBID):
		"""
		<Define method>
		初始化玩家商城数据		
		"""
		#处理被拒绝礼物的消息提示
		if str(playerDBID) in self.giftBoxSendDatas:
			for i in self.giftBoxSendDatas[str(playerDBID)]:
				if i.uid in list(self.beRefuseGiftID):
					player.statusMessage(csstatus.STORE_GIFT_BE_REFUSE, i.receiverName)
					self.beRefuseGiftID.remove(i.uid)
		# 处理离线再上线显示礼品盒显示红点的问题
		if playerDBID in self.presentRedPointList:
			player.client.CLINET_GiftBoxShowRedPoint(0)
		if playerDBID in self.receiveRedPointList:
			player.client.CLINET_GiftBoxShowRedPoint(1)

	def onUpdateStoreGoods(self, player, goodsType, itemType, cfgTime):
		"""
		<Define method>
		更新商城数据
		"""
		time = 0
		if cfgTime:
			time = int(cfgTime)
		if self.configTime <= time:  # 服务器没有更新配置时，客户端用旧的数据
			player.client.CLIENT_OnUpdateStoreGoodsOver(goodsType, itemType)
			return
		goodsList = g_storeMgr.getGoodsByType(goodsType, itemType)
		if not goodsList:
			player.client.CLIENT_OnUpdateStoreGoodsOver(goodsType, itemType)
			return
		player.client.CLIENT_OnUpdateStoreGoods(str(self.configTime), {"Datas" : goodsList })

	def getStoreNewGoods(self, player, goodsType, cfgTime):
		"""
		<Define method>
		获得商城新品数据
		"""
		time = 0
		if cfgTime:
			time = int(cfgTime)
		if self.configTime <= time:  # 服务器没有更新配置时，客户端用旧的数据
			player.client.CLIENT_OnUpdateStoreNewGoodsOver(goodsType)
			return
		goodsList = g_storeMgr.getNewGoods(goodsType)
		if not goodsList:
			player.client.CLIENT_OnUpdateStoreNewGoodsOver(goodsType)
			return	
		player.client.CLIENT_OnGetStoreNewGoods(str(self.configTime), {"Datas" : goodsList})

	def requestStoreLimitGoodsList(self, player, playerDBID):
		"""
		<defined method>
		获得当前商城限制数量购买的商品数量
		"""
		goodsIDList, amountList = self.serverLimits.getLimitGoodsAmount()
		temp1, temp2 = self.playerLimits.getLimitGoodsAmount(playerDBID)
		goodsIDList.extend(temp1)
		amountList.extend(temp2)
		if len(goodsIDList) == len(amountList):
			player.onRequestStoreLimitGoodsList( goodsIDList, amountList )


	def requestBuyStoreGoods(self, player, playerDBID, goodsID, amount):
		"""
		<defined method>
		申请购买
		"""
		goods = g_storeMgr.getGoodsByID(goodsID)
		# 如果商品已经下架
		if goods.GoodsState == csdefine.STORE_GOODS_STATE_SOLD_OUT:
			player.statusMessage(csstatus.STORE_GOODS_SOLD_OUT, "")
			return

		# 判断商品数量是否足够
		if not self.buyLimitGoods(playerDBID, goods, amount):
			player.statusMessage(csstatus.STORE_GOODS_CANT_BUY_MORE, "")
			return
		player.onRequestBuyStoreGoods(goodsID, amount)
			
	def buyLimitGoods(self, playerDBID, goods, amount):
		"""
		购买限制数量商品
		"""
		result = True
		if goods.ServeLimitAmount > 0:
			result &= self.serverLimits.isNoLimitAmount(goods.ID, amount)
		if goods.LimitAmount > 0:
			self.playerLimits.getLimitGoods(playerDBID, goods)
			result &= self.playerLimits.isNoLimitAmount(playerDBID, goods.ID, amount)
		return result


	def onBuyStoreGoods(self, playerDBID, goodsID, amount ):
		"""
		<defined method>
		购买成功回调
		"""
		pass

	def requestPresentGift(self, player, giftBox):
		"""
		<defined method>
		赠送
		"""
		if giftBox.senderDBID not in self.giftBoxSendDatas:
			self.giftBoxSendDatas[giftBox.senderDBID] = []
		if giftBox.receiverDBID not in self.giftBoxReceiveDatas:
			self.giftBoxReceiveDatas[giftBox.receiverDBID] = []
		self.giftBoxSendDatas[giftBox.senderDBID].append(giftBox)
		self.giftBoxReceiveDatas[giftBox.receiverDBID].append(copy.copy(giftBox))
		player.client.CLIENT_OnRequestPresentGift(giftBox)
		KBEngine.lookUpEntityByDBID( "Role", int(giftBox.receiverDBID), Functions.Functor( self.onReceiveStoreGift,giftBox.receiverDBID ) )

	def setPresentRecords(self, player, records):
		"""
		<defined method>
		设置赠送记录
		"""
		for record in records:
			if record.senderDBID not in self.sendPresentRecords:
				self.sendPresentRecords[record.senderDBID] = []
			self.sendPresentRecords[record.senderDBID].append(record)
			if record.receiverDBID not in self.receivePresentRecords:
				self.receivePresentRecords[record.receiverDBID] = []
			self.receivePresentRecords[record.receiverDBID].append(record)
		player.client.CLIENT_OnUpdatePresentRecords({"Datas" : records})

	def queryPresentRecords(self, player, playerDBID):
		"""
		<defined method>
		查询赠送记录		
		"""
		List = []
		if playerDBID in self.sendPresentRecords:
			List.extend(self.sendPresentRecords[playerDBID])
		if playerDBID in self.receivePresentRecords:
			List.extend(self.receivePresentRecords[playerDBID])
		player.client.CLIENT_OnUpdatePresentRecords({"Datas" : List})

	def deletePresentRecord(self, playerDBID, uid):
		"""
		<defined method>
		删除赠送记录		
		"""
		if playerDBID in self.sendPresentRecords:
			for i in self.sendPresentRecords[playerDBID]:
				if uid == i.uid:
					self.sendPresentRecords[playerDBID].remove(i)
					return
		if playerDBID in self.receivePresentRecords:
			for i in self.receivePresentRecords[playerDBID]:
				if uid == i.uid:
					self.receivePresentRecords[playerDBID].remove(i)
					return

	def deletePresentRecords(self, playerDBID):
		"""
		<defined method>
		清空赠送记录		
		"""
		if playerDBID in self.sendPresentRecords:
			self.sendPresentRecords[playerDBID].clear()
		if playerDBID in self.receivePresentRecords:
			self.receivePresentRecords[playerDBID].clear()

	def onReceiveStoreGift(self, receiverDBID, target):
		"""
		"""
		self.receiveRedPointList.append(int(receiverDBID))
		if target is False:
			return
		if target is True:
			return
		ReceiveList = []
		if receiverDBID in self.giftBoxReceiveDatas:
			ReceiveList = self.giftBoxReceiveDatas[receiverDBID]
		if target.client:
			target.client.CLINET_GiftBoxShowRedPoint(1)
			target.client.CLIENT_OnUpdateGiftBox({"Datas" : [] }, {"Datas" : ReceiveList })

	def buyStoreCartGoods(self, player, playerDBID, goodsIDList, amountList):
		"""
		<defined method>
		购物车批量购买商品
		"""
		index = 0
		for goodsID in goodsIDList:
			goods = g_storeMgr.getGoodsByID(goodsID)
			# 如果商品已经下架
			if goods.GoodsState == csdefine.STORE_GOODS_STATE_SOLD_OUT:
				player.statusMessage(csstatus.STORE_GOODS_SOLD_OUT, "")
				return

			# 判断商品数量是否足够
			if not self.buyLimitGoods(playerDBID, goods, amountList[index]):
				player.statusMessage(csstatus.STORE_GOODS_CANT_BUY_MORE, "")
				return
			index += 1
		player.onBuyStoreCartGoods(goodsIDList, amountList)

	def updateGiftBox(self, playerDBID):
		"""
		更新某个玩家礼品盒
		"""
		sRemoveList = []
		rRemoveList = []
		if str(playerDBID) in self.giftBoxSendDatas:
			for i in self.giftBoxSendDatas[str(playerDBID)]:
				if i.giftState == csdefine.STORE_GIFT_STATE_NONE and int(i.overtime) < Functions.getTime():
					i.giftState = csdefine.STORE_GIFT_STATE_OVERDUE
					i.endTime = str(int(i.overtime) + 4*24*60*60*csconst.TIME_ENLARGE_MULTIPLE)
				if i.endTime and int(i.endTime) < Functions.getTime():
					sRemoveList.append(i)
		if str(playerDBID) in self.giftBoxReceiveDatas:
			for i in self.giftBoxReceiveDatas[str(playerDBID)]:
				if i.giftState == csdefine.STORE_GIFT_STATE_NONE and int(i.overtime) < Functions.getTime():
					i.giftState = csdefine.STORE_GIFT_STATE_OVERDUE
					i.endTime = str(int(i.overtime) + 4*24*60*60*csconst.TIME_ENLARGE_MULTIPLE)
				if i.endTime and int(i.endTime) < Functions.getTime():
					rRemoveList.append(i)
		for i in sRemoveList:
			self.giftBoxSendDatas[playerDBID].remove(i)
		for i in sRemoveList:
			self.giftBoxReceiveDatas[playerDBID].remove(i)		


	def requestOpenGiftBox(self, player, playerDBID):
		"""
		<defined method>
		申请打开礼品盒
		"""
		self.updateGiftBox(playerDBID)
		sendList = []
		receiveList = []
		if str(playerDBID) in self.giftBoxSendDatas:
			sendList = self.giftBoxSendDatas[str(playerDBID)]
		if str(playerDBID) in self.giftBoxReceiveDatas:
			receiveList = self.giftBoxReceiveDatas[str(playerDBID)]
		self.onUpdateGiftBox(player, playerDBID, sendList, receiveList)

	def acceptGift(self, player, playerDBID, uid):
		"""
		<defined method>
		收取礼品
		"""
		List = self.giftBoxReceiveDatas.get(str(playerDBID), None)
		if not List:
			return
		
		itemID = 0
		amount = 0 
		for i in List:
			if i.giftState == csdefine.STORE_GIFT_STATE_NONE and i.uid == uid:
				itemID = i.itemID
				amount = i.amount
				break
		player.onAcceptGift(itemID, amount, uid)

	def acceptGifts(self, player, playerDBID):
		"""
		<defined method>
		全部收取礼品
		"""
		List = self.giftBoxReceiveDatas.get(str(playerDBID), None)
		if not List:
			return
		
		itemIDList = []
		amountList = []
		for i in List:
			if i.giftState == csdefine.STORE_GIFT_STATE_NONE:
				itemIDList.append(i.itemID)
				amountList.append(i.amount)
		player.onAcceptGifts(itemIDList, amountList)

	def getBackGift(self, player, playerDBID, uid):
		"""
		<defined method>
		取回礼品
		"""
		List = self.giftBoxSendDatas.get(str(playerDBID), None)
		if not List:
			return
		
		itemID = 0
		amount = 0 
		for i in List:
			if i.giftState == csdefine.STORE_GIFT_STATE_REFUSE and i.uid == uid:
				itemID = i.itemID
				amount = i.amount
				break
		player.onGetBackGift(itemID, amount, uid)

	def getBackGifts(self, player, playerDBID):
		"""
		<defined method>
		全部取回礼品
		"""
		List = self.giftBoxSendDatas[str(playerDBID)]
		itemIDList = []
		amountList = []		
		for i in List:
			if i.giftState == csdefine.STORE_GIFT_STATE_OVERDUE or i.giftState == csdefine.STORE_GIFT_STATE_REFUSE:
				itemIDList.append(i.itemID)
				amountList.append(i.amount)
		player.onGetBackGifts(itemIDList, amountList)	

	def setGiftBoxState(self, type, player, playerDBID, uid, state):
		"""
		<defined method>
		设置礼品盒状态
		@ prama type 1：表示处理送礼品盒 2：表示处理收礼品盒
		"""
		sendList = []
		receiveList = []
		if type == 1:
			DBID = 0
			for i in self.giftBoxSendDatas[str(playerDBID)]:
				if uid == i.uid:
					i.giftState = state
					if state == csdefine.STORE_GIFT_STATE_RECAPTION:
						i.endTime = str(Functions.getTime(7*24*60*60))
					DBID = i.receiverDBID
					sendList.append(i)
					break
		if type == 2:
			DBID = 0
			for i in self.giftBoxReceiveDatas[str(playerDBID)]:
				if uid == i.uid:
					i.giftState = state
					i.endTime = str(Functions.getTime(7*24*60*60))
					DBID = i.senderDBID									
					receiveList.append(i)
					if state == csdefine.STORE_GIFT_STATE_SELF_REFUSE:
						break		
					if i.message:
						string = i.senderName + "|" +  i.message
						player.statusMessage(csstatus.STORE_GIFT_CUSTOM_MESSAGE, string)
					else:
						player.statusMessage(csstatus.STORE_GIFT_DEFAULT_MESSAGE, i.senderName)
					break
			for j in self.giftBoxSendDatas[str(DBID)]:  # 设置收礼盒状态，要设置对方的送礼盒状态
				if uid == j.uid:
					j.giftState = STORE_GIFT_STATE[state]
					if state != csdefine.STORE_GIFT_STATE_SELF_REFUSE:
						j.endTime = str(Functions.getTime(7*24*60*60))
					break

		self.onUpdateGiftBox(player, playerDBID, sendList, receiveList)

	def setAllGiftBoxState(self, type, player, playerDBID, state):
		"""
		<defined method>
		设置所有默认状态的礼品盒状态
		@ prama type 1：表示处理送礼品盒 2：表示处理收礼品盒
		"""
		sendList = []
		receiveList = []
		if type == 1:
			List1 = []
			for i in self.giftBoxSendDatas[str(playerDBID)]:
				if i.giftState == csdefine.STORE_GIFT_STATE_NONE:
					i.giftState = state
					if state == csdefine.STORE_GIFT_STATE_RECAPTION:
						i.endTime = str(Functions.getTime(7*24*60*60))
					sendList.append(i)
					List1.append((i.receiverDBID, i.uid))

		if type == 2:
			List2 = []
			for i in self.giftBoxReceiveDatas[str(playerDBID)]:
				if i.giftState == csdefine.STORE_GIFT_STATE_NONE:
					i.giftState = state
					i.endTime = str(Functions.getTime(7*24*60*60))
					receiveList.append(i)
					List2.append((i.senderDBID, i.uid))
			for t in List2:    # 全部设置收礼盒状态，要设置对方的送礼盒状态
				for s in self.giftBoxSendDatas[t[0]]:
					if t[1] == s.uid:
						s.giftState = STORE_GIFT_STATE[state]
						if state != csdefine.STORE_GIFT_STATE_SELF_REFUSE:
							s.endTime = str(Functions.getTime(7*24*60*60))
						break
		self.onUpdateGiftBox(player, playerDBID, sendList, receiveList)

	def onAcceptGiftOver(self, player, playerDBID, uid):
		"""
		<defined method>
		收礼完成
		"""
		sendList = []
		receiveList = []
		DBID = 0 
		for i in self.giftBoxReceiveDatas[str(playerDBID)]:
			if uid == i.uid:
				i.giftState = csdefine.STORE_GIFT_STATE_SELF_ACCEPT
				i.endTime = str(Functions.getTime(7*24*60*60))
				DBID = i.senderDBID									
				receiveList.append(i)	
				if i.message:
					string = i.senderName + "|" +  i.message
					player.statusMessage(csstatus.STORE_GIFT_CUSTOM_MESSAGE, string)
				else:
					player.statusMessage(csstatus.STORE_GIFT_DEFAULT_MESSAGE, i.senderName)
				break
		for j in self.giftBoxSendDatas[str(DBID)]:  # 设置收礼盒状态，要设置对方的送礼盒状态
			if uid == j.uid:
				j.giftState = STORE_GIFT_STATE[csdefine.STORE_GIFT_STATE_SELF_ACCEPT]
				j.endTime = str(Functions.getTime(7*24*60*60))
				break

		self.onUpdateGiftBox(player, playerDBID, sendList, receiveList)

	def onAcceptGiftOvers(self, player, playerDBID):
		"""
		<defined method>
		全部收礼完成
		"""
		sendList = []
		receiveList = []
		List2 = []
		for i in self.giftBoxReceiveDatas[str(playerDBID)]:
			if i.giftState == csdefine.STORE_GIFT_STATE_NONE:
				i.giftState = csdefine.STORE_GIFT_STATE_SELF_ACCEPT
				i.endTime = str(Functions.getTime(7*24*60*60))
				receiveList.append(i)
				List2.append((i.senderDBID, i.uid))
		for t in List2:    # 全部设置收礼盒状态，要设置对方的送礼盒状态
			for s in self.giftBoxSendDatas[t[0]]:
				if t[1] == s.uid:
					s.giftState = STORE_GIFT_STATE[csdefine.STORE_GIFT_STATE_SELF_ACCEPT]
					s.endTime = str(Functions.getTime(7*24*60*60))
					break
		self.onUpdateGiftBox(player, playerDBID, sendList, receiveList)


	def refuseGift(self, player, playerDBID, uid):
		"""
		<defined method>
		拒绝礼品
		"""
		sendList = []
		receiveList = []
		DBID = 0 
		for i in self.giftBoxReceiveDatas[str(playerDBID)]:
			if uid == i.uid:
				i.giftState = csdefine.STORE_GIFT_STATE_SELF_REFUSE
				i.endTime = str(Functions.getTime(7*24*60*60))
				DBID = i.senderDBID									
				receiveList.append(i)
				break
		for j in self.giftBoxSendDatas[str(DBID)]:  # 设置收礼盒状态，要设置对方的送礼盒状态
			if uid == j.uid:
				j.giftState = STORE_GIFT_STATE[csdefine.STORE_GIFT_STATE_SELF_REFUSE]
				KBEngine.lookUpEntityByDBID( "Role", int(DBID), Functions.Functor( self.onRefuseGift, uid, j.receiverName, int(DBID) ) )
				break
		
		self.onUpdateGiftBox(player, playerDBID, sendList, receiveList)

	def refuseGifts(self, player, playerDBID):
		"""
		<defined method>
		拒绝全部礼品
		"""
		sendList = []
		receiveList = []
		List2 = []
		for i in self.giftBoxReceiveDatas[str(playerDBID)]:
			if i.giftState == csdefine.STORE_GIFT_STATE_NONE:
				i.giftState = csdefine.STORE_GIFT_STATE_SELF_REFUSE
				i.endTime = str(Functions.getTime(7*24*60*60))
				receiveList.append(i)
				List2.append((i.senderDBID, i.uid))
		for t in List2:    # 全部设置收礼盒状态，要设置对方的送礼盒状态
			for s in self.giftBoxSendDatas[t[0]]:
				if t[1] == s.uid:
					s.giftState = STORE_GIFT_STATE[csdefine.STORE_GIFT_STATE_SELF_REFUSE]
					KBEngine.lookUpEntityByDBID( "Role", int(t[0]), Functions.Functor( self.onRefuseGift, s.uid, s.receiverName, int(t[0]) ) )
					break
		self.onUpdateGiftBox(player, playerDBID, sendList, receiveList)

	def onGetBackGiftOver(self, player, playerDBID, uid):
		"""
		<defined method>
		取回礼品完成
		"""
		sendList = []
		receiveList = []
		for i in self.giftBoxSendDatas[str(playerDBID)]:
			if uid == i.uid:
				i.giftState = csdefine.STORE_GIFT_STATE_RECAPTION
				i.endTime = str(Functions.getTime(7*24*60*60))
				sendList.append(i)
				break
		self.onUpdateGiftBox(player, playerDBID, sendList, receiveList)

	def onGetBackGiftsOver(self, player, playerDBID):
		"""
		<defined method>
		全部取回礼品完成
		"""
		sendList = []
		receiveList = []
		for i in self.giftBoxSendDatas[str(playerDBID)]:
			if i.giftState == csdefine.STORE_GIFT_STATE_REFUSE:
				i.giftState = csdefine.STORE_GIFT_STATE_RECAPTION
				i.endTime = str(Functions.getTime(7*24*60*60))
				sendList.append(i)
		self.onUpdateGiftBox(player, playerDBID, sendList, receiveList)

	def onRefuseGift(self, uid, receiverName, senderDBID,target):
		"""
		拒绝礼物后给送礼者发消息
		"""
		self.presentRedPointList.append(int(senderDBID))
		if target is False:
			return
		if target is True:
			self.beRefuseGiftID.append(uid)
			return
		target.statusMessage(csstatus.STORE_GIFT_BE_REFUSE, receiverName)
		if target.client:
			target.client.CLINET_GiftBoxShowRedPoint(0)

	def removeGiftBoxRecord(self, type, player, playerDBID, uid):
		"""
		<defined method>
		删除礼品盒记录
		@ prama type 1：表示处理送礼品盒 2：表示处理收礼品盒
		"""
		if type == 1:
			for i in self.giftBoxSendDatas[str(playerDBID)]:
				if uid == i.uid and i.endTime:
					self.giftBoxSendDatas[str(playerDBID)].remove(i)
					break
			player.client.CLINET_OnDeleteGiftBoxSendRecord(uid)
		if type == 2:
			for i in self.giftBoxReceiveDatas[str(playerDBID)]:
				if uid == i.uid and i.endTime:
					self.giftBoxReceiveDatas[str(playerDBID)].remove(i)
					break
			player.client.CLINET_OnDeleteGiftBoxReceiveRecord(uid)
		

	def removeAllGiftBoxRecord(self, type, player, playerDBID):
		"""
		<defined method>
		删除所有礼品盒记录
		@ prama type 1：表示处理送礼品盒 2：表示处理收礼品盒
		"""
		if type == 1:
			if str(playerDBID) in self.giftBoxSendDatas:
				length = len(self.giftBoxSendDatas[str(playerDBID)])                 
				for i in range(length-1, -1, -1):
					if self.giftBoxSendDatas[str(playerDBID)][i].endTime:
						self.giftBoxSendDatas[str(playerDBID)].pop(i)
				player.client.CLINET_OnDeleteGiftBoxSendRecords()
		if type == 2:
			if str(playerDBID) in self.giftBoxReceiveDatas:
				length = len(self.giftBoxReceiveDatas[str(playerDBID)])
				for i in range(length-1, -1, -1):
					if self.giftBoxReceiveDatas[str(playerDBID)][i].endTime:
						self.giftBoxReceiveDatas[str(playerDBID)].pop(i)
				player.client.CLINET_OnDeleteGiftBoxReceiveRecords()
		

	def onUpdateGiftBox(self, player, playerDBID, SendList, ReceiveList):

		player.client.CLIENT_OnUpdateGiftBox({"Datas" : SendList }, {"Datas" : ReceiveList })

	def transferPresent(self, player, playerDBID, uid, receiverName, receiverDBID, message):
		"""
		<Define method>
		转增
		"""
		sendList = []
		giftBox = None
		if playerDBID in self.giftBoxSendDatas:
			for i in self.giftBoxSendDatas[playerDBID]:
				if i.uid == uid:
					i.endTime = ""
					i.overtime = str(Functions.getTime(3*24*60*60))
					i.receiverName = receiverName
					i.receiverDBID = receiverDBID
					i.giftState = csdefine.STORE_GIFT_STATE_NONE
					i.message = message
					sendList.append(i)
					giftBox = copy.copy(i)
					break

		if receiverDBID not in self.giftBoxReceiveDatas:
			self.giftBoxReceiveDatas[receiverDBID] = []
		for i in self.giftBoxReceiveDatas[receiverDBID]:
			if i.uid == uid:
				self.giftBoxReceiveDatas[receiverDBID].remove(i)		
		self.giftBoxReceiveDatas[receiverDBID].append(giftBox)

		player.client.CLIENT_OnUpdateGiftBox({"Datas" : sendList }, {"Datas" : [] })			
		KBEngine.lookUpEntityByDBID( "Role", int(receiverDBID), Functions.Functor( self.onReceiveStoreGift,receiverDBID) )
		player.onTransferPresent(giftBox)

	def onShowGiftBoxRedPoint(self, player, playerDBID, type):
		"""
		<Define method>
		玩家显示完小红点后
		"""
		if type == 0:
			if playerDBID in self.presentRedPointList:
				self.presentRedPointList.remove(playerDBID)
		else:
			if playerDBID in self.receiveRedPointList:
				self.receiveRedPointList.remove(playerDBID)
		

#--------------------------------------------灵石寄售---------------------------------------------

	def requestGetOrder( self, role, roleDBID ):
		"""
		<Define method>
		获得订单
		"""
		data = {}
		myOrderList = []
		sellOrderList = []
		collectOrderList = []
		for tradeData in self.lingShiTradeData.values():
			tradeData["remainTime"] = str(int(tradeData["endTime"]) - Functions.getTime())
			tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"] * csconst.LINGSHI_TRADE_QTY_UNIT,"price":tradeData["price"],"remainTime":tradeData["remainTime"],"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"]}
			if tradeData["playerDbid"] == roleDBID:
				role.addOrder( tradeData )
				myOrderList.append( tempData )
			if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL and int(tradeData["remainTime"]) > 0 and tradeData["amount"] > 0:
				role.addAllLingShiTradeSellOrder( tradeData )
				sellOrderList.append( tempData )
			if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT and int(tradeData["remainTime"]) > 0 and tradeData["amount"] > 0:
				role.addAllLingShiTradeCollectOrder( tradeData )
				collectOrderList.append( tempData )
		data["lingShiTradeOrder"] = myOrderList
		data["allLingShiTradeSellOrder"] = sellOrderList
		data["allLingShiTradeCollectOrder"] = collectOrderList
		data["tax"] = int(csconst.LINGSHI_TRADE_PRICE * csconst.LINGSHI_TRADE_QTY_UNIT)
		role.client.GetAllOrderCB( data )

	def addLingShiTradeData( self, tradeData, role ):
		"""
		<Define method>
		增加寄售数据
		"""
		uid = tradeData["uid"]
		self.lingShiTradeData[uid] = tradeData
		if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL:
			role.addSellOrderCB(tradeData)
		elif tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
			role.addCollectOrderCB(tradeData)
		#self.writeToDB()
		if self.tradeTimeID == 0:
			self.tradeTimeID = self.addTimerCallBack(72*3600 , "overdueLingShiTradeData",(uid,) )

	def overdueLingShiTradeData( self, tradeDataUID ):
		"""
		寄售数据过期
		"""
		tradeData = self.lingShiTradeData.get( tradeDataUID,None )
		if tradeData == None:
			return
		tradeData["remainTime"] = "-1"
		self.lingShiTradeData[tradeDataUID] = tradeData
		#self.gobackMaillToSeller(tradeData)  #过期邮件  通过玩家手动下架方式领取
		self.popTimer(self.tradeTimeID)
		self.tradeTimeID = 0
		tradeData = self.getMinTimeOfTradeData( self.lingShiTradeData )
		if tradeData == None:
			return
		if self.tradeTimeID <= 0:
			self.tradeTimeID = self.addTimerCallBack( (int(tradeData["endTime"]) - Functions.getTime())/csconst.TIME_ENLARGE_MULTIPLE,"overdueLingShiTradeData",(tradeData["uid"],) )
		#self.writeToDB()

	def dealLinShiTradeOrder( self, amount, totalPrice, uid, type, role, roleDBID ):
		"""
		<Define method>
		购买或出让寄售订单
		"""
		tradeData = self.lingShiTradeData.get(uid,None)
		if tradeData == None:
			#CST-8944：如果购买或收购的商品已下架或已售完，则提示当前提示“商品剩余数量不足”
			role.client.statusMessage( csstatus.STALL_ITEM_AMOUNT_NOT_ENOUGH,"" )
			#KBEDebug.ERROR_MSG(" this tradeData is error %s "%uid)
			return
		if roleDBID == tradeData["playerDbid"]:
			role.client.statusMessage( csstatus.LINGSHI_TRADE_CANT_BUY_SELF,"" )
			return
		if tradeData["tradeType"] != type:
			KBEDebug.ERROR_MSG("tradeData is error %i"%tradeData["tradeType"])
			return
		if tradeData["amount"] < amount:
			role.client.statusMessage( csstatus.STALL_ITEM_AMOUNT_NOT_ENOUGH,"" )
			#role.base.UpdataSellOrder( tradeData )
			return
		tradeData["amount"] -= amount
		tradeData["earnMoney"] += amount * tradeData["price"]
		if type == csdefine.LINGSHI_TRADE_SELL:
			role.buyLinShiTradeOrderCB( amount* csconst.LINGSHI_TRADE_QTY_UNIT )
			role.cell.buyLinShiTradeOrderCB( totalPrice )
		elif type == csdefine.LINGSHI_TRADE_COLLECT:
			role.sellLingShiTradeOrderCB( (amount * csconst.LINGSHI_TRADE_QTY_UNIT) )
			role.cell.sellLingShiTradeOrderCB( totalPrice )
		tempData = {"uid":tradeData["uid"],"amount":amount,"price":tradeData["price"],"isSend":0,"tradeType":type}
		self.lingShiTradeSuccessDatas.insert(0,tempData)
		role.updataOrder(tradeData,self.lingShiTradeSuccessDatas[0])
		self.sendMaillToSeller(tradeData, self.lingShiTradeSuccessDatas[0])
		KBEngine.lookUpEntityByDBID("Role",tradeData["playerDbid"],Functor(self.dealLinShiTradeOrderCallBack,tradeData,self.lingShiTradeSuccessDatas[0]))
		if tradeData["amount"] == 0:
			del self.lingShiTradeData[uid]

	def dealLinShiTradeOrderCallBack( self, tradeData, successTradeData, target ):
		"""
		获得玩家MailBox回调
		"""
		if target is False:
			return
		if target is True:
			return
		for data in self.lingShiTradeSuccessDatas:
			if data.uid == successTradeData.uid:
				data.isSend = 1
		target.updataMyOrderToClient(tradeData,successTradeData)

	def removeLingShiTradeOrder( self, uid, role ):
		"""
		<Define method>
		下架订单
		"""
		tradeData = self.lingShiTradeData.get(uid,None)
		if tradeData == None:
			return
		
		totalPrice = 0
		if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL:
			totalPrice = tradeData["amount"] * csconst.LINGSHI_TRADE_QTY_UNIT
		elif tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
			totalPrice = tradeData["amount"] * tradeData["price"]
	
		del self.lingShiTradeData[uid]
		role.removeLingShiTradeOrderCB(totalPrice,uid)

	def refreshPlayerOrder( self, role, roleDBID):
		"""
		<Define method>
		更新玩家订单
		"""
		orderList = []
		data = {}
		for tradeData in self.lingShiTradeData.values():
			if tradeData["playerDbid"] == roleDBID:
				role.addOrder( tradeData )
				tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"] * csconst.LINGSHI_TRADE_QTY_UNIT,"price":tradeData["price"],"remainTime":str(int(tradeData["endTime"]) - Functions.getTime()),"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"]}
				orderList.append(tempData)
		data["orderData"] = orderList
		role.client.RefreshMyOrderCB( data )

	def takeOutMoney( self, role,roleDBID ):
		"""
		<Define method>
		取出收益
		"""
		totalPrice = 0
		totalLingshi = 0
		for tradeData in self.lingShiTradeData.values():
			if tradeData["playerDbid"] == roleDBID and tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL:
				totalPrice += tradeData["earnMoney"]
			elif tradeData["playerDbid"] == roleDBID and tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
				totalLingshi += tradeData["earnMoney"]
		role.takeOutMoneyCB( totalPrice,totalLingshi )

	def takeOutMoneyCB( self, totalPirce,totalLingshi,role,roleDBID ):
		"""
		<Define method>
		取出收益回调
		"""
		for tradeData in self.lingShiTradeData.values():
			if tradeData["playerDbid"] == roleDBID:
				tradeData["earnMoney"] = 0
				role.base.updataMyOrder(tradeData)
		role.addMoneyBuySOrder( totalPrice )		
		role.base.addLingShiBuyOrder( totalLingshi )

	def refreshAllSellOrder( self, role, roleDBID ):
		"""
		<Define method>
		刷新所有出售订单
		"""
		orderList = []
		data = {}
		for tradeData in self.lingShiTradeData.values():
			if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL and int(tradeData["remainTime"]) > 0 and tradeData["amount"] > 0:
				role.addAllLingShiTradeSellOrder( tradeData )
				tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"] * csconst.LINGSHI_TRADE_QTY_UNIT,"price":tradeData["price"],"remainTime":str(int(tradeData["endTime"]) - Functions.getTime()),"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"]}
				orderList.append( tempData )
		data["orderData"] = orderList
		role.client.RefreshAllSellOrderCB( data )

	def refreshAllCollectOrder( self, role, roleDBID ):
		"""
		<Define method>
		刷新所有收购订单
		"""
		orderList = []
		data = {}
		for tradeData in self.lingShiTradeData.values():
			if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT and int(tradeData["remainTime"]) > 0 and tradeData["amount"] > 0:
				role.addAllLingShiTradeCollectOrder( tradeData )
				tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"] * csconst.LINGSHI_TRADE_QTY_UNIT,"price":tradeData["price"],"remainTime":str(int(tradeData["endTime"]) - Functions.getTime()),"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"]}
				orderList.append( tempData )
		data["orderData"] = orderList
		role.client.RefreshAllCollectOrder( data )

	def getMinTimeOfTradeData( self, lingShiTradeDataList ):
		"""
		获得订单的最小下单时间，用于添加定时器
		"""
		if len( lingShiTradeDataList ) < 0:
			return None
		tradeTimeList = []
		for tradeData in lingShiTradeDataList.values():
			remainTime = int(tradeData["endTime"]) - Functions.getTime()
			if remainTime > 0 and tradeData["amount"] > 0:
				tradeTimeList.append(tradeData["endTime"])
		if len(tradeTimeList) <= 0:
			return None
		tradeTimeList.sort()
		for tradeData in lingShiTradeDataList.values():
			if tradeData["endTime"] == tradeTimeList[0]:
				return tradeData
		return None

	def sendMaillToSeller(self, tradeData, successTradeData):
		"""
		发送邮件附件给卖家
		"""
		sender = g_mailContentDataLoader.getMailDataSenderNameByMailID("100000001")
		title = g_mailContentDataLoader.getMailDataTitleByMailID("100000001")
		content = g_mailContentDataLoader.getMailDataContentByMailID("100000001")
		if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL:
			price = successTradeData.amount *successTradeData.price
			KBEngine.globalData["MailManager"].send( None, tradeData["sellerName"], csdefine.MAIL_SENDER_TYPE_SYS, sender, title, content, price, 0, [], 0, 0)
		elif tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
			price = successTradeData.amount * csconst.LINGSHI_TRADE_QTY_UNIT	
			KBEngine.globalData["MailManager"].send( None, tradeData["sellerName"], csdefine.MAIL_SENDER_TYPE_SYS, sender, title, content, 0, 0, [], 0, price)

	def gobackMaillToSeller(self, tradeData):
		"""
		邮件过期退回
		"""
		price = tradeData.amount * csconst.LINGSHI_TRADE_QTY_UNIT
		sender = g_mailContentDataLoader.getMailDataSenderNameByMailID("100000002")
		title = g_mailContentDataLoader.getMailDataTitleByMailID("100000002")
		content = g_mailContentDataLoader.getMailDataContentByMailID("100000002")
		if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL:			
			KBEngine.globalData["MailManager"].send( None, tradeData["sellerName"], csdefine.MAIL_SENDER_TYPE_SYS, sender, title, content, 0, 0, [], 0, price)
		elif tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
			KBEngine.globalData["MailManager"].send( None, tradeData["sellerName"], csdefine.MAIL_SENDER_TYPE_SYS, sender, title, content, price, 0, [], 0, 0)