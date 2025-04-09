# -*- coding: utf-8 -*-
class RoleSpaceStrategyInterface():
	def __init__(self):
		pass
	def ReceiveOpenSpaceStrategy( self, p1, p2 ):
		pass
	def ReceiveCompleteSpaceStrategy( self, p1, p2 ):
		pass
	def OnUpdateStrategy( self, p1, p2 ):
		pass
	def StartSpaceStrategy( self, p1, p2 ):
		pass
	def OnUpdateStrategyPointValue( self, p1, p2, p3 ):
		pass
	def EndSpaceStrategy( self, p1, p2, p3, p4 ):
		pass
	def OnUpdateRewardValue( self, p1, p2, p3 ):
		pass
	def OnUpdateStrategyValue( self, p1, p2, p3 ):
		pass
	def CLIENT_StartSpaceStrategy( self, p1, p2 ):
		pass
	def CLIENT_EndSpaceStrategy( self, p1, p2 ):
		pass
	def CLIENT_ReceiveCompleteSpaceStrategy( self, p1, p2 ):
		pass
	def CLIENT_ReceiveOpenSpaceStrategy( self, p1, p2 ):
		pass
	def CLIENT_OnUpdateStrategyValue( self, p1, p2, p3 ):
		pass
	def CLIENT_OnUpdateRewardValue( self, p1, p2, p3 ):
		pass
