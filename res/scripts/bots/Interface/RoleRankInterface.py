# -*- coding: utf-8 -*-
class RoleRankInterface():
	def __init__(self):
		pass
	def OpenGameRank( self, p1, p2, p3, p4 ):
		pass
	def OnRequestLevelRankFirstTime( self, p1, p2, p3, p4 ):
		pass
	def OnRequestCombatRankFirstTime( self, p1, p2, p3, p4 ):
		pass
	def OnRequestMoneyRankFirstTime( self, p1, p2, p3, p4 ):
		pass
	def OnRequestWeaponRankFirstTime( self, p1, p2, p3, p4 ):
		pass
	def OnRequestLevelRank( self, p1, p2 ):
		pass
	def OnRequestCombatRank( self, p1, p2 ):
		pass
	def OnRequestMoneyRank( self, p1, p2 ):
		pass
	def OnRequestWeaponRank( self, p1, p2 ):
		pass
	def OnRequestRankStoreMoney( self, p1 ):
		pass
	def Client_updateRankData( self, p1 ):
		pass
