# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import csdefine
import csconst
import csstatus
import Functions

class RoleLingShiTradeInterface:
	"""
	玩家灵石寄售接口
	"""
	def __init__( self ):
		"""
		"""
		pass
		
	def addSellOrder( self, playerID, price, amount ):
		"""
		<Exposed method>
		增加出售订单
		"""
		if not self.validateClientCall( playerID ):
			return
		if self.isPWKitBagLock():
			KBEDebug.ERROR_MSG(" kitbag is lock ")
			return
		self.base.addSellOrder(price,amount)

	def addCollectOrder( self, playerID, price, amount ):
		"""
		<Exposed method>
		增加收购订单
		"""
		if not self.validateClientCall( playerID ):
			return
		if price <= 0:
			self.statusMessage( csstatus.LINGSHI_TRADE_PRICE_ERROR,"" )
			return
		if amount <= 0:
			self.statusMessage( csstatus.LINGSHI_TRADE_AMOUNT_ERROR,"" )
			return
		result = self.money - price * amount
		if result < 0:
			self.statusMessage( csstatus.LINGSHI_TRADE_MONEY_NOT_ENOUGH,"" )
			return
		if result < price * amount * csconst.LINGSHI_TRADE_PRICE:
			self.statusMessage( csstatus.LINGSHI_TRADE_MONEY_NOT_POUNDAGE,"" )
			return
		self.base.addCollectOrder( price,amount )

	def addCollectOrderCB( self, totalPirce ):
		"""
		<Define method>
		增加收购订单回调
		"""
		self.subMoney( totalPirce, csdefine.MONEY_SUB_REASON_LINGSHI_TRADE )

	def buyLinShiTradeOrder( self, playerID, amount, totalPirce, uid ):
		"""
		<Exposed method>
		购买寄售订单
		"""
		if not self.validateClientCall( playerID ):
			return
		if self.money < totalPirce:
			self.statusMessage( csstatus.LINGSHI_TRADE_MONEY_NOT_ENOUGH,"" )
			return
		self.base.buyLinShiTradeOrder(amount,totalPirce,uid )

	def buyLinShiTradeOrderCB( self, totalPirce ):
		"""
		<Define method>
		购买寄售订单回调
		"""
		self.subMoney(totalPirce, csdefine.MONEY_SUB_REASON_LINGSHI_TRADE)

	def sellLingShiTradeOrder( self, playerID, amount, totalPirce, uid ):
		"""
		<Exposed method>
		出让灵石
		"""
		if not self.validateClientCall( playerID ):
			return
		totalPirce = totalPirce
		if self.money + totalPirce > csconst.MONEY_MAX_AMOUNT:
			self.statusMessage(csstatus.LINGSHI_TRADE_MONEY_MAX)
			return
		self.base.sellLingShiTradeOrder(amount,totalPirce,uid)

	def sellLingShiTradeOrderCB( self, totalPirce ):
		"""
		<Define method>
		出让灵石回调
		"""
		self.addMoneyBuySOrder( totalPirce )

	def addMoneyBuySOrder( self, totalPirce ):
		"""
		<Define method>
		订单 增加金币
		"""
		self.addMoney( totalPirce,csdefine.MONEY_ADD_REASON_LINGSHI_TRADE )

	def removeLingShiTradeOrder( self, uid, totalPirce ):
		"""
		<Define method>
		下架订单
		"""
		if self.money + totalPirce > csconst.MONEY_MAX_AMOUNT:
			self.statusMessage(csstatus.LINGSHI_TRADE_MONEY_MAX)
			return
		KBEngine.globalData["StoreManager"].removeLingShiTradeOrder(uid, self)

	def removeLingShiTradeOrderCB( self, totalPirce,uid ):
		"""
		<Define method>
		下架订单回调
		"""
		self.addMoney( totalPirce,csdefine.MONEY_ADD_REASON_LINGSHI_TRADE )
		self.client.RemoveLingShiTradeOrderCB(uid)

	def takeOutMoney( self, playerID ):
		"""
		<Exposed method>
		取出收益
		"""
		if not self.validateClientCall( playerID ):
			return
		self.base.takeOutMoney()

	def takeOutMoneyCB( self, totalPrice,totalLingshi ):
		"""
		<Define method
		取出收益回调
		"""
		if self.money + totalPirce > csconst.MONEY_MAX_AMOUNT:
			self.statusMessage(csstatus.LINGSHI_TRADE_MONEY_MAX)
			return
		KBEngine.globalData["StoreManager"].takeOutMoneyCB(totalPirce,totalLingshi,self,self.playerDBID)



