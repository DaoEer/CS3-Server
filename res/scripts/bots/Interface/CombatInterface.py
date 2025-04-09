# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import botdefine
from Interface.StateInterface import StateInterface
from Interface.SkillInterface import SkillInterface
class CombatInterface( SkillInterface, StateInterface ):
	
	def __init__(self):
		SkillInterface.__init__( self )
		StateInterface.__init__( self )
		
	def set_HP(self, old):
		self.eventObj.fireEvent("Event_OnHPChanged", self.HP)
		
	def set_MP(self, old):
		self.eventObj.fireEvent("Event_OnMPChanged", self.MP)
		
	def OnHPChanged(self, curHP, oldHP):
		pass
	
	def OnMPChanged(self, curMP, oldMP):
		pass
	
	def CheckClientPosition(self):
		pass
	
	def OnWalkAroundTarget(self, targetID):
		pass
		
	def OnWalkAroundTargetEnd(self):
		pass
	
	def OnReceiveDirectionFromClient(self):
		pass
		
	def NotifyStopMoving(self):
		pass
	def CLIENT_OnHPChanged( self, p1, p2 ):
		pass
	def CLIENT_OnMPChanged( self, p1, p2 ):
		pass
	def CLIENT_CheckClientPosition( self ):
		pass
	def CLIENT_OnWalkAroundTarget( self, p1 ):
		pass
	def CLIENT_OnWalkAroundTargetEnd( self ):
		pass
	def CLIENT_NotifyStopMoving( self ):
		pass
