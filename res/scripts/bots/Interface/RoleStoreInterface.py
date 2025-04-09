# -*- coding: utf-8 -*-
from KBEDebug import *
class RoleStoreInterface():
	def __init__(self):
		self.storeMapping = {}
		self.buyRecords = {}
		self.sendGiftList = {}
		self.recvGiftList = {}
		
	def CLIENT_OnUpdateStoreGoods( self, p1, p2 ):
		datas = p2["Datas"]
		for data in datas:
			self.storeMapping[data["ID"]] = data
		
	def CLIENT_OnRequestStoreLimitGoodsList( self, p1, p2 ):
		pass
		
	def CLIENT_StoreNotEnoughMoney( self, p1 ):
		pass
	def CLIENT_OnRequestPresentGift( self, p1 ):
		pass
	
	def CLIENT_OnUpdateGiftBox( self, p1, p2 ):
		self.sendGiftList.clear()
		self.recvGiftList.clear()
	
		datas = p1["Datas"]
		for data in datas:
			self.sendGiftList[data["uid"]] = data
		
		datas = p2["Datas"]
		for data in datas:
			self.recvGiftList[data["uid"]] = data
	
	def CLIENT_OnUpdateBuyRecords( self, p1 ):
		datas = p1["Datas"]
		for data in datas:
			self.buyRecords[data["uid"]] = data
	
	def CLIENT_OnUpdatePresentRecords( self, p1 ):
		pass
	def CLIENT_OnGetGoodsListByIDList( self, p1 ):
		pass
	def CLIENT_UpdateStoreCart( self, p1 ):
		pass
	def CLIENT_OnUpdateStoreGoodsOver( self, p1, p2 ):
		pass
	def CLIENT_OnGetStoreNewGoods( self, p1 ):
		pass
	def CLINET_OnDeleteBuyRecord( self, p1 ):
		pass
	def CLINET_OnDeleteBuyRecords( self ):
		pass
	def CLINET_OnDeletePresentRecord( self, p1 ):
		pass
	def CLINET_OnDeletePresentRecords( self ):
		pass
	def CLINET_OnDeleteGiftBoxReceiveRecord( self, p1 ):
		pass
	def CLINET_OnDeleteGiftBoxReceiveRecords( self ):
		pass
	def CLINET_OnDeleteGiftBoxSendRecord( self, p1 ):
		pass
	def CLINET_OnDeleteGiftBoxSendRecords( self ):
		pass
	def CLIENT_OnUpdateStoreNewGoodsOver( self, p1 ):
		pass
	def CLIENT_OnAddStoreCartGoods( self, p1, p2, p3 ):
		pass
	def CLIENT_OnDeleteStoreCartGoods( self, p1, p2 ):
		pass
	def CLIENT_OnClearStoreCartGoods( self, p1 ):
		pass
	def OnDeleteSoldOutStoreCartGoods( self, p1, p2 ):
		pass
	def CLIENT_OnGetRecommentGoods( self, p1 ):
		pass
	def CLINET_GiftBoxShowRedPoint( self, p1 ):
		pass
	def AddHasStoreAppearance( self, p1 ):
		pass
	def RemoveStoreAppearance( self, p1 ):
		pass
	def UpdateStoreBackAdornParam( self, p1, p2 ):
		pass
	def AddStoreAppearance( self, p1 ):
		pass

	def OnUpdateStoreAppearance( self, p1 ):
		pass
	def OnStoreBuyComplete(self):
		pass
	