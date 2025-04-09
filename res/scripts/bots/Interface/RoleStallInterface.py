# -*- coding: utf-8 -*-
#------RoleStallInterface------
class RoleStallInterface:
	def __init__(self):
		pass
		
	def ReceiveStallItems(self, str1 ):
		pass
		
	def UpdateStallItem( self, int1, int2, int3, str1 ):
		pass 
		
	def StallItemSuccessToClient(self, int1, str1):
		pass 
		
	def AddStallRecord(self, int1, str1 ):
		pass
		
	def BalanceStallCB(self, str1 ):
		pass
	def GetStallItems( self, str1 ):
		pass
		
	def AddCollectionItemSuccessCB(self, param):
		pass
		
	def AddCollectionItemSuccessCB(self, str1 ):
		pass
		
	def UpdateStallCollectionItemCB(self, int1, str1 ):
		pass
	
	def RemoveStallCollectionItemCB(self, int1, int2 ):
		pass
	def AddStallSellItemSuccessCB( self, str1 ):
		pass
	def UpdateStallSellItemCB( self, int1, str1 ):
		pass
	def RemoveStallSellItemCB( self, int1, int2 ):
		pass
	
	def StallSuccessCB( self, int1 ):
		pass
	def StallFailCB( self ):
		pass
	
	def onEndStall( self ):
		pass
	def OnFindStallPoint( self, p1, p2 ):
		pass
	def CLIENT_OnFindStallPoint( self, p1, p2 ):
		pass
	def CLIENT_OnReceiveOtherStallItems( self, p1, p2, p3 ):
		pass
	def CLIENT_UpdateStallItem( self, p1, p2, p3, p4 ):
		pass
	def CLIENT_StallItemSuccessToClient( self, p1, p2 ):
		pass
	def CLIENT_AddStallRecord( self, p1, p2 ):
		pass
	def CLIENT_OnRequestStallItems( self, p1, p2 ):
		pass
	def CLIENT_AddCollectionItemSuccessCB( self, p1 ):
		pass
	def CLIENT_UpdateStallCollectionItemCB( self, p1, p2 ):
		pass
	def CLIENT_RemoveStallCollectionItemCB( self, p1 ):
		pass
	def CLIENT_AddStallSellItemSuccessCB( self, p1 ):
		pass
	def CLIENT_UpdateStallSellItemCB( self, p1, p2 ):
		pass
	def CLIENT_RemoveStallSellItemCB( self, p1 ):
		pass
	def CLIENT_StallSuccessCB( self, p1 ):
		pass
	def CLIENT_UpdateOtherStallItems( self, p1, p2 ):
		pass
