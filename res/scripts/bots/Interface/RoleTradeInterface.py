# -*- coding: utf-8 -*-
import KBEngine
class RoleTradeInterface:
	
	def __init__(self):
		pass
		
	def RoleTrade_onRoleTrade(self, entityID, playername):
		pass
		
	def RoleTrade_tradeOvertime(self):
		pass
		
	def RoleTrade_onTradeState(self, state):
		pass
		
	def RoleTrade_onDstTradeLock(self, state):
		pass
		
	def RoleTrade_onDstTradeSure(self, state):
		pass
		
	def RoleTrade_onMoneyChange(self, money):
		pass
		
	def RoleTrade_onDstMoneyChange(self, money):
		pass
		
	def RoleTrade_onItemAdd(self, swapOrder, kitOrder ):
		pass
		
	def RoleTrade_onDstItemAdd(self, swapOrder, itemStream):
		pass
		
	def RoleTrade_onItemRemove(self, swapOrder):
		pass
		
	def RoleTrade_onDstItemRemove(self, swapOrder):
		pass
	def RoleTrade_onItemSwap( self, p1, p2 ):
		pass
	def RoleTrade_onDstItemSwap( self, p1, p2 ):
		pass
	def CLIENT_onRoleTrade( self, p1, p2 ):
		pass
	def CLIENT_tradeOvertime( self ):
		pass
	def CLIENT_onTradeState( self, p1 ):
		pass
	def CLIENT_onDstTradeLock( self, p1 ):
		pass
	def CLIENT_onDstTradeSure( self, p1 ):
		pass
	def CLIENT_onMoneyChange( self, p1 ):
		pass
	def CLIENT_onDstMoneyChange( self, p1 ):
		pass
	def CLIENT_onItemAdd( self, p1, p2, p3 ):
		pass
	def CLIENT_onDstItemAdd( self, p1, p2 ):
		pass
	def CLIENT_onItemRemove( self, p1 ):
		pass
	def CLIENT_onDstItemRemove( self, p1 ):
		pass
	def CLIENT_onItemSwap( self, p1, p2, p3 ):
		pass
	def CLIENT_onDstItemSwap( self, p1, p2 ):
		pass
