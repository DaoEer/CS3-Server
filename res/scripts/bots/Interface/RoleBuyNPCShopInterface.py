# -*- coding: utf-8 -*-
import KBEngine
class RoleBuyNPCShopInterface:
	
	def __init__(self):
		pass
		
	def getBuyBackItemList(self, dataStream):
		pass
		
	def getNPCShopItemList(self, shopNPCID, shopID, itemList):
		pass
		
	def addBuyBackItem(self, itemList):
		pass
		
	def addHighBuyBackItem(self, uid, time, tempDict):
		pass
		
	def subBuyBackItem(self, itemList):
		pass
		
	def subHighBuyBackItem(self, itemList):
		pass
		
	def reduceNPCShopItem(self,shopID, slot, itemID, amount ):
		pass
		
	def OnRequestTongShop( self, p1, p2, p3 ):
		pass
	def OnRequestUpdatePagodaSoul( self, p1, p2 ):
		pass
	def OnRequestBuyCombatSoulItem( self, p1 ):
		pass
	def OnRequestSellCombatSoulItem( self, p1 ):
		pass
	def OnRequestBuyGuardSoul( self, p1 ):
		pass
	def OpenTraviaShop( self, p1, p2 ):
		pass
	def CLIENT_OpenTraviaShop( self, p1, p2 ):
		pass
	def CLIENT_OnRequestBuyCombatSoulItem( self, p1, p2 ):
		pass
	def CLIENT_OnRequestSellCombatSoulItem( self, p1 ):
		pass
	def CLIENT_OnRequestBuyGuardSoul( self, p1, p2 ):
		pass
	def CLIENT_OnRequestUpdatePagodaSoul( self, p1, p2 ):
		pass
	def CLIENT_OnInitBuyBackItemList( self, p1 ):
		pass
	def CLIENT_InitNPCShopItemList( self, p1, p2, p3 ):
		pass
	def CLIENT_OnRequestSellItem( self, p1 ):
		pass
	def CLIENT_OnRequestBuyBackItem( self, p1 ):
		pass
	def CLIENT_OnSuccessBuyShopItem( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_OnRequestTongShop( self, p1, p2, p3 ):
		pass
	def CLIENT_openLMNeuralShop( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_OnBuyNeuralGuard( self, p1 ):
		pass
	def OnRequestBuyBackItem( self, p1 ):
		pass
	def CLIENT_InitNPCShopItemListByDiscount( self, p1, p2, p3, p4 ):
		pass
	def OnLockTongShop( self ):
		pass
	def OnTongPlunderShopSellStart( self, p1, p2 ):
		pass
	def OnUnLockTongShop( self ):
		pass
	def OnTongPlunderShopSellEnd( self ):
		pass
	def CLIENT_TongPlunderShopSellEnd( self ):
		pass
	def OnTongPlunderShopItemBuySuccess( self, p1, p2, p3 ):
		pass
	def CLIENT_LockTongShop( self ):
		pass
	def CLIENT_UnLockTongShop( self ):
		pass

	def onNotifyRandomItemSellEndTime( self, p1, p2 ):
		pass