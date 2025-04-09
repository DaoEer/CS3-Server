# -*- coding: utf-8 -*-
from Interface.StateInterface import StateInterface
class RoleStateInterface(
	StateInterface, ):
	def __init__(self):
		StateInterface.__init__(self) 
	def OnRepJumpState( self, p1 ):
		pass
	def OnRepClimbLadderState( self, p1, p2 ):
		pass
