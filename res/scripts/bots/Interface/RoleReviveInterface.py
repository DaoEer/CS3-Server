# -*- coding: utf-8 -*-
class RoleReviveInterface( object ):
	def __init__( self ):
		pass
	
	def revive_onNoticeRoleDie(self):
		self.GMCommand(self,"revive")
		
	def OnHideRevive(self):
		pass
		
	def OnSetRevivePosStatus(self, statusID, scriptID):
		pass
		
	def CLIENT_OnHideRevive( self ):
		pass
	def CLIENT_SetRevivePosStatus( self, p1, p2 ):
		pass
	def NotifyReviveSpaceScriptID( self, p1 ):
		pass
