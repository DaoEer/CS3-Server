# -*- coding: utf-8 -*-
class StateInterface:
	def __init__( self ):
		pass
		
	def set_state( self, old ):
		"""
		"""
		self.eventObj.fireEvent("Event_OnStateChanged", self.state, old)
	
	def SetGameState( self, state ):
		pass
