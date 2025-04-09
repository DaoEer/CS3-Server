# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
import csconst
import csstatus
import Functions
import json

class RoleLingShiTradeInterface:
	"""
	玩家灵石寄售接口
	"""
	def __init__( self ):
		"""
		"""
		self.lingShiTradeOrder = {}
		self.allLingShiTradeSellOrder = {}
		self.allLingShiTradeCollectOrder = {}
		self.allLingShiTradeSuccessData = []

	def requestGetOrder( self ):
		"""
		<Exposed method>
		请求获得订单
		"""
		if not self.validateClientCall():
			return
		self.lingShiTradeOrder.clear()
		self.allLingShiTradeSellOrder.clear()
		self.allLingShiTradeCollectOrder.clear()
		self.allLingShiTradeSuccessData.clear()
		KBEngine.globalData["StoreManager"].requestGetOrder( self, self.databaseID )

	def addSellOrder( self, price, amount ):
		"""
		增加出售订单
		<define method>
		"""
		if len(self.lingShiTradeOrder) >= csconst.LINGSHI_TRADE_UPPER_LIMIT:
			self.statusMessage(csstatus.LINGSHI_TRADE_NOT_ADD,"")
			return
		if price <= 0:
			self.statusMessage( csstatus.LINGSHI_TRADE_PRICE_ERROR,"" )
			return
		if amount <= 0:
			self.statusMessage( csstatus.LINGSHI_TRADE_AMOUNT_ERROR,"" )
			return
		result = self.xianshi - amount * csconst.LINGSHI_TRADE_QTY_UNIT
		if result < 0:
			self.statusMessage( csstatus.LINGSHI_TRADE_AMOUNT_ERROR,"" )
			return
		if result < amount * csconst.LINGSHI_TRADE_QTY_UNIT * csconst.LINGSHI_TRADE_PRICE:
			self.statusMessage( csstatus.LINGSHI_TRADE_XIANSHI_NOT_POUNDAGE,"" )
			return
			
		tempData = {"uid":str(KBEngine.genUUID64()),"amount":amount,"price":price,"endTime":str(Functions.getTime() + 72*3600*csconst.TIME_ENLARGE_MULTIPLE) ,"remainTime":str(72*3600*csconst.TIME_ENLARGE_MULTIPLE),"playerDbid":self.databaseID,"tradeType":csdefine.LINGSHI_TRADE_SELL,"earnMoney":0, "sellerName":self.getName() }
		KBEngine.globalData["StoreManager"].addLingShiTradeData(tempData,self)

	def addSellOrderCB( self, tradeData ):
		"""
		<Define method>
		增加出售订单的回调
		"""
		self.addOrder(tradeData)
		self.addAllLingShiTradeSellOrder(tradeData)
		totalXianshi = tradeData["amount"] * csconst.LINGSHI_TRADE_QTY_UNIT + tradeData["amount"] * csconst.LINGSHI_TRADE_QTY_UNIT * csconst.LINGSHI_TRADE_PRICE
		self.payXianShi(int(totalXianshi), csdefine.CHANGE_XIANSHI_BY_TRADE)
		tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"] * csconst.LINGSHI_TRADE_QTY_UNIT,"price":tradeData["price"],"remainTime":tradeData["remainTime"],"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"]}
		self.client.AddOrderCB( tempData) 

	def updataMyOrderToClient( self, tradeData,successTradeData ):
		"""
		<Define method>
		更新订单到客户端(自己)
		"""
		self.updataMyOrder(tradeData)
		self.updataOrder(tradeData,successTradeData)
		tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"],"price":tradeData["price"],"remainTime":str(int(tradeData["endTime"]) - Functions.getTime()),"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"] }
		if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL:
			self.statusMessage( csstatus.LINGSHI_TRADE_SELL_ORDER_SUCCESS,successTradeData.amount * 100,successTradeData.amount *successTradeData.price )
			self.statusMessage( csstatus.LINGSHI_TRADE_SELL_SUCCESS,"" )
		elif tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
			self.statusMessage( csstatus.LINGSHI_TRADE_COLLECT_ORDER_SUCCESS,successTradeData.amount * 100,successTradeData.amount *successTradeData.price )
			self.statusMessage( csstatus.LINGSHI_TRADE_COLLECT_SUCCESS,"" )
		self.client.UpdataMyOrderToClient( tempData )

	def updataMyOrder( self, tradeData ):
		"""
		<Define method>
		更新自己订单
		"""
		if self.lingShiTradeOrder.get(tradeData["uid"]) != None:
			if tradeData["amount"] == 0:
				del self.lingShiTradeOrder[tradeData["uid"]]
			else:
				self.lingShiTradeOrder[tradeData["uid"]] = tradeData

	def addCollectOrder( self, price, amount ):
		"""
		<Define method>
		增加收购订单
		"""
		if len(self.lingShiTradeOrder) >= csconst.LINGSHI_TRADE_UPPER_LIMIT:
			KBEDebug.ERROR_MSG("not add LingShi Trade Data")
			self.statusMessage(csstatus.LINGSHI_TRADE_NOT_ADD,"")
			return
		tempData = {"uid":str(KBEngine.genUUID64()),"amount":amount,"price":price,"endTime":str(Functions.getTime() + 72*3600*csconst.TIME_ENLARGE_MULTIPLE),"playerDbid":self.databaseID,"tradeType":csdefine.LINGSHI_TRADE_COLLECT,"earnMoney":0,"remainTime":str(72*3600*csconst.TIME_ENLARGE_MULTIPLE), "sellerName":self.getName() }
		KBEngine.globalData["StoreManager"].addLingShiTradeData(tempData,self)

	def addCollectOrderCB( self, tradeData ):
		"""
		<Define method>
		增加收购订单回调
		"""
		self.addOrder(tradeData)
		self.addAllLingShiTradeCollectOrder( tradeData )
		totalPrice = tradeData["amount"] * tradeData["price"] + tradeData["amount"] * tradeData["price"] * csconst.LINGSHI_TRADE_PRICE
		self.cell.addCollectOrderCB(int(totalPrice))
		tempData = {"uid":tradeData["uid"],"amount":tradeData["amount"] * csconst.LINGSHI_TRADE_QTY_UNIT,"price":tradeData["price"],"remainTime":tradeData["remainTime"],"tradeType":tradeData["tradeType"],"earnMoney":tradeData["earnMoney"]}
		self.client.AddOrderCB( tempData) 

	def updataOrder( self, tradeData, successTradeData ):
		"""
		更新订单(所有)
		"""
		if tradeData["tradeType"] == csdefine.LINGSHI_TRADE_SELL:
			tempData = self.allLingShiTradeSellOrder.get( tradeData["uid"],None )
			if tempData == None:
				return
			self.addAllLingShiTradeSellOrder(tradeData)
		elif tradeData["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
			tempData = self.allLingShiTradeCollectOrder.get( tradeData["uid"],None )
			if tempData == None:
				return
			#数量为0时，删除它
			self.addAllLingShiTradeCollectOrder(tradeData)
		data = {}
		self.allLingShiTradeSuccessData.insert(0,successTradeData)
		data["allTradeData"] = {"uid":tradeData["uid"],"tradeType":tradeData["tradeType"],"amount":tradeData["amount"] * 100,"remainTime":str(int(tradeData["endTime"]) - Functions.getTime())}
		data["allTradeSuccess"] = successTradeData;
		self.client.UpdataOrder( data )

	def addOrder( self, tradeData ):
		"""
		<Define method>
		增加订单
		"""
		self.lingShiTradeOrder[tradeData["uid"]] = tradeData

	def buyLinShiTradeOrder( self, amount, totalPrice, uid ):
		"""
		<Define method>
		购买寄售订单
		"""
		KBEngine.globalData["StoreManager"].dealLinShiTradeOrder( amount, totalPrice, uid, csdefine.LINGSHI_TRADE_SELL,self,self.databaseID )

	def buyLinShiTradeOrderCB( self, totalPrice ):
		"""
		<Define method>
		购买寄售订单回调
		"""
		self.addLingShiBuyOrder(totalPrice)

	def addLingShiBuyOrder( self, totalPrice ):
		"""
		<Define method>
		订单 增加仙石
		"""
		#self.addLingShi(totalPrice,csdefine.CHANGE_LINGSHI_BY_STORE)
		self.addXianShi(totalPrice, csdefine.CHANGE_XIANSHI_BY_TRADE)

	def sellLingShiTradeOrder( self, amount, totalPrice, uid ):
		"""
		<Define method>
		出让灵石
		"""
		if self.xianshi < amount * 100:
			self.statusMessage( csstatus.LINGSHI_TRADE_ORDER_XIANSHI_NOT_ENOUGH,"" )
			return
		KBEngine.globalData["StoreManager"].dealLinShiTradeOrder( amount,totalPrice,uid,csdefine.LINGSHI_TRADE_COLLECT,self,self.databaseID )
		
	def sellLingShiTradeOrderCB( self, totalPrice ):
		"""
		出让灵石回调
		"""
		self.payXianShi(totalPrice, csdefine.CHANGE_XIANSHI_BY_TRADE)

	def removeLingShiTradeOrder( self, uid ):
		"""
		<Exposed method>
		下架订单
		"""
		if not self.validateClientCall():
			return
		order = self.lingShiTradeOrder.get(uid,None)
		if order == None:
			KBEDebug.ERROR_MSG(" remove uid(%s) order is error "%uid)
			return
		# data = None
		# if order["tradeType"] == csdefine.LINGSHI_TRADE_SELL:
		# 	data = self.allLingShiTradeSellOrder.get(uid,None)
		# elif order["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
		# 	data = self.allLingShiTradeCollectOrder.get(uid,None)
		# if data == None:
		# 	return
		totalPrice = order["amount"] * order["price"] * csconst.LINGSHI_TRADE_QTY_UNIT
		if order["tradeType"] == csdefine.LINGSHI_TRADE_SELL:
			if self.xianshi + totalPrice > csconst.ROLE_XIANSHI_UPPER_LIMIT:
				KBEDebug.ERROR_MSG( " xianshi is more than " )
				return
			KBEngine.globalData["StoreManager"].removeLingShiTradeOrder(uid,self)
		elif order["tradeType"] == csdefine.LINGSHI_TRADE_COLLECT:
			self.cell.removeLingShiTradeOrder(uid,totalPrice)

	def removeLingShiTradeOrderCB( self, totalPrice, uid ):
		"""
		<Define method>
		下架订单回调
		"""
		del self.lingShiTradeOrder[uid]
		self.addXianShi(totalPrice, csdefine.CHANGE_XIANSHI_BY_TRADE)
		self.client.RemoveLingShiTradeOrderCB(uid)

	def refreshMyOrder( self ):
		"""
		<Exposed method>
		刷新自己的寄售订单
		"""
		if not self.validateClientCall():
			return
		self.lingShiTradeOrder.clear()
		KBEngine.globalData["StoreManager"].refreshPlayerOrder( self,self.databaseID )

	def takeOutMoney( self ):
		"""
		<Define method>
		取出收益
		"""
		KBEngine.globalData["StoreManager"].takeOutMoney(self,self.databaseID)

	def takeOutMoneyCB( self, totalPrice,totalLingshi ):
		"""
		<Define method>
		取出收益回调
		"""
		if self.lingshi + totalLingshi > csconst.ROLE_LINGSHI_UPPER_LIMIT:
			self.statusMessage( csstatus.LINGSHI_TRADE_LINGSHI_MAX )
			return
		self.cell.takeOutMoneyCB( totalPrice,totalLingshi )

	def refreshAllSellOrder( self ):
		"""
		刷新所有寄售的订单
		Exposed method
		"""
		if not self.validateClientCall():
			return
		self.allLingShiTradeSellOrder.clear()
		KBEngine.globalData["StoreManager"].refreshAllSellOrder( self, self.databaseID )

	def addAllLingShiTradeSellOrder( self, tradeData ):
		"""
		<Define method>
		增加出售订单
		"""
		self.allLingShiTradeSellOrder[tradeData["uid"]] = tradeData

	def refreshAllCollectOrder( self ):
		"""
		刷新所有收购订单
		Exposed mehtod
		"""
		if not self.validateClientCall():
			return
		self.allLingShiTradeCollectOrder.clear()
		KBEngine.globalData["StoreManager"].refreshAllCollectOrder( self, self.databaseID )

	def addAllLingShiTradeCollectOrder( self,tradeData ):
		"""
		<Define method>
		增加收购订单
		"""
		self.allLingShiTradeCollectOrder[tradeData["uid"]] = tradeData
