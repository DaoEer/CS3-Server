# -*- coding: utf-8 -*-
import KBEngine
from Interface.GameObject import GameObject
from Interface.NPCAmbulantInterface import NPCAmbulantInterface
from Interface.CombatInterface import CombatInterface
class VehiclePet(
	NPCAmbulantInterface,
		KBEngine.Entity,
		GameObject, 
		CombatInterface,
	):
	def __init__( self ):
		NPCAmbulantInterface.__init__(self)
		"""
		"""
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		CombatInterface.__init__(self)
		
	def OnRiseEnd(self,arg0_int32):
		pass
