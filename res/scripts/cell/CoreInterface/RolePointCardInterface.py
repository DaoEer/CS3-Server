# -*- coding: utf-8 -*-
import KBEngine
import csconst
import csdefine
import KST
import KBEDebug

class RolePointCardInterface:
	def __init__( self ):
		pass
	
	def sellPointCard( self, srcEntityID, cardNo, pwd, severName, cardPrice ):
		"""
		exposed method
		玩家寄售点卡
		"""
		if self.money < csconst.SELL_POINT_CARD_YAJIN:
			self.statusMessage( csstatus.POINT_CARD_FORBID_NOT_ENOUGH_MONEY )
			return
			
		if not KBEngine.globalData.has_key( "serverName" ):
			self.statusMessage( csstatus.POINT_CARD_FORBID_CELL_HAS_NOT_NAME )
			return
			
		self.base.sellPointCard( cardNo, pwd, KBEngine.globalData["serverName"], cardPrice )

	def onSellPointCard( self ):
		"""
		define method
		寄售点卡成功，收取押金
		"""
		self.payMoney( csconst.SELL_POINT_CARD_YAJIN, csdefine.CHANGE_MONEY_POINT_CARD_YAJIN )

	def buyPointCard( self, srcEntityID, cardNo ):
		"""
		exposed method
		购买点卡
		"""
		self.base.buyPointCard( cardNo, self.money )

	def onBuyPointCard( self, price ):
		"""
		购买点卡回调。
		不管是否成功都先收取费用。如果不成功，后面会归还。
		"""
		self.payMoney( price, csdefine.CHANGE_MONEY_POINT_CARD_YAJIN )